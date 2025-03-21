# --- fauna_monitor.py ---
import logging
import datetime

def monitor_fauna(activity_level, location, species=None):
    """Monitors and analyzes fauna activity."""
    timestamp = datetime.datetime.now()
    log_message = f"Fauna activity at {location}: Activity Level={activity_level}"
    if species:
        log_message += f", Species={species}"
    logging.info(log_message)

    analysis = {"alert": False, "message": "Fauna activity normal", "details": {}}

    if activity_level > 80:  # Example threshold
        analysis["alert"] = True
        analysis["message"] = "High fauna activity detected."
        analysis["details"]["activity_level"] = f"Activity Level: {activity_level}"
        if species:
            analysis["details"]["species"] = species

    return analysis
