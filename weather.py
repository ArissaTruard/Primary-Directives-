# weather.py
import logging
import datetime
import requests
import json
from sub_location import get_location_from_address, get_address_from_location

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_weather(
    location_input=None,
    latitude=None,
    longitude=None,
    weather_api_key=None,
):
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
            api_data = get_weather_api_data(location_str)
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

    analysis = {
        "alert": False,
        "message": "Weather conditions analysis complete.",
        "details": combined_data,
    }

    try:
        location_data = location
        if location_data:
            optimal_humidity = 60
            max_temperature = 30
            max_uv = 8
            max_precipitation = 15

            if combined_data.get("humidity", None) is not None and combined_data.get("humidity", 0) > optimal_humidity + 20:
                analysis["alert"] = True
                analysis["message"] = "High humidity detected."
                analysis["details"]["humidity"] = f"Humidity: {combined_data['humidity']}%"
            if combined_data.get("temperature", None) is not None and combined_data.get("temperature", 0) > max_temperature + 5:
                analysis["alert"] = True
                analysis["message"] = "High temperature detected."
                analysis["details"]["temperature"] = f"Temperature: {combined_data['temperature']}°C"
            if combined_data.get("uv", None) is not None and combined_data.get("uv", 0) > max_uv + 2:
                analysis["alert"] = True
                analysis["message"] = "High UV index detected."
                analysis["details"]["uv"] = f"UV Index: {combined_data['uv']}"
            if combined_data.get("precipitation", None) is not None and combined_data.get("precipitation", 0) > max_precipitation:
                analysis["alert"] = True
                analysis["message"] = f"Heavy precipitation detected: {combined_data['precipitation']} mm/hr"
                analysis["details"]["precipitation"] = f"Precipitation: {combined_data['precipitation']} mm/hr, Type: {combined_data.get('precipitation_type')}"
            if combined_data.get("water_level") and combined_data["water_level"] == "flood":
                analysis["alert"] = True
                analysis["message"] = "Flood conditions detected."
                analysis["details"]["water_level"] = "Flood conditions"
            if combined_data.get("storm_alert"):
                analysis["alert"] = True
                analysis["message"] = f"Storm alert: {combined_data['storm_alert']}"
                analysis["details"]["storm_alert"] = combined_data["storm_alert"]
            if combined_data.get("air_quality") and combined_data["air_quality"].get('alert'):
                analysis["alert"] = True
                analysis["message"] = "Adverse air quality detected."
                analysis["details"]["air_quality"] = combined_data["air_quality"]["message"]
            if combined_data.get("allergens") and combined_data["allergens"].get('alert'):
                analysis["alert"] = True
                analysis["message"] = "High allergen levels detected."
                analysis["details"]["allergens"] = combined_data["allergens"]["message"]
            if combined_data.get("wind_speed", None) is not None and combined_data.get("wind_speed", 0) > 50:
                analysis["alert"] = True
                analysis["message"] = "High wind speed detected."
                analysis["details"]["wind_speed"] = f"Wind Speed: {combined_data['wind_speed']} km/h, Direction: {combined_data.get('wind_direction')}"
            if combined_data.get("solar_radiation", None) is not None and combined_data.get("solar_radiation", 0) > 1000:
                analysis["alert"] = True
                analysis["message"] = "High solar radiation detected."
                analysis["details"]["solar_radiation"] = f"Solar Radiation: {combined_data['solar_radiation']} W/m²"

            if weather_api_key:
                try:
                    external_weather = get_external_weather(location_str, weather_api_key)
                    analysis["details"]["external_weather"] = external_weather
                except Exception as e:
                    logging.error(f"Error fetching external weather data: {e}")
                    analysis["details"]["external_weather_error"] = str(e)
        else:
            logging.warning(f"Location data not found for {location_str}.")
            analysis["message"] = f"Weather conditions could not be evaluated due to missing location data for {location_str}"

    except Exception as e:
        logging.error(f"Error processing weather data: {e}")
        analysis["alert"] = True
        analysis["message"] = "Error processing weather data."
        analysis["details"]["error"] = str(e)

    analysis["location"] = location
    return analysis

def get_weather_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "humidity": 70,
        "temperature": 28,
        "uv": 6,
        "air_quality": {"alert": False, "message": "Good"},
        "allergens": {"alert": False, "message": "Low"},
        "precipitation": 5,
        "precipitation_type": "Rain",
        "water_level": None,
        "storm_alert": None,
        "wind_speed": 20,
        "wind_direction": "North",
        "solar_radiation": 800,
    }

def get_weather_api_data(location):
    # Replace with real API call
    return {
        "humidity": 72,
        "temperature": 29,
        "uv": 7,
        "air_quality": {"alert": False, "message": "Good"},
        "allergens": {"alert": False, "message": "Low"},
        "precipitation": 6,
        "precipitation_type": "Rain",
        "wind_speed": 22,
        "wind_direction": "North",
        "solar_radiation": 820,
    }

def get_external_weather(location, api_key):
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
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
