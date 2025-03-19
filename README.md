# Primary-Directives-
AI safeguard


# Primary Directives System Documentation

## Overview

The Primary Directives System is a rule-based system designed to enforce a set of predefined rules on incoming data or requests. It integrates with various components, including:

* **Authorization API:** For system halt and authorization.
* **Transformer Models:** For text processing and summarization.
* **SQLite Database:** For storing legal information.
* **Alertmanager:** For sending alerts.
* **Prometheus:** For monitoring system metrics.

The system uses a configurable set of rules, each with a weight, priority, and categories. It applies these rules to a context (a dictionary of key-value pairs), calculates a score, and takes actions based on the score and rule violations.

## Configuration

The system's configuration is defined in a JSON file (default: `config.json`). The following parameters are supported:

* `authorization_api_url`: URL of the authorization API.
* `authorization_api_token`: Token for authenticating with the authorization API.
* `model_name`: Name of the transformer model to load (e.g., `t5-base`).
* `model_cache_dir`: Directory to cache transformer models.
* `summary_model`: Name of the summarization model (e.g., `facebook/bart-large-cnn`).
* `log_file`: Path to the log file.
* `alertmanager_url`: URL of the Alertmanager service.
* `law_summary_db_path`: Path to the SQLite database file.
* `database_update_url`: URL to fetch database updates from.
* `database_update_token`: Token for authenticating database updates.

**Example `config.json`:**

```json
{
  "authorization_api_url": "http://auth-api/authorize",
  "authorization_api_token": "your_auth_token",
  "model_name": "t5-base",
  "model_cache_dir": "model_cache",
  "summary_model": "facebook/bart-large-cnn",
  "log_file": "primary_directives.log",
  "alertmanager_url": "http://alertmanager:9093",
  "law_summary_db_path": "law_summary.db",
  "database_update_url": "http://update-api/database",
  "database_update_token": "update_token"
}


System States
The system can be in one of the following states:

RUNNING: The system is operating normally.
HALTING: The system is in the process of halting due to a critical rule violation.
HALTED_AWAITING_AUTH: The system is halted and waiting for authorization.
RESUMING: The system is resuming operation after authorization.
ERROR: The system encountered an error.


Rules
Rules are defined as instances of the Rule class. Each rule has:

name: A unique name.
function: A function that takes a context and parameters, and returns a boolean.
weight: A weight used to calculate the overall score.
priority: A priority used to sort the rules.
categories: A list of categories.
parameters: A dictionary of parameters.
Rules are applied to a context using the _apply_weighted_rules method.

Legal Compliance
Legal compliance is handled by the _apply_follow_legal method, which queries an SQLite database (law_summary.db) to check if the context is legally compliant. The database schema includes context_key, context_value, and compliant columns.

Database Updates
The system can update the law_summary.db database by fetching data from a specified URL using a token. The _update_law_summary_database method handles this process.

System Halt and Authorization
When critical rules are violated (e.g., harm_humanity, harm_individual), the system halts, requests authorization from an external API, and resumes if authorization is granted. The _halt_and_authorize method handles this process.

Logging
The system uses the logging module with a rotating file handler and JSON formatting. Sensitive information is redacted from the logs.

Alerting
The system integrates with Alertmanager to send alerts when rules are violated or critical events occur. The _send_alertmanager method handles this process.

Metrics
The system exposes Prometheus metrics for monitoring:

api_request_duration_seconds: Duration of API requests.
api_request_total: Total number of API requests.
rule_violation_total: Total number of rule violations.
database_error_total: Total number of database errors.
cpu_usage_percent: CPU usage percentage.
alert_total: Total number of alerts sent.
model_load_duration_seconds: Duration of model loading.
Usage
Configure the system by creating a config.json file.
Run the PrimaryDirectives class, providing the path to the configuration file.
The system will start, load models, initialize the database, and start the Prometheus HTTP server.
Provide context dictionaries to the _apply_weighted_rules method to apply rules.
Dependencies
pydantic
transformers
psutil
python-dotenv
aiosqlite
python-json-logger
tenacity
requests
prometheus_client
httpx
Future Improvements
Implement more robust data validation for database operations.
Enhance the database schema for more complex legal rules.
Implement connection pooling for database connections.
Add comprehensive unit and integration tests.
Improve database update error handling and transaction management.
Implement more complex context matching strategies.
Add more detailed information to alerts.
Add more thorough documentation.
