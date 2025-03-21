# --- air_quality_monitor.py ---
import logging
import datetime
import requests

def monitor_air_quality(pm25, pm10, vocs, o3, no2, so2, co, location, weather_api_key=None):
    """Monitors and analyzes air quality data."""
    timestamp = datetime.datetime.now()
    logging.info(f"Air quality data at {location}: PM2.5={pm25}, PM10={pm10}, VOCs={vocs}, O3={o3}, NO2={no2}, SO2={so2}, CO={co}")
    analysis = {"alert": False, "message": "Air quality normal"}

    if pm25 > 50 or pm10 > 100 or vocs > 100:
        logging.warning(f"High air pollution levels detected at {location}")
        analysis["alert"] = True
        analysis["message"] = "High pollution levels detected"

    if weather_api_key:
        try:
            weather_data = get_weather_data(location, weather_api_key)
            logging.info(f"Weather data: {weather_data}")
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}")

    return analysis

def get_weather_data(location, api_key):
    """Retrieves weather data from an external API."""
    # Replace with your actual weather API call
    return {"temperature": 25, "humidity": 60, "wind_speed": 10}
