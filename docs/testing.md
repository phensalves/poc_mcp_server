
# Testing Strategy

The MCP Server project employs a comprehensive testing strategy to ensure the reliability, correctness, and maintainability of its codebase. This includes unit tests for individual components and integration tests for verifying interactions between different parts of the system.

## Testing Framework

-   **`pytest`**: The primary testing framework used for Python components. `pytest` is chosen for its simplicity, powerful features, and extensive plugin ecosystem.

## Test Types

### 1. Unit Tests

**Purpose**: To test individual functions, methods, or classes in isolation, ensuring that each component works as expected.

**Location**: `mcp_server/tests/test_plugins.py`

**Details**:
-   Focus on the logic within the language analyzer plugins (e.g., `ruby_plugin.py`).
-   Mocks are used where necessary to isolate the unit under test from external dependencies (e.g., network calls to AI providers, although currently, LLM providers are tested via integration tests).

**Example (from `tests/test_plugins.py`):

```python
import pytest
from app.plugins import ruby_plugin

def test_ruby_plugin_good_code():
    code = "class MyClass; end"
    report = ruby_plugin.analyze(code)
    assert not report['issues']
    assert report['metrics']['line_count'] == 1

def test_ruby_plugin_detects_eval():
    code = "eval('puts \'hello\')"
    report = ruby_plugin.analyze(code)
    assert len(report['issues']) == 1
    assert "Use of 'eval'" in report['issues'][0]
```

### 2. Integration Tests

**Purpose**: To verify the interactions between different modules or services, ensuring that they work together correctly as a cohesive system.

**Location**: `mcp_server/tests/test_api.py`

**Details**:
-   Tests the FastAPI application's endpoints (`/analyze`, `/supported-languages`, `/supported-providers`).
-   Uses `FastAPI.testclient.TestClient` to simulate HTTP requests to the application.
-   Includes tests for:
    -   Frontend serving (`test_read_root`).
    -   Correct listing of supported languages and AI providers.
    -   Successful analysis requests, including those routed to the `python_analyzer_service` microservice.
    -   Error handling for unsupported languages/providers.

**Example (from `tests/test_api.py`):

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_python_code_mock_provider():
    response = client.post(
        "/analyze",
        json={"language": "python", "code": "x=1", "provider": "mock"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "python"
    assert "[Mock Suggestion]" in data["analysis"]["refactoring_suggestion"]
    assert "metrics" in data["analysis"]
    assert "issues" in data["analysis"]
```

## Running Tests

Tests are integrated into the Docker Compose setup, allowing for consistent execution across different environments.

To run all tests:

1.  Ensure your Docker environment is running.
2.  Navigate to the `mcp_server` directory in your terminal.
3.  Execute the following command:

    ```bash
    docker-compose run --rm tester
    ```

    -   `docker-compose run`: Executes a one-off command in a service.
    -   `--rm`: Removes the container after it exits.
    -   `tester`: Specifies the service defined in `docker-compose.yml` that is configured to run `pytest`.

## Continuous Testing

Tests are automatically executed as part of the [CI/CD pipeline with GitHub Actions](ci-cd.md) on every push and pull request to the `main` branch. This ensures that new code changes do not introduce regressions and maintain the overall quality of the project.
