"""Tests for POST /api/v1/copilot/chat

Covers:
    - Happy path (valid incident + question)
    - Empty question string
    - Missing required fields (question / incident)
    - Malformed JSON body
    - Incident with extra unexpected fields
    - Incident with empty dict
    - Gemini API raises a generic exception → Fallback HTTP 200 summary
    - Gemini API times out → Fallback HTTP 200 summary (not 504)
    - Gemini API rate limit (429) → HTTP 429
    - Extremely long question (10 000 chars)
    - Gemini returns empty / none content → Fallback HTTP 200 summary
    - Direct verification of generate_fallback_summary keyword analysis
"""
import asyncio
from unittest.mock import MagicMock, patch

import pytest
from services.copilot import generate_fallback_summary

# ---------------------------------------------------------------------------
# Shared valid incident payload used across multiple tests
# ---------------------------------------------------------------------------
VALID_INCIDENT = {
    "id": "INC-7842",
    "asset": "Prod-DB-01",
    "user": "root",
    "ip": "185.15.2.14",
    "title": "Unauthorized Database Access",
    "risk_score": 88,
    "severity": "CRITICAL",
    "status": "Investigating",
    "events": [
        "50 failed logins",
        "successful login from new IP",
        "privilege escalation",
        "large file download",
    ],
}

VALID_PAYLOAD = {"incident": VALID_INCIDENT, "question": "What happened?"}


# ===========================================================================
# Happy-path tests
# ===========================================================================


def test_happy_path(client, mock_gemini):
    """Valid incident + question → 200 with live answer text."""
    resp = client.post("/api/v1/copilot/chat", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body
    assert body["answer"] == "Mocked copilot answer"


def test_incident_extra_fields(client, mock_gemini):
    """Extra unknown fields in incident dict must not crash the endpoint."""
    payload = {
        "incident": {**VALID_INCIDENT, "unknown_field": "surprise", "nested": {"a": 1}},
        "question": "Any extra data crash?",
    }
    resp = client.post("/api/v1/copilot/chat", json=payload)
    assert resp.status_code == 200


def test_empty_incident_dict(client, mock_gemini):
    """Empty incident dict is valid — copilot should still respond."""
    payload = {"incident": {}, "question": "No incident data, what can you tell me?"}
    resp = client.post("/api/v1/copilot/chat", json=payload)
    assert resp.status_code == 200


def test_long_question(client, mock_gemini):
    """A 10 000-character question should not cause an unhandled exception."""
    payload = {"incident": VALID_INCIDENT, "question": "A" * 10_000}
    resp = client.post("/api/v1/copilot/chat", json=payload)
    assert resp.status_code in (200, 413, 422)


# ===========================================================================
# Validation / bad-input tests
# ===========================================================================


def test_empty_question_string(client, mock_gemini):
    """An empty string question is allowed through to Gemini."""
    payload = {"incident": VALID_INCIDENT, "question": ""}
    resp = client.post("/api/v1/copilot/chat", json=payload)
    assert resp.status_code == 200


def test_missing_question_field(client):
    """Body missing 'question' field → Pydantic 422."""
    resp = client.post("/api/v1/copilot/chat", json={"incident": VALID_INCIDENT})
    assert resp.status_code == 422


def test_missing_incident_field(client):
    """Body missing 'incident' field → Pydantic 422."""
    resp = client.post("/api/v1/copilot/chat", json={"question": "Where is the incident?"})
    assert resp.status_code == 422


def test_missing_both_fields(client):
    """Completely empty body → 422."""
    resp = client.post("/api/v1/copilot/chat", json={})
    assert resp.status_code == 422


def test_malformed_json(client):
    """Non-JSON body → 422."""
    resp = client.post(
        "/api/v1/copilot/chat",
        content=b"this is not json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 422


def test_question_is_null(client):
    """question: null → 422 (field is required, not Optional)."""
    resp = client.post("/api/v1/copilot/chat", json={"incident": VALID_INCIDENT, "question": None})
    assert resp.status_code == 422


# ===========================================================================
# Fallback & Error Handling tests
# ===========================================================================


def test_gemini_timeout_returns_fallback_200(client, mock_gemini):
    """When the Gemini call times out, the endpoint returns HTTP 200 with a structured fallback summary."""
    with patch("main.asyncio.wait_for", side_effect=asyncio.TimeoutError):
        resp = client.post("/api/v1/copilot/chat", json=VALID_PAYLOAD)

    assert resp.status_code == 200
    answer = resp.json()["answer"]
    assert "[Quick Summary — AI analysis unavailable]" in answer
    assert "INC-7842" in answer
    assert "88/100" in answer
    assert "Prod-DB-01" in answer


def test_gemini_api_error_returns_fallback_200(client, mock_gemini):
    """When Gemini raises a generic exception, the endpoint returns HTTP 200 with a structured fallback."""
    mock_gemini.side_effect = Exception("Internal server error from Gemini backend")
    resp = client.post("/api/v1/copilot/chat", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    answer = resp.json()["answer"]
    assert "[Quick Summary — AI analysis unavailable]" in answer
    assert "INC-7842" in answer


def test_gemini_empty_response_returns_fallback_200(client, mock_gemini):
    """When Gemini returns an empty response or empty text, the endpoint falls back gracefully."""
    empty_response = MagicMock()
    empty_response.text = ""
    mock_gemini.return_value = empty_response

    resp = client.post("/api/v1/copilot/chat", json=VALID_PAYLOAD)
    assert resp.status_code == 200
    answer = resp.json()["answer"]
    assert "[Quick Summary — AI analysis unavailable]" in answer
    assert "INC-7842" in answer


def test_gemini_rate_limit_returns_429(client, mock_gemini):
    """When Gemini returns a 429 / RESOURCE_EXHAUSTED rate limit error, the endpoint returns
    HTTP 429 with a friendly rate-limit message and Retry-After header.
    """
    mock_gemini.side_effect = Exception("429 Resource exhausted: quota exceeded")
    resp = client.post("/api/v1/copilot/chat", json=VALID_PAYLOAD)
    assert resp.status_code == 429
    detail = resp.json()["detail"].lower()
    assert "rate" in detail or "quota" in detail or "limit" in detail
    assert resp.headers.get("retry-after") == "60"


def test_generate_fallback_summary_keyword_patterns():
    """Verify generate_fallback_summary accurately detects attack patterns from event keywords."""
    incident = {
        "id": "INC-9901",
        "title": "Suspicious DB Ingestion",
        "risk_score": 92,
        "asset": "Analytics-Cluster-02",
        "status": "Active",
        "events": [
            "50 failed logins",
            "successful login from new IP",
            "privilege escalation",
            "large file download",
        ],
    }
    summary = generate_fallback_summary(incident)
    assert "[Quick Summary — AI analysis unavailable]" in summary
    assert "INC-9901" in summary
    assert "92/100" in summary
    assert "CRITICAL" in summary
    assert "credential compromise" in summary
    assert "privilege escalation" in summary
    assert "data exfiltration" in summary
    assert "Recommended next steps" in summary
