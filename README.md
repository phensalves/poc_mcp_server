# MCP Server: Modular Code Analysis Platform

This project is a Proof-of-Concept (POC) for a modular, multi-client, and multi-AI-provider code analysis server. It is designed to demonstrate advanced software architecture principles, including a plugin-based design, containerization, and a clear path towards a microservices architecture.

## Core Concepts & Architecture

The primary goal of this project is to build a system that is **extensible by default**. The two main axes of extension are **programming languages** (analyzers) and **AI providers** (for suggestions).

### Architectural Pattern: Modular Monolith

For this POC, we are using a **Modular Monolith** architecture. This provides the simplicity and speed of a single application while being structured for an easy migration to microservices.

- **Why a Monolith first?** It avoids the complexity of a distributed system (networking, service discovery, distributed transactions) during the initial development phase, allowing us to focus on the core business logic.
- **Why Modular?** The code is organized into loosely-coupled modules (`plugins`, `llm_providers`). Each module has a clear responsibility and a well-defined interface. This separation of concerns is what makes the future migration to microservices straightforward.

### Plugin System: Dynamic Loading & Strategy Pattern

The entire system is built around a powerful plugin system that leverages dynamic importing and polymorphism.

1.  **Language Analyzers (`/plugins`)**: To add support for a new language, you simply add a new Python file to the `app/plugins` directory. This file must contain a function named `analyze` that accepts a string of code and returns a report. The main application will automatically detect and load it on startup.

2.  **LLM Providers (`/llm_providers`)**: This system uses the **Strategy Pattern**. 
    - An abstract base class, `LLMProvider` (`base.py`), defines the common interface (`get_refactoring_suggestion`).
    - Each provider (e.g., `MockProvider`, `OpenAIProvider`) is a concrete implementation of this interface.
    - The main application dynamically loads all available provider classes and can switch between them based on the client's request (`/analyze` endpoint).

This design means you can add a new AI provider (e.g., for Anthropic or a local model) by adding one new file, without changing any of the core application logic.

## How to Run This Project

This project is fully containerized using Docker and Docker Compose.

**Prerequisites**:
- Docker
- Docker Compose

**Running the server**:

From the `mcp_server` directory, run:

```bash
docker-compose up --build -d
```

This will build the Docker image and start the FastAPI server in the background.

## Web Interface

This project includes a simple web interface to interact with the analysis engine. Once the server is running, you can access it at:

`http://localhost:8000`

The interface allows you to select the programming language, choose an AI provider, and submit your code for analysis.

## API Endpoints

For a full, interactive API documentation, visit `http://localhost:8000/docs` after starting the server.

- `POST /analyze`: The core endpoint. 
  - **Request Body**:
    ```json
    {
      "language": "python",
      "code": "def hello(): print('world')",
      "provider": "mock" 
    }
    ```
  - **Response**: An analysis report including metrics, issues, and an AI-powered refactoring suggestion.

- `GET /supported-languages`: Returns a list of all currently loaded language analyzer plugins.

- `GET /supported-providers`: Returns a list of all currently loaded LLM provider plugins.

## How to Extend the System

### Adding a New Language Analyzer

1.  Create a new file in `mcp_server/app/plugins/`, for example `javascript_plugin.py`.
2.  In that file, define an `analyze` function:
    ```python
    def analyze(code: str):
        # Your analysis logic here
        return {"metrics": {}, "issues": []}
    ```
3.  Restart the server. The `javascript` language will now be available.

### Adding a New LLM Provider

1.  Create a new file in `mcp_server/app/llm_providers/`, for example `anthropic_provider.py`.
2.  In that file, implement the `LLMProvider` interface:
    ```python
    from .base import LLMProvider

    class AnthropicProvider(LLMProvider):
        def get_name(self) -> str:
            return "anthropic"

        def get_refactoring_suggestion(self, code: str) -> str:
            # Logic to call Anthropic's API
            return "[Anthropic Suggestion] ..."
    ```
3.  Restart the server. The `anthropic` provider will now be available.

## CI/CD with GitHub Actions

This project uses GitHub Actions for Continuous Integration and Continuous Deployment. The workflow is defined in `.github/workflows/ci.yml`.

### Workflow Details

- **Triggers**: The workflow runs on every `push` to the `main` branch and on every `pull_request` targeting the `main` branch.
- **Steps**:
    1.  **Checkout code**: Retrieves the latest code from the repository.
    2.  **Set up Docker Buildx**: Configures Docker Buildx for efficient multi-platform image builds.
    3.  **Build Docker images**: Builds all necessary Docker images (`server`, `python_analyzer`, `tester`) using `docker-compose build`.
    4.  **Run tests**: Executes the test suite using the `tester` service (`docker-compose run --rm tester`).
    5.  **Run linters**: Performs code quality checks using `flake8` and `black` on the application code.

This automated pipeline ensures that all code changes are thoroughly tested and adhere to code quality standards before being merged into the `main` branch.

## Testing

This project includes a comprehensive test suite to ensure the correctness and reliability of the application.

### Running Tests

All tests can be run using Docker Compose:

```bash
docker-compose run --rm tester
```

### Test Types

- **Unit Tests**: Located in `tests/test_plugins.py`, these tests verify the individual logic of language analyzer plugins.
- **Integration Tests**: Located in `tests/test_api.py`, these tests ensure that the FastAPI application's endpoints and their interactions with plugins and providers work as expected.

## Migration Path to Production (Microservices) - Initial Steps

This POC is designed to evolve into a full microservices architecture. We have already taken the first steps in this direction:

1.  **Message Broker (RabbitMQ)**: A RabbitMQ instance has been integrated into the `docker-compose.yml` to serve as the communication backbone for future microservices.
2.  **Extracted Python Analyzer Service**: The Python language analyzer has been extracted from the main FastAPI application into its own dedicated microservice (`python_analyzer_service`).
    - The main `mcp_server` now communicates with the `python_analyzer_service` via HTTP requests (demonstrating inter-service communication).
    - This allows the Python analyzer to be scaled independently and developed in isolation.

The next steps in the full migration would involve:

1.  **Extract Other Language Analyzers**: Similarly, other language analyzers (e.g., Ruby) can be extracted into their own microservices.
2.  **Introduce an Orchestrator Service**: A dedicated orchestrator service would handle incoming analysis requests, publish them to a message queue (e.g., RabbitMQ), and then collect results from worker services.
3.  **Worker Services**: The language-specific analyzer services would consume jobs from the queue, perform the analysis, and publish the results back.
4.  **API Gateway**: An API Gateway would be placed in front of the system to handle routing, authentication, and rate limiting.

This incremental evolution provides greater scalability, resilience, and technological flexibility, which are hallmarks of a senior-level architecture.

## How to Extend the System

### Adding a New Language Analyzer

For languages other than Python, you can still add a new Python file to `mcp_server/app/plugins/`, for example `javascript_plugin.py`. This file must contain an `analyze` function:
```python
def analyze(code: str):
    # Your analysis logic here
    return {"metrics": {}, "issues": []}
```
Restart the main server, and the new language will be available.

For Python, the analysis is now handled by the `python_analyzer_service`. To modify Python analysis, you would update the code within `python_analyzer_service/app/python_analyzer.py` and rebuild/restart that specific service.

### Adding a New LLM Provider

1.  Create a new file in `mcp_server/app/llm_providers/`, for example `anthropic_provider.py`.
2.  In that file, implement the `LLMProvider` interface:
    ```python
    from .base import LLMProvider

    class AnthropicProvider(LLMProvider):
        def get_name(self) -> str:
            return "anthropic"

        def get_refactoring_suggestion(self, code: str) -> str:
            # Logic to call Anthropic's API
            return "[Anthropic Suggestion] ..."
    ```
3.  Restart the main server. The `anthropic` provider will now be available.