from app.agents.specialists import (
    ResearchAgent, TradingAnalysisAgent, CodeReviewAgent,
    StrategyAgent, RiskAgent, GeneralAgent
)

class AgentRegistry:
    def __init__(self):
        agents = [ResearchAgent(), TradingAnalysisAgent(), CodeReviewAgent(),
                  StrategyAgent(), RiskAgent(), GeneralAgent()]
        self._agents = {a.agent_id: a for a in agents}
        self._routes = {task_type: a for a in agents for task_type in a.supported_types}

    def route(self, task_type: str):
        agent = self._routes.get(task_type)
        if agent is None:
            raise ValueError(f"No agent registered for task type: {task_type}")
        return agent

    def list_agents(self):
        return [{"agent_id": a.agent_id, "supported_types": sorted(a.supported_types)}
                for a in self._agents.values()]
