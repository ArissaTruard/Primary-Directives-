# vegetation_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_vegetation(location_input=None, latitude=None, longitude=None, vegetation_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_ndvi_from_sensor()
        if sensor_data is not None:
            sensor_data_available = True
            logging.info(f"Vegetation sensor data at {location_str}: NDVI={sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_vegetation_api_data(location_str, vegetation_api_key)
            if api_data is not None:
                api_data_available = True
                logging.info(f"Vegetation API data at {location_str}: NDVI={api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No vegetation data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data["ndvi"] = sensor_data
    if api_data_available:
        combined_data["ndvi"] = api_data

    analysis = {"alert": False, "message": "Vegetation health analysis complete.", "details": combined_data}

    if combined_data.get("ndvi", 1) < 0.3:
        logging.warning(f"Unhealthy vegetation detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Unhealthy vegetation detected."
        analysis["details"]["ndvi"] = f"NDVI: {combined_data['ndvi']}"
    analysis["location"] = location

    return analysis

def get_ndvi_from_sensor():
    # Replace with real sensor data retrieval
    return 0.5

def get_vegetation_api_data(location, api_key):
    # Replace with real API call
    return 0.55

def get_vegetation_data(location, api_key):
    url = f"https://api.example-vegetation.com/vegetation?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        vegetation_data = response.json()
        return vegetation_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Vegetation API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from vegetation API")
        return {"error": "Invalid JSON response"}
