
# Getting Started: Local Setup and Running

This guide will walk you through setting up and running the MCP Server project on your local machine. The project is fully containerized using Docker and Docker Compose, ensuring a consistent development environment.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop) (includes Docker Engine and Docker Compose).
    -   Ensure Docker Desktop is running before proceeding.

## Project Structure

```
mcp_server/
├── .github/             # GitHub Actions workflows
├── app/                 # Main FastAPI application code
│   ├── llm_providers/   # LLM Provider implementations
│   ├── plugins/         # Language analyzer plugins (e.g., Ruby)
│   └── ...
├── docs/                # Project documentation (this wiki)
├── frontend/            # Web interface HTML, CSS, JavaScript
├── python_analyzer_service/ # Dedicated microservice for Python analysis
│   └── ...
├── tests/               # Unit and integration tests
├── Dockerfile           # Dockerfile for the main server and tester
├── docker-compose.yml   # Defines multi-service Docker environment
├── requirements.txt     # Python dependencies for the main server
└── README.md            # Project overview
```

## Running the Project

1.  **Navigate to the Project Root**: Open your terminal or command prompt and navigate to the `mcp_server` directory:

    ```bash
    cd /path/to/your/project/mcp_server
    ```

2.  **Build and Start Services**: Use Docker Compose to build the images and start all the defined services in detached mode (`-d`):

    ```bash
    docker-compose up --build -d
    ```

    -   `--build`: This flag ensures that Docker images are rebuilt. It's good practice to include this when you've made changes to the `Dockerfile` or `requirements.txt`.
    -   `-d`: Runs the containers in the background.

    You should see output indicating that `rabbitmq`, `python_analyzer`, `server`, and `tester` services are being created and started.

3.  **Verify Services are Running**: You can check the status of your running containers:

    ```bash
    docker-compose ps
    ```

    All services (`server`, `python_analyzer`, `rabbitmq`, `tester`) should show a `Status` of `Up`.

## Accessing the Application

Once the `server` container is running, you can access the web interface and API documentation:

-   **Web Interface**: Open your web browser and go to:
    [http://localhost:8000](http://localhost:8000)

    Here you can interact with the MCP Server, select languages and AI providers, and submit code for analysis.

-   **API Documentation (Swagger UI)**: For detailed API endpoints and to test them directly, visit:
    [http://localhost:8000/docs](http://localhost:8000/docs)

## Stopping the Project

To stop and remove all running containers, networks, and volumes created by Docker Compose, run:

```bash
docker-compose down
```

To stop containers without removing them (so you can restart them later quickly), omit the `--volumes` flag:

```bash
docker-compose stop
```

This completes the basic setup and running of the MCP Server. You are now ready to explore its functionalities and extend it further.
