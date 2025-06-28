
# Plugin System Deep Dive

The MCP Server is designed with extensibility at its core, primarily through its robust plugin system. This system allows for easy integration of new programming language analyzers and AI providers without modifying the core application logic.

## Dynamic Loading Mechanism

The server dynamically discovers and loads plugins at startup. This is achieved by scanning predefined directories (`app/plugins` for language analyzers and `app/llm_providers` for AI providers) and importing Python modules found within them.

### How it Works:

1.  **Directory Scanning**: The `load_language_analyzers()` and `load_llm_providers()` functions in `app/main.py` iterate through files in their respective plugin directories.
2.  **Module Importation**: For each valid plugin file (e.g., ending with `_plugin.py` or being a Python module for LLM providers), Python's `importlib` is used to dynamically load it as a module.
3.  **Interface Adherence**: The loaded modules are expected to adhere to a specific interface:
    -   **Language Analyzers**: Must expose an `analyze(code: str)` function.
    -   **LLM Providers**: Must implement the `LLMProvider` abstract base class, providing `get_name()` and `get_refactoring_suggestion(code: str)` methods.
4.  **Registration**: Once loaded, the plugins (or their relevant functions/instances) are registered in internal dictionaries, making them accessible by their unique names (e.g., `"python"`, `"mock"`, `"openai"`).

This dynamic loading mechanism means that adding new capabilities often only requires dropping a new file into the correct directory and restarting the server, rather than modifying and redeploying the core application.

## Language Analyzers (`app/plugins`)

Language analyzers are responsible for performing static code analysis on specific programming languages. Each analyzer is a Python module that exposes an `analyze` function.

### Interface (`analyze` function):

```python
def analyze(code: str) -> dict:
    """Analyzes a snippet of code for a specific language.

    Args:
        code (str): The source code to analyze.

    Returns:
        dict: A dictionary containing analysis results, typically with:
              - 'metrics': (dict) Key-value pairs of code metrics (e.g., line count, node count).
              - 'issues': (list) A list of detected issues or suggestions.
    """
    # ... implementation ...
```

### Examples:

-   **`ruby_plugin.py`**: A simple analyzer for Ruby code that checks for `eval` usage and provides line count metrics.
-   **`python_analyzer.py` (in `python_analyzer_service`)**: A more sophisticated analyzer for Python code that uses the `ast` module to parse code and identify long functions. This has been extracted into a separate microservice.

## LLM Providers (`app/llm_providers`)

LLM Providers are responsible for interacting with Large Language Models to generate code-related suggestions, such as refactoring advice. They are implemented using the **Strategy Pattern**, allowing the application to use different AI models interchangeably.

### Interface (`LLMProvider` Abstract Base Class):

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract Base Class for all LLM Providers."""

    @abstractmethod
    def get_name(self) -> str:
        """Return the unique name of the provider."""
        pass

    @abstractmethod
    def get_refactoring_suggestion(self, code: str) -> str:
        """Given a piece of code, return a refactoring suggestion."
        pass
```

### Concrete Implementations:

-   **`mock_provider.py`**: A placeholder provider that returns a static mock suggestion. Ideal for development and testing without external API calls.
-   **`openai_provider.py`**: A placeholder for integrating with OpenAI's API. In a full implementation, this would make actual API calls to GPT models.

### Adding a New LLM Provider:

To add a new LLM provider (e.g., for Anthropic, Google Gemini, or a local Ollama instance), you would:

1.  Create a new Python file (e.g., `anthropic_provider.py`) in the `app/llm_providers` directory.
2.  Define a class within that file that inherits from `LLMProvider` and implements its abstract methods (`get_name` and `get_refactoring_suggestion`).
3.  Implement the logic to interact with the specific LLM's API within the `get_refactoring_suggestion` method.
4.  Restart the main MCP Server to dynamically load the new provider.

This modular and extensible design is a cornerstone of the MCP Server, enabling it to adapt to new languages and AI technologies with minimal effort.
