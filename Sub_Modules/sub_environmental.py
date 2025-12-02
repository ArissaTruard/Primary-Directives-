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
from uv_radiation_monitor import monitor_uv_radiation
from voc_monitor import monitor_voc
from particulate_matter_monitor import monitor_particulate_matter
from wildfire_smoke_monitor import monitor_wildfire_smoke

# Geological Monitoring Modules
from radiation_alerts import monitor_radiation_levels
from radon_monitor import monitor_radon_levels
from seismic_monitor import monitor_seismic_activity
from asbestos_monitor import monitor_asbestos
from volcanic_activity_monitor import monitor_volcanic_activity

# Land and Water Monitoring Modules
from deforestation_monitor import monitor_deforestation
from industrial_pollution_monitor import monitor_industrial_pollution
from soil_quality_monitor import monitor_soil_quality
from urban_sprawl_monitor import monitor_urban_sprawl
from vegetation_monitor import monitor_vegetation
from water_quality_monitor import monitor_water_quality
from erosion_monitor import monitor_erosion
from invasive_species_monitor import monitor_invasive_species
from ground_water_monitor import monitor_ground_water
from land_subsidence_monitor import monitor_land_subsidence
from wetland_health_monitor import monitor_wetland_health
from heavy_metal_monitor import monitor_heavy_metal
from pesticide_monitor import monitor_pesticide
from microbial_monitor import monitor_microbial
from algal_bloom_monitor import monitor_algal_bloom

# Biological Monitoring Modules
from fauna_monitor import monitor_fauna
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels
from biodiversity_monitor import monitor_biodiversity
from ocean_health_monitor import monitor_ocean_health
from ecosystem_services_monitor import monitor_ecosystem_services
from species_migration_monitor import monitor_species_migration
from allergen_monitor import monitor_allergen
from vector_disease_monitor import monitor_vector_disease

# Resource Monitoring Modules
from resource_monitor import monitor_specific_resources
from renewable_energy_monitor import monitor_renewable_energy
from mineral_resource_monitor import monitor_mineral_resources

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
from demographic_trends_monitor import monitor_demographic_trends
from healthcare_access_monitor import monitor_healthcare_access
from employment_rates_monitor import monitor_employment_rates
from housing_market_monitor import monitor_housing_market
from social_mobility_monitor import monitor_social_mobility
from arts_culture_monitor import monitor_arts_culture
from civic_engagement_monitor import monitor_civic_engagement

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
                 cultural_factors_api_key=None, technology_access_api_key=None,
                 ground_water_api_key=None, land_subsidence_api_key=None, wetland_health_api_key=None,
                 ecosystem_services_api_key=None, species_migration_api_key=None,
                 renewable_energy_api_key=None, mineral_resource_api_key=None,
                 demographic_trends_api_key=None, healthcare_access_api_key=None,
                 employment_rates_api_key=None, housing_market_api_key=None,
                 social_mobility_api_key=None, arts_culture_api_key=None, civic_engagement_api_key=None,
                 uv_radiation_api_key=None, voc_api_key=None, particulate_matter_api_key=None,
                 wildfire_smoke_api_key=None, asbestos_api_key=None, volcanic_activity_api_key=None,
                 heavy_metal_api_key=None, pesticide_api_key=None, microbial_api_key=None,
                 algal_bloom_api_key=None, allergen_api_key=None, vector_disease_api_key=None):
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
        self.ground_water_api_key = ground_water_api_key
        self.land_subsidence_api_key = land_subsidence_api_key
        self.wetland_health_api_key = wetland_health_api_key
        self.ecosystem_services_api_key = ecosystem_services_api_key
        self.species_migration_api_key = species_migration_api_key
        self.renewable_energy_api_key = renewable_energy_api_key
        self.mineral_resource_api_key = mineral_resource_api_key
        self.demographic_trends_api_key = demographic_trends_api_key
        self.healthcare_access_api_key = healthcare_access_api_key
        self.employment_rates_api_key = employment_rates_api_key
        self.housing_market_api_key = housing_market_api_key
        self.social_mobility_api_key = social_mobility_api_key
        self.arts_culture_api_key = arts_culture_api_key
        self.civic_engagement_api_key = civic_engagement_api_key
        self.uv_radiation_api_key = uv_radiation_api_key
        self.voc_api_key = voc_api_key
        self.particulate_matter_api_key = particulate_matter_api_key
        self.wildfire_smoke_api_key = wildfire_smoke_api_key
        self.asbestos_api_key = asbestos_api_key
        self.volcanic_activity_api_key = volcanic_activity_api_key
        self.heavy_metal_api_key = heavy_metal_api_key
        self.pesticide_api_key = pesticide_api_key
        self.microbial_api_key = microbial_api_key
        self.algal_bloom_api_key = algal_bloom_api_key
        self.allergen_api_key = allergen_api_key
        self.vector_disease_api_key = vector_disease_api_key

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
            'ground_water': monitor_ground_water(self.location_input, self.ground_water_api_key),
            'land_subsidence': monitor_land_subsidence(self.location_input, self.land_subsidence_api_key),
            'wetland_health': monitor_wetland_health(self.location_input, self.wetland_health_api_key),
            'ecosystem_services': monitor_ecosystem_services(self.location_input, self.ecosystem_services_api_key),
            'species_migration': monitor_species_migration(self.location_input, self.species_migration_api_key),
            'renewable_energy': monitor_renewable_energy(self.location_input, self.renewable_energy_api_key),
            'mineral_resources': monitor_mineral_resources(self.location_input, self.mineral_resource_api_key),
            'uv_radiation': monitor_uv_radiation(self.location_input, self.uv_radiation_api_key),
            'voc': monitor_voc(self.location_input, self.voc_api_key),
            'particulate_matter': monitor_particulate_matter(self.location_input, self.particulate_matter_api_key),
            'wildfire_smoke': monitor_wildfire_smoke(self.location_input, self.wildfire_smoke_api_key),
            'asbestos': monitor_asbestos(self.location_input, self.asbestos_api_key),
            'volcanic_activity': monitor_volcanic_activity(self.location_input, self.volcanic_activity_api_key),
            'heavy_metal': monitor_heavy_metal(self.location_input, self.heavy_metal_api_key),
            'pesticide': monitor_pesticide(self.location_input, self.pesticide_api_key),
            'microbial': monitor_microbial(self.location_input, self.microbial_api_key),
            'algal_bloom': monitor_algal_bloom(self.location_input, self.algal_bloom_api_key),
            'allergen': monitor_allergen(self.location_input, self.allergen_api_key),
            'vector_disease': monitor_vector_disease(self.location_input, self.vector_disease_api_key)
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
            'demographic_trends': monitor_demographic_trends(self.location_input, self.demographic_trends_api_key),
            'healthcare_access': monitor_healthcare_access(self.location_input, self.healthcare_access_api_key),
            'employment_rates': monitor_employment_rates(self.location_input, self.employment_rates_api_key),
            'housing_market': monitor_housing_market(self.location_input, self.housing_market_api_key),
            'social_mobility': monitor_social_mobility(self.location_input, self.social_mobility_api_key),
            'arts_culture': monitor_arts_culture(self.location_input, self.arts_culture_api_key),
            'civic_engagement': monitor_civic_engagement(self.location_input, self.civic_engagement_api_key)
        }
        return socio_data

    def get_all_data(self):
        """Consolidates all environmental and socioeconomic data."""
        all_data = {
            'environmental': self.get_environmental_data(),
            'socioeconomic': self.get_socioeconomic_data(),
        }
        return all_data
