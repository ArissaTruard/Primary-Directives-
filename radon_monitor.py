# --- radon_monitor.py ---
import logging
import datetime

def monitor_radon(radon_level, location):
    """Monitors and analyzes radon levels."""
    timestamp = datetime.datetime.now()
    logging.info(f"Radon level at {location}: {radon_level} pCi/L")
    analysis = {"alert": False, "message": "Radon levels normal", "details": {}}

    if radon_level > 4:  # Example threshold
        analysis["alert"] = True
        analysis["message"] = "High radon levels detected."
        analysis["details"]["radon_level"] = f"Radon Level: {radon_level} pCi/L"

    return analysis
