# --- sub_location.py ---
import geocoder
import logging
from typing import Optional, Dict, Any, List

def get_aggregated_location(results: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Aggregates location data from multiple providers to create a final location.

    This function takes a list of location data dictionaries and aggregates them to
    produce a final location with enhanced accuracy.

    Args:
        results (List[Dict[str, Any]]): A list of location data dictionaries.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the aggregated location, or None if aggregation fails.
    """
    if not results:
        return None

    try:
        latitudes = [r["latitude"] for r in results if r.get("latitude") is not None]
        longitudes = [r["longitude"] for r in results if r.get("longitude") is not None]
        cities = [r["city"] for r in results if r.get("city") is not None]
        states = [r["state"] for r in results if r.get("state") is not None]
        countries = [r["country"] for r in results if r.get("country") is not None]

        if not latitudes or not longitudes:
            return None

        avg_lat = sum(latitudes) / len(latitudes)
        avg_lng = sum(longitudes)
        city = max(set(cities), key=cities.count) if cities else None
        state = max(set(states), key=states.count) if states else None
        country = max(set(countries), key=countries.count) if countries else None

        return {
            "latitude": avg_lat,
            "longitude": avg_lng,
            "city": city,
            "state": state,
            "country": country
        }

    except Exception as e:
        logging.error(f"Error aggregating location: {e}")
        return None

def get_current_location(gps_lat: Optional[float] = None, gps_lng: Optional[float] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves the robot's current location details, prioritizing GPS if available.

    This function attempts to retrieve the most accurate location, prioritizing GPS
    coordinates if provided. If GPS coordinates are not available, it uses IP-based
    geocoding and aggregates results from multiple providers.

    Args:
        gps_lat (Optional[float]): Latitude from GPS (if available).
        gps_lng (Optional[float]): Longitude from GPS (if available).

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing location details, or None if location
              cannot be determined.
    """
    if gps_lat is not None and gps_lng is not None:
        try:
            g = geocoder.reverse([gps_lat, gps_lng])
            if g.address:
                logging.info(f"Location determined from GPS: {g.address}")
                return {
                    "latitude": gps_lat,
                    "longitude": gps_lng,
                    "address": g.address
                }
            else:
                logging.warning("Could not reverse geocode GPS coordinates.")
        except Exception as e:
            logging.error(f"Error reverse geocoding GPS: {e}")

    try:
        results = []
        providers = ['freegeoip', 'ipinfo', 'ipapi']  # Prioritized providers
        for provider in providers:
            g = geocoder.ip('me', method=provider)
            if g.latlng:
                results.append({
                    "latitude": g.latlng[0],
                    "longitude": g.latlng[1],
                    "city": g.city,
                    "state": g.state,
                    "country": g.country,
                    "provider": provider
                })
        return get_aggregated_location(results)

    except Exception as e:
        logging.error(f"Error getting location from IP: {e}")
        return None

def get_location_from_address(address: str) -> Optional[Dict[str, float]]:
    """
    Retrieves latitude and longitude coordinates from a given address, with enhanced accuracy.

    This function attempts to retrieve the most accurate coordinates by querying multiple
    geocoding services and aggregating results.

    Args:
        address (str): The address to geocode.

    Returns:
        Optional[Dict[str, float]]: A dictionary containing latitude and longitude, or None if
              geocoding fails.
    """
    try:
        results = []
        providers = ['google', 'osm', 'arcgis'] # Prioritized providers.
        for provider in providers:
            g = geocoder.geocode(address, provider=provider)
            if g.latlng:
                results.append({
                    "latitude": g.latlng[0],
                    "longitude": g.latlng[1],
                    "provider": provider
                })
        return get_aggregated_location(results)

    except Exception as e:
        logging.error(f"Error geocoding address '{address}': {e}")
        return None

def get_address_from_location(lat: float, lng: float) -> Optional[Dict[str, str]]:
    """
    Retrieves an address from latitude and longitude coordinates, with enhanced accuracy.

    This function attempts to retrieve the most accurate address by querying multiple
    reverse geocoding services and selecting the most consistent result.

    Args:
        lat (float): The latitude coordinate.
        lng (float): The longitude coordinate.

    Returns:
        Optional[Dict[str, str]]: A dictionary containing the address, or None if reverse
              geocoding fails.
    """
    try:
        results = []
        providers = ['google', 'osm', 'arcgis'] # Prioritized providers.
        for provider in providers:
            g = geocoder.reverse([lat, lng], provider=provider)
            if g.address:
                results.append({
                    "address": g.address,
                    "provider": provider
                })
        if results:
            addresses = [r["address"] for r in results]
            most_common_address = max(set(addresses), key=addresses.count)
            logging.info(f"Aggregated reverse geocoded location ({lat}, {lng}) to: {most_common_address}")
            return {
                "address": most_common_address
            }
        else:
            logging.warning(f"Could not reverse geocode location ({lat}, {lng}) using any provider.")
            return None

    except Exception as e:
        logging.error(f"Error reverse geocoding location ({lat}, {lng}): {e}")
        return None
