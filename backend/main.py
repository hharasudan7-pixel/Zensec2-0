from dotenv import load_dotenv
load_dotenv()
from services.copilot import get_copilot_response, RateLimitError, generate_fallback_summary

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
import time
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("zentrasec")

app = FastAPI(title="ZentraSec API", description="AI-Powered Cybersecurity APIs", version="1.0.0")

# ---------------------------------------------------------------------------
# CORS — explicit origins; "*" is kept for development convenience but
# allow_credentials must be False when allow_origins contains a wildcard.
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request logging middleware — fires BEFORE any route handler or LLM call
# ---------------------------------------------------------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("► %s %s (from %s)", request.method, request.url.path, request.client)
    response = await call_next(request)
    logger.info("◄ %s %s → %s", request.method, request.url.path, response.status_code)
    return response

class ResponseAction(BaseModel):
    action_id: str
    target: str

class ResponseExecutionRequest(BaseModel):
    incident_id: str
    actions: List[ResponseAction]
    analyst_id: str

class ActionStatus(BaseModel):
    action_id: str
    status: str # SUCCESS, FAILED
    reason: str = ""

class CopilotRequest(BaseModel):
    incident: dict
    question: str
    # Optional conversation history — list of {"role": "user"|"assistant", "content": str}.
    # The backend caps how many turns are used (see services/copilot.py MAX_HISTORY_TURNS).
    history: List[dict] = []

@app.post("/api/v1/incidents/{incident_id}/response-actions")
async def execute_response_actions(incident_id: str, request: ResponseExecutionRequest):
    """Simulate executing a list of security response actions against an incident.

    Each action has a 10 % chance of failure to mimic real-world partial failures.
    Returns the per-action results and an overall containment status.
    """
    await asyncio.sleep(2)  # Simulate processing delay

    results = []
    for action in request.actions:
        # 10% chance of failure for simulation realism
        if random.random() < 0.1:
            results.append(ActionStatus(
                action_id=action.action_id,
                status="FAILED",
                reason="Target unreachable or access denied",
            ))
        else:
            results.append(ActionStatus(
                action_id=action.action_id,
                status="SUCCESS",
                reason="Action executed successfully",
            ))

    return {
        "incident_id": incident_id,
        "results": results,
        "timestamp": time.time(),
        "status": "Contained" if all(r.status == "SUCCESS" for r in results) else "Containing",
    }

# ---------------------------------------------------------------------------
# Timeout tuning:
#   COPILOT_TIMEOUT_SECONDS (25s) is intentionally shorter than the frontend
#   AbortController limit (28s).  When timed out or unreachable, the copilot
#   falls back to a structured incident summary so the user is never stranded.
# ---------------------------------------------------------------------------
COPILOT_TIMEOUT_SECONDS = 25

@app.post("/api/v1/copilot/chat")
async def copilot_chat(request: CopilotRequest):
    """Accept a user question and incident context, call Google Gemini in a thread-pool
    executor, and return the AI answer or a structured fallback summary on timeout/error.

    Raises HTTP 429 if Gemini is rate-limiting.
    Falls back to a structured incident summary if Gemini times out or errors.
    """
    logger.info(
        "[Copilot] Request received (incident=%s, history_len=%d)",
        request.incident.get("id", "?"),
        len(request.history),
    )
    logger.debug("[Copilot] Question: %r", request.question)

    loop = asyncio.get_event_loop()
    try:
        answer = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                get_copilot_response,
                request.incident,
                request.question,
                request.history,   # ← pass conversation history
            ),
            timeout=COPILOT_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        logger.warning(
            "[Copilot] Gemini call timed out after %ds — serving structured fallback summary",
            COPILOT_TIMEOUT_SECONDS,
        )
        answer = generate_fallback_summary(request.incident)
    except RateLimitError as exc:
        logger.warning("[Copilot] Rate limited by Gemini: %s", exc)
        raise HTTPException(
            status_code=429,
            detail=str(exc),
            headers={"Retry-After": "60"},
        )
    except Exception as exc:
        logger.exception("[Copilot] Gemini call failed: %s — serving structured fallback summary", exc)
        answer = generate_fallback_summary(request.incident)
    return {"answer": answer}

@app.get("/")
def read_root():
    return {"status": "ZentraSec Backend Running", "modules": ["ML Anomaly Detection", "RAG Copilot", "Event Correlation"]}

