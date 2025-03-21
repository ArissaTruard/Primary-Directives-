# --- sub_environmental.py ---
import logging
import datetime
import requests
import json
from .air_quality_monitor import monitor_air_quality, get_weather_data
from .water_quality_monitor import monitor_water_quality
from .soil_quality_monitor import monitor_soil_quality
from .noise_monitor import monitor_noise_levels
from .seismic_monitor import monitor_seismic_activity

def monitor_environment(location, air_data=None, water_data=None, soil_data=None, noise_level=None, seismic_data=None, weather_api_key=None):
    """
    Monitors and analyzes environmental data, integrating various sensors.

    Args:
        location (str): Location of the environmental measurement.
        air_data (dict, optional): Air quality data.
        water_data (dict, optional): Water quality data.
        soil_data (dict, optional): Soil quality data.
        noise_level (float, optional): Noise level in dB.
        seismic_data (float, optional): Ground movement data.
        weather_api_key (str, optional): API key for weather data.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    timestamp = datetime.datetime.now()
    logging.info(f"Environmental monitoring at {location} - {timestamp}")

    analysis_results = {}

    if air_data:
        air_results = monitor_air_quality(air_data.get('pm25'), air_data.get('pm10'), air_data.get('vocs'),
                                          air_data.get('o3'), air_data.get('no2'), air_data.get('so2'),
                                          air_data.get('co'), location, weather_api_key)
        analysis_results['air_quality'] = air_results

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
