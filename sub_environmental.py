# --- sub_environmental.py ---
import logging
import datetime
import json
from .weather import monitor_weather
from .water_quality_monitor import monitor_water_quality
from .soil_quality_monitor import monitor_soil_quality
from .noise_monitor import monitor_noise_levels
from .seismic_monitor import monitor_seismic_activity

def monitor_environment(location, weather_data=None, water_data=None, soil_data=None, noise_level=None, seismic_data=None):
    """
    Monitors and analyzes environmental data, integrating various sensors.

    Args:
        location (str): Location of the environmental measurement.
        weather_data (dict, optional): Weather related data (humidity, temperature, uv, air quality, allergens).
        water_data (dict, optional): Water quality data.
        soil_data (dict, optional): Soil quality data.
        noise_level (float, optional): Noise level in dB.
        seismic_data (float, optional): Ground movement data.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    timestamp = datetime.datetime.now()
    logging.info(f"Environmental monitoring at {location} - {timestamp}")

    analysis_results = {}

    if weather_data:
        weather_results = monitor_weather(weather_data.get('humidity'), weather_data.get('temperature'), weather_data.get('uv'), weather_data.get('air_quality'), weather_data.get('allergens'), location)
        analysis_results['weather'] = weather_results

    if water_data:
        water_results = monitor_water_quality(water_data.get('ph'), water_data.get('turbidity'),
                                              water_data.get('dissolved_oxygen'), water_data.get('heavy_metals'),
                                              water_data.get('pollutants'), location)
        analysis_results['water_quality'] = water_results

    if soil_data:
        soil_results = monitor_soil_quality(soil_data.get('ph'), soil_data.get('moisture'),
                                            soil_data.get('nutrients'), soil_data.get('heavy_metals'),
                                            soil_data.get('pesticides'), location)
        analysis_results['soil_quality'] = soil_results

    if noise_level is not None:
        noise_results = monitor_noise_levels(noise_level, location)
        analysis_results['noise_level'] = noise_results

    if seismic_data is not None:
        seismic_results = monitor_seismic_activity(seismic_data, location)
        analysis_results['seismic_activity'] = seismic_results

    return analysis_results
