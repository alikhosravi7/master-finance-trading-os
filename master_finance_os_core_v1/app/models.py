from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from uuid import uuid4

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class TaskType(str, Enum):
    research = "research"
    trading_analysis = "trading_analysis"
    code_review = "code_review"
    strategy = "strategy"
    risk_check = "risk_check"
    general = "general"

class TaskRequest(BaseModel):
    task_type: TaskType
    objective: str = Field(min_length=5, max_length=2000)
    payload: dict[str, Any] = Field(default_factory=dict)

class AgentResult(BaseModel):
    agent_id: str
    status: str
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)
    validation_passed: bool = True

class TaskResponse(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    task_type: TaskType
    routed_agent: str
    status: str
    result: AgentResult
    approval_required: bool = False
    approval_id: str | None = None

class ApprovalDecision(BaseModel):
    approved: bool
    reviewer: str = Field(default="local_owner", min_length=1, max_length=100)
    comment: str = Field(default="", max_length=1000)
