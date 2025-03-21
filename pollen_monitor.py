# --- pollen_monitor.py ---
import logging
import datetime

def monitor_pollen(pollen_count, location):
    """Monitors and analyzes pollen counts."""
    timestamp = datetime.datetime.now()
    logging.info(f"Pollen count at {location}: {pollen_count}")
    analysis = {"alert": False, "message": "Pollen levels normal", "details": {}}

    if pollen_count > 50:  # Example threshold
        analysis["alert"] = True
        analysis["message"] = "High pollen levels detected."
        analysis["details"]["pollen_count"] = f"Pollen Count: {pollen_count}"

    return analysis
