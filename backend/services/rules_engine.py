"""Real-time Rule & Correlation Engine for the two-laptop live demo.

Rules implemented:
  1. BRUTE_FORCE_PATTERN        — >= 5 LOGIN_FAILURE within a 2-minute window (per user/IP).
  2. SUSPICIOUS_AUTH_SEQUENCE   — brute force followed by a LOGIN_SUCCESS.
  3. POTENTIAL_ACCOUNT_COMPROMISE — failures + success + PRIVILEGE_ACCESS / LARGE_FILE_DOWNLOAD.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Risk band mapping: 0-24 LOW, 25-49 MEDIUM, 50-74 HIGH, 75-100 CRITICAL
BRUTE_FORCE_WINDOW_MINUTES = 2
BRUTE_FORCE_THRESHOLD = 5
CORRELATION_WINDOW_MINUTES = 15

BASE_SCORES = {
    "LOGIN_FAILURE": 10.0,
    "LOGIN_FAILED": 10.0,
    "LOGIN_SUCCESS": 5.0,
    "PRIVILEGE_ACCESS": 45.0,
    "PRIVILEGE_ESCALATION": 45.0,
    "LARGE_FILE_DOWNLOAD": 40.0,
    "DATA_EXPORT": 40.0,
    "PAGE_VIEW": 2.0,
}


def classify_risk(score: float) -> str:
    """Map a 0-100 score to the demo risk bands."""
    if score < 25:
        return "LOW"
    if score < 50:
        return "MEDIUM"
    if score < 75:
        return "HIGH"
    return "CRITICAL"


class RulesEngine:
    """Stateless helpers that query recent events to detect attack patterns."""

    def __init__(self, db):
        self.db = db

    def _recent_events(self, event_type: str, user_id: Optional[str],
                       source_ip: Optional[str], connection_id: Optional[str],
                       minutes: int, since: datetime):
        from models import SecurityEvent
        from sqlalchemy import or_

        match = [SecurityEvent.event_type.in_([event_type, event_type.replace("_FAILURE", "_FAILED")])]
        ident = []
        if user_id:
            ident.append(SecurityEvent.user_id == user_id)
        if source_ip:
            ident.append(SecurityEvent.source_ip == source_ip)
        if not ident:
            return []
        return self.db.query(SecurityEvent).filter(
            *match,
            or_(*ident),
            SecurityEvent.connection_id == connection_id,
            SecurityEvent.timestamp >= since,
        ).order_by(SecurityEvent.timestamp.asc()).all()

    def evaluate(self, event_type: str, user_id: Optional[str], source_ip: Optional[str],
                 connection_id: Optional[str], timestamp: datetime) -> Dict:
        """Run all rules against the incoming event and return detection results."""
        detections: List[str] = []
        fault_desc: Optional[Dict] = None

        etype = (event_type or "").upper()
        base = BASE_SCORES.get(etype, 5.0)

        # ---- Rule 1: Brute Force Detection (5 failures in 2 mins) ----
        failures = self._recent_events(
            "LOGIN_FAILURE", user_id, source_ip, connection_id,
            BRUTE_FORCE_WINDOW_MINUTES, timestamp - timedelta(minutes=BRUTE_FORCE_WINDOW_MINUTES),
        )
        brute_force = len(failures) >= BRUTE_FORCE_THRESHOLD

        if brute_force and "BRUTE_FORCE_PATTERN" not in detections:
            detections.append("BRUTE_FORCE_PATTERN")
            base = max(base, 60.0)

        # ---- Rule 2: Brute force + Success ----
        if brute_force and etype in ("LOGIN_SUCCESS", "SUSPICIOUS_LOGIN"):
            detections.append("SUSPICIOUS_AUTHENTICATION_SEQUENCE")
            base = max(base, 70.0)

        # ---- Rule 3: Full compromise chain ----
        if etype in ("PRIVILEGE_ACCESS", "PRIVILEGE_ESCALATION", "LARGE_FILE_DOWNLOAD", "DATA_EXPORT"):
            window_start = timestamp - timedelta(minutes=CORRELATION_WINDOW_MINUTES)
            chain_failures = self._recent_events(
                "LOGIN_FAILURE", user_id, source_ip, connection_id,
                CORRELATION_WINDOW_MINUTES, window_start,
            )
            chain_success = [
                e for e in self._recent_events(
                    "LOGIN_SUCCESS", user_id, source_ip, connection_id,
                    CORRELATION_WINDOW_MINUTES, window_start,
                )
            ]
            if len(chain_failures) >= BRUTE_FORCE_THRESHOLD and chain_success:
                detections.append("POTENTIAL_ACCOUNT_COMPROMISE")
                base = max(base, 90.0)

        # ---- Build a fault description when any rule fires ----
        if detections:
            user_id = event.user_id
            source_ip = event.source_ip
            target = user_id or source_ip or "unknown"
            if "POTENTIAL_ACCOUNT_COMPROMISE" in detections:
                summary = (
                    f"Potential account compromise detected: repeated login failures followed by a "
                    f"successful login and privileged access for user '{target}' from {source_ip}."
                )
            elif "SUSPICIOUS_AUTHENTICATION_SEQUENCE" in detections:
                summary = (
                    f"Suspicious authentication sequence: successful login for '{target}' "
                    f"immediately following {len(chain_failures)} failed attempts from {source_ip}."
                )
            else:
                summary = (
                    f"Brute force pattern detected: {len(chain_failures)} failed login attempts "
                    f"against '{target}' from {source_ip} within "
                    f"{BRUTE_FORCE_WINDOW_MINUTES} minutes."
                )
            fault_desc = {
                "detections": detections,
                "summary": summary,
                "affected_user": user_id,
                "source_ip": source_ip,
                "failed_attempts": len(failures),
            }

        return {
            "score": round(min(100.0, base), 1),
            "risk_band": classify_risk(base),
            "detections": detections,
            "fault_description": fault_desc,
        }
