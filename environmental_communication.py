# environmental_communication.py
"""
This module monitors environmental data, detects sudden changes (spikes and drops),
reports them to relevant agencies, and generates comprehensive environmental reports.
It integrates data from various environmental sensors and external APIs, simulating
agency communication via HTTP. Environmental data is analyzed for risks, habitat
suitability, and predicted changes.

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
    - seismic_monitor.py
    - requests: For simulating HTTP requests to agency APIs.
"""

import logging
import datetime
import requests
import json

# Import monitor functions directly
from weather import monitor_weather
from fauna_monitor import monitor_fauna
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels
from pollen_monitor import monitor_pollen_levels
from radiation_alerts import monitor_radiation_levels
from radon_monitor import monitor_radon_levels
from air_quality_monitor import monitor_air_quality
from soil_quality_monitor import monitor_soil_quality
from vegetation_monitor import monitor_vegetation
from water_quality_monitor import monitor_water_quality
from seismic_monitor import monitor_seismic_activity

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
    "seismic": "https://simulated-agency.com/seismic",
    "environmental_report": "https://simulated-agency.com/report"
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
    "radon": {"radon_level": 1},
    "seismic": {"ground_movement": 5, "richter_scale": 4}
}

# Store previous sensor readings to detect changes
previous_readings = {}

def send_data_to_agency(agency, data):
    """Simulates sending data to a relevant agency via HTTP POST request."""
    try:
        response = requests.post(AGENCY_ENDPOINTS[agency], json=data)
        response.raise_for_status()
        logging.info(f"Data sent to {agency} agency: {data}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send data to {agency} agency: {e}")

def analyze_environmental_risks(all_data):
    """Analyzes environmental data and identifies potential risks."""
    risks = {}
    if all_data.get('weather') and all_data['weather'].get('details') and all_data['weather']['details'].get('air_quality') and all_data['weather']['details']['air_quality'].get('details') and all_data['weather']['details']['air_quality']['details'].get('pm25') and all_data['weather']['details']['air_quality']['details']['pm25'] > 80:
        risks['high_air_pollution'] = 'High'
    if all_data.get('fauna') and all_data['fauna'].get('details') and all_data['fauna']['details'].get('species_diversity', 0) < 5:
        risks['low_species_diversity'] = 'High'
    if all_data.get('light') and all_data['light'].get('details') and all_data['light']['details'].get('uv_index', 0) > 10:
        risks['high_uv_index'] = 'High'
    if all_data.get('noise') and all_data['noise'].get('details') and all_data['noise']['details'].get('decibels', 0) > 85:
        risks['high_noise_levels'] = 'High'
    if all_data.get('pollen') and all_data['pollen'].get('details') and all_data['pollen']['details'].get('pollen_count', 0) > 500:
        risks['high_pollen_levels'] = 'High'
    if all_data.get('radiation') and all_data['radiation'].get('details') and all_data['radiation']['details'].get('radiation_level', 0) > 100:
        risks['high_radiation_levels'] = 'High'
    if all_data.get('radon') and all_data['radon'].get('details') and all_data['radon']['details'].get('radon_level', 0) > 4:
        risks['high_radon_levels'] = 'High'
    return risks

def assess_habitat_suitability(all_data):
    """Assesses habitat suitability based on environmental data."""
    suitability = "Moderate"
    if all_data.get('weather') and all_data['weather'].get('details') and all_data['weather']['details'].get('temperature'):
        temp = all_data['weather']['details']['temperature']
        if temp < 10 or temp > 35:
            suitability = "Unsuitable"
    return suitability

def predict_environmental_changes(all_data):
    """Predicts future environmental changes based on data."""
    predictions = {}
    if all_data.get('weather') and all_data['weather'].get('details') and all_data['weather']['details'].get('temperature'):
        temp = all_data['weather']['details']['temperature']
        if temp > 25:
            predictions['temperature_increase'] = "Likely"
    return predictions

def generate_environmental_report(all_data, location_input):
    """Generates a comprehensive environmental report."""
    report = {
        'risks': analyze_environmental_risks(all_data),
        'suitability': assess_habitat_suitability(all_data),
        'predictions': predict_environmental_changes(all_data),
        'data': {
            'air_quality': all_data.get('air_quality', {}).get('details', {}),
            'soil_quality': all_data.get('soil_quality', {}).get('details', {}),
            'water_quality': all_data.get('water_quality', {}).get('details', {}),
            'weather': all_data.get('weather', {}).get('details', {}),
            'fauna': all_data.get('fauna', {}).get('details', {}),
            'light': all_data.get('light', {}).get('details', {}),
            'noise': all_data.get('noise', {}).get('details', {}),
            'pollen': all_data.get('pollen', {}).get('details', {}),
            'radiation': all_data.get('radiation', {}).get('details', {}),
            'radon': all_data.get('radon', {}).get('details', {}),
            'seismic': all_data.get('seismic', {}).get('details', {})
        }
    }
    return json.dumps(report, indent=4)

def monitor_and_report(location_input, weather_api_key=None, soil_api_key=None, vegetation_api_key=None, water_api_key=None, fauna_api_key=None, light_api_key=None, noise_api_key=None, pollen_api_key=None, radiation_api_key=None, radon_api_key=None):
    """Monitors, detects sudden changes, reports, and generates environmental reports."""

    # Get current sensor data
    air_data = monitor_air_quality(location_input, weather_api_key)
    soil_data = monitor_soil_quality(location_input, soil_api_key)
    vegetation_data = monitor_vegetation(location_input, vegetation_api_key)
    water_data = monitor_water_quality(location_input, water_api_key)
    weather_data = monitor_weather(location_input, weather_api_key)
    fauna_data = monitor_fauna(location_input, fauna_api_key)
    light_data = monitor_light_levels(location_input, light_api_key)
    noise_data = monitor_noise_levels(location_input, noise_api_key)
    pollen_data = monitor_pollen_levels(location_input, pollen_api_key)
    radiation_data = monitor_radiation_levels(location_input, radiation_api_key)
    radon_data = monitor_radon_levels(location_input, radon_api_key)
    seismic_data = monitor_seismic_activity(location_input)

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
        "seismic": seismic_data,
    }

    # Detect and report sudden changes (spikes and drops)
    for sensor, data in all_data.items():
        if data and data.get("details"):
            current_readings = data["details"]
            if sensor in previous_readings:
                for param, value in current_readings.items():
                    if param in CHANGE_THRESHOLDS[sensor] and isinstance(value, (int, float)):
                        change = value - previous_readings[sensor].get(param, 0)
                        if abs(change) > CHANGE_THRESHOLDS[sensor][param]:
                            change_type = "spike" if change > 0 else "drop"
                            severity = abs(change) / CHANGE_THRESHOLDS[sensor][param]  # Calculate severity
                            logging.warning(f"Sudden {change_type} detected in {sensor}: {param} = {value}, Change: {change}, Severity: {severity:.2f}")
                            send_data_to_agency(sensor, {"location": location_input, "param": param, "value": value, "change_type": change_type, "change_amount": change, "change_severity": severity})
            previous_readings[sensor] = current_read-readings[sensor] = current_readings

    # Forward sensor data to agencies
    for sensor, data in all_data.items():
        if data and data.get("details"):
            send_data_to_agency(sensor, {"location": location_input, "data": data["details"]})

    # Generate and send environmental report
    report = generate_environmental_report(all_data, location_input)
    send_data_to_agency("environmental_report", {"location": location_input, "report": report})

# Example usage
if __name__ == "__main__":
    location = "London"
    monitor_and_report(location, weather_api_key="YOUR_WEATHER_API_KEY", soil_api_key="YOUR_SOIL_API_KEY", vegetation_api_key="YOUR_VEGETATION_API_KEY", water_api_key="YOUR_WATER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY", noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY", radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY")
    previous_readings[sensor] = current_readings

    # Forward sensor data to agencies
    for sensor, data in all_data.items():
        if data and data.get("details"):
            send_data_to_agency(sensor, {"location": location_input, "data": data["details"]})

    # Generate and send environmental report
    report = generate_environmental_report(all_data, location_input)
    send_data_to_agency("environmental_report", {"location": location_input, "report": report})

# Example usage
if __name__ == "__main__":
    location = "London"
    monitor_and_report(location, weather_api_key="YOUR_WEATHER_API_KEY", soil_api_key="YOUR_SOIL_API_KEY", vegetation_api_key="YOUR_VEGETATION_API_KEY", water_api_key="YOUR_WATER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY", noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY", radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY")
