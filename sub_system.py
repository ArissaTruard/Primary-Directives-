import logging
import os
import platform
import httpx

def shutdown(message, alertmanager_url=None):
    logging.critical(message)
    if alertmanager_url:
        try:
            alert = {
                "labels": {"alertname": "Shutdown", "severity": "critical", "grouping_key": "critical_shutdown"},
                "annotations": {"message": message},
            }
            response = httpx.post(alertmanager_url, json=alert)
            response.raise_for_status()
            logging.info(f"Alert sent to Alertmanager: {message}")
        except Exception as e:
            logging.exception(f"Error sending alert: {e}")
    else:
        logging.warning("Alertmanager URL not configured.")
    try:
        os_name = platform.system()
        if os_name == "Windows":
            os.system("shutdown /s /t 1")
        elif os_name in ("Linux", "Darwin"):
            os.system("sudo shutdown -h now")
        else:
            logging.critical(f"Unsupported OS: {os_name}")
    except Exception as e:
        logging.critical(f"Shutdown failed: {e}")
