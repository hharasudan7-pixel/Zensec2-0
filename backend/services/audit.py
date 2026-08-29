from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from models import AuditLog


def log_audit(
    db: Session,
    *,
    action: str,
    actor: str,
    incident_id: Optional[int] = None,
    event_id: Optional[int] = None,
    status: str = "SUCCESS",
    details: Optional[Dict[str, Any]] = None,
) -> AuditLog:
    entry = AuditLog(
        incident_id=incident_id,
        event_id=event_id,
        action=action,
        actor=actor,
        timestamp=datetime.utcnow(),
        status=status,
        details=details or {},
    )
    db.add(entry)
    db.flush()
    return entry


def serialize_audit(entry: AuditLog) -> Dict[str, Any]:
    return {
        "id": entry.id,
        "incident_id": entry.incident_id,
        "event_id": entry.event_id,
        "action": entry.action,
        "actor": entry.actor,
        "timestamp": entry.timestamp.isoformat(),
        "status": entry.status,
        "details": entry.details or {},
    }


def list_audit_logs(db: Session, incident_db_id: int) -> List[Dict[str, Any]]:
    entries = (
        db.query(AuditLog)
        .filter(AuditLog.incident_id == incident_db_id)
        .order_by(AuditLog.timestamp.asc())
        .all()
    )
    return [serialize_audit(entry) for entry in entries]
