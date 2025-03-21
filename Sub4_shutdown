"""
Sub4_shutdown Module

This module provides a function to trigger alert notifications and initiate a system shutdown.
It logs critical messages, sends alerts to Alertmanager (if configured), and attempts
to shut down the system based on the operating system.

Functions:
    sub4_shutdown(message, alertmanager_url=None): Triggers an alert and initiates shutdown.
"""

import logging
import os
import platform

def sub4_shutdown(message, alertmanager_url=None):
    """
    Triggers an alert notification and initiates a system shutdown.

    Args:
        message (str): The message to log and send as an alert.
        alertmanager_url (str, optional): The URL of the Alertmanager instance.
            Defaults to None.

    Raises:
        ImportError: If the httpx library is not found.
        httpx.HTTPStatusError: If sending the alert to Alertmanager fails.
        Exception: For unexpected errors during alert sending or shutdown.
    """
    logging.critical(message)

    # Send alert to Alertmanager (if configured)
    if alertmanager_url:
        try:
            import httpx  # Import httpx only when needed

            alert = {
                "labels": {
                    "alertname": "PrimaryDirectivesShutdown",
                    "severity": "critical",
                    "grouping_key": "critical_shutdown",
                },
                "annotations": {"message": message},
            }
            response = httpx.post(alertmanager_url, json=alert)
            response.raise_for_status()
            logging.info(f"Alert sent to Alertmanager: {message}")
        except ImportError:
            logging.error("httpx library not found. Alertmanager alert not sent.")
        except httpx.HTTPStatusError as e:
            logging.error(f"Failed to send alert to Alertmanager: {e}")
        except Exception as e:
            logging.exception("Unexpected error sending alert to Alertmanager:")
    else:
        logging.warning("Alertmanager URL not configured.")

    # Initiate system shutdown
    try:
        logging.critical("Initiating system shutdown...")
        os_name = platform.system()
        if os_name == "Windows":
            os.system("shutdown /s /t 1")
        elif os_name == "Linux":
            os.system("sudo shutdown -h now")
        elif os_name == "Darwin": #macOS
            os.system("sudo shutdown -h now")
        else:
            logging.critical(f"Unsupported OS: {os_name}")
    except Exception as e:
        logging.critical(f"Shutdown failed: {e}")
