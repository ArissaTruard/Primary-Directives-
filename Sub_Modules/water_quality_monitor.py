# water_quality_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_water_quality(location_input=None, latitude=None, longitude=None, inquiry_location_input=None, inquiry_latitude=None, inquiry_longitude=None, water_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None
    inquiry_location = get_location_from_address(inquiry_location_input) if inquiry_location_input else get_address_from_location(inquiry_latitude, inquiry_longitude) if inquiry_latitude and inquiry_longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_water_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Water sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_water_api_data(location_str, water_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Water API data at {location_str}: {api_data}")
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

    analysis = {"alert": False, "message": "Water quality analysis complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}

    if combined_data.get("ph", 0) < 6 or combined_data.get("ph", 0) > 9:
        analysis["ppe_recommendation"] = "Eye and Skin Protection (gloves, goggles)"
    if combined_data.get("heavy_metals"):
        for metal, concentration in combined_data["heavy_metals"].items():
            if concentration is not None and concentration > 20:
                analysis["ppe_recommendation"] = "Full Protective Suit"
    if combined_data.get("pollutants"):
        for pollutant, concentration in combined_data["pollutants"].items():
            if concentration is not None and concentration > 10:
                analysis["ppe_recommendation"] = "Full Protective Suit and Respiratory Protection"

    if combined_data.get("ph", 0) < 6.5 or combined_data.get("ph", 0) > 8.5:
        logging.warning(f"Water pH outside optimal range at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Water pH outside optimal range."
        analysis["details"]["ph"] = combined_data.get("ph")

    if combined_data.get("turbidity", 0) > 5:
        logging.warning(f"High turbidity detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High turbidity detected."
        analysis["details"]["turbidity"] = combined_data.get("turbidity")

    if combined_data.get("dissolved_oxygen", 0) < 4:
        logging.warning(f"Low dissolved oxygen detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low dissolved oxygen detected."
        analysis["details"]["dissolved_oxygen"] = combined_data.get("dissolved_oxygen")

    if combined_data.get("conductivity", 0) > 1500:
        logging.warning(f"High conductivity detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High conductivity detected."
        analysis["details"]["conductivity"] = combined_data.get("conductivity")

    if combined_data.get("heavy_metals"):
        for metal, concentration in combined_data["heavy_metals"].items():
            if concentration is not None and concentration > 1:
                logging.warning(f"Heavy metal {metal} exceeds safe limits at {location_str}")
                analysis["alert"] = True
                analysis["message"] = f"Heavy metal {metal} exceeds safe limits."
                analysis["details"][f"heavy_metal_{metal}"] = concentration

    if combined_data.get("pollutants"):
        for pollutant, concentration in combined_data["pollutants"].items():
            if concentration is not None and concentration > 1:
                logging.warning(f"Pollutant {pollutant} exceeds safe limits at {location_str}")
                analysis["alert"] = True
                analysis["message"] = f"Pollutant {pollutant} exceeds safe limits."
                analysis["details"][f"pollutant_{pollutant}"] = concentration

    analysis["location"] = location
    analysis["inquiry_location"] = inquiry_location

    return analysis

def get_water_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "ph": 7.5,
        "turbidity": 2,
        "dissolved_oxygen": 6,
        "conductivity": 1000,
        "heavy_metals": {"lead": 0.5, "mercury": 0.1},
        "pollutants": {"pesticides": 0.2, "nitrates": 2},
    }

def get_water_api_data(location, api_key):
    # Replace with real API call
    return {
        "ph": 7.8,
        "turbidity": 2.5,
        "dissolved_oxygen": 6.5,
        "conductivity": 1100,
        "heavy_metals": {"lead": 0.6, "mercury": 0.12},
        "pollutants": {"pesticides": 0.22, "nitrates": 2.2},
    }

def get_water_data(location, api_key):
    url = f"https://api.example-water.com/water?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        water_data = response.json()
        return water_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Water API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from water API")
        return {"error": "Invalid JSON response"}
