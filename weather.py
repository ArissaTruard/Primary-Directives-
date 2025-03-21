# --- weather.py ---
import logging
import datetime
import requests
import json
from .sub_location import get_location_data  # Assuming sub_location.py exists

def monitor_weather(humidity, temperature, uv, air_quality, allergens, sensor_location, weather_api_key=None, precipitation=None, precipitation_type=None, water_level=None, storm_alert=None):
    """
    Monitors and analyzes weather-related data, integrating external weather API if available,
    and adjusts thresholds based on sensor location.

    Args:
        humidity (float, optional): Humidity level (percentage).
        temperature (float, optional): Temperature in Celsius.
        uv (float, optional): UV index.
        air_quality (dict, optional): Air quality data dictionary from air_quality_monitor.
        allergens (dict, optional): Allergen data dictionary.
        sensor_location (str): Location of the weather sensor.
        weather_api_key (str, optional): API key for external weather service.
        precipitation (float, optional): Precipitation amount (e.g., mm/hr).
        precipitation_type (str, optional): Type of precipitation (e.g., rain, snow, hail).
        water_level (str, optional): Water level (e.g., normal, high, flood).
        storm_alert (str, optional): Storm alert message.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    timestamp = datetime.datetime.now()
    logging.info(f"Weather data at {sensor_location}: Humidity={humidity}, Temperature={temperature}, UV={uv}, Air Quality={air_quality}, Allergens={allergens}, Precipitation={precipitation}, Precipitation Type={precipitation_type}, Water Level={water_level}, Storm Alert={storm_alert}")
    analysis = {
        "alert": False,
        "message": "Weather conditions normal",
        "details": {}
    }

    try:
        location_data = get_location_data(sensor_location)  # Get location-specific data
        if location_data:
            optimal_humidity = location_data.get("optimal_humidity", 60)  # Default optimal humidity
            max_temperature = location_data.get("max_temperature", 30)  # Default max temperature
            max_uv = location_data.get("max_uv", 8)  # Default max UV index
            max_precipitation = location_data.get("max_precipitation", 15) #Default max precipitation.

            # Adjust thresholds based on location-specific optimal conditions
            if humidity is not None and humidity > optimal_humidity + 20:  # Example adjustment
                analysis["alert"] = True
                analysis["message"] = "High humidity detected."
                analysis["details"]["humidity"] = f"Humidity: {humidity}%"

            if temperature is not None and temperature > max_temperature + 5: #Example adjustment
                analysis["alert"] = True
                analysis["message"] = "High temperature detected."
                analysis["details"]["temperature"] = f"Temperature: {temperature}°C"

            if uv is not None and uv > max_uv + 2: #Example adjustment
                analysis["alert"] = True
                analysis["message"] = "High UV index detected."
                analysis["details"]["uv"] = f"UV Index: {uv}"

            if precipitation is not None and precipitation > max_precipitation:
                analysis["alert"] = True
                analysis["message"] = f"Heavy precipitation detected: {precipitation} mm/hr"
                analysis["details"]["precipitation"] = f"Precipitation: {precipitation} mm/hr, Type: {precipitation_type}"

            if water_level and water_level == "flood":
                analysis["alert"] = True
                analysis["message"] = "Flood conditions detected."
                analysis["details"]["water_level"] = "Flood conditions"

            if storm_alert:
                analysis["alert"] = True
                analysis["message"] = f"Storm alert: {storm_alert}"
                analysis["details"]["storm_alert"] = storm_alert

            if air_quality and air_quality.get('alert'):
                analysis["alert"] = True
                analysis["message"] = "Adverse air quality detected."
                analysis["details"]["air_quality"] = air_quality["message"]

            if allergens and allergens.get('alert'):
                analysis["alert"] = True
                analysis["message"] = "High allergen levels detected."
                analysis["details"]["allergens"] = allergens["message"]

            # Integrate external weather API if available
            if weather_api_key:
                try:
                    external_weather = get_external_weather(sensor_location, weather_api_key)
                    analysis["details"]["external_weather"] = external_weather
                    # Add logic to compare internal and external data.
                    # And modify the alert and message if there is a discrepancy.
                except Exception as e:
                    logging.error(f"Error fetching external weather data: {e}")
                    analysis["details"]["external_weather_error"] = str(e)
        else:
            logging.warning(f"Location data not found for {sensor_location}.")
            analysis["message"] = f"Weather conditions could not be evaluated due to missing location data for {sensor_location}"

    except Exception as e:
        logging.error(f"Error processing weather data: {e}")
        analysis["alert"] = True
        analysis["message"] = "Error processing weather data."
        analysis["details"]["error"] = str(e)

    return analysis

def get_external_weather(location, api_key):
    """
    Retrieves weather data from an external API.

    Args:
        location (str): Location for weather data.
        api_key (str): API key for the weather service.

    Returns:
        dict: Weather data from the API.
    """
    url = f"https://api.exampleweather.com/weather?q={location}&appid={api_key}" #Replace with real url.
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        weather_data = response.json()
        return weather_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from weather API")
        return {"error": "Invalid JSON response"}
