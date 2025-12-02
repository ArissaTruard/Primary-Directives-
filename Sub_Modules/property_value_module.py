# property_value_module.py
"""Simulates property value trends with location awareness."""
import random
from typing import Optional, Dict, Any
from sub_location import get_location_from_address, get_address_from_location

class PropertyValueTrends:
    """Represents property value trends with a simulated trend and location."""

    def __init__(self, value_trend=0.0, location: Optional[Dict[str, Any]] = None):
        """
        Initializes the property value trends with a default or specified trend and location.

        Args:
            value_trend (float): Initial property value trend.
            location (Optional[Dict[str, Any]]): Location dictionary.
        """
        self.value_trend = value_trend
        self.location = location

    def get_value_trend(self):
        """Returns the current property value trend."""
        return self.value_trend

    def get_location(self):
        """Returns the location dictionary."""
        return self.location

    def adjust_value_trend(self, delta):
        """
        Adjusts the property value trend by a given amount.

        Args:
            delta (float): Change in property value trend (positive or negative).
        """
        self.value_trend += delta
        self.value_trend = round(self.value_trend, 2)

    def simulate_value_trend_changes(self, change_range=(-0.2, 0.2)):
        """
        Simulates random changes in the property value trend.

        Args:
            change_range (tuple): Range for property value trend changes (min, max).
        """
        delta = random.uniform(change_range[0], change_range[1])
        self.adjust_value_trend(delta)

    def set_location_from_address(self, address: str):
        """Sets the location from an address string."""
        self.location = get_location_from_address(address)

    def set_address_from_coordinates(self, lat: float, lng: float):
         """sets address from coordinates"""
         self.location = get_address_from_location(lat, lng)

# Example Usage (within property_value_module.py)
if __name__ == "__main__":
    property_trends = PropertyValueTrends(value_trend=0.05) # Initialize with a specific trend
    print(f"Initial Property Trend: {property_trends.get_value_trend()}")
    print(f"Initial Location: {property_trends.get_location()}")

    property_trends.adjust_value_trend(-0.1)
    print(f"Adjusted Property Trend: {property_trends.get_value_trend()}")

    property_trends.simulate_value_trend_changes()
    print(f"Randomized Property Trend: {property_trends.get_value_trend()}")

    property_trends.set_location_from_address("1 Wall Street, New York, NY")
    print(f"Location after address set: {property_trends.get_location()}")

    if property_trends.get_location() and property_trends.get_location().get("latitude") and property_trends.get_location().get("longitude"):
      property_trends.set_address_from_coordinates(property_trends.get_location().get("latitude"), property_trends.get_location().get("longitude"))
      print(f"Location after reverse geocode: {property_trends.get_location()}")
