from app.models import AgentResult
from app.quality import validate_result

def test_valid_result_passes():
    result = AgentResult(agent_id="test", status="completed", summary="ok")
    assert validate_result(result) == (True, [])

def test_empty_summary_fails():
    result = AgentResult(agent_id="test", status="completed", summary=" ")
    passed, errors = validate_result(result)
    assert not passed
    assert "empty_summary" in errors
