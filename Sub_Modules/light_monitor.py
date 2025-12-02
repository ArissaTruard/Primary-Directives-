# light_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_light_levels(location_input=None, latitude=None, longitude=None, light_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_light_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Light sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_light_api_data(location_str, light_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Light API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No light level data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Light level monitoring complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}

    if combined_data.get("illuminance", 0) < 50:
        logging.warning(f"Low illuminance detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low light levels detected."
        analysis["details"]["illuminance"] = f"Illuminance: {combined_data['illuminance']} lux"

    if combined_data.get("uv_index", 0) > 10:
        logging.warning(f"High UV index detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High UV index detected."
        analysis["details"]["uv_index"] = f"UV Index: {combined_data['uv_index']}"
        analysis["ppe_recommendation"] = "Eye Protection (UV protective glasses)"

    analysis["location"] = location

    return analysis

def get_light_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "illuminance": 100,
        "uv_index": 5,
        "visible_light": {"red": 255, "green": 200, "blue": 150},
    }

def get_light_api_data(location, api_key):
    # Replace with real API call
    return {
        "illuminance": 110,
        "uv_index": 6,
        "visible_light": {"red": 250, "green": 205, "blue": 155},
    }

def get_light_data(location, api_key):
    url = f"https://api.example-light.com/light?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        light_data = response.json()
        return light_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Light API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from light API")
        return {"error": "Invalid JSON response"}
