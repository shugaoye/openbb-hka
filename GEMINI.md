# Project Overview

This project, `openbb-hka`, is a Python-based backend application that provides financial data and analysis dashboards for China A-shares and Hong Kong H-shares. It is designed to be used with the OpenBB Workspace, a front-end platform for financial data analysis.

The application is built using the **FastAPI** web framework and leverages the **OpenBB Platform** for financial data. Specifically, it uses the `openbb-akshare` and `openbb-tushare` extensions to fetch data from Chinese financial data providers. The application also uses **Plotly** for generating charts and **uv** for dependency management.

The core functionality of the application is to provide a set of API endpoints that serve financial data and widget configurations to the OpenBB Workspace. These widgets can be used to build custom dashboards for analyzing A-shares and H-shares.

# Building and Running

## Environment Setup

1.  **API Keys:** Configure the necessary API keys in `$HOME/.openbb_platform/user_settings.json`. At a minimum, you will need to set the `akshare_api_key`.

2.  **Environment Variables:** Create a `.env` file based on the `env.example` file and configure the required environment variables.

## Running Locally

1.  **Install Dependencies:** This project uses `uv` for dependency management. To install the dependencies, run:

    ```bash
    uv sync
    ```

2.  **Run the Application:** To start the FastAPI application, run:

    ```bash
    uvicorn main:app --reload
    ```

## Running with Docker

1.  **Build the Docker Image:**

    ```bash
    docker build -t openbb-hka:0.2.4 .
    ```

2.  **Run the Docker Container:**

    ```bash
    docker-compose up
    ```

# Development Conventions

*   **API:** The application follows the REST API design principles, with endpoints defined in the `routes` directory.
*   **Modularity:** The code is organized into modules, with a clear separation of concerns. The `core` directory contains the core application logic, the `routes` directory contains the API endpoints, and the `fin_data` directory contains the data fetching logic.
*   **Dependency Management:** The project uses `uv` for dependency management, with dependencies defined in the `pyproject.toml` file.
*   **Widget Registration:** Widgets are registered using the `@register_widget` decorator in the `routes` files. This decorator defines the metadata for the widget, which is then used by the OpenBB Workspace to display the widget.
