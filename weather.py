# --- weather.py ---
import logging
import datetime
import requests
import json

def monitor_weather(humidity, temperature, uv, air_quality, allergens, location, weather_api_key=None, precipitation=None, precipitation_type=None, water_level=None, storm_alert=None):
    """
    Monitors and analyzes weather-related data, integrating external weather API if available.

    Args:
        humidity (float, optional): Humidity level (percentage).
        temperature (float, optional): Temperature in Celsius.
        uv (float, optional): UV index.
        air_quality (dict, optional): Air quality data dictionary from air_quality_monitor.
        allergens (dict, optional): Allergen data dictionary.
        location (str): Location for weather monitoring.
        weather_api_key (str, optional): API key for external weather service.
        precipitation (float, optional): Precipitation amount (e.g., mm/hr).
        precipitation_type (str, optional): Type of precipitation (e.g., rain, snow, hail).
        water_level (str, optional): Water level (e.g., normal, high, flood).
        storm_alert (str, optional): Storm alert message.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    timestamp = datetime.datetime.now()
    logging.info(f"Weather data at {location}: Humidity={humidity}, Temperature={temperature}, UV={uv}, Air Quality={air_quality}, Allergens={allergens}, Precipitation={precipitation}, Precipitation Type={precipitation_type}, Water Level={water_level}, Storm Alert={storm_alert}")
    analysis = {"alert": False, "message": "Weather conditions normal", "details": {}}

    # Basic threshold checks
    if humidity is not None and humidity > 80:
        analysis["alert"] = True
        analysis["message"] = "High humidity detected."
        analysis["details"]["humidity"] = f"Humidity: {humidity}%"

    if temperature is not None and temperature > 35:
        analysis["alert"] = True
        analysis["message"] = "High temperature detected."
        analysis["details"]["temperature"] = f"Temperature: {temperature}°C"

    if uv is not None and uv > 10:
        analysis["alert"] = True
        analysis["message"] = "High UV index detected."
        analysis["details"]["uv"] = f"UV Index: {uv}"

    if air_quality and air_quality.get('alert'):
        analysis["alert"] = True
        analysis["message"] = "Adverse air quality detected."
        analysis["details"]["air_quality"] = air_quality["message"]

    if allergens and allergens.get('alert'):
        analysis["alert"] = True
        analysis["message"] = "High allergen levels detected."
        analysis["details"]["allergens"] = allergens["message"]

    if precipitation is not None and precipitation > 10: #example threshold
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

    # Integrate external weather API if available
    if weather_api_key:
        try:
            external_weather = get_external_weather(location, weather_api_key)
            analysis["details"]["external_weather"] = external_weather
            # Add logic to compare internal and external data.
            # And modify the alert and message if there is a discrepancy.
        except Exception as e:
            logging.error(f"Error fetching external weather data: {e}")
            analysis["details"]["external_weather_error"] = str(e)

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
    # Example using a placeholder API endpoint (replace with your actual API)
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
