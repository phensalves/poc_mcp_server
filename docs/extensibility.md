
# Extending the MCP Server

The MCP Server is designed with extensibility as a core principle, allowing you to easily add support for new programming languages, integrate with different AI providers, or even introduce new functionalities.

## 1. Adding a New Language Analyzer

The system supports adding new language analyzers by simply creating a new Python file in the `mcp_server/app/plugins/` directory. These are dynamically loaded by the main server.

### For Languages Other Than Python (Local Plugins):

If the language analyzer is relatively simple or you prefer to keep it within the main server's process for now, follow these steps:

1.  **Create a new plugin file**: In the `mcp_server/app/plugins/` directory, create a new Python file named after your language (e.g., `javascript_plugin.py`, `go_plugin.py`).

2.  **Implement the `analyze` function**: Inside this new file, define a function named `analyze` that accepts a `code` string and returns a dictionary containing `metrics` and `issues`.

    ```python
    # Example: javascript_plugin.py

def analyze(code: str) -> dict:
    """Analyzes a snippet of JavaScript code.

    Args:
        code (str): The JavaScript source code to analyze.

    Returns:
        dict: A dictionary containing analysis results.
              Example: {"metrics": {"lines": 10}, "issues": ["Missing semicolon"]}
    """
    report = {
        "metrics": {
            "line_count": len(code.splitlines())
        },
        "issues": []
    }

    if "console.log" in code:
        report["issues"].append("Consider removing console.log statements in production.")

    return report
    ```

3.  **Restart the main server**: The main MCP Server will automatically discover and load your new plugin on startup.

    ```bash
    cd mcp_server
    docker-compose up --build -d
    ```

    Your new language will now appear in the `/supported-languages` endpoint and the frontend dropdown.

### For Python (or when extracting to a Microservice):

As demonstrated with the `python_analyzer_service`, for more complex analyzers or when you need independent scaling/technology choices, you should extract the analyzer into its own microservice.

1.  **Create a new service directory**: Create a new directory at the root level (e.g., `go_analyzer_service/`).
2.  **Develop the analyzer service**: Implement a new FastAPI application (or any other framework/language) within this directory that exposes an `/analyze` endpoint.
3.  **Update `docker-compose.yml`**: Add a new service entry for your new analyzer service, defining its build context, ports, and volumes.
4.  **Modify main `mcp_server`**: Update `mcp_server/app/main.py` to make an HTTP request to your new analyzer service when its corresponding language is requested, similar to how the Python analyzer is called.

## 2. Adding a New LLM Provider

New Large Language Model (LLM) providers can be integrated by implementing the `LLMProvider` interface. This adheres to the Strategy Pattern, making it easy to swap AI models.

1.  **Create a new provider file**: In the `mcp_server/app/llm_providers/` directory, create a new Python file (e.g., `anthropic_provider.py`, `gemini_provider.py`).

2.  **Implement the `LLMProvider` interface**: Define a class within this file that inherits from `LLMProvider` (from `app.llm_providers.base`) and implements its abstract methods:

    -   `get_name(self) -> str`: Returns the unique name of your provider (e.g., `"anthropic"`, `"gemini"`).
    -   `get_refactoring_suggestion(self, code: str) -> str`: Contains the logic to call the specific LLM's API and return a refactoring suggestion.

    ```python
    # Example: anthropic_provider.py

    import os
    # import anthropic # You would install the actual library
    from .base import LLMProvider

    class AnthropicProvider(LLMProvider):
        def __init__(self):
            # self.api_key = os.environ.get("ANTHROPIC_API_KEY")
            # self.client = anthropic.Anthropic(api_key=self.api_key)
            pass

        def get_name(self) -> str:
            return "anthropic"

        def get_refactoring_suggestion(self, code: str) -> str:
            # In a real implementation, make an API call to Anthropic
            # response = self.client.messages.create(
            #     model="claude-3-opus-20240229",
            #     max_tokens=1024,
            #     messages=[
            #         {"role": "user", "content": f"Provide a refactoring suggestion for the following code:\n\n{code}"}
            #     ]
            # )
            # return response.content[0].text
            return f"[Anthropic Suggestion] A Claude-powered suggestion for your code would appear here."
    ```

3.  **Restart the main server**: The main MCP Server will automatically discover and load your new LLM provider on startup.

    ```bash
    cd mcp_server
    docker-compose up --build -d
    ```

    Your new provider will now appear in the `/supported-providers` endpoint and the frontend dropdown.

## 3. Adding New Functionalities

Beyond language analysis and LLM integration, you can extend the MCP Server to include other functionalities like:

-   **Test Coverage Verification**: Integrate with tools like `coverage.py` (Python), SimpleCov (Ruby), or JaCoCo (Java) to collect and report test coverage data.
-   **Continuous Commit Analysis**: Implement webhooks to trigger analysis on new commits, providing real-time feedback.
-   **Integration with Development Tools**: Develop specific integrations or APIs that allow tools like GitHub Copilot or Cursor to leverage the MCP Server's analysis capabilities.

Each new functionality should ideally be designed as a modular component, following the principles of loose coupling and clear interfaces, to maintain the project's extensibility and ease of maintenance.
