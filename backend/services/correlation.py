from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session

from models import SecurityEvent, Incident, IncidentEvent, AttackTimeline, WebsiteConnection
from schemas import EventIngestRequest
from services.anomaly_detection import AnomalyDetectionService

anomaly_service = AnomalyDetectionService()

STAGE_MAPPING = {
    "PORT_SCAN": "Reconnaissance",
    "LOGIN_FAILED": "Initial Access",
    "LOGIN_SUCCESS": "Initial Access",
    "SUSPICIOUS_LOGIN": "Initial Access",
    "POWERSHELL_EXECUTION": "Execution",
    "PRIVILEGE_ESCALATION": "Privilege Escalation",
    "FILE_ACCESS": "Collection",
    "MASS_FILE_ACCESS": "Collection",
    "DATA_EXPORT": "Exfiltration"
}

BASE_RISK = {
    "PORT_SCAN": 10.0,
    "LOGIN_FAILED": 5.0,
    "LOGIN_SUCCESS": 0.0,
    "SUSPICIOUS_LOGIN": 25.0,
    "POWERSHELL_EXECUTION": 20.0,
    "PRIVILEGE_ESCALATION": 30.0,
    "FILE_ACCESS": 5.0,
    "MASS_FILE_ACCESS": 15.0,
    "DATA_EXPORT": 35.0
}

def determine_stage(event_type: str) -> str:
    return STAGE_MAPPING.get(event_type.upper(), "Unknown")

class CorrelationEngine:
    def __init__(self, db: Session):
        self.db = db

    def process_event(self, request: EventIngestRequest) -> SecurityEvent:
        event_id = request.event_id or f"EVT-{uuid.uuid4().hex[:8]}"
        now = datetime.utcnow()
        timestamp = request.timestamp or now

        # Connection ID lookup or registration
        connection_id = request.connection_id
        if not connection_id and request.website_url:
            # Check if url mapping exists
            conn = self.db.query(WebsiteConnection).filter(WebsiteConnection.website_url == request.website_url).first()
            if conn:
                connection_id = conn.connection_id
            else:
                # Dynamic connection registration
                from urllib.parse import urlparse
                domain = urlparse(request.website_url).netloc or request.website_url
                domain = domain.replace("www.", "").split(":")[0]
                clean_name = domain.split(".")[0].capitalize()
                
                connection_id = f"CONN-{clean_name.upper()}-{uuid.uuid4().hex[:4].upper()}"
                new_conn = WebsiteConnection(
                    connection_id=connection_id,
                    website_url=request.website_url,
                    customer_name=f"{clean_name} Customer"
                )
                self.db.add(new_conn)
                self.db.commit()
                self.db.refresh(new_conn)

        context = {
            "failed_login_count": 0,
            "login_frequency": 0,
            "is_unusual_ip": False
        }
        
        if request.user_id:
            recent_failed = self.db.query(SecurityEvent).filter(
                SecurityEvent.user_id == request.user_id,
                SecurityEvent.connection_id == connection_id,
                SecurityEvent.event_type == "LOGIN_FAILED",
                SecurityEvent.timestamp >= now - timedelta(minutes=30)
            ).count()
            context["failed_login_count"] = recent_failed
            
            recent_ips = self.db.query(SecurityEvent.source_ip).filter(
                SecurityEvent.user_id == request.user_id,
                SecurityEvent.connection_id == connection_id,
                SecurityEvent.timestamp >= now - timedelta(days=7)
            ).distinct().all()
            if request.source_ip and request.source_ip not in [ip[0] for ip in recent_ips if ip[0]]:
                context["is_unusual_ip"] = True

        event_dict = request.model_dump()
        event_dict["timestamp"] = timestamp
        
        score, classification, ml_status = anomaly_service.score_event(event_dict, context)

        sec_event = SecurityEvent(
            event_id=event_id,
            timestamp=timestamp,
            user_id=request.user_id,
            source_ip=request.source_ip,
            destination=request.destination,
            device_id=request.device_id,
            event_type=request.event_type,
            severity=request.severity,
            authentication_status=request.authentication_status,
            location=request.location,
            metadata_json=request.metadata,
            anomaly_score=score,
            anomaly_classification=classification,
            connection_id=connection_id,
            ml_status=ml_status
        )
        self.db.add(sec_event)
        self.db.commit()
        self.db.refresh(sec_event)

        self.correlate(sec_event)
        return sec_event

    def correlate(self, new_event: SecurityEvent):
        window_start = new_event.timestamp - timedelta(minutes=30)
        
        related_events = []
        if new_event.user_id:
            related_events = self.db.query(SecurityEvent).filter(
                SecurityEvent.user_id == new_event.user_id,
                SecurityEvent.connection_id == new_event.connection_id,
                SecurityEvent.timestamp >= window_start,
                SecurityEvent.timestamp <= new_event.timestamp
            ).order_by(SecurityEvent.timestamp.asc()).all()
        elif new_event.source_ip:
             related_events = self.db.query(SecurityEvent).filter(
                SecurityEvent.source_ip == new_event.source_ip,
                SecurityEvent.connection_id == new_event.connection_id,
                SecurityEvent.timestamp >= window_start,
                SecurityEvent.timestamp <= new_event.timestamp
            ).order_by(SecurityEvent.timestamp.asc()).all()
            
        if not related_events:
            related_events = [new_event]
            
        if new_event.id not in [e.id for e in related_events]:
            related_events.append(new_event)

        if len(related_events) < 2:
            return 

        existing_incident_id = None
        for ev in related_events:
            inc_ev = self.db.query(IncidentEvent).filter(IncidentEvent.event_id == ev.id).first()
            if inc_ev:
                existing_incident_id = inc_ev.incident_id
                break

        if existing_incident_id:
            incident = self.db.query(Incident).filter(Incident.id == existing_incident_id).first()
            if incident and not incident.connection_id and new_event.connection_id:
                incident.connection_id = new_event.connection_id
        else:
            incident = Incident(
                incident_id=f"INC-{uuid.uuid4().hex[:8]}",
                title="Correlated Security Alert",
                severity="MEDIUM",
                status="OPEN",
                user_id=new_event.user_id,
                source_ip=new_event.source_ip,
                connection_id=new_event.connection_id
            )
            self.db.add(incident)
            self.db.commit()
            self.db.refresh(incident)

        total_risk = 0.0
        
        self.db.query(IncidentEvent).filter(IncidentEvent.incident_id == incident.id).delete()
        self.db.query(AttackTimeline).filter(AttackTimeline.incident_id == incident.id).delete()
        
        stages_detected = []
        
        for i, ev in enumerate(related_events):
            base_r = BASE_RISK.get(ev.event_type.upper(), 5.0)
            if ev.anomaly_score:
                base_r += ev.anomaly_score * 0.2
            
            risk_contribution = round(min(base_r, 100.0 - total_risk), 1)
            total_risk += risk_contribution
            
            stage = determine_stage(ev.event_type)
            if stage not in stages_detected:
                stages_detected.append(stage)
            
            inc_evt = IncidentEvent(
                incident_id=incident.id,
                event_id=ev.id,
                relationship_type="correlated"
            )
            self.db.add(inc_evt)
            
            desc = ev.metadata_json.get("description", "") if ev.metadata_json else ""
            timeline = AttackTimeline(
                incident_id=incident.id,
                event_id=ev.id,
                timestamp=ev.timestamp,
                sequence=i+1,
                description=f"[{stage}] {ev.event_type}: {desc}",
                source=ev.source_ip,
                user_id=ev.user_id,
                anomaly_score=ev.anomaly_score,
                severity=ev.severity,
                risk_contribution=risk_contribution
            )
            self.db.add(timeline)
            
        total_risk = min(100.0, total_risk)
        incident.risk_score = round(total_risk, 1)
        
        if total_risk < 25:
            incident.severity = "LOW"
        elif total_risk < 50:
            incident.severity = "MEDIUM"
        elif total_risk < 75:
            incident.severity = "HIGH"
        else:
            incident.severity = "CRITICAL"
            
        if "Exfiltration" in stages_detected and "Privilege Escalation" in stages_detected:
            incident.title = "Possible Account Compromise and Exfiltration"
        elif "Execution" in stages_detected and "Reconnaissance" in stages_detected:
            incident.title = "Multi-Stage Attack Detected"
        elif "Initial Access" in stages_detected and len(related_events) >= 3:
            incident.title = "Possible Account Compromise"
            
        summary = (
            f"Multiple related events ({len(related_events)}) were detected for "
            f"{incident.user_id or incident.source_ip} within a 30-minute window. "
            f"The activity progressed across {len(stages_detected)} stages: {', '.join(stages_detected)}. "
            f"The sequence indicates {incident.title.lower()}."
        )
        incident.description = summary
        incident.updated_at = datetime.utcnow()
        
        self.db.commit()
