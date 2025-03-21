# --- soil_quality_monitor.py ---
import logging
import datetime

def monitor_soil_quality(ph, moisture, nutrients, heavy_metals, pesticides, location):
    """Monitors and analyzes soil quality data."""
    timestamp = datetime.datetime.now()
    logging.info(f"Soil quality data at {location}: pH={ph}, Moisture={moisture}, Nutrients={nutrients}, Heavy Metals={heavy_metals}, Pesticides={pesticides}")
    analysis = {"alert": False, "message": "Soil quality normal"}

    if ph < 6 or ph > 7 or nutrients < 5:
        logging.warning(f"Soil quality outside acceptable range at {location}")
        analysis["alert"] = True
        analysis["message"] = "Unacceptable soil quality"

    return analysis
