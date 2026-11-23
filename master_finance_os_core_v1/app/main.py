from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.config import settings
from app import database
from app.models import TaskRequest, ApprovalDecision
from app.agents.registry import AgentRegistry
from app.orchestrator import Orchestrator

registry = AgentRegistry()
orchestrator = Orchestrator(registry)

@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialize()
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "service": "master-finance-core", "mode": "local-development"}

@app.get("/api/v1/system/status")
def system_status():
    return {
        "product": "Master Finance OS",
        "core_version": "1.0.0",
        "environment": settings.app_env,
        "ai_provider": settings.ai_provider,
        "ai_provider_ready": False,
        "trading_execution_enabled": False,
        "approval_policy": "controlled"
    }

@app.get("/api/v1/agents")
def agents():
    return {"agents": registry.list_agents()}

@app.post("/api/v1/tasks")
def create_task(task: TaskRequest):
    try:
        return orchestrator.execute(task)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/api/v1/approvals")
def approvals():
    return {"approvals": database.list_approvals()}

@app.post("/api/v1/approvals/{approval_id}/decision")
def approval_decision(approval_id: str, decision: ApprovalDecision):
    result = database.decide_approval(approval_id, decision.model_dump())
    if result is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    if "error" in result:
        raise HTTPException(status_code=409, detail=result["error"])
    database.audit("approval_decided", decision.reviewer, approval_id, result)
    return result
