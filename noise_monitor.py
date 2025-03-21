# --- noise_monitor.py ---
import logging
import datetime

def monitor_noise_levels(noise_level, location):
    """Monitors and analyzes noise pollution levels."""
    timestamp = datetime.datetime.now()
    logging.info(f"Noise level at {location}: {noise_level} dB")
    analysis = {"alert": False, "message": "Noise levels normal"}

    if noise_level > 80:
        logging.warning(f"High noise levels detected at {location}")
        analysis["alert"]
