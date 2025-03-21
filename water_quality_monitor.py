# --- water_quality_monitor.py ---
import logging
import datetime

def monitor_water_quality(ph, turbidity, dissolved_oxygen, heavy_metals, pollutants, location):
    """Monitors and analyzes water quality data."""
    timestamp = datetime.datetime.now()
    logging.info(f"Water quality data at {location}: pH={ph}, Turbidity={turbidity}, DO={dissolved_oxygen}, Heavy Metals={heavy_metals}, Pollutants={pollutants}")
    analysis = {"alert": False, "message": "Water quality normal"}

    if ph < 6.5 or ph > 8.5 or turbidity > 10:
        logging.warning(f"Water quality outside acceptable range at {location}")
        analysis["alert"] = True
        analysis["message"] = "Unacceptable water quality"
    return analysis
