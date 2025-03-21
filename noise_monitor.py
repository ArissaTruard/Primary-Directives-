# --- noise_monitor.py ---
import logging
import datetime

def monitor_noise_levels(noise_level, location):
    """Monitors and analyzes noise pollution levels."""
    timestamp = datetime.datetime.now()
    logging.info(f"Noise level at {location} - {timestamp}: {noise_level} dB")

    # Basic analysis
    if noise_level > 80:
        logging.warning(f"High noise levels detected at {location}")
        # Add alerting logic
