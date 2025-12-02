# weather.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_weather(location_input=None, latitude=None, longitude=None, weather_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_weather_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Weather sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_weather_api_data(location_str, weather_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Weather API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No weather data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Weather conditions analysis complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}

    if combined_data.get("uv", 0) > 8:
        analysis["ppe_recommendation"] = "Sun Protection (sunscreen, hat, UV protective clothing)"
    if combined_data.get("precipitation", 0) > 50:
        analysis["ppe_recommendation"] = "Waterproof Clothing"
    if combined_data.get("wind_speed", 0) > 70:
        analysis["ppe_recommendation"] = "Windproof Clothing"

    if combined_data.get("temperature", 0) > 35:
        logging.warning(f"High temperature detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High temperature detected."
        analysis["details"]["temperature"] = f"{combined_data['temperature']} °C"

    if combined_data.get("humidity", 0) > 80:
        logging.warning(f"High humidity detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High humidity detected."
        analysis["details"]["humidity"] = f"{combined_data['humidity']} %"

    if combined_data.get("precipitation", 0) > 10:
        logging.warning(f"Significant precipitation detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Significant precipitation detected."
        analysis["details"]["precipitation"] = f"{combined_data['precipitation']} mm"

    if combined_data.get("wind_speed", 0) > 50:
        logging.warning(f"High wind speed detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High wind speed detected."
        analysis["details"]["wind_speed"] = f"{combined_data['wind_speed']} m/s"

    if combined_data.get("uv", 0) > 7:
        logging.warning(f"High UV index detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "High UV index detected."
        analysis["details"]["uv"] = combined_data.get("uv")

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

def get_weather_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "temperature": 28,
        "humidity": 60,
        "precipitation": 2,
        "wind_speed": 15,
        "uv": 6,
    }

def get_weather_api_data(location, api_key):
    # Replace with real API call
    return {
        "temperature": 30,
        "humidity": 65,
        "precipitation": 3,
        "wind_speed": 18,
        "uv": 7,
    }

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
