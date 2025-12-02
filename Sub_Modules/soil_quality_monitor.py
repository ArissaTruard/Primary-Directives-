# soil_quality_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_soil_quality(location_input=None, latitude=None, longitude=None, soil_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_soil_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Soil sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_soil_api_data(location_str, soil_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Soil API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No soil quality data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Soil conditions analysis complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}

    if combined_data.get("ph", 0) < 5 or combined_data.get("ph", 0) > 9:
        analysis["ppe_recommendation"] = "Eye and Skin Protection (gloves, goggles)"
    if combined_data.get("heavy_metals"):
        for metal, concentration in combined_data["heavy_metals"].items():
            if concentration is not None and concentration > 50:
                analysis["ppe_recommendation"] = "Full Protective Suit and Respiratory Protection"
    if combined_data.get("pesticides"):
        for pesticide, concentration in combined_data["pesticides"].items():
            if concentration is not None and concentration > 20:
                analysis["ppe_recommendation"] = "Full Protective Suit and Respiratory Protection"

    if combined_data.get("ph", 0) < 5.5 or combined_data.get("ph", 0) > 8.5:
        logging.warning(f"Soil pH outside optimal range at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Soil pH outside optimal range."
        analysis["details"]["ph"] = combined_data.get("ph")

    if combined_data.get("nitrogen", 0) < 20 or combined_data.get("nitrogen", 0) > 150:
        logging.warning(f"Nitrogen levels outside optimal range at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Nitrogen levels outside optimal range."
        analysis["details"]["nitrogen"] = combined_data.get("nitrogen")

    if combined_data.get("phosphorus", 0) < 10 or combined_data.get("phosphorus", 0) > 100:
        logging.warning(f"Phosphorus levels outside optimal range at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Phosphorus levels outside optimal range."
        analysis["details"]["phosphorus"] = combined_data.get("phosphorus")

    if combined_data.get("potassium", 0) < 50 or combined_data.get("potassium", 0) > 300:
        logging.warning(f"Potassium levels outside optimal range at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Potassium levels outside optimal range."
        analysis["details"]["potassium"] = combined_data.get("potassium")

    if combined_data.get("heavy_metals"):
        for metal, concentration in combined_data["heavy_metals"].items():
            if concentration is not None and concentration > 10:
                logging.warning(f"Heavy metal {metal} exceeds safe limits at {location_str}")
                analysis["alert"] = True
                analysis["message"] = f"Heavy metal {metal} exceeds safe limits."
                analysis["details"][f"heavy_metal_{metal}"] = concentration

    if combined_data.get("pesticides"):
        for pesticide, concentration in combined_data["pesticides"].items():
            if concentration is not None and concentration > 5:
                logging.warning(f"Pesticide {pesticide} exceeds safe limits at {location_str}")
                analysis["alert"] = True
                analysis["message"] = f"Pesticide {pesticide} exceeds safe limits."
                analysis["details"][f"pesticide_{pesticide}"] = concentration

    analysis["location"] = location

    return analysis

def get_soil_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "ph": 6.5,
        "nitrogen": 80,
        "phosphorus": 50,
        "potassium": 200,
        "heavy_metals": {"lead": 5, "cadmium": 2},
        "pesticides": {"atrazine": 1, "glyphosate": 3},
    }

def get_soil_api_data(location, api_key):
    # Replace with real API call
    return {
        "ph": 6.8,
        "nitrogen": 85,
        "phosphorus": 55,
        "potassium": 210,
        "heavy_metals": {"lead": 6, "cadmium": 2.5},
        "pesticides": {"atrazine": 1.2, "glyphosate": 3.2},
    }

def get_soil_data(location, api_key):
    url = f"https://api.example-soil.com/soil?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soil_data = response.json()
        return soil_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Soil API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from soil API")
        return {"error": "Invalid JSON response"}
