# environmental_communication.py
"""
This module monitors environmental data from various sensors, detects sudden changes,
reports them to relevant agencies, and provides enhanced analysis and predictions.

Dependencies:
    - air_quality_monitor.py
    - soil_quality_monitor.py
    - vegetation_monitor.py
    - water_quality_monitor.py
    - weather.py
    - fauna_monitor.py
    - light_monitor.py
    - noise_monitor.py
    - pollen_monitor.py
    - radiation_alerts.py
    - radon_monitor.py
    - sub_environmental.py
    - sub_environmental_analysis.py
    - requests (for simulating agency communication)
"""

import logging
import datetime
import requests
from sub_environmental import Environment  # Import Environment class
from sub_environmental_analysis import analyze_environmental_risks, assess_habitat_suitability, predict_environmental_changes, generate_environmental_report

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Simulated agency endpoints (replace with real agency APIs)
AGENCY_ENDPOINTS = {
    "air_quality": "https://simulated-agency.com/air",
    "soil_quality": "https://simulated-agency.com/soil",
    "water_quality": "https://simulated-agency.com/water",
    "weather": "https://simulated-agency.com/weather",
    "fauna": "https://simulated-agency.com/fauna",
    "light": "https://simulated-agency.com/light",
    "noise": "https://simulated-agency.com/noise",
    "pollen": "https://simulated-agency.com/pollen",
    "radiation": "https://simulated-agency.com/radiation",
    "radon": "https://simulated-agency.com/radon",
    "environmental_report": "https://simulated-agency.com/report" #Added for report generation
}

# Thresholds for sudden changes (adjust as needed)
CHANGE_THRESHOLDS = {
    "air_quality": {"pm25": 50, "pm10": 100, "vocs": 100},
    "soil_quality": {"ph": 1, "nitrogen": 50, "phosphorus": 30, "potassium": 100},
    "water_quality": {"ph": 1, "turbidity": 3, "dissolved_oxygen": 2, "conductivity": 500},
    "weather": {"temperature": 5, "humidity": 10, "precipitation": 10, "wind_speed": 10, "uv": 2},
    "fauna": {"species_diversity": 3},
    "light": {"illuminance": 100, "uv_index": 3},
    "noise": {"decibels": 10},
    "pollen": {"pollen_count": 200},
    "radiation": {"radiation_level": 20},
    "radon": {"radon_level": 1}
}

# Store previous sensor readings to detect changes
previous_readings = {}

def send_data_to_agency(agency, data):
    """
    Simulates sending data to a relevant agency.

    Args:
        agency (str): The agency identifier (e.g., "air_quality").
        data (dict): The data to send to the agency.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
    """
    try:
        response = requests.post(AGENCY_ENDPOINTS[agency], json=data)
        response.raise_for_status()
        logging.info(f"Data sent to {agency} agency: {data}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send data to {agency} agency: {e}")

def monitor_and_report(location_input, weather_api_key=None, soil_api_key=None, vegetation_api_key=None, water_api_key=None, fauna_api_key=None, light_api_key=None, noise_api_key=None, pollen_api_key=None, radiation_api_key=None, radon_api_key=None):
    """
    Monitors environmental data, detects sudden changes, reports to agencies, and generates reports.

    Args:
        location_input (str): The location for which to monitor environmental data.
        weather_api_key (str, optional): API key for weather data. Defaults to None.
        soil_api_key (str, optional): API key for soil data. Defaults to None.
        vegetation_api_key (str, optional): API key for vegetation data. Defaults to None.
        water_api_key (str, optional): API key for water data. Defaults to None.
        fauna_api_key (str, optional): API key for fauna data. Defaults to None.
        light_api_key (str, optional): API key for light data. Defaults to None.
        noise_api_key (str, optional): API key for noise data. Defaults to None.
        pollen_api_key (str, optional): API key for pollen data. Defaults to None.
        radiation_api_key (str, optional): API key for radiation data. Defaults to None.
        radon_api_key (str, optional): API key for radon data. Defaults to None.
    """

    # Create Environment object
    env = Environment(location_input=location_input, weather_api_key=weather_api_key, soil_api_key=soil_api_key, vegetation_api_key=vegetation_api_key, water_api_key=water_api_key, fauna_api_key=fauna_api_key, light_api_key=light_api_key, noise_api_key=noise_api_key, pollen_api_key=pollen_api_key, radiation_api_key=radiation_api_key, radon_api_key=radon_api_key)

    # Get current sensor data
    air_data = env.get_air_quality_data()
    soil_data = env.get_soil_quality_data()
    vegetation_data = env.get_vegetation_data()
    water_data = env.get_water_quality_data()
    weather_data = env.get_weather_data()
    fauna_data = env.get_fauna_data()
    light_data = env.get_light_level()
    noise_data = env.get_noise_data()
    pollen_data = env.get_pollen_data()
    radiation_data = env.get_radiation_data()
    radon_data = env.get_radon_data()

    all_data = {
        "air_quality": air_data,
        "soil_quality": soil_data,
        "water_quality": water_data,
        "weather": weather_data,
        "fauna": fauna_data,
        "light": light_data,
        "noise": noise_data,
        "pollen": pollen_data,
        "radiation": radiation_data,
        "radon": radon_data,
    }

    # Detect and report sudden changes
    for sensor, data in all_data.items():
        if data and data.get("details"):
            current_readings = data["details"]
            if sensor in previous_readings:
                for param, value in current_readings.items():
                    if param in CHANGE_THRESHOLDS[sensor] and isinstance(value, (int, float)):
                        if abs(value - previous_readings[sensor].get(param, 0)) > CHANGE_THRESHOLDS[sensor][param]:
                            logging.warning(f"Sudden change detected in {sensor}: {param} = {value}")
                            send_data_to_agency(sensor, {"location": location_input, "param": param, "value": value})
            previous_readings[sensor] = current_readings

    # Forward sensor data to agencies
    for sensor, data in all_data.items():
        if data and data.get("details"):
            send_data_to_agency(sensor, {"location": location_input, "data": data["details"]})

    # Generate and send environmental report
    report = generate_environmental_report(env)
    send_data_to_agency("environmental_report", {"location": location_input, "report": report})

# Example usage
if __name__ == "__main__":
    location = "London"
    monitor_and_report(location, weather_api_key="YOUR_WEATHER_API_KEY", soil_api_key="YOUR_SOIL_API_KEY", vegetation_api_key="YOUR_VEGETATION_API_KEY",
        water_api_key="YOUR_WATER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY",
        noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY",
        radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY")

