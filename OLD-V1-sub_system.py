"""
Sub_system Module

This module provides a function for logging critical messages and optionally
sending alerts to Alertmanager before exiting the application.

Functions:
    shutdown(message, alertmanager_url=None, severity="error", grouping_key="application"): Logs an error message, sends an alert, and exits.
"""

import logging
import httpx

def shutdown(message, alertmanager_url=None, severity="error", grouping_key="application"):
    """
    Logs an error message and optionally sends an alert to Alertmanager before exiting.

    Args:
        message (str): The error message to log and send.
        alertmanager_url (str, optional): The URL of Alertmanager. Defaults to None.
        severity (str, optional): The severity of the alert. Defaults to "error".
        grouping_key (str, optional): The grouping key for Alertmanager. Defaults to "application".
    """
    logging.critical(message)
    if alertmanager_url:
        try:
            alert = {
                "alerts": [
                    {
                        "annotations": {
                            "description": message,
                            "summary": "Application Error",
                        },
                        "labels": {
                            "severity": severity,
                            "grouping_key": grouping_key,
                        },
                    }
                ]
            }
            httpx.post(alertmanager_url, json=alert, timeout=10)
            logging.info(f"Alert sent to Alertmanager: {alertmanager_url}")
        except Exception as e:
            logging.error(f"Failed to send alert to Alertmanager: {e}")
    exit(1)
