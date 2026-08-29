"""Tests for services/anomaly_detection.py

Covers:
    - classify_anomaly_score boundary values
    - extract_features returns correct shape
    - score_event with datetime timestamp (normal path)
    - score_event with string ISO timestamp (B12 regression)
    - score_event with None/missing timestamp (B12 regression)
    - score_event with model unavailable (heuristic fallback)
    - Privilege escalation event boosts score
    - Sensitive data event boosts score
"""
import sys
import os
from datetime import datetime
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.anomaly_detection import (  # noqa: E402
    AnomalyDetectionService,
    classify_anomaly_score,
    _parse_hour,
)


# ===========================================================================
# classify_anomaly_score
# ===========================================================================


@pytest.mark.parametrize("score,expected", [
    (0,   "NORMAL"),
    (29,  "NORMAL"),
    (30,  "LOW"),
    (49,  "LOW"),
    (50,  "MEDIUM"),
    (69,  "MEDIUM"),
    (70,  "HIGH"),
    (84,  "HIGH"),
    (85,  "CRITICAL"),
    (100, "CRITICAL"),
])
def test_classify_anomaly_score_boundaries(score, expected):
    """All boundary values must map to the correct classification."""
    assert classify_anomaly_score(score) == expected


# ===========================================================================
# _parse_hour helper
# ===========================================================================


def test_parse_hour_with_datetime():
    dt = datetime(2024, 1, 15, 14, 30, 0)  # 14:30
    assert _parse_hour(dt) == 14.0


def test_parse_hour_with_iso_string():
    assert _parse_hour("2024-01-15T09:00:00") == 9.0


def test_parse_hour_with_none():
    assert _parse_hour(None) == 12.0


def test_parse_hour_with_invalid_string():
    """An unparseable string should fall back to 12.0, not raise."""
    assert _parse_hour("not-a-date") == 12.0


# ===========================================================================
# extract_features
# ===========================================================================


def test_extract_features_returns_eight_floats():
    svc = AnomalyDetectionService()
    event = {"event_type": "login_attempt", "severity": "high",
              "authentication_status": "failed", "timestamp": datetime.now()}
    context = {"failed_login_count": 3, "login_frequency": 5, "is_unusual_ip": True}
    features = svc.extract_features(event, context)
    assert len(features) == 8
    assert all(isinstance(f, float) for f in features)


def test_extract_features_string_timestamp_no_crash():
    """B12 regression: string timestamp must not raise AttributeError."""
    svc = AnomalyDetectionService()
    event = {
        "event_type": "login_attempt",
        "severity": "medium",
        "timestamp": "2024-06-01T08:30:00",  # <-- string, not datetime
    }
    context = {}
    features = svc.extract_features(event, context)  # Must not raise
    assert len(features) == 8


def test_extract_features_no_timestamp_key():
    """B12 regression: missing timestamp key must not crash."""
    svc = AnomalyDetectionService()
    event = {"event_type": "file_access", "severity": "low"}
    context = {}
    features = svc.extract_features(event, context)
    assert len(features) == 8


# ===========================================================================
# score_event — heuristic fallback (model unavailable)
# ===========================================================================


def test_score_event_heuristic_fallback():
    """With model_ready=False, the heuristic path must return a valid tuple."""
    svc = AnomalyDetectionService()
    svc.model_ready = False
    svc.model = None

    event = {"event_type": "login_attempt", "severity": "high",
              "authentication_status": "failed"}
    context = {"failed_login_count": 5}
    score, classification, status = svc.score_event(event, context)

    assert 0.0 <= score <= 100.0
    assert classification in ("NORMAL", "LOW", "MEDIUM", "HIGH", "CRITICAL")
    assert status == "unavailable"


def test_score_event_privilege_escalation_boosts_score():
    """Privilege-change events must score >= 80 when the ML model is active."""
    svc = AnomalyDetectionService()
    if not svc.model_ready:
        pytest.skip("sklearn not available; skipping ML-path test")

    event = {"event_type": "privilege_escalation", "severity": "high"}
    context = {}
    score, _, _ = svc.score_event(event, context)
    assert score >= 80.0


def test_score_event_sensitive_data_boosts_score():
    """Sensitive document access must score >= 85 when the ML model is active."""
    svc = AnomalyDetectionService()
    if not svc.model_ready:
        pytest.skip("sklearn not available; skipping ML-path test")

    event = {"event_type": "document_download", "severity": "medium"}
    context = {}
    score, _, _ = svc.score_event(event, context)
    assert score >= 85.0


def test_score_event_returns_valid_tuple_with_string_timestamp():
    """B12 regression: score_event must complete without error when timestamp is a string."""
    svc = AnomalyDetectionService()
    event = {
        "event_type": "login_attempt",
        "severity": "low",
        "timestamp": "2024-06-01T08:30:00",
    }
    context = {}
    result = svc.score_event(event, context)
    assert len(result) == 3
    score, classification, _ = result
    assert 0.0 <= score <= 100.0
    assert classification in ("NORMAL", "LOW", "MEDIUM", "HIGH", "CRITICAL")
