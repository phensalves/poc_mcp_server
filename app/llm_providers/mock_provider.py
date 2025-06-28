from .base import LLMProvider

class MockProvider(LLMProvider):
    """A mock provider for development and testing."""

    def get_name(self) -> str:
        return "mock"

    def get_refactoring_suggestion(self, code: str) -> str:
        return f"[Mock Suggestion] Consider simplifying the following code:\n\n{code[:100]}..."