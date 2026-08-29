from dotenv import load_dotenv
load_dotenv()
from services.copilot import get_copilot_response, RateLimitError, generate_fallback_summary

from fastapi import FastAPI, HTTPException, Request, Depends, WebSocket, WebSocketDisconnect
import sqlalchemy
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import random
import time
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("zentrasec")

from database import get_db, engine
from schemas import EventIngestRequest, WebsiteConnectionCreate, WebsiteConnectionResponse
from services.correlation import CorrelationEngine
import models

inspector = sqlalchemy.inspect(engine)
if inspector.has_table("security_events"):
    columns = [col['name'] for col in inspector.get_columns("security_events")]
    if "connection_id" not in columns:
        print("Schema changed (connection_id missing). Recreating database...")
        models.Base.metadata.drop_all(bind=engine)

models.Base.metadata.create_all(bind=engine)

# Seed initial connection if none exists
with Session(engine) as db:
    if not db.query(models.WebsiteConnection).first():
        default_conn = models.WebsiteConnection(
            connection_id="default-zensec-001",
            website_url="https://admin.zensec.ai",
            customer_name="Zensec Default Customer"
        )
        db.add(default_conn)
        db.commit()

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

@app.post("/api/v1/events")
def ingest_event(request: EventIngestRequest, db: Session = Depends(get_db)):
    engine = CorrelationEngine(db)
    event = engine.process_event(request)
    return {"status": "success", "event_id": event.event_id}

@app.post("/api/v1/simulate/timeline")
def simulate_timeline(db: Session = Depends(get_db)):
    engine = CorrelationEngine(db)
    
    user = "employee01"
    ip = "10.10.10.25"
    unusual_ip = "192.168.1.100"
    
    now = datetime.utcnow()
    
    events = [
        {"type": "LOGIN_FAILED", "ip": ip, "time_offset": 0, "desc": "Failed login attempt"},
        {"type": "LOGIN_FAILED", "ip": ip, "time_offset": 1, "desc": "Failed login attempt"},
        {"type": "LOGIN_FAILED", "ip": ip, "time_offset": 2, "desc": "Failed login attempt"},
        {"type": "LOGIN_FAILED", "ip": ip, "time_offset": 3, "desc": "Failed login attempt"},
        {"type": "LOGIN_FAILED", "ip": ip, "time_offset": 4, "desc": "Failed login attempt"},
        {"type": "LOGIN_SUCCESS", "ip": ip, "time_offset": 5, "desc": "Successful login after failures"},
        {"type": "SUSPICIOUS_LOGIN", "ip": unusual_ip, "time_offset": 10, "desc": "Login from unusual location"},
        {"type": "PRIVILEGE_ESCALATION", "ip": unusual_ip, "time_offset": 15, "desc": "User added to Administrators group"},
        {"type": "MASS_FILE_ACCESS", "ip": unusual_ip, "time_offset": 20, "desc": "Accessed 500+ documents in 1 minute"},
        {"type": "DATA_EXPORT", "ip": unusual_ip, "time_offset": 25, "desc": "Large outbound data transfer detected"}
    ]
    
    processed = []
    
    for ev in events:
        req = EventIngestRequest(
            timestamp=now + timedelta(minutes=ev["time_offset"]),
            user_id=user,
            source_ip=ev["ip"],
            event_type=ev["type"],
            metadata={"description": ev["desc"]}
        )
        saved_ev = engine.process_event(req)
        processed.append(saved_ev.event_id)
        
    from models import Incident, AttackTimeline
    latest_incident = db.query(Incident).order_by(Incident.created_at.desc()).first()
        
    return {
        "status": "Simulation complete", 
        "events_processed": len(processed),
        "incident_id": latest_incident.incident_id if latest_incident else None
    }

@app.get("/api/v1/incidents/{incident_id}/timeline")
def get_incident_timeline(incident_id: str, db: Session = Depends(get_db)):
    from models import Incident, AttackTimeline
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    timeline_entries = db.query(AttackTimeline).filter(AttackTimeline.incident_id == incident.id).order_by(AttackTimeline.sequence.asc()).all()
    
    stages = []
    events_data = []
    
    for t in timeline_entries:
        stage = "Unknown"
        event_name = "Unknown"
        if "] " in t.description:
            parts = t.description.split("] ", 1)
            stage = parts[0].strip("[")
            if ":" in parts[1]:
                event_name = parts[1].split(":")[0]
            else:
                event_name = parts[1]
                
        stages.append(stage)
        events_data.append({
            "sequence": t.sequence,
            "timestamp": t.timestamp,
            "description": t.description,
            "stage": stage,
            "event_name": event_name,
            "source": t.source,
            "anomaly_score": t.anomaly_score,
            "severity": t.severity,
            "risk_contribution": t.risk_contribution
        })
        
    # Remove duplicates from stages while preserving order
    unique_stages = []
    for s in stages:
        if s not in unique_stages:
            unique_stages.append(s)
    
    return {
        "incident_id": incident.incident_id,
        "title": incident.title,
        "severity": incident.severity,
        "risk_score": incident.risk_score,
        "description": incident.description,
        "stages": unique_stages,
        "timeline": events_data
    }

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, connection_id: str):
        await websocket.accept()
        if connection_id not in self.active_connections:
            self.active_connections[connection_id] = []
        self.active_connections[connection_id].append(websocket)

    def disconnect(self, websocket: WebSocket, connection_id: str):
        if connection_id in self.active_connections:
            self.active_connections[connection_id].remove(websocket)

    async def broadcast(self, message: dict, connection_id: str):
        if connection_id in self.active_connections:
            for connection in self.active_connections[connection_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.post("/api/v1/connections", response_model=WebsiteConnectionResponse)
def create_connection(conn: WebsiteConnectionCreate, db: Session = Depends(get_db)):
    db_conn = models.WebsiteConnection(
        connection_id=conn.connection_id,
        website_url=conn.website_url,
        customer_name="Unknown"
    )
    db.add(db_conn)
    db.commit()
    db.refresh(db_conn)
    return db_conn

@app.get("/api/v1/connections", response_model=List[WebsiteConnectionResponse])
def get_connections(db: Session = Depends(get_db)):
    return db.query(models.WebsiteConnection).all()

@app.post("/api/v1/incidents/{incident_id}/suspend-7min")
async def suspend_account_7min(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    incident.status = "Mitigated"
    db.commit()
    
    return {
        "status": "Success",
        "message": "User account temporarily blocked for 7 minutes.",
        "incident_id": incident_id,
        "mitigation_time": 420
    }

@app.websocket("/api/v1/ws/security-flow/{connection_id}")
async def websocket_endpoint(websocket: WebSocket, connection_id: str):
    await manager.connect(websocket, connection_id)
    try:
        while True:
            await asyncio.sleep(3)
            
            flow_event = {
                "type": "FLOW_UPDATE",
                "timestamp": datetime.utcnow().isoformat(),
                "metrics": {
                    "active_sessions": random.randint(100, 500),
                    "traffic_rate": f"{random.randint(5, 50)} req/s",
                    "threat_level": random.choice(["Low", "Medium", "High", "Critical"])
                },
                "events": [
                    {
                        "source": "Firewall",
                        "event": "Traffic Analyzed",
                        "status": "OK"
                    },
                    {
                        "source": "WAF",
                        "event": "Anomaly Detected" if random.random() > 0.7 else "Traffic OK",
                        "status": "Blocked" if random.random() > 0.8 else "Logged"
                    }
                ]
            }
            await manager.broadcast(flow_event, connection_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, connection_id)

