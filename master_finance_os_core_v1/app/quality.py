from app.models import AgentResult

def validate_result(result: AgentResult) -> tuple[bool, list[str]]:
    errors = []
    if not result.agent_id:
        errors.append("missing_agent_id")
    if result.status != "completed":
        errors.append("agent_not_completed")
    if not result.summary.strip():
        errors.append("empty_summary")
    if not result.validation_passed:
        errors.append("agent_validation_failed")
    return (len(errors) == 0, errors)
