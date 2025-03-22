# sub_environmental.py
"""
This module provides functions for simulating and interacting with
environmental variables in a simplified context, and links to other modules.
"""

import random
from crime_module import CrimeData
from school_ratings_module import SchoolRatings
from property_value_module import PropertyValueTrends
from air_quality_monitor import monitor_air_quality
from soil_quality_monitor import monitor_soil_quality
from vegetation_monitor import monitor_vegetation
from water_quality_monitor import monitor_water_quality
from weather import monitor_weather
from fauna_monitor import monitor_fauna
from sub_location import get_location_from_address
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels
from pollen_monitor import monitor_pollen_levels
from radiation_alerts import monitor_radiation_levels
from radon_monitor import monitor_radon_levels

class Environment:
    """Represents an environment with environmental and socioeconomic factors."""

    def __init__(self, location_input=None, temperature=25.0, humidity=50.0, light_level=100.0, crime_rate=5.0, school_rating=7.0, property_trend=0.0, weather_api_key=None, soil_api_key=None, vegetation_api_key=None, water_api_key=None, fauna_api_key = None, light_api_key = None, noise_api_key = None, pollen_api_key = None, radiation_api_key = None, radon_api_key = None):
        """
        Initializes the environment with default or specified values.

        Args:
            location_input (str): Location for sensor data.
            temperature (float): Initial temperature in Celsius.
            humidity (float): Initial humidity as a percentage.
            light_level (float): Initial light level (arbitrary units).
            crime_rate (float): Initial crime rate
            school_rating (float): Initial school rating.
            property_trend (float): Initial property value trend.
            weather_api_key (str): API key for weather data.
            soil_api_key (str): API key for soil data.
            vegetation_api_key (str): API key for vegetation data.
            water_api_key (str): API key for water data.
            fauna_api_key (str): API key for fauna data.
            light_api_key (str): API key for light data.
            noise_api_key (str): API key for noise data.
            pollen_api_key (str): API key for pollen data.
            radiation_api_key (str): API key for radiation data.
            radon_api_key (str): API key for radon data.
        """
        self.location = get_location_from_address(location_input) if location_input else None
        self.temperature = temperature
        self.humidity = humidity
        self.light_level = light_level
        self.crime_data = CrimeData(crime_rate)
        self.school_ratings = SchoolRatings(school_rating)
        self.property_value_trends = PropertyValueTrends(property_trend)
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

    def get_temperature(self):
        """Returns the current temperature."""
        if self.location and self.weather_api_key:
            weather_data = monitor_weather(location_input=self.location.get('address'), weather_api_key=self.weather_api_key)
            if weather_data and weather_data.get('details') and weather_data['details'].get('temperature'):
                return weather_data['details']['temperature']
        return self.temperature

    def get_humidity(self):
        """Returns the current humidity."""
        if self.location and self.weather_api_key:
            weather_data = monitor_weather(location_input=self.location.get('address'), weather_api_key=self.weather_api_key)
            if weather_data and weather_data.get('details') and weather_data['details'].get('humidity'):
                return weather_data['details']['humidity']
        return self.humidity

    def get_light_level(self):
        """Returns the current light level."""
        if self.location and self.light_api_key:
            light_data = monitor_light_levels(location_input=self.location.get('address'), light_api_key=self.light_api_key)
            if light_data and light_data.get('details') and light_data['details'].get('illuminance'):
                return light_data['details']['illuminance']
        return self.light_level

    def get_crime_rate(self):
        """Returns the current crime rate."""
        return self.crime_data.get_crime_rate()

    def get_school_rating(self):
        """Returns the current school rating."""
        return self.school_ratings.get_rating()

    def get_property_trend(self):
        """Returns the current property value trend."""
        return self.property_value_trends.get_value_trend()

    def get_fauna_data(self):
        """Returns the current fauna data."""
        if self.location and self.fauna_api_key:
            fauna_data = monitor_fauna(location_input=self.location.get('address'), fauna_api_key=self.fauna_api_key)
            return fauna_data
        return None

    def get_noise_data(self):
        """Returns the current noise data."""
        if self.location and self.noise_api_key:
            noise_data = monitor_noise_levels(location_input=self.location.get('address'), noise_api_key=self.noise_api_key)
            return noise_data
        return None

    def get_pollen_data(self):
        """Returns the current pollen data."""
        if self.location and self.pollen_api_key:
            pollen_data = monitor_pollen_levels(location_input=self.location.get('address'), pollen_api_key=self.pollen_api_key)
            return pollen_data
        return None

    def get_radiation_data(self):
        """Returns the current radiation data."""
        if self.location and self.radiation_api_key:
            radiation_data = monitor_radiation_levels(location_input=self.location.get('address'), radiation_api_key=self.radiation_api_key)
            return radiation_data
        return None

    def get_radon_data(self):
        """Returns the current radon data."""
        if self.location and self.radon_api_key:
            radon_data = monitor_radon_levels(location_input=self.location.get('address'), radon_api_key=self.radon_api_key)
            return radon_data
        return None

    def adjust_temperature(self, delta):
        """Adjusts the temperature by a given amount."""
        self.temperature += delta
        self.temperature = round(self.temperature, 2)

    def adjust_humidity(self, delta):
        """Adjusts the humidity by a given amount."""
        self.humidity += delta
        self.humidity = round(self.humidity, 2)

    def adjust_light_level(self, delta):
        """Adjusts the light level by a given amount."""
        self.light_level += delta
        self.light_level = round(self.light_level, 2)

    def simulate_random_changes(self, temp_range=(-2, 2), humidity_range=(-5, 5), light_range=(-10, 10),
                                crime_range=(-1.0, 1.0), school_range=(-0.5, 0.5), property_range=(-0.2, 0.2)):
        """Simulates random changes in all environmental and socioeconomic factors."""
        self.adjust_temperature(random.uniform(temp_range[0], temp_range[1]))
        self.adjust_humidity(random.uniform(humidity_range[0], humidity_range[1]))
        self.adjust_light_level(random.uniform(light_range[0], light_range[1]))
        self.crime_data.simulate_crime_changes(crime_range)
        self.school_ratings.simulate_rating_changes(school_range)
        self.property_value_trends.simulate_value_trend_changes(property_range)

# Example usage (within sub_environmental.py):
if __name__ == "__main__":
    env = Environment(location_input="London", weather_api_key="YOUR_WEATHER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY", noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY", radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY")
    print(f"Initial Temperature: {env.get_temperature()}°C")
    print(f"Initial Crime Rate: {env.get_crime_rate()}")
    print(f"Initial School Rating: {env.get_school_rating()}")
    print(f"Initial Property Trend: {env.get_property_trend()}")
    print(f"Fauna Data: {env.get_fauna_data()}")
    print(f"Light Data: {env.get_light_level()}")
    print(f"Noise Data: {env.get_noise_data()}")
    print(f"Pollen Data: {env.get_pollen_data()}")
    print(f"Radiation Data: {env.get_radiation_data()}")
    print(f"Radon Data: {env.get_radon_data()}")
    env.simulate_random_changes()
    print(f"Randomized Temperature: {env.get_temperature()}°C")
    print(f"Randomized Crime Rate: {env.get_crime_rate()}")
    print(f"Randomized School Rating: {env.get_school_rating()}")
    print(f"Randomized Property Trend: {env.get_property_trend()}")
