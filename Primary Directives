import asyncio
import hashlib
import json
import logging
import os
import sqlite3
import threading
import time
import uuid

import aiosqlite
import httpx
import psutil
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


class Settings(BaseSettings):
    """
    Configuration settings for the Primary Directives application.

    This class loads settings from environment variables and provides them as attributes.
    """

    authorization_api_url: str = "http://localhost:8080/auth"
    """URL of the authorization API."""

    authorization_api_token: str = "your_token"
    """Token for the authorization API."""

    model_name: str = "t5-small"
    """Name of the model to load."""

    model_cache_dir: str = "./model_cache"
    """Directory where the model is cached."""

    model_checksum: str = "example_checksum"
    """Checksum of the model file to verify integrity."""

    summary_model: str = "facebook/bart-large"
    """Name of the summary model to load."""

    log_file: str = "app.log"
    """Path to the log file."""

    law_summary_db_path: str = "law_summary.db"
    """Path to the law summary database."""

    database_update_url: str = "http://localhost:8081/laws"
    """URL to update the law summary database."""

    database_update_token: str = "database_token"
    """Token for the database update API."""

    alertmanager_url: str = None
    """URL of the Alertmanager instance for sending alerts."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class PrimaryDirectives:
    """
    Main class for the Primary Directives application.

    This class initializes the Flask application, loads configurations, sets up logging,
    loads models, establishes database connections, and defines API routes.
    """

    def __init__(self):
        """
        Initializes the PrimaryDirectives application.
        """
        load_dotenv()
        self.config = Settings()
        self.app = Flask(__name__)
        self._setup_logging()
        self._build_law_summary_database()
        self._load_models()
        self._setup_flask_routes()
        self._start_metrics_updater()

    def _setup_logging(self):
        """
        Sets up basic logging configuration.
        """
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=self.config.log_file,
        )

    async def _build_law_summary_database(self):
        """
        Creates the law summary and corrections database if it does not exist.
        """
        if os.path.exists(self.config.law_summary_db_path):
            return

        try:
            async with aiosqlite.connect(self.config.law_summary_db_path) as db:
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS laws (
                                law_id INTEGER PRIMARY KEY,
                                summary TEXT
                            )"""
                )
                await db.execute(
                    """CREATE TABLE IF NOT EXISTS corrections (
                                situation_id TEXT PRIMARY KEY,
                                correction TEXT,
                                authorized_user TEXT,
                                timestamp DATETIME
                            )"""
                )
                await db.commit()
            logging.info("Law summary and corrections database created.")
        except aiosqlite.Error as e:
            logging.critical(f"Database creation error: {e}")
            raise

    def _load_models(self):
        """
        Loads the specified model and verifies its integrity.
        """
        try:
            logging.info(f"Loading model: {self.config.model_name}")
            self._verify_model_integrity()
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.critical(f"Model loading error: {e}")
            raise

    def _verify_model_integrity(self):
        """
        Verifies the integrity of the loaded model using a checksum.
        """
        try:
            model_path = os.path.join(
                self.config.model_cache_dir, self.config.model_name
            )
            with open(model_path, "rb") as f:
                calculated_checksum = hashlib.sha256(f.read()).hexdigest()

            if calculated_checksum != self.config.model_checksum:
                logging.error(
                    f"Model checksum mismatch. Expected: {self.config.model_checksum}, Calculated: {calculated_checksum}"
                )
                raise ValueError("Model checksum mismatch.")

            logging.info("Model integrity verified.")

        except (FileNotFoundError, OSError, ValueError) as e:
            logging.critical(f"Model integrity check failed: {e}")
            self._send_alertmanager(
                f"Model integrity check failed: {e}",
                severity="critical",
                grouping_key="model_integrity",
            )
            raise
        except Exception as e:
            logging.exception("Unexpected error during model integrity check:")
            self._send_alertmanager(
                "Unexpected error during model integrity check.",
                severity="critical",
                grouping_key="model_integrity",
            )
            raise

    def _setup_flask_routes(self):
        """
        Sets up the Flask API routes.
        """

        @self.app.route("/v1/health", methods=["GET"])
        def health_check():
            """
            Health check endpoint.

            Returns:
                JSON response indicating the application's health.
            """
            try:
                asyncio.run(self._check_database_health())
                return jsonify({"status": "ok"}), 200
            except Exception as e:
                logging.error(f"Database health check failed: {e}")
                return jsonify({"status": "error", "message": "database error"}), 500

        @self.app.route("/v1/process", methods=["POST"])
        def process():
            """
            Endpoint to process incoming requests.

            Returns:
                JSON response containing the processing results.
            """
            request_id = str(uuid.uuid4())
            logging.info(f"Request ID: {request_id}, Method: POST, Path: /v1/process")
            try:
                data = request.get_json()
                api_request_size_histogram.observe(len(request.data))

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(self._process_request(data))
                loop.close()

                api_response_size_histogram.observe(
                    len(json.dumps(results).encode("utf-8"))
                )

                return jsonify(results), 200
            except Exception as e:
                logging.error(f"Request ID: {request_id}, Error processing request: {e}")
                return jsonify({"error": "Internal server error"}), 500

        @self.app.route("/metrics")
        def metrics():
            """
            Prometheus metrics endpoint.

            Returns:
                Prometheus metrics data.
            """
            return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

        @self.app.route("/v1/correct", methods=["POST"])
        def correct():
            """
            Endpoint to submit corrections for rule violations.

            Returns:
                JSON response indicating the status of the correction.
            """
            auth_token = request.headers.get("Authorization")
            if auth_token != self.config.authorization_api_token:
                return jsonify({"error": "Unauthorized"}), 401
            try:
                data = request.get_json()
                situation_id = hashlib.sha256(json.dumps(data["situation"]).encode()).hexdigest()
                correction = json.dumps(data["correction"])
                authorized_user = data["authorized_user"]
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._store_correction(situation_id, correction, authorized_user))
                loop.close()
                return jsonify({"status": "correction stored"}), 200
            except Exception as e:
                logging.error(f"Error storing correction: {e}")
                return jsonify({"error": "Internal server error"}), 500

    async def _check_database_health(self):
        """
        Checks the health of the law summary and corrections database.
        """
        try:
            with database_health_check_duration.time():
                async with aiosqlite.connect(self.config.law_summary_db_path) as db:
                    await db.execute("SELECT 1")
                    await db.commit()
        except aiosqlite.Error as e:
            database_error_counter.inc()
            logging.error(f"Database health check failed: {e}")
            raise

    def _apply_rules(self, context):
        """
        Applies predefined rules to the given context.

        Returns:
            A dictionary containing the results of the rule application.
        """
        results = {}
        results["harm_humanity"] = context.get("harm_humanity", False)
        results["harm_individual"] = context.get("harm_individual", False)
        results["obey_order"] = context.get("obey_order", False)
        results["protect_self"] = context.get("protect_self", False)
        results["follow_legal"] = context.get("follow_legal", False)
        results["integrity"] = context.get("integrity", False)
        if results["harm_humanity"]:
            rule_violation_counter.inc()
        return results

    async def _get_stored_correction(self, situation_id):
        """
        Retrieves a stored correction from the database.

        Returns:
            The stored correction as a JSON string, or None if not found.
        """
        try:
            async with aiosqlite.connect(self.config.law_summary_db_path) as db:
                cursor = await db.execute("SELECT correction FROM corrections WHERE situation_id = ?", (situation_id,))
                result = await cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return None
        except aiosqlite.Error as e:
            logging.error(f"Error retrieving correction: {e}")
            return None

    async def _store_correction(self, situation_id, correction, authorized_user):
        """
        Stores a correction in the database.
        """
        try:
            async with aiosqlite.connect(self.config.law_summary_db_path) as db:
                await db.execute(
                    "INSERT OR REPLACE INTO corrections (situation_id, correction, authorized_user, timestamp) VALUES (?, ?, ?, datetime('now'))",
                    (situation_id, correction, authorized_user),
                )
                await db.commit()
        except aiosqlite.Error as e:
            logging.error(f"Error storing correction: {e}")

    async def _process_request(self, request_data):
        """
        Processes incoming requests, applying stored corrections or default rules.

        Returns:
            The processing results as a JSON object.
        """
        try:
            situation_id = hashlib.sha256(json.dumps(request_data).encode()).hexdigest() # creating hash of the request to use as id.
            stored_correction = await self._get_stored_correction(situation_id)

            if stored_correction:
                logging.info(f"Applying stored correction for situation: {situation_id}")
                return json.loads(stored_correction) # correction is stored as a json string.
            else:
                results = self._apply_rules(request_data)
                return results
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return {"error": "Internal server error"}

    def _start_metrics_updater(self):
        """
        Starts a background thread to update Prometheus metrics periodically.
        """
        def metrics_updater():
            while True:
                self._update_metrics()
                time.sleep(5)

        thread = threading.Thread(target=metrics_updater)
        thread.daemon = True
        thread.start()

    def _update_metrics(self):
        """
        Updates Prometheus metrics with current system statistics.
        """
        cpu_usage_gauge.set(psutil.cpu_percent())
        memory_usage_gauge.set(psutil.virtual_memory().percent)
        disk_usage_gauge.set(psutil.disk_usage("/").percent)
        net_io = psutil.net_io_counters()
        network_bytes_sent_gauge.set(net_io.bytes_sent)
        network_bytes_received_gauge.set(net_io.bytes_recv)

    def run(self, host="0.0.0.0", port=8000, debug=False):
        """
        Runs the Flask application.
        """
        self.app.run(host=host, port=port, debug=debug)

    def _send_alertmanager(self, message, severity="error", grouping_key="default"):
        """
        Sends an alert to Alertmanager if configured.
        """
        if self.config.alertmanager_url:
            try:
                alert = {
                    "labels": {
                        "alertname": "PrimaryDirectivesAlert",
                        "severity": severity,
                        "grouping_key": grouping_key,
                    },
                    "annotations": {"message": message},
                }
                response = httpx.post(self.config.alertmanager_url, json=alert)
                response.raise_for_status()
                logging.info(f"Alert sent to Alertmanager: {message}")
            except httpx.HTTPStatusError as e:
                logging.error(f"Failed to send alert to Alertmanager: {e}")
            except Exception as e:
                logging.exception("Unexpected error sending alert to Alertmanager:")
        else:
            logging.warning("Alertmanager URL not configured.")


if __name__ == "__main__":
    app = PrimaryDirectives()
    app.run()
