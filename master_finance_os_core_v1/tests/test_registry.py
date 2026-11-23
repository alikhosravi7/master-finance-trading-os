from app.agents.registry import AgentRegistry

def test_research_routes_to_research_agent():
    registry = AgentRegistry()
    assert registry.route("research").agent_id == "research_agent"

def test_unknown_route_raises():
    registry = AgentRegistry()
    try:
        registry.route("unknown")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
