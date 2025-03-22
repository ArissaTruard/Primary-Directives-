# water_quality_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_water_quality(
    location_input=None,
    latitude=None,
    longitude=None,
    inquiry_location_input=None,
    inquiry_latitude=None,
    inquiry_longitude=None,
    water_api_key=None,
):
    timestamp = datetime.datetime.now()
    test_location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None
    inquiry_location = get_location_from_address(inquiry_location_input) if inquiry_location_input else get_address_from_location(inquiry_latitude, inquiry_longitude) if inquiry_latitude and inquiry_longitude else None

    if not test_location:
        logging.error("Test location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    test_location_str = test_location.get("address") if test_location.get("address") else f"Lat: {test_location.get('latitude')}, Lng: {test_location.get('longitude')}"
    inquiry_location_str = inquiry_location.get("address") if inquiry_location else None

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_water_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Water sensor data at {test_location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_water_api_data(test_location_str, water_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Water API data at {test_location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No water quality data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    log_message = f"Water quality data at {test_location_str}: {combined_data}"
    if inquiry_location_str:
        log_message += f", Inquiry Location: {inquiry_location_str}"
    logging.info(log_message)

    analysis = {"alert": False, "message": "Water quality analysis complete.", "details": combined_data}

    if combined_data.get("ph", 0) < 6.5 or combined_data.get("ph", 0) > 8.5 or combined_data.get("turbidity", 0) > 10:
        logging.warning(f"Water quality outside acceptable range at {test_location_str}")
        analysis["alert"] = True
        analysis["message"] = "Unacceptable water quality"
        analysis["details"]["ph"] = combined_data.get("ph")
        analysis["details"]["turbidity"] = combined_data.get("turbidity")
        analysis["details"]["dissolved_oxygen"] = combined_data.get("dissolved_oxygen")
        analysis["details"]["heavy_metals"] = combined_data.get("heavy_metals")
        analysis["details"]["pollutants"] = combined_data.get("pollutants")
    analysis["test_location"] = test_location
    analysis["inquiry_location"] = inquiry_location

    return analysis

def get_water_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "ph": 7.0,
        "turbidity": 5,
        "dissolved_oxygen": 8,
        "heavy_metals": {"lead": 1, "mercury": 0.5},
        "pollutants": {"pesticides": 2, "nitrates": 10},
    }

def get_water_api_data(location, api_key):
    # Replace with real API call
    return {
        "ph": 7.2,
        "turbidity": 6,
        "dissolved_oxygen": 8.2,
        "heavy_metals": {"lead": 1.1, "mercury": 0.6},
        "pollutants": {"pesticides": 2.1, "nitrates": 10.2},
    }

def get_water_data(location, api_key):
    url = f"https://api.example-water-quality.com/water?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        water_data = response.json()
        return water_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Water quality API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from water quality API")
        return {"error": "Invalid JSON response"}
