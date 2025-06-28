
# Project Architecture

## Architectural Pattern: Modular Monolith

For this Proof-of-Concept (POC), the MCP Server is built using a **Modular Monolith** architectural pattern. This choice provides a balance between rapid development and a clear path for future scalability and evolution into a microservices architecture.

### Why a Modular Monolith for the POC?

-   **Simplicity and Speed**: During the initial development phase, a single codebase avoids the complexities inherent in distributed systems, such as network latency, inter-service communication protocols, distributed data management, and service discovery. This allows for faster iteration and focus on core business logic.
-   **Lower Cognitive Overhead**: Developers can work within a single repository and deployment unit, reducing the mental burden associated with managing multiple services.
-   **Clear Migration Path**: By designing the monolith with strong module boundaries and well-defined interfaces, extracting modules into independent microservices later becomes a more straightforward process, minimizing refactoring efforts.

### How Modularity is Achieved:

The codebase is organized into distinct, loosely-coupled modules:

-   **`app/plugins`**: Houses the language-specific code analyzers.
-   **`app/llm_providers`**: Contains the implementations for various AI providers.
-   **`app/models.py`**: Defines shared data structures and contracts.

Each module has a clear responsibility and communicates with others through defined interfaces, adhering to the **Single Responsibility Principle** and promoting **loose coupling**.

## Current State: Hybrid Microservice (Python Analyzer Extracted)

While the overall pattern is a modular monolith, we have already taken the first step towards a full microservices architecture by extracting the Python language analyzer into its own dedicated service.

### Diagram of Current Architecture:

```mermaid
graph TD
    User[User/Frontend] -->|HTTP Request| MainServer(MCP Server - FastAPI)
    MainServer -->|HTTP Request (Python Analysis)| PythonAnalyzerService(Python Analyzer Service - FastAPI)
    MainServer -->|Local Call (Ruby Analysis)| RubyPlugin(Ruby Plugin)
    MainServer -->|Strategy Pattern| LLMProvider(LLM Provider - Mock/OpenAI)
    MainServer --&gt; RabbitMQ(RabbitMQ - Message Broker)
    PythonAnalyzerService --&gt; RabbitMQ
```

### Components:

-   **MCP Server (Main FastAPI Application)**:
    -   Serves the web frontend.
    -   Exposes the primary API endpoints (`/analyze`, `/supported-languages`, `/supported-providers`).
    -   Acts as an orchestrator: for Python code, it forwards the request to the `Python Analyzer Service`; for other languages (e.g., Ruby), it calls the local plugin directly.
    -   Integrates with LLM Providers using the Strategy Pattern to fetch refactoring suggestions.
    -   Connects to RabbitMQ (though not yet actively using it for analysis requests in this hybrid setup).

-   **Python Analyzer Service (Separate FastAPI Application)**:
    -   A standalone microservice responsible *only* for analyzing Python code.
    -   Receives analysis requests via HTTP from the main MCP Server.
    -   Performs the Python-specific code analysis.
    -   Can be scaled independently of the main server.

-   **Ruby Plugin (Local to Main Server)**:
    -   Currently, the Ruby analyzer remains a local plugin within the main MCP Server.
    -   It processes Ruby code analysis requests directly within the main application's process.

-   **LLM Providers (Local to Main Server)**:
    -   Implemented using the Strategy Pattern, allowing easy swapping of AI models (e.g., Mock, OpenAI placeholder).
    -   These are currently loaded directly into the main server.

-   **RabbitMQ (Message Broker)**:
    -   Integrated into the `docker-compose.yml`.
    -   Currently serves as a foundational component for future microservice communication, but not yet actively used for the analysis request flow in this hybrid setup.

## Trade-offs and Alternatives Considered

-   **Full Microservices from the Start**: While ideal for large-scale production, starting with full microservices introduces significant overhead (service discovery, distributed tracing, complex deployments) that can slow down initial development. The modular monolith approach mitigates this while keeping the path open.
-   **Different Backend Technologies**: FastAPI (Python) was chosen over Gin (Go) primarily due to the developer's learning goals (improving Python skills) and Python's rich ecosystem for code analysis libraries, which simplifies plugin development.
-   **Monolithic Frontend**: For simplicity in the POC, the frontend is served directly by the FastAPI backend. In production, this would typically be a separate Single Page Application (SPA) served by a CDN or a dedicated web server.

This architecture provides a robust and flexible foundation, demonstrating key principles of modern software engineering while allowing for incremental complexity as the project evolves.
