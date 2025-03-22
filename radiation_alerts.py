# radiation_alerts.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_radiation_levels(location_input=None, latitude=None, longitude=None, radiation_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_radiation_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Radiation sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_radiation_api_data(location_str, radiation_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Radiation API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No radiation level data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Radiation level monitoring complete.", "details": combined_data}

    if combined_data.get("radiation_level", 0) > 100:
        logging.warning(f"High radiation levels detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High radiation levels detected."
        analysis["details"]["radiation_level"] = f"Radiation Level: {combined_data['radiation_level']} µSv/h"

    if combined_data.get("radiation_type"):
        analysis["details"]["radiation_type"] = combined_data["radiation_type"]

    analysis["location"] = location

    return analysis

def get_radiation_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "radiation_level": 80,
        "radiation_type": "Gamma",
    }

def get_radiation_api_data(location, api_key):
    # Replace with real API call
    return {
        "radiation_level": 90,
        "radiation_type": "Gamma",
    }

def get_radiation_data(location, api_key):
    url = f"https://api.example-radiation.com/radiation?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        radiation_data = response.json()
        return radiation_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Radiation API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from radiation API")
        return {"error": "Invalid JSON response"}
