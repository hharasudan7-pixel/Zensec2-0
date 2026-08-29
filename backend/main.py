from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
import time
import asyncio

app = FastAPI(title="ZentraSec API", description="AI-Powered Cybersecurity APIs", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/v1/incidents/{incident_id}/response-actions")
async def execute_response_actions(incident_id: str, request: ResponseExecutionRequest):
    # Simulated execution logic
    await asyncio.sleep(2) # Simulate processing delay
    
    results = []
    for action in request.actions:
        # 10% chance of failure for simulation
        if random.random() < 0.1:
            results.append(ActionStatus(
                action_id=action.action_id,
                status="FAILED",
                reason="Target unreachable or access denied"
            ))
        else:
            results.append(ActionStatus(
                action_id=action.action_id,
                status="SUCCESS",
                reason="Action executed successfully"
            ))
    
    return {
        "incident_id": incident_id,
        "results": results,
        "timestamp": time.time(),
        "status": "Contained" if all(r.status == "SUCCESS" for r in results) else "Containing"
    }

@app.get("/")
def read_root():
    return {"status": "ZentraSec Backend Running", "modules": ["ML Anomaly Detection", "RAG Copilot", "Event Correlation"]}
