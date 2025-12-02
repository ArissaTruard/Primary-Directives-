# --- seismic_monitor.py ---
import logging
import datetime
import requests

# Simulated API endpoint for seismic data (replace with a real API)
SEISMIC_API_ENDPOINT = "https://simulated-seismic-api.com/data"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_seismic_data_from_api(location):
    """Retrieves seismic data from a simulated API."""
    try:
        response = requests.get(f"{SEISMIC_API_ENDPOINT}?location={location}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve seismic data from API: {e}")
        return None

def monitor_seismic_activity(location, ground_movement=None, richter_scale=None):
    """Monitors and analyzes seismic activity, handling both sensor and API data."""
    timestamp = datetime.datetime.now()
    analysis = {"alert": False, "message": "Seismic activity normal", "details": {}}

    # Check for available sensor data
    if ground_movement is not None:
        logging.info(f"Seismic activity at {location} - {timestamp}: Ground Movement={ground_movement}")
        analysis["details"]["ground_movement"] = ground_movement

        if ground_movement > 5:  # Example threshold
            logging.warning(f"Significant ground movement detected at {location}")
            analysis["alert"] = True
            analysis["message"] = "Significant ground movement detected."
            analysis["details"]["ground_movement_alert"] = f"Ground Movement: {ground_movement}"

    if richter_scale is not None:
        logging.info(f"Seismic activity at {location} - {timestamp}: Richter Scale={richter_scale}")
        analysis["details"]["richter_scale"] = richter_scale

        if richter_scale > 4: #Example richter scale threshold
          logging.warning(f"Significant Richter Scale reading detected at {location}")
          analysis["alert"] = True
          analysis["message"] = "Significant Richter Scale reading detected."
          analysis["details"]["richter_scale_alert"] = f"Richter Scale: {richter_scale}"

    # If no sensor data, try retrieving from API
    if ground_movement is None and richter_scale is None:
        api_data = get_seismic_data_from_api(location)
        if api_data:
            ground_movement = api_data.get("ground_movement")
            richter_scale = api_data.get("richter_scale")

            if ground_movement is not None:
                logging.info(f"Seismic activity at {location} - {timestamp} (API): Ground Movement={ground_movement}")
                analysis["details"]["ground_movement"] = ground_movement
                if ground_movement > 5:
                  logging.warning(f"Significant ground movement detected at {location} from api")
                  analysis["alert"] = True
                  analysis["message"] = "Significant ground movement detected from api."
                  analysis["details"]["ground_movement_api_alert"] = f"Ground Movement: {ground_movement}"

            if richter_scale is not None:
                logging.info(f"Seismic activity at {location} - {timestamp} (API): Richter Scale={richter_scale}")
                analysis["details"]["richter_scale"] = richter_scale
                if richter_scale > 4:
                  logging.warning(f"Significant richter scale reading detected at {location} from api")
                  analysis["alert"] = True
                  analysis["message"] = "Significant richter scale reading detected from api."
                  analysis["details"]["richter_scale_api_alert"] = f"Richter Scale: {richter_scale}"
        else:
            logging.warning(f"No sensor data or API data available for {location}")
            analysis["message"] = "No seismic data available."
            analysis["details"]["error"] = "No sensor or API data."

    return analysis

# Example usage
if __name__ == "__main__":
    location = "San Francisco"
    #Simulating sensor data
    sensor_analysis = monitor_seismic_activity(location, ground_movement=3.2, richter_scale = 5.2)
    print(sensor_analysis)

    #Simulating api data
    api_analysis = monitor_seismic_activity(location)
    print(api_analysis)
