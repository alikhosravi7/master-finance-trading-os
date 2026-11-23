from app.agents.base import BaseAgent
from app.models import TaskRequest, AgentResult

class ResearchAgent(BaseAgent):
    agent_id = "research_agent"
    supported_types = {"research"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Research task accepted for structured analysis.",
            data={"objective": task.objective, "mode": "stub", "next_step": "connect approved research sources"})

class TradingAnalysisAgent(BaseAgent):
    agent_id = "trading_analysis_agent"
    supported_types = {"trading_analysis"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Analysis request recorded; no live market data or orders are used.",
            data={"objective": task.objective, "execution_enabled": False})

class CodeReviewAgent(BaseAgent):
    agent_id = "code_review_agent"
    supported_types = {"code_review"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Code review request queued; source files are not modified.",
            data={"objective": task.objective, "write_access": False})

class StrategyAgent(BaseAgent):
    agent_id = "strategy_agent"
    supported_types = {"strategy"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Strategy evaluation request recorded.",
            data={"objective": task.objective, "backtest_executed": False})

class RiskAgent(BaseAgent):
    agent_id = "risk_agent"
    supported_types = {"risk_check"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Risk review request recorded; no trade authorization is issued.",
            data={"objective": task.objective, "order_authorized": False})

class GeneralAgent(BaseAgent):
    agent_id = "general_agent"
    supported_types = {"general"}
    def run(self, task: TaskRequest) -> AgentResult:
        return AgentResult(agent_id=self.agent_id, status="completed",
            summary="Request received by the central general-purpose agent.",
            data={"objective": task.objective})
