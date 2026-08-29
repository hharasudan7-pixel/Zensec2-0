from datetime import datetime
from typing import Dict, List, Tuple, Union

SEVERITY_WEIGHTS = {"low": 0.2, "medium": 0.5, "high": 0.75, "critical": 1.0}


def classify_anomaly_score(score: float) -> str:
    """Map a 0-100 anomaly score to a human-readable risk classification.

    Thresholds:
        0-29   → NORMAL
        30-49  → LOW
        50-69  → MEDIUM
        70-84  → HIGH
        85-100 → CRITICAL
    """
    if score <= 29:
        return "NORMAL"
    if score <= 49:
        return "LOW"
    if score <= 69:
        return "MEDIUM"
    if score <= 84:
        return "HIGH"
    return "CRITICAL"


def _parse_hour(timestamp: Union[datetime, str, None]) -> float:
    """Extract the hour (0-23) from a timestamp that may be a datetime or ISO string.

    Returns 12.0 (midday, neutral) when the value is absent or unparseable,
    rather than raising AttributeError (B12 fix).
    """
    if timestamp is None:
        return 12.0
    if isinstance(timestamp, datetime):
        return float(timestamp.hour)
    if isinstance(timestamp, str):
        try:
            return float(datetime.fromisoformat(timestamp).hour)
        except ValueError:
            return 12.0
    # Unexpected type — degrade gracefully
    return 12.0


class AnomalyDetectionService:
    """ML-backed anomaly scorer using Isolation Forest with heuristic fallback."""

    def __init__(self):
        self.model = None
        self.model_ready = False
        self._init_model()

    def _init_model(self):
        """Fit an IsolationForest on synthetic baseline data.

        Falls back to a pure heuristic scorer if sklearn is unavailable.
        """
        try:
            from sklearn.ensemble import IsolationForest
            import numpy as np

            rng = np.random.default_rng(42)
            baseline = rng.normal(loc=0.0, scale=1.0, size=(500, 8))
            self.model = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
            self.model.fit(baseline)
            self.model_ready = True
        except Exception:
            self.model = None
            self.model_ready = False

    def extract_features(self, event: Dict, context: Dict) -> List[float]:
        """Convert a raw security event + context dict into an 8-element feature vector.

        Features (in order):
            0. failed_login_count (from context)
            1. login_frequency   (from context)
            2. auth_failed flag  (1.0 if authentication_status == "failed")
            3. auth_success flag (1.0 if authentication_status == "success")
            4. hour of event     (normalised to 0-1)
            5. privilege_change  (1.0 if "privilege" in event_type)
            6. sensitive_access  (1.0 if "document"/"data"/"file" in event_type)
            7. combined severity + unusual_ip score
        """
        failed_logins = float(context.get("failed_login_count", 0))
        login_frequency = float(context.get("login_frequency", 0))
        auth_failed = 1.0 if event.get("authentication_status") == "failed" else 0.0
        auth_success = 1.0 if event.get("authentication_status") == "success" else 0.0

        # B12 FIX: use _parse_hour() so string timestamps don't raise AttributeError
        hour = _parse_hour(event.get("timestamp")) / 23.0

        privilege_change = 1.0 if "privilege" in event.get("event_type", "").lower() else 0.0
        sensitive_access = 1.0 if any(
            k in event.get("event_type", "").lower() for k in ["document", "data", "file"]
        ) else 0.0
        severity = SEVERITY_WEIGHTS.get(event.get("severity", "low"), 0.2)
        unusual_ip = 1.0 if context.get("is_unusual_ip") else 0.0
        return [
            failed_logins,
            login_frequency,
            auth_failed,
            auth_success,
            hour,
            privilege_change,
            sensitive_access,
            severity * 2 + unusual_ip,
        ]

    def score_event(self, event: Dict, context: Dict) -> Tuple[float, str, str]:
        """Score a security event and return (score, classification, model_status).

        Args:
            event:   Raw security event dict (from SecurityEvent model or ingestion).
            context: Surrounding context dict with aggregated metrics.

        Returns:
            A 3-tuple of:
                score          – float in [0, 100]
                classification – one of NORMAL / LOW / MEDIUM / HIGH / CRITICAL
                model_status   – "ok" if ML model was used, "unavailable" otherwise
        """
        features = self.extract_features(event, context)
        if not self.model_ready or self.model is None:
            heuristic = min(
                100.0,
                features[0] * 8
                + features[1] * 4
                + features[2] * 15
                + features[5] * 25
                + features[6] * 20
                + features[7] * 20,
            )
            return round(heuristic, 1), classify_anomaly_score(heuristic), "unavailable"

        raw = float(self.model.decision_function([features])[0])
        normalized = max(0.0, min(100.0, (0.5 - raw) * 120))
        if context.get("failed_login_count", 0) >= 3:
            normalized = max(normalized, 35.0)
        if context.get("is_unusual_ip"):
            normalized = max(normalized, 60.0)
        if "privilege" in event.get("event_type", "").lower():
            normalized = max(normalized, 80.0)
        if "document" in event.get("event_type", "").lower() or "sensitive" in event.get("event_type", "").lower():
            normalized = max(normalized, 85.0)
        return round(normalized, 1), classify_anomaly_score(normalized), "ok"
