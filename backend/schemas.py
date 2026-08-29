from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class EventIngestRequest(BaseModel):
    event_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    source_ip: Optional[str] = None
    destination: Optional[str] = None
    device_id: Optional[str] = None
    event_type: str
    severity: str = "low"
    authentication_status: Optional[str] = None
    location: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    connection_id: Optional[str] = None
    website_url: Optional[str] = None


class ThreatIntelLookupRequest(BaseModel):
    indicator: str
    indicator_type: str


class CopilotRequest(BaseModel):
    question: Optional[str] = None


class ResponseActionItem(BaseModel):
    action_id: str
    target: str


class ResponseExecutionRequest(BaseModel):
    incident_id: str
    actions: List[ResponseActionItem]
    analyst_id: str


class ActionApprovalRequest(BaseModel):
    analyst_id: str


class ActionExecuteRequest(BaseModel):
    analyst_id: str
    target: Optional[str] = None


class WebsiteConnectionCreate(BaseModel):
    website_url: str
    customer_name: str


class WebsiteConnectionResponse(BaseModel):
    connection_id: str
    website_url: str
    customer_name: str
    created_at: datetime

    class Config:
        from_attributes = True
