# --- light_monitor.py ---
import logging
import datetime

def monitor_light(lux, location):
    """Monitors and analyzes light levels."""
    timestamp = datetime.datetime.now()
    logging.info(f"Light level at {location}: {lux} lux")
    analysis = {"alert": False, "message": "Light levels normal", "details": {}}

    if lux < 10:  # Example threshold
        analysis["alert"] = True
        analysis["message"] = "Low light levels detected."
        analysis["details"]["lux"] = f"Light Level: {lux} lux"

    return analysis
