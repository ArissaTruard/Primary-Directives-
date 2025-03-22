# sub_environmental.py
"""
This module simulates an environment by gathering data from various sensors and APIs.
It provides methods to retrieve environmental data, which can then be analyzed for
risks, habitat suitability, and predicted changes.
"""

import logging
import datetime

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

class Environment:
    """Simulates an environment by gathering data from various sensors and APIs."""

    def __init__(self, location_input, weather_api_key=None, soil_api_key=None, vegetation_api_key=None, water_api_key=None, fauna_api_key=None, light_api_key=None, noise_api_key=None, pollen_api_key=None, radiation_api_key=None, radon_api_key=None):
        """Initializes the environment with location and API keys."""
        self.location_input = location_input
        self.weather_api_key = weather_api_key
        self.soil_api_key = soil_api_key
        self.vegetation_api_key = vegetation_api_key
        self.water_api_key = water_api_key
        self.fauna_api_key = fauna_api_key
        self.light_api_key = light_api_key
        self.noise_api_key = noise_api_key
        self.pollen_api_key = pollen_api_key
        self.radiation_api_key = radiation_api_key
        self.radon_api_key = radon_api_key

    def get_air_quality(self):
        """Retrieves air quality data."""
        return monitor_air_quality(self.location_input, self.weather_api_key)

    def get_soil_quality(self):
        """Retrieves soil quality data."""
        return monitor_soil_quality(self.location_input, self.soil_api_key)

    def get_vegetation_data(self):
        """Retrieves vegetation data."""
        return monitor_vegetation(self.location_input, self.vegetation_api_key)

    def get_water_quality(self):
        """Retrieves water quality data."""
        return monitor_water_quality(self.location_input, self.water_api_key)

    def get_weather_data(self):
        """Retrieves weather data."""
        return monitor_weather(self.location_input, self.weather_api_key)

    def get_fauna_data(self):
        """Retrieves fauna data."""
        return monitor_fauna(self.location_input, self.fauna_api_key)

    def get_light_data(self):
        """Retrieves light data."""
        return monitor_light_levels(self.location_input, self.light_api_key)

    def get_noise_data(self):
        """Retrieves noise data."""
        return monitor_noise_levels(self.location_input, self.noise_api_key)

    def get_pollen_data(self):
        """Retrieves pollen data."""
        return monitor_pollen_levels(self.location_input, self.pollen_api_key)

    def get_radiation_data(self):
        """Retrieves radiation data."""
        return monitor_radiation_levels(self.location_input, self.radiation_api_key)

    def get_radon_data(self):
        """Retrieves radon data."""
        return monitor_radon_levels(self.location_input, self.radon_api_key)

    def get_seismic_data(self):
        """Retrieves seismic data."""
        return monitor_seismic_activity(self.location_input)

# Example Usage
if __name__ == "__main__":
    env = Environment(location_input="London", weather_api_key="YOUR_WEATHER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY", noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY", radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY") #add api keys as needed.
    print(f"Air Quality: {env.get_air_quality()}")
    print(f"Soil Quality: {env.get_soil_quality()}")
    print(f"Vegetation Data: {env.get_vegetation_data()}")
    print(f"Water Quality: {env.get_water_quality()}")
    print(f"Weather Data: {env.get_weather_data()}")
    print(f"Fauna Data: {env.get_fauna_data()}")
    print(f"Light Data: {env.get_light_data()}")
    print(f"Noise Data: {env.get_noise_data()}")
    print(f"Pollen Data: {env.get_pollen_data()}")
    print(f"Radiation Data: {env.get_radiation_data()}")
    print(f"Radon Data: {env.get_radon_data()}")
    print(f"Seismic Data: {env.get_seismic_data()}")
