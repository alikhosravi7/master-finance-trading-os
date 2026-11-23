from uuid import uuid4
from app.models import TaskRequest, TaskResponse
from app.agents.registry import AgentRegistry
from app.quality import validate_result
from app import database

SENSITIVE_TYPES = {"code_review", "trading_analysis", "strategy", "risk_check"}

class Orchestrator:
    def __init__(self, registry: AgentRegistry | None = None):
        self.registry = registry or AgentRegistry()

    def execute(self, task: TaskRequest) -> TaskResponse:
        agent = self.registry.route(task.task_type.value)
        result = agent.run(task)
        passed, errors = validate_result(result)
        task_id = str(uuid4())

        if not passed:
            database.audit("task_rejected", "quality_gate", task_id, {"errors": errors})
            return TaskResponse(task_id=task_id, task_type=task.task_type,
                routed_agent=agent.agent_id, status="rejected",
                result=result.model_copy(update={"validation_passed": False}))

        approval_required = task.task_type.value in SENSITIVE_TYPES
        approval_id = None
        status = "awaiting_approval" if approval_required else "completed"

        if approval_required:
            approval_id = str(uuid4())
            database.create_approval(approval_id, task_id, task.model_dump(mode="json"))

        database.audit("task_processed", "master_core", task_id, {
            "task_type": task.task_type.value,
            "agent": agent.agent_id,
            "status": status,
            "approval_required": approval_required
        })
        return TaskResponse(task_id=task_id, task_type=task.task_type,
            routed_agent=agent.agent_id, status=status, result=result,
            approval_required=approval_required, approval_id=approval_id)
