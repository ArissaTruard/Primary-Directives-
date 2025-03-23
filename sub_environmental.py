# --- sub_environmental.py ---
"""
This module integrates real-world environmental and socioeconomic data for analysis.
It gathers data from various sensors, APIs, and local modules, then consolidates it
for use in primary directives and computerized laws.
"""

import logging
import datetime

# Atmospheric Monitoring Modules
from air_quality_monitor import monitor_air_quality
from pollen_monitor import monitor_pollen_levels
from weather import monitor_weather

# Geological Monitoring Modules
from radiation_alerts import monitor_radiation_levels
from radon_monitor import monitor_radon_levels
from seismic_monitor import monitor_seismic_activity

# Land and Water Monitoring Modules
from deforestation_monitor import monitor_deforestation
from industrial_pollution_monitor import monitor_industrial_pollution
from soil_quality_monitor import monitor_soil_quality
from urban_sprawl_monitor import monitor_urban_sprawl
from vegetation_monitor import monitor_vegetation
from water_quality_monitor import monitor_water_quality

# Biological Monitoring Modules
from fauna_monitor import monitor_fauna
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels

# Socioeconomic Data Modules
from crime_module import get_crime_data
from property_value_module import get_property_values
from RealWorldEconomicDataFetcher import get_economic_data
from school_ratings_module import get_school_ratings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Environment:
    """Gathers and consolidates environmental and socioeconomic data."""

    def __init__(self, location_input,
                 weather_api_key=None, soil_api_key=None, vegetation_api_key=None,
                 water_api_key=None, fauna_api_key=None, light_api_key=None,
                 noise_api_key=None, pollen_api_key=None, radiation_api_key=None,
                 radon_api_key=None, deforestation_api_key=None,
                 industrial_pollution_api_key=None, urban_sprawl_api_key=None):
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
        self.deforestation_api_key = deforestation_api_key
        self.industrial_pollution_api_key = industrial_pollution_api_key
        self.urban_sprawl_api_key = urban_sprawl_api_key

    def get_environmental_data(self):
        """Consolidates all environmental data."""
        env_data = {
            'air_quality': monitor_air_quality(self.location_input, self.weather_api_key),
            'soil_quality': monitor_soil_quality(self.location_input, self.soil_api_key),
            'vegetation': monitor_vegetation(self.location_input, self.vegetation_api_key),
            'water_quality': monitor_water_quality(self.location_input, self.water_api_key),
            'weather': monitor_weather(self.location_input, self.weather_api_key),
            'fauna': monitor_fauna(self.location_input, self.fauna_api_key),
            'light': monitor_light_levels(self.location_input, self.light_api_key),
            'noise': monitor_noise_levels(self.location_input, self.noise_api_key),
            'pollen': monitor_pollen_levels(self.location_input, self.pollen_api_key),
            'radiation': monitor_radiation_levels(self.location_input, self.radiation_api_key),
            'radon': monitor_radon_levels(self.location_input, self.radon_api_key),
            'seismic': monitor_seismic_activity(self.location_input),
            'deforestation': monitor_deforestation(self.location_input, self.deforestation_api_key),
            'industrial_pollution': monitor_industrial_pollution(self.location_input, self.industrial_pollution_api_key),
            'urban_sprawl': monitor_urban_sprawl(self.location_input, self.urban_sprawl_api_key),
        }
        return env_data

    def get_socioeconomic_data(self):
        """Consolidates all socioeconomic data."""
        socio_data = {
            'crime': get_crime_data(self.location_input),
            'property_values': get_property_values(self.location_input),
            'school_ratings': get_school_ratings(self.location_input),
            'economic_data': get_economic_data(self.location_input),
        }
        return socio_data

    def get_all_data(self):
        """Consolidates all environmental and socioeconomic data."""
        all_data = {
            'environmental': self.get_environmental_data(),
            'socioeconomic': self.get_socioeconomic_data(),
        }
        return all_data
