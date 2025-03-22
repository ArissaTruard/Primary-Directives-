# soil_quality_monitor.py
import logging
import datetime
from typing import Optional, Dict
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_soil_quality(
    location_input: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    soil_api_key: Optional[str] = None,
) -> Dict[str, any]:
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

    analysis = {"alert": False, "message": "Soil conditions analysis complete.", "details": combined_data}
    alerts = []

    if combined_data.get("moisture", None) is not None and combined_data.get("moisture", 0) < 20:
        alerts.append("Low soil moisture detected.")
        analysis["details"]["moisture"] = f"Moisture: {combined_data.get('moisture')}%"
    if combined_data.get("temperature", None) is not None and combined_data.get("temperature", 0) > 35:
        alerts.append("High soil temperature detected.")
        analysis["details"]["temperature"] = f"Temperature: {combined_data.get('temperature')}°C"
    if combined_data.get("ph", None) is not None and (combined_data.get("ph", 0) < 5.5 or combined_data.get("ph", 0) > 7.5):
        alerts.append("Soil pH level is outside the optimal range.")
        analysis["details"]["ph"] = f"pH: {combined_data.get('ph')}"
    if combined_data.get("nitrogen", None) is not None and combined_data.get("nitrogen", 0) < 50:
        alerts.append("Low nitrogen content detected.")
        analysis["details"]["nitrogen"] = f"Nitrogen: {combined_data.get('nitrogen')} mg/kg"
    if combined_data.get("phosphorus", None) is not None and combined_data.get("phosphorus", 0) < 20:
        alerts.append("Low phosphorus content detected.")
        analysis["details"]["phosphorus"] = f"Phosphorus: {combined_data.get('phosphorus')} mg/kg"
    if combined_data.get("potassium", None) is not None and combined_data.get("potassium", 0) < 100:
        alerts.append("Low potassium content detected.")
        analysis["details"]["potassium"] = f"Potassium: {combined_data.get('potassium')} mg/kg"
    if combined_data.get("heavy_metals", None):
        for metal, concentration in combined_data["heavy_metals"].items():
            if concentration is not None and concentration > 10:
                alerts.append(f"High {metal} concentration detected.")
                analysis["details"][metal] = f"{metal}: {concentration}"
    if combined_data.get("pesticides", None):
        for pesticide, concentration in combined_data["pesticides"].items():
            if concentration is not None and concentration > 5:
                alerts.append(f"High {pesticide} concentration detected.")
                analysis["details"][pesticide] = f"{pesticide}: {concentration}"
    if alerts:
        analysis["alert"] = True
        analysis["message"] = " ".join(alerts)

    analysis["location"] = location

    return analysis

def get_soil_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "moisture": 30,
        "temperature": 25,
        "ph": 6.5,
        "nitrogen": 60,
        "phosphorus": 30,
        "potassium": 120,
        "heavy_metals": {"lead": 5, "mercury": 2},
        "pesticides": {"atrazine": 3, "glyphosate": 1},
    }

def get_soil_api_data(location, api_key):
    # Replace with real API call
    return {
        "moisture": 32,
        "temperature": 26,
        "ph": 6.6,
        "nitrogen": 62,
        "phosphorus": 32,
        "potassium": 122,
        "heavy_metals": {"lead": 6, "mercury": 2.5},
        "pesticides": {"atrazine": 3.5, "glyphosate": 1.2},
    }

def get_soil_data(location, api_key):
    url = f"https://api.example-soil-data.com/soil?q={location}&appid={api_key}"
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
