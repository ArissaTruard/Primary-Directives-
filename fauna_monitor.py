# fauna_monitor.py
import logging
import datetime
from sub_location import get_location_from_address, get_address_from_location
import requests
import json
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_fauna_database():
    """Creates the fauna database and species table if they don't exist."""
    conn = sqlite3.connect('fauna.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            species_name TEXT,
            estimated_population INTEGER,
            population_density REAL,
            last_updated TEXT
        )
    ''')
    conn.commit()
    conn.close()

def update_species_data(location, species_name, estimated_population, population_density):
    """Updates or inserts species data into the database."""
    conn = sqlite3.connect('fauna.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO species (location, species_name, estimated_population, population_density, last_updated)
        VALUES (?, ?, ?, ?, ?)
    ''', (location, species_name, estimated_population, population_density, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_species_data(location):
    """Retrieves species data for a given location from the database."""
    conn = sqlite3.connect('fauna.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT species_name, estimated_population, population_density, last_updated
        FROM species
        WHERE location = ?
    ''', (location,))
    data = cursor.fetchall()
    conn.close()
    return data

def monitor_fauna(location_input=None, latitude=None, longitude=None, fauna_api_key=None):
    timestamp = datetime.datetime.now()
    location = get_location_from_address(location_input) if location_input else get_address_from_location(latitude, longitude) if latitude and longitude else None

    if not location:
        logging.error("Location not provided or could not be determined.")
        return {"alert": True, "message": "Location error", "details": {}}

    location_str = location.get("address") if location.get("address") else f"Lat: {location.get('latitude')}, Lng: {location.get('longitude')}"

    sensor_data_available = False
    api_data_available = False

    try:
        sensor_data = get_fauna_sensor_data()
        if sensor_data:
            sensor_data_available = True
            logging.info(f"Fauna sensor data at {location_str}: {sensor_data}")
        else:
            logging.warning("Sensor data unavailable.")
    except Exception as e:
        logging.warning(f"Error reading sensor data: {e}")

    if not sensor_data_available:
        try:
            api_data = get_fauna_api_data(location_str, fauna_api_key)
            if api_data:
                api_data_available = True
                logging.info(f"Fauna API data at {location_str}: {api_data}")
            else:
                logging.warning("API data unavailable.")
        except Exception as api_e:
            logging.error(f"Error using API data: {api_e}")

    if not sensor_data_available and not api_data_available:
        return {"alert": True, "message": "No fauna data available.", "details": {}}

    combined_data = {}
    if sensor_data_available:
        combined_data.update(sensor_data)
    if api_data_available:
        combined_data.update(api_data)

    analysis = {"alert": False, "message": "Fauna monitoring complete.", "details": combined_data}

    if combined_data.get("species_diversity", 0) < 5:
        logging.warning(f"Low species diversity detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Low species diversity."
        analysis["details"]["species_diversity"] = combined_data.get("species_diversity")

    if combined_data.get("invasive_species", False):
        logging.warning(f"Invasive species detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Invasive species present."
        analysis["details"]["invasive_species"] = combined_data.get("invasive_species")

    if combined_data.get("endangered_species", False):
        logging.warning(f"Endangered species detected at {location_str}")
        analysis["alert"] = True
        analysis["message"] = "Endangered species present."
        analysis["details"]["endangered_species"] = combined_data.get("endangered_species")

    # Database Integration
    create_fauna_database()  # Ensure database exists
    if combined_data.get("species_data"):
        for species in combined_data["species_data"]:
            update_species_data(location_str, species["name"], species.get("population"), species.get("density"))

    species_data_from_db = get_species_data(location_str)
    analysis["details"]["species_data_from_db"] = species_data_from_db

    analysis["location"] = location

    return analysis

def get_fauna_sensor_data():
    # Replace with real sensor data retrieval
    return {
        "species_diversity": 8,
        "invasive_species": False,
        "endangered_species": True,
        "species_data": [
            {"name": "deer", "population": 100, "density": 10.0},
            {"name": "birds", "population": 500, "density": 50.0},
        ],
    }

def get_fauna_api_data(location, api_key):
    # Replace with real API call
    return {
        "species_diversity": 9,
        "invasive_species": False,
        "endangered_species": True,
        "species_data": [
            {"name": "deer", "population": 110, "density": 11.0},
            {"name": "birds", "population": 520, "density": 52.0},
        ],
    }

def get_fauna_data(location, api_key):
    url = f"https://api.example-fauna.com/fauna?q={location}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        fauna_data = response.json()
        return fauna_data
    except requests.exceptions.RequestException as e:
        logging.error(f"Fauna API request failed: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError:
        logging.error("Invalid JSON response from fauna API")
        return {"error": "Invalid JSON response"}
