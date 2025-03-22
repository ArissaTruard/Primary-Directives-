# air_quality_monitor.py
import logging
import datetime
import requests
import json
from sub_location import get_location_from_address, get_address_from_location

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_air_quality(location_input, weather_api_key=None, latitude=None, longitude=None):
    """Monitors and analyzes air quality data from sensors, integrating location and weather."""
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    # Try to get sensor data
    try:
        sensor_data = get_air_quality_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Air quality sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    # Try to get API data if sensor data is unavailable or supplement with API data if available
    if not sensor_data_available:
        try:
            api_data = get_air_quality_api_data(location_str) # Replace with real API
            if api_data:
                api_data_available = True
                logging.info(f"Air quality API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No air quality data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Air quality analysis complete.", "details": combined_data}

    if combined_data.get("pm25", 0) > 50 or combined_data.get("pm10", 0) > 100 or combined_data.get("vocs", 0) > 100:
        logging.warning(f"High air pollution levels detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High pollution levels detected"

    if weather_api_key:
        try:
            weather_data = get_weather_data(location_str, weather_api_key)
            logging.info(f"Weather data: {weather_data}")
            analysis["details"]["weather"] = weather_data
        except Exception as e:
            logging.error(f"Error fetching weather data: {e}")
            analysis["details"]["weather_error"] = str(e)

    return analysis

def get_air_quality_sensor_data():
    # Replace with real sensor data retrieval
    return {"pm25": 10, "pm10": 20, "vocs": 30, "o3": 5, "no2": 2, "so2": 1, "co": 3}

def get_air_quality_api_data(location):
    # Replace with real API call
    return {"pm25": 15, "pm10": 25, "vocs": 35}

def get_weather_data(location, api_key):
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from weather API")
        return {"error": "Invalid JSON response"}
