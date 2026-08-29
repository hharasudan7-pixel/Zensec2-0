import os
import time
import logging

logger = logging.getLogger("zentrasec.copilot")

# Model configuration — gemini-3.6-flash is the current fast, cost-efficient model
# for incident response copilot workflows.
GEMINI_MODEL = "gemini-3.6-flash"

SYSTEM_INSTRUCTION = """You are ZentraSec's AI Incident Copilot, a SOC (Security Operations Center) 
assistant. You explain security incidents clearly, reference relevant MITRE ATT&CK techniques when 
applicable, and recommend concrete response actions. Keep responses concise (3-5 sentences) and 
professional, matching a cybersecurity analyst's tone."""

import google.generativeai as genai

# Google Gemini client initialization
# Uses GOOGLE_API_KEY from environment
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY") or "dummy-key-for-init")

model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    system_instruction=SYSTEM_INSTRUCTION,
)

# Maximum number of recent conversation turns to include when building the prompt.
MAX_HISTORY_TURNS = 6

# Hard cap on total prompt character length sent to Gemini.
MAX_PROMPT_CHARS = 8_000


class RateLimitError(Exception):
    """Raised when Gemini API returns a 429 / RESOURCE_EXHAUSTED response."""


def _is_rate_limit_error(exc: Exception) -> bool:
    """Return True if *exc* represents a Google Gemini 429 / RESOURCE_EXHAUSTED / rate limit error."""
    if hasattr(exc, "code") and getattr(exc, "code") == 429:
        return True
    if hasattr(exc, "status_code") and getattr(exc, "status_code") == 429:
        return True
    msg = str(exc).lower()
    return "429" in msg or "resource_exhausted" in msg or "quota" in msg or "rate limit" in msg or "rate_limit" in msg


def generate_fallback_summary(incident: dict) -> str:
    """Build a human-readable explanation using only the incident's existing
    structured fields when live AI generation is unavailable.

    Args:
        incident: Incident metadata dict.

    Returns:
        Structured fallback summary string prefixed with a distinguishable marker.
    """
    incident_id = incident.get("id") or incident.get("incident_id") or "INC-7842"
    title = incident.get("title") or incident.get("name") or "Security Anomaly Detected"
    risk_score = incident.get("risk_score") if incident.get("risk_score") is not None else incident.get("score", 85)
    
    try:
        score_val = float(risk_score)
        severity = incident.get("severity") or ("CRITICAL" if score_val >= 85 else "HIGH" if score_val >= 70 else "MEDIUM" if score_val >= 50 else "LOW")
    except (ValueError, TypeError):
        severity = incident.get("severity") or "HIGH"

    asset = incident.get("asset") or incident.get("host") or incident.get("target") or "Prod-DB-01"
    status = incident.get("status") or "Investigating"

    # Extract evidence / events
    raw_events = incident.get("events") or incident.get("evidence") or incident.get("logs") or []
    if isinstance(raw_events, list):
        event_descriptions = []
        for ev in raw_events:
            if isinstance(ev, dict):
                event_descriptions.append(ev.get("description") or ev.get("name") or ev.get("type") or str(ev))
            else:
                event_descriptions.append(str(ev))
        evidence_str = ", ".join(event_descriptions) if event_descriptions else "Multiple anomalous authentication and event telemetry entries"
    elif isinstance(raw_events, str) and raw_events.strip():
        evidence_str = raw_events
    else:
        evidence_str = "Multiple anomalous authentication and event telemetry entries"

    # Analyze patterns based on keywords
    combined_text = f"{title} {evidence_str} {str(incident)}".lower()
    patterns = []

    if ("failed login" in combined_text or "failed logins" in combined_text) and ("successful login" in combined_text or "login" in combined_text):
        patterns.append("potential credential compromise (brute-force password attempts followed by unauthorized login)")
    elif "failed login" in combined_text or "failed logins" in combined_text or "brute" in combined_text:
        patterns.append("credential brute-force attack attempts")
    elif "successful login" in combined_text or "new ip" in combined_text:
        patterns.append("suspicious access from an unrecognized source")

    if "privilege escalation" in combined_text or "privilege" in combined_text or "root" in combined_text:
        patterns.append("potential privilege escalation and unauthorized administrative access")

    if "data transfer" in combined_text or "exfiltration" in combined_text or "file download" in combined_text or "download" in combined_text:
        patterns.append("potential unauthorized data exfiltration")

    if not patterns:
        patterns.append("suspicious anomalies deviating from baseline system behavior")

    pattern_desc = "; ".join(patterns)

    return (
        f"[Quick Summary — AI analysis unavailable]\n"
        f"🚨 Incident {incident_id}: {title}\n"
        f"Risk Score: {risk_score}/100 — {severity}\n"
        f"Affected Asset: {asset}\n"
        f"Status: {status}\n"
        f"Evidence: {evidence_str}\n\n"
        f"This incident shows signs of {pattern_desc}.\n\n"
        f"Recommended next steps: review authentication logs for the affected asset, "
        f"verify whether this activity was authorized, and consider isolating the asset if unverified."
    )


def _build_prompt(incident: dict, question: str, history: list[dict] | None = None) -> str:
    """Assemble the prompt string sent in the user message to Gemini.

    Includes:
    - Incident metadata
    - The last MAX_HISTORY_TURNS turns of the conversation (if present)
    - The current analyst question

    Args:
        incident: Incident metadata dict.
        question: The current analyst question.
        history:  Optional list of {"role": "user"|"assistant", "content": str} dicts.

    Returns:
        Formatted prompt string capped at MAX_PROMPT_CHARS.
    """
    lines: list[str] = [f"Incident context: {incident}"]

    if history:
        recent = history[-(MAX_HISTORY_TURNS * 2):]
        if recent:
            lines.append("\n--- Recent conversation ---")
            for msg in recent:
                role_label = "Analyst" if msg["role"] == "user" else "Copilot"
                lines.append(f"{role_label}: {msg['content']}")
            lines.append("--- End of conversation ---")

    lines.append(f"\nAnalyst question: {question}")
    lines.append("\nRespond as the copilot would, based on this incident's specific details.")

    prompt = "\n".join(lines)

    if len(prompt) > MAX_PROMPT_CHARS:
        prompt = prompt[-MAX_PROMPT_CHARS:]
        logger.warning(
            "[Copilot] Prompt truncated to %d chars (was longer)", MAX_PROMPT_CHARS
        )

    return prompt


def get_copilot_response(
    incident: dict,
    question: str,
    history: list[dict] | None = None,
) -> str:
    """Send an analyst question with incident context to Google Gemini and return the answer.

    If an unrecoverable exception, timeout, or empty response occurs, falls back
    to generating a structured local summary from the incident context.

    Args:
        incident: Dict of incident metadata (id, asset, user, ip, etc.).
        question: The analyst's free-text question about the incident.
        history:  Optional recent conversation history (list of role/content dicts).

    Returns:
        The copilot's text response or a structured fallback summary.

    Raises:
        RateLimitError: Custom exception when Gemini API returns HTTP 429 / RESOURCE_EXHAUSTED.
    """
    prompt = _build_prompt(incident, question, history)
    prompt_len = len(prompt)

    logger.info(
        "[Copilot] → Sending to Gemini (%s) | prompt_chars=%d | history_turns=%d",
        GEMINI_MODEL,
        prompt_len,
        len(history) // 2 if history else 0,
    )
    t_start = time.perf_counter()

    try:
        response = model.generate_content(prompt)
    except BaseException as exc:
        elapsed = time.perf_counter() - t_start
        exc_type_name = type(exc).__qualname__
        logger.error(
            "[Copilot] ← Gemini CALL FAILED after %.2fs | ExceptionType: %s | Message: %s",
            elapsed,
            exc_type_name,
            exc,
            exc_info=True,
        )
        if isinstance(exc, Exception) and _is_rate_limit_error(exc):
            logger.warning(
                "[Copilot] ← Gemini RATE LIMITED after %.2fs — %s", elapsed, exc
            )
            raise RateLimitError(
                "Copilot is rate-limited by Gemini API. "
                "Please wait a moment and try again."
            ) from exc
        
        logger.warning("[Copilot] Falling back to local structured summary due to: %s", exc)
        return generate_fallback_summary(incident)

    elapsed = time.perf_counter() - t_start
    logger.info("[Copilot] ← Gemini responded in %.2fs", elapsed)

    if not response or not getattr(response, "text", None):
        logger.warning("[Copilot] Gemini returned empty response — using fallback summary")
        return generate_fallback_summary(incident)

    text = response.text.strip() if hasattr(response, "text") and response.text else None
    if not text:
        logger.warning("[Copilot] Gemini response text is blank — using fallback summary")
        return generate_fallback_summary(incident)

    return text
