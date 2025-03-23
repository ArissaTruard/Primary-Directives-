# IMPORTANT!!
- This file is outdated
- This code is extensively interconnected
- !This code is NOT ready for use!
- some of the code has documentation and docstrings to help implement it but not all.
# Primary Directives Application

  
This application implements a Flask-based API designed to process requests, enforce rules, and manage data corrections. It incorporates features like database interaction, model loading, system metrics, and error handling.

## Key Features

-   API endpoints for health checks, request processing, metrics, and data correction.
-   Rule enforcement using a complex rule checking module.
-   Database operations for storing and retrieving data corrections and law summaries.
-   Model loading and integrity verification.
-   System metrics collection and exposure via Prometheus.
-   Configuration management using pydantic-settings and .env files.
-   Logging to a file.
-   Location services for context enrichment.
-   Input sanitization to prevent security vulnerabilities.
-   Robust error handling and system shutdown capabilities.


## Getting Started

### Prerequisites

-   Python 3.x
-   pip
-   Virtual environment (recommended)

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd Primary-Directives-
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:

    -   On Windows:

        ```bash
        venv\Scripts\activate
        ```

    -   On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

4.  Install the dependencies:

    ```bash
    pip install -r requirements.txt 
    ```
    (e.g. SAMPLE.requirments.txt this is configured for the basic setting for the code but should be adpted individually)

5.  Create a `.env` file in the root directory and configure the environment variables (see `.env.example` for reference).

### Running the Application

```bash
python PrimaryDirectives.py

The application will start running on http://0.0.0.0:8000/.
API Endpoints
 * /v1/health: Health check endpoint.
 * /v1/process: Processes incoming requests.
 * /metrics: Exposes Prometheus metrics.
 * /v1/correct: Stores user-provided corrections.
Configuration
The application uses environment variables for configuration. Create a .env file in the root directory and set the required variables. (e.g. sample.env)
Example .env file:
AUTHORIZATION_API_URL=http://localhost:8080/auth
AUTHORIZATION_API_TOKEN=your_token
MODEL_NAME=t5-small
MODEL_CACHE_DIR=./model_cache
MODEL_CHECKSUM=example_checksum
SUMMARY_MODEL=facebook/bart-large
LOG_FILE=app.log
LAW_SUMMARY_DB_PATH=law_summary.db
DATABASE_UPDATE_URL=http://localhost:8081/laws
DATABASE_UPDATE_TOKEN=database_token
ALERTMANAGER_URL=http://localhost:9093/api/v1/alerts

Contributing
Please feel free to contribute by submitting pull requests, reporting bugs, or suggesting enhancements.
