# --- vegetation_monitor.py ---
import logging
import datetime

def monitor_vegetation(ndvi, location):
    """Monitors and analyzes vegetation health using NDVI."""
    timestamp = datetime.datetime.now()
    logging.info(f"Vegetation data at {location}: NDVI={ndvi}")
    analysis = {"alert": False, "message": "Vegetation health normal", "details": {}}

    if ndvi < 0.3:  # Example threshold
        analysis["alert"] = True
        analysis["message"] = "Unhealthy vegetation detected."
        analysis["details"]["ndvi"] = f"NDVI: {ndvi}"

    return analysis
