from abc import ABC, abstractmethod
from app.models import TaskRequest, AgentResult

class BaseAgent(ABC):
    agent_id: str
    supported_types: set[str]

    @abstractmethod
    def run(self, task: TaskRequest) -> AgentResult:
        raise NotImplementedError
