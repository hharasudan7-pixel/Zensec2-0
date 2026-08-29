"""Tests for POST /api/v1/incidents/{incident_id}/response-actions

Covers:
    - Happy path with multiple valid actions → 200
    - Empty actions list → 200 (no crash, all-success result)
    - Missing required fields → 422
    - Results always contain action_ids from the request
    - Status field reflects outcome ("Contained" or "Containing")
"""
import sys
import os
from unittest.mock import MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

VALID_PAYLOAD = {
    "incident_id": "INC-7842",
    "actions": [
        {"action_id": "restrict_account", "target": "root"},
        {"action_id": "block_ip", "target": "185.15.2.14"},
    ],
    "analyst_id": "sec-admin-01",
}


def test_response_actions_success(client):
    """Valid payload with multiple actions → 200 with results for each action."""
    resp = client.post(
        "/api/v1/incidents/INC-7842/response-actions",
        json=VALID_PAYLOAD,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["incident_id"] == "INC-7842"
    assert "results" in body
    assert len(body["results"]) == 2
    returned_ids = {r["action_id"] for r in body["results"]}
    assert returned_ids == {"restrict_account", "block_ip"}
    assert "timestamp" in body
    assert body["status"] in ("Contained", "Containing")


def test_response_actions_empty_actions(client):
    """Empty actions list should not crash — returns empty results and 'Contained'."""
    payload = {**VALID_PAYLOAD, "actions": []}
    resp = client.post("/api/v1/incidents/INC-7842/response-actions", json=payload)
    assert resp.status_code == 200
    body = resp.json()
    assert body["results"] == []
    # all() of an empty sequence is True → status should be "Contained"
    assert body["status"] == "Contained"


def test_response_actions_single_action(client):
    """Single action in the list still returns a list with one result."""
    payload = {
        **VALID_PAYLOAD,
        "actions": [{"action_id": "revoke_sessions", "target": "root"}],
    }
    resp = client.post("/api/v1/incidents/INC-7842/response-actions", json=payload)
    assert resp.status_code == 200
    assert len(resp.json()["results"]) == 1


def test_response_actions_missing_analyst_id(client):
    """Missing analyst_id → Pydantic 422."""
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "analyst_id"}
    resp = client.post("/api/v1/incidents/INC-7842/response-actions", json=payload)
    assert resp.status_code == 422


def test_response_actions_missing_actions(client):
    """Missing actions field → 422."""
    payload = {k: v for k, v in VALID_PAYLOAD.items() if k != "actions"}
    resp = client.post("/api/v1/incidents/INC-7842/response-actions", json=payload)
    assert resp.status_code == 422


def test_response_actions_action_missing_target(client):
    """Action item missing target → 422."""
    payload = {
        **VALID_PAYLOAD,
        "actions": [{"action_id": "restrict_account"}],  # no target
    }
    resp = client.post("/api/v1/incidents/INC-7842/response-actions", json=payload)
    assert resp.status_code == 422
