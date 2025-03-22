# sub_environmental.py
"""
This module provides functions for simulating and interacting with
environmental variables in a simplified context, and links to other modules.
"""

import random
from crime_module import CrimeData
from school_ratings_module import SchoolRatings
from property_value_module import PropertyValueTrends

class Environment:
    """Represents an environment with environmental and socioeconomic factors."""

    def __init__(self, temperature=25.0, humidity=50.0, light_level=100.0, crime_rate=5.0, school_rating=7.0, property_trend=0.0):
        """
        Initializes the environment with default or specified values.

        Args:
            temperature (float): Initial temperature in Celsius.
            humidity (float): Initial humidity as a percentage.
            light_level (float): Initial light level (arbitrary units).
            crime_rate (float): Initial crime rate.
            school_rating (float): Initial school rating.
            property_trend (float): Initial property value trend.
        """
        self.temperature = temperature
        self.humidity = humidity
        self.light_level = light_level
        self.crime_data = CrimeData(crime_rate)
        self.school_ratings = SchoolRatings(school_rating)
        self.property_value_trends = PropertyValueTrends(property_trend)

    def get_temperature(self):
        """Returns the current temperature."""
        return self.temperature

    def get_humidity(self):
        """Returns the current humidity."""
        return self.humidity

    def get_light_level(self):
        """Returns the current light level."""
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
    env = Environment()
    print(f"Initial Temperature: {env.get_temperature()}°C")
    print(f"Initial Crime Rate: {env.get_crime_rate()}")
    print(f"Initial School Rating: {env.get_school_rating()}")
    print(f"Initial Property Trend: {env.get_property_trend()}")
    env.simulate_random_changes()
    print(f"Randomized Temperature: {env.get_temperature()}°C")
    print(f"Randomized Crime Rate: {env.get_crime_rate()}")
    print(f"Randomized School Rating: {env.get_school_rating()}")
    print(f"Randomized Property Trend: {env.get_property_trend()}")
