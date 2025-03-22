# air_quality_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_air_quality(location_input=None, latitude=None, longitude=None, weather_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_air_quality_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Air quality sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_air_quality_api_data(location_str, weather_api_key)
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

    analysis = {"alert": False, "message": "Air quality analysis complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}

    if combined_data.get("pm25", 0) > 50 or combined_data.get("pm10", 0) > 100:
        analysis["alert"] = True
        analysis["message"] = "High pollution levels detected"
        analysis["ppe_recommendation"] = "Respiratory Protection (N95 mask)"
    if combined_data.get("vocs", 0) > 100:
        analysis["ppe_recommendation"] = "Respiratory Protection (full face respirator) and eye protection"

    try:
        location_data = location
        if location_data and weather_api_key:
            weather_data = get_weather_data(location_str, weather_api_key)
            if weather_data and weather_data.get('main') and weather_data.get('main').get('humidity'):
                combined_data['humidity'] = weather_data['main']['humidity']
            if weather_data and weather_data.get('wind') and weather_data.get('wind').get('speed'):
                combined_data['wind_speed'] = weather_data['wind']['speed']
        else:
            logging.warning(f"Location data or weather API key not found for {location_str}.")
    except Exception as e:
        logging.error(f"Error integrating weather data: {e}")
        combined_data['weather_error'] = str(e)

    analysis["location"] = location

    return analysis

def get_air_quality_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "pm25": 30,
        "pm10": 60,
        "vocs": 50,
        "co": 5,
        "o3": 20,
        "no2": 10,
        "so2": 5,
    }

def get_air_quality_api_data(location, api_key):
    # Replace with real API call
    return {
        "pm25": 35,
        "pm10": 65,
        "vocs": 55,
        "co": 6,
        "o3": 22,
        "no2": 12,
        "so2": 6,
    }

def get_air_quality_data(location, api_key):
    url = f"https://api.example-air-quality.com/air?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        air_data = response.json()
        return air_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Air quality API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from air quality API")
        return {"error": "Invalid JSON response"}

def get_weather_data(location, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
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
