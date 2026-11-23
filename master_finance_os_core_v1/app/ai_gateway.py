from typing import Protocol

class AIProvider(Protocol):
    def generate(self, system_prompt: str, user_prompt: str) -> str: ...

class StubProvider:
    """Safe deterministic provider used until a real provider is configured."""
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return "AI provider is not configured. This is a safe stub response."

def get_provider() -> AIProvider:
    # Provider-specific integrations will be added behind this interface.
    return StubProvider()
