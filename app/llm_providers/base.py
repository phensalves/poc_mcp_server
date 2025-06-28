
from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract Base Class for all LLM Providers."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the unique name of the provider."""
        pass

    @abstractmethod
    def get_refactoring_suggestion(self, code: str) -> str:
        """Given a piece of code, return a refactoring suggestion."""
        pass
