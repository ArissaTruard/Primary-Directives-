"""
Primary Directives Application

This application implements a Flask-based API designed to process requests,
enforce rules, and manage data corrections. It incorporates features like
database interaction, model loading, system metrics, and error handling.

Key Features:
- API endpoints for health checks, request processing, metrics, and data correction.
- Rule enforcement using a complex rule checking module.
- Database operations for storing and retrieving data corrections and law summaries.
- Model loading and integrity verification.
- System metrics collection and exposure via Prometheus.
- Configuration management using pydantic-settings and .env files.
- Logging to a file.
- Location services for context enrichment.
- Input sanitization to prevent security vulnerabilities.
- Robust error handling and system shutdown capabilities.
"""

import asyncio
import hashlib
import json
import logging
import os
import uuid

import aiosqlite
import httpx
from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Gauge,
    Histogram,
    generate_latest,
    Counter,
)
from pydantic_settings import BaseSettings, SettingsConfigDict
import html  # For input sanitization

# Prometheus metrics
database_health_check_duration = Histogram(
    "database_health_check_duration_seconds", "Database health check duration"
)
database_error_counter = Counter("database_error_count", "Number of database errors")
rule_violation_counter = Counter("rule_violation_count", "Number of rule violations")

# Additional Prometheus metrics
cpu_usage_gauge = Gauge("cpu_usage_percent", "CPU usage percentage")
memory_usage_gauge = Gauge("memory_usage_percent", "Memory usage percentage")
disk_usage_gauge = Gauge("disk_usage_percent", "Disk usage percentage")
network_bytes_sent_gauge = Gauge("network_bytes_sent", "Network bytes sent")
network_bytes_received_gauge = Gauge(
    "network_bytes_received", "Network bytes received"
)

# API request size histogram
api_request_size_histogram = Histogram(
    "api_request_size_bytes", "API request size in bytes"
)

# API response size histogram
api_response_size_histogram = Histogram(
    "api_response_size_bytes", "API response size in bytes"
)

# Import sub-codes
from sub3_complex_rule import Sub3ComplexRule, DataContext, RuleViolationError
from sub_system import shutdown
from sub_system_metrics import SystemMetrics
from sub_database import DatabaseHandler
from sub_location import LocationHandler

class Settings(BaseSettings):
    authorization_api_url: str = "http://localhost:8080/auth"
    authorization_api_token: str = "your_token"
    model_name: str = "t5-small"
    model_cache_dir: str = "./model_cache"
    model_checksum: str = "example_checksum"
    summary_model: str = "facebook/bart-large"
    log_file: str = "app.log"
    law_summary_db_path: str = "law_summary.db"
    database_update_url: str = "http://localhost:8081/laws"
    database_update_token: str = "database_token"
    alertmanager_url: str = None
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

class PrimaryDirectives:
    def __init__(self):
        """Initializes the PrimaryDirectives application."""
        load_dotenv()
        self.config = Settings()
        self.app = Flask(__name__)
        self._setup_logging()
        asyncio.run(self._build_law_summary_database())
        self._load_models()
        self._setup_flask_routes()
        self.system_metrics = SystemMetrics(cpu_usage_gauge, memory_usage_gauge, disk_usage_gauge, network_bytes_sent_gauge, network_bytes_received_gauge)
        self.system_metrics.start_metrics_updater()
        self.database_handler = DatabaseHandler(self.config.law_summary_db_path)
        self.location_handler = LocationHandler()
        self.rule_checker = Sub3ComplexRule(self._check_complex_rule, shutdown, self.database_handler)

    def _setup_logging(self):
        """Configures logging for the application."""
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", filename=self.config.log_file)

    async def _build_law_summary_database(self):
        """Asynchronously builds the law summary database."""
        await self.database_handler.build_database()

    def _load_models(self):
        """Loads machine learning models and verifies integrity."""
        try:
            logging.info(f"Loading model: {self.config.model_name}")
            self._verify_model_integrity()
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.critical(f"Model loading error: {e}")
            raise

    def _verify_model_integrity(self):
        """Verifies the integrity of the loaded model using checksums."""
        try:
            model_path = os.path.join(self.config.model_cache_dir, self.config.model_name)
            with open(model_path, "rb") as f:
                calculated_checksum = hashlib.sha256(f.read()).hexdigest()
            if calculated_checksum != self.config.model_checksum:
                logging.error(f"Model checksum mismatch.")
                raise ValueError("Model checksum mismatch.")
            logging.info("Model integrity verified.")
        except (FileNotFoundError, OSError, ValueError) as e:
            logging.critical(f"Model integrity check failed: {e}")
            shutdown(f"Model integrity check failed: {e}", self.config.alertmanager_url, severity="critical", grouping_key="model_integrity")
            raise
        except Exception as e:
            logging.exception("Unexpected error during model integrity check:")
            shutdown("Unexpected error during model integrity check.", self.config.alertmanager_url, severity="critical", grouping_key="model_integrity")
            raise

    def _setup_flask_routes(self):
        """Sets up Flask routes for the application."""
        @self.app.route("/v1/health", methods=["GET"])
        def health_check():
            """Performs database health check."""
            try:
                asyncio.run(self.database_handler.check_database_health(database_health_check_duration, database_error_counter))
                return jsonify({"status": "ok"}), 200
            except Exception as e:
                logging.error(f"Database health check failed: {e}")
                return jsonify({"status": "error", "message": "database error"}), 500

        @self.app.route("/v1/process", methods=["POST"])
        def process():
            """Processes incoming requests, applies rules, and returns results."""
            request_id = str(uuid.uuid4())
            logging.info(f"Request ID: {request_id}, Method: POST, Path: /v1/process")
            try:
                data = request.get_json()
                sanitized_data = self._sanitize_input(data)
                api_request_size_histogram.observe(len(request.data))
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(self._process_request(sanitized_data, request_id))
                loop.close()
                api_response_size_histogram.observe(len(json.dumps(results).encode("utf-8")))
                return jsonify(results), 200
            except Exception as e:
                logging.error(f"Request ID: {request_id}, Error processing request: {e}")
                return jsonify({"error": "Internal server error"}), 500

        @self.app.route("/metrics")
        def metrics():
            """Exposes Prometheus metrics."""
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

        @self.app.route("/v1/correct", methods=["POST"])
        def correct():
            """Stores user-provided corrections for situations."""
            auth_token = request.headers.get("Authorization")
            if auth_token != self.config.authorization_api_token:
                return jsonify({"error": "Unauthorized"}), 401
            try:
                data = request.get_json()
                sanitized_data = self._sanitize_input(data)
                situation_id = hashlib.sha256(json.dumps(sanitized_data["situation"]).encode()).hexdigest()
                correction = json.dumps(sanitized_data["correction"])
                authorized_user = sanitized_data["authorized_user"]
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.database_handler.store_correction(situation_id, correction, authorized_user))
                loop.close()
                return jsonify({"status": "correction stored"}), 200
            except Exception as e:
                logging.error(f"Error storing correction: {e}")
                return jsonify({"error": "Internal server error"}), 500

    def _check_complex_rule(self, context, request_id):
        """
        Placeholder for complex rule checking.

        Args:
            context (DataContext): The context data for rule checking.
            request_id (str): The request ID.

        Returns:
            bool: True if the rule is satisfied, False otherwise.
        """
        logging.info(f"Complex rule check called: {request_id}, context: {context.context_data}")
        return True

    async def _process_request(self, request_data, request_id):
        """
        Processes an incoming request, applies rules, and returns results.

        Args:
            request_data (dict): The request data.
            request_id (str): The request ID.

        Returns:
            dict: The processing results.
        """
        try:
            situation_id = hashlib.sha256(json.dumps(request_data).encode()).hexdigest()
            stored_correction = await self.database_handler.get_stored_correction(situation_id)

            if stored_correction:
                logging.info(f"Applying stored correction for situation: {situation_id}")
                return json.loads(stored_correction)
            else:
                context_dict = request_data
                try:
                    location_data = await self.location_handler.get_location()
                    context_dict.update(location_data)

                    results = await self.rule_checker.process_rule(context_dict, request_id, alertmanager_url = self.config.alertmanager_url)
                    return results
                except RuleViolationError:
                    rule_violation_counter.inc()
                    logging.warning(f"Rule violation detected for request: {request_id}")
                    return {"rule_violation": True}

        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return {"error": "Internal server error"}

    def run(self, host="0.0.0.0", port=8000, debug=False):
        """
        Runs the Flask application.

        Args:
            host (str): The host to run the application on.
            port (int): The port to run the application on.
            debug (bool): Whether to run in debug mode.
        """
        self.app.run(host=host, port=port, debug=debug)

    def _sanitize_input(self, data):
        """
        Sanitizes input data to prevent injection attacks.

        Args:
            data (dict): The input data to sanitize.

        Returns:
            dict: The sanitized data.
        """
        if isinstance(data, dict):
            sanitized_data = {}
            for key, value in data.items():
                sanitized_data[key] = self._sanitize_input(value)
            return sanitized_data
        elif isinstance(data, list):
            return [self._sanitize_input(item) for item in data]
        elif isinstance(data, str):
            return html.escape(data)
        else:
            return data

if __name__ == "__main__":
    app = PrimaryDirectives()
    app.run()
