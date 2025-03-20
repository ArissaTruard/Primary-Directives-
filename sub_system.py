import logging
import httpx

def shutdown(message, alertmanager_url, severity="critical", grouping_key="system_shutdown"):
    """Sends a shutdown alert to Alertmanager and then shuts down the system."""
    try:
        if alertmanager_url:
            alert = {
                "alerts": [
                    {
                        "annotations": {
                            "description": message,
                            "summary": "System Shutdown Alert",
                        },
                        "labels": {
                            "severity": severity,
                            "grouping_key": grouping_key,
                        },
                    }
                ]
            }
            httpx.post(alertmanager_url, json=alert)
            logging.info("Shutdown alert sent to Alertmanager.")
        else:
            logging.warning("Alertmanager URL not configured. Shutdown alert not sent.")
    except Exception as e:
        logging.error(f"Error sending shutdown alert: {e}")
    finally:
        logging.critical("System is shutting down.")
        exit(1)
