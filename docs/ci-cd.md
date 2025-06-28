
# CI/CD with GitHub Actions

The MCP Server project leverages **GitHub Actions** to automate its Continuous Integration (CI) and Continuous Deployment (CD) processes. This ensures that every code change is automatically built, tested, and validated, maintaining a high standard of code quality and enabling rapid, reliable deployments.

## Workflow Definition

The primary CI/CD workflow is defined in the file: `.github/workflows/ci.yml`.

## Workflow Triggers

The `ci.yml` workflow is configured to run automatically on the following events:

-   **`push` to `main` branch**: Every time code is pushed directly to the `main` branch.
-   **`pull_request` targeting `main` branch**: Whenever a pull request is opened, synchronized, or reopened against the `main` branch.

This ensures that all new code entering the `main` branch has passed automated checks.

## Workflow Steps

The `build-and-test` job within the `ci.yml` workflow executes a series of steps:

1.  **`Checkout code`**:
    -   `uses: actions/checkout@v4`
    -   Retrieves the latest version of the project code from the GitHub repository, making it available to subsequent steps.

2.  **`Set up Docker Buildx`**:
    -   `uses: docker/setup-buildx-action@v3`
    -   Initializes Docker Buildx, an extension that provides enhanced build capabilities, including support for multi-platform builds. This is a best practice for modern Docker-based projects.

3.  **`Build Docker images`**:
    -   `run: docker-compose build`
    -   `working-directory: mcp_server`
    -   Builds all Docker images defined in `docker-compose.yml` (e.g., `server`, `python_analyzer`, `tester`). This step ensures that the application and its dependencies are correctly packaged into containers.

4.  **`Run tests`**:
    -   `run: docker-compose run --rm tester`
    -   `working-directory: mcp_server`
    -   Executes the comprehensive test suite. The `tester` service, configured to run `pytest`, is launched as a one-off container. The `--rm` flag ensures the container is removed after the tests complete.
    -   If any tests fail, this step will fail, and the workflow will stop.

5.  **`Run linters`**:
    -   `run: docker-compose run --rm server bash -c "flake8 app && black --check app"`
    -   `working-directory: mcp_server`
    -   Performs static code analysis and formatting checks. `flake8` checks for style guide violations and programming errors, while `black --check` verifies code formatting adherence. These tools help maintain code consistency and quality.
    -   This step runs within the `server` container, ensuring that the linting environment matches the application's runtime environment.

## Benefits

-   **Automated Quality Assurance**: Catches bugs and style issues early in the development cycle.
-   **Faster Feedback Loop**: Developers receive immediate feedback on their code changes.
-   **Consistent Environment**: Builds and tests are run in a consistent, containerized environment, eliminating "it works on my machine" issues.
-   **Streamlined Collaboration**: Ensures all contributions adhere to project standards.
-   **Deployment Readiness**: A passing CI build indicates that the code is ready for potential deployment.

This CI/CD setup is fundamental to the project's commitment to high-quality, maintainable, and deployable software.
