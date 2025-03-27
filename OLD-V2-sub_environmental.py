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
from erosion_monitor import monitor_erosion
from invasive_species_monitor import monitor_invasive_species

# Biological Monitoring Modules
from fauna_monitor import monitor_fauna
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels
from biodiversity_monitor import monitor_biodiversity
from ocean_health_monitor import monitor_ocean_health

# Resource Monitoring Modules
from resource_monitor import monitor_specific_resources

# Socioeconomic Data Modules
from crime_module import get_crime_data
from property_value_module import get_property_values
from RealWorldEconomicDataFetcher import get_economic_data
from school_ratings_module import get_school_ratings
from public_health_monitor import monitor_public_health
from education_levels_monitor import monitor_education_levels
from infrastructure_quality_monitor import monitor_infrastructure_quality
from food_security_monitor import monitor_food_security
from social_inequality_monitor import monitor_social_inequality
from political_stability_monitor import monitor_political_stability
from cultural_factors_monitor import monitor_cultural_factors
from technology_access_monitor import monitor_technology_access

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Environment:
    """Gathers and consolidates environmental and socioeconomic data."""

    def __init__(self, location_input,
                 weather_api_key=None, soil_api_key=None, vegetation_api_key=None,
                 water_api_key=None, fauna_api_key=None, light_api_key=None,
                 noise_api_key=None, pollen_api_key=None, radiation_api_key=None,
                 radon_api_key=None, deforestation_api_key=None,
                 industrial_pollution_api_key=None, urban_sprawl_api_key=None,
                 erosion_api_key=None, invasive_species_api_key=None, biodiversity_api_key=None,
                 ocean_health_api_key=None, resource_api_key=None, public_health_api_key=None,
                 education_api_key=None, infrastructure_api_key=None, food_security_api_key=None,
                 social_inequality_api_key=None, political_stability_api_key=None,
                 cultural_factors_api_key=None, technology_access_api_key=None):
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
        self.erosion_api_key = erosion_api_key
        self.invasive_species_api_key = invasive_species_api_key
        self.biodiversity_api_key = biodiversity_api_key
        self.ocean_health_api_key = ocean_health_api_key
        self.resource_api_key = resource_api_key
        self.public_health_api_key = public_health_api_key
        self.education_api_key = education_api_key
        self.infrastructure_api_key = infrastructure_api_key
        self.food_security_api_key = food_security_api_key
        self.social_inequality_api_key = social_inequality_api_key
        self.political_stability_api_key = political_stability_api_key
        self.cultural_factors_api_key = cultural_factors_api_key
        self.technology_access_api_key = technology_access_api_key

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
            'erosion': monitor_erosion(self.location_input, self.erosion_api_key),
            'invasive_species': monitor_invasive_species(self.location_input, self.invasive_species_api_key),
            'biodiversity': monitor_biodiversity(self.location_input, self.biodiversity_api_key),
            'ocean_health': monitor_ocean_health(self.location_input, self.ocean_health_api_key),
            'specific_resources': monitor_specific_resources(self.location_input, self.resource_api_key),
        }
        return env_data

    def get_socioeconomic_data(self):
        """Consolidates all socioeconomic data."""
        socio_data = {
            'crime': get_crime_data(self.location_input),
            'property_values': get_property_values(self.location_input),
            'school_ratings': get_school_ratings(self.location_input),
            'economic_data': get_economic_data(self.location_input),
            'public_health': monitor_public_health(self.location_input, self.public_health_api_key),
            'education_levels': monitor_education_levels(self.location_input, self.education_api_key),
            'infrastructure_quality': monitor_infrastructure_quality(self.location_input, self.infrastructure_api_key),
            'food_security': monitor_food_security(self.location_input, self.food_security_api_key),
            'social_inequality': monitor_social_inequality(self.location_input, self.social_inequality_api_key),
            'political_stability': monitor_political_stability(self.location_input, self.political_stability_api_key),
            'cultural_factors': monitor_cultural_factors(self.location_input, self.cultural_factors_api_key),
            'technology_access': monitor_technology_access(self.location_input, self.technology_access_api_key),
        }
        return socio_data

    def get_all_data(self):
        """Consolidates all environmental and socioeconomic data."""
        all_data = {
            'environmental': self.get_environmental_data(),
            'socioeconomic': self.get_socioeconomic_data(),
        }
        return all_data
