# --- seismic_monitor.py ---
import logging
import datetime

def monitor_seismic_activity(ground_movement, location):
    """Monitors and analyzes seismic activity."""
    timestamp = datetime.datetime.now()
    logging.info(f"Seismic activity at {location} - {timestamp}: Ground Movement={ground_movement}")

    # Basic analysis
    if ground_movement > 5:  # Example threshold
        logging.warning(f"Significant ground movement detected at {location}")
        # Add alerting logic
