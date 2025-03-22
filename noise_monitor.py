# noise_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_noise_levels(location_input=None, latitude=None, longitude=None, noise_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_noise_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Noise sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_noise_api_data(location_str, noise_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Noise API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No noise level data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Noise level monitoring complete.", "details": combined_data}

    if combined_data.get("decibels", 0) > 70:
        logging.warning(f"High noise levels detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High noise levels detected."
        analysis["details"]["decibels"] = f"Noise Level: {combined_data['decibels']} dB"

    if combined_data.get("frequency_range"):
        analysis["details"]["frequency_range"] = combined_data["frequency_range"]

    analysis["location"] = location

    return analysis

def get_noise_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "decibels": 65,
        "frequency_range": {"low": 20, "high": 20000},
    }

def get_noise_api_data(location, api_key):
    # Replace with real API call
    return {
        "decibels": 68,
        "frequency_range": {"low": 22, "high": 20010},
    }

def get_noise_data(location, api_key):
    url = f"https://api.example-noise.com/noise?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        noise_data = response.json()
        return noise_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Noise API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from noise API")
        return {"error": "Invalid JSON response"}
