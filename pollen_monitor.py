# pollen_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_pollen_levels(location_input=None, latitude=None, longitude=None, pollen_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_pollen_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Pollen sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_pollen_api_data(location_str, pollen_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Pollen API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No pollen level data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Pollen level monitoring complete.", "details": combined_data}

    if combined_data.get("pollen_count", 0) > 500:
        logging.warning(f"High pollen levels detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High pollen levels detected."
        analysis["details"]["pollen_count"] = f"Pollen Count: {combined_data['pollen_count']}"

    if combined_data.get("dominant_species"):
        analysis["details"]["dominant_species"] = combined_data["dominant_species"]

    analysis["location"] = location

    return analysis

def get_pollen_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "pollen_count": 300,
        "dominant_species": "Oak",
    }

def get_pollen_api_data(location, api_key):
    # Replace with real API call
    return {
        "pollen_count": 350,
        "dominant_species": "Oak",
    }

def get_pollen_data(location, api_key):
    url = f"https://api.example-pollen.com/pollen?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        pollen_data = response.json()
        return pollen_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Pollen API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from pollen API")
        return {"error": "Invalid JSON response"}
