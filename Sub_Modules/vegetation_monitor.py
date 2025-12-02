# vegetation_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_vegetation(location_input=None, latitude=None, longitude=None, vegetation_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_vegetation_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Vegetation sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_vegetation_api_data(location_str, vegetation_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Vegetation API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No vegetation data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Vegetation health analysis complete.", "details": combined_data, "ppe_recommendation": "Minimal PPE"}
    if combined_data.get("ndvi", 1) < 0.2:
        analysis["ppe_recommendation"] = "Eye and Skin Protection (for potential allergens or irritants)"

    if combined_data.get("ndvi", 1) < 0.3:
        logging.warning(f"Low NDVI detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low vegetation health."
        analysis["details"]["ndvi"] = combined_data.get("ndvi")

    if combined_data.get("leaf_area_index", 0) < 1.0:
        logging.warning(f"Low leaf area index detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low vegetation density."
        analysis["details"]["leaf_area_index"] = combined_data.get("leaf_area_index")

    if combined_data.get("canopy_cover", 0) < 50:
        logging.warning(f"Low canopy cover detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Sparse vegetation cover."
        analysis["details"]["canopy_cover"] = combined_data.get("canopy_cover")

    if combined_data.get("stress_index", 0) > 0.5:
        logging.warning(f"High vegetation stress detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Vegetation stress detected."
        analysis["details"]["stress_index"] = combined_data.get("stress_index")

    if combined_data.get("species_diversity", 0) < 5:
        logging.warning(f"Low species diversity detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low species diversity."
        analysis["details"]["species_diversity"] = combined_data.get("species_diversity")

    analysis["location"] = location

    return analysis

def get_vegetation_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "ndvi": 0.6,
        "leaf_area_index": 2.5,
        "canopy_cover": 70,
        "stress_index": 0.2,
        "species_diversity": 8,
    }

def get_vegetation_api_data(location, api_key):
    # Replace with real API call
    return {
        "ndvi": 0.65,
        "leaf_area_index": 2.7,
        "canopy_cover": 75,
        "stress_index": 0.22,
        "species_diversity": 9,
    }

def get_vegetation_data(location, api_key):
    url = f"https://api.example-vegetation.com/vegetation?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        vegetation_data = response.json()
        return vegetation_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Vegetation API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from vegetation API")
        return {"error": "Invalid JSON response"}
