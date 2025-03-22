# school_ratings_module.py
"""Simulates school rating data with location awareness."""
import random
from typing import Optional, Dict, Any
from sub_location import get_location_from_address, get_address_from_location

class SchoolRatings:
    """Represents school rating data with a simulated rating and location."""

    def __init__(self, rating=7.0, location: Optional[Dict[str, Any]] = None):
        """
        Initializes the school rating data with a default or specified rating and location.

        Args:
            rating (float): Initial school rating.
            location (Optional[Dict[str, Any]]): Location dictionary.
        """
        self.rating = rating
        self.location = location

    def get_rating(self):
        """Returns the current school rating."""
        return self.rating

    def get_location(self):
        """Returns the location dictionary."""
        return self.location

    def adjust_rating(self, delta):
        """
        Adjusts the school rating by a given amount.

        Args:
            delta (float): Change in school rating (positive or negative).
        """
        self.rating += delta
        self.rating = round(self.rating, 2)

    def simulate_rating_changes(self, change_range=(-0.5, 0.5)):
        """
        Simulates random changes in the school rating.

        Args:
            change_range (tuple): Range for school rating changes (min, max).
        """
        delta = random.uniform(change_range[0], change_range[1])
        self.adjust_rating(delta)

    def set_location_from_address(self, address: str):
        """Sets the location from an address string."""
        self.location = get_location_from_address(address)

    def set_address_from_coordinates(self, lat: float, lng: float):
        """sets address from coordinates"""
        self.location = get_address_from_location(lat, lng)

# Example Usage (within school_ratings_module.py)
if __name__ == "__main__":
    school_ratings = SchoolRatings(rating=8.5) # Initialize with a specific rating
    print(f"Initial School Rating: {school_ratings.get_rating()}")
    print(f"Initial Location: {school_ratings.get_location()}")

    school_ratings.adjust_rating(-0.3)
    print(f"Adjusted School Rating: {school_ratings.get_rating()}")

    school_ratings.simulate_rating_changes()
    print(f"Randomized School Rating: {school_ratings.get_rating()}")

    school_ratings.set_location_from_address("Stanford University, Stanford, CA")
    print(f"Location after address set: {school_ratings.get_location()}")

    if school_ratings.get_location() and school_ratings.get_location().get("latitude") and school_ratings.get_location().get("longitude"):
      school_ratings.set_address_from_coordinates(school_ratings.get_location().get("latitude"), school_ratings.get_location().get("longitude"))
      print(f"Location after reverse geocode: {school_ratings.get_location()}")
