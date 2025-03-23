# crime_module.py
"""Simulates crime data with location awareness."""
import random
from typing import Optional, Dict, Any
from sub_location import get_location_from_address, get_address_from_location

class CrimeData:
    """Represents crime data with a simulated crime rate and location."""

    def __init__(self, crime_rate=5.0, location: Optional[Dict[str, Any]] = None):
        """
        Initializes the crime data with a default or specified crime rate and location.

        Args:
            crime_rate (float): Initial crime rate.
            location (Optional[Dict[str, Any]]): Location dictionary (latitude, longitude, etc.).
        """
        self.crime_rate = crime_rate
        self.location = location

    def get_crime_rate(self):
        """Returns the current crime rate."""
        return self.crime_rate

    def get_location(self):
        """Returns the location dictionary."""
        return self.location

    def adjust_crime_rate(self, delta):
        """
        Adjusts the crime rate by a given amount.

        Args:
            delta (float): Change in crime rate (positive or negative).
        """
        self.crime_rate += delta
        self.crime_rate = round(self.crime_rate, 2)

    def simulate_crime_changes(self, change_range=(-1.0, 1.0)):
        """
        Simulates random changes in the crime rate.

        Args:
            change_range (tuple): Range for crime rate changes (min, max).
        """
        delta = random.uniform(change_range[0], change_range[1])
        self.adjust_crime_rate(delta)

    def set_location_from_address(self, address: str):
        """Sets the location from an address string."""
        self.location = get_location_from_address(address)

    def set_address_from_coordinates(self, lat: float, lng: float):
        """sets address from coordinates"""
        self.location = get_address_from_location(lat, lng)

# Example Usage (within crime_module.py)
if __name__ == "__main__":
    crime_data = CrimeData(crime_rate=8.0)  # Initialize with a specific crime rate
    print(f"Initial Crime Rate: {crime_data.get_crime_rate()}")
    print(f"Initial Location: {crime_data.get_location()}")

    crime_data.adjust_crime_rate(-1.5)
    print(f"Adjusted Crime Rate: {crime_data.get_crime_rate()}")

    crime_data.simulate_crime_changes()
    print(f"Randomized Crime Rate: {crime_data.get_crime_rate()}")

    crime_data.set_location_from_address("1600 Amphitheatre Parkway, Mountain View, CA")
    print(f"Location after address set: {crime_data.get_location()}")

    if crime_data.get_location() and crime_data.get_location().get("latitude") and crime_data.get_location().get("longitude"):
      crime_data.set_address_from_coordinates(crime_data.get_location().get("latitude"), crime_data.get_location().get("longitude"))
      print(f"Location after reverse geocode: {crime_data.get_location()}")
