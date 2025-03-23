# --- incident_reporter.py ---
import os
import time
import datetime
import logging
import json
import geocoder
import platform
import uuid
from sub_database import add_incident_report, get_applicable_laws #Import database functions

def report_illegal_action(event_details, audio_file=None, video_file=None, electronic_log=None, sensor_data=None):
    """
    Reports an illegal action to the appropriate authorities, including event details,
    time, date, location, and relevant media.

    Args:
        event_details (str): A detailed description of the observed illegal action.
        audio_file (str, optional): The file path to an audio recording related to the event.
        video_file (str, optional): The file path to a video recording related to the event.
        electronic_log (str, optional): The file path to an electronic log file documenting the event.
        sensor_data (dict, optional): Additional sensor data related to the incident.

    Returns:
        None. The function logs the report and attempts to send it to authorities.

    Raises:
        Exception: If an error occurs during the reporting process.
    """
    try:
        timestamp = datetime.datetime.now().isoformat()
        location_data = _get_location_data()
        identity_data = _get_identity_data()
        report_id = str(uuid.uuid4())

        report_data = {
            "report_id": report_id,
            "timestamp": timestamp,
            "location": location_data,
            "event_details": event_details,
            "identity_data": identity_data,
        }

        if audio_file and os.path.exists(audio_file):
            report_data["audio_file"] = audio_file
        if video_file and os.path.exists(video_file):
            report_data["video_file"] = video_file
        if electronic_log and os.path.exists(electronic_log):
            report_data["electronic_log"] = electronic_log
        if sensor_data:
            report_data["sensor_data"] = sensor_data

        print(f"Reporting illegal action: {json.dumps(report_data, indent=4)}")
        log_event(f"Reported illegal action: {json.dumps(report_data)}")

        # Database integration:
        add_incident_report(report_data) #Store the report in the database
        applicable_laws = get_applicable_laws(location_data) #Get applicable laws
        print(f"Applicable Laws: {applicable_laws}") #Print applicable laws.

    except Exception as e:
        logging.error(f"Error reporting illegal action: {e}")
        log_event(f"Error reporting illegal action: {e}")
        raise

def _get_location_data():
    """
    Retrieves the current location data using the geocoder library.

    Returns:
        dict: A dictionary containing latitude, longitude, city, state, and country.
        str: A string indicating that the location could not be determined.

    Raises:
        Exception: If an error occurs during location retrieval.
    """
    try:
        g = geocoder.ip('me')
        if g.latlng:
            return {
                "latitude": g.latlng[0],
                "longitude": g.latlng[1],
                "city": g.city,
                "state": g.state,
                "country": g.country
            }
        else:
            return "Location could not be determined."
    except Exception as e:
        logging.error(f"Error getting location: {e}")
        return "Location could not be determined."

def _get_identity_data():
    """
    Retrieves identity data, including system ID and placeholders for potential
    face image or license plate capture.

    Returns:
        dict: A dictionary containing identity data.

    Raises:
        Exception: If an error occurs during identity data retrieval.
    """
    try:
        identity_data = {}

        # Placeholder: Capture face image (requires camera access and facial recognition)
        # identity_data["face_image"] = capture_face_image()

        # Placeholder: Capture license plate and vehicle info (requires camera and OCR)
        # identity_data["license_plate"] = capture_license_plate()
        # identity_data["vehicle_info"] = get_vehicle_info(identity_data["license_plate"])

        identity_data["system_id"] = platform.node()

        return identity_data

    except Exception as e:
        logging.error(f"Error getting identity data: {e}")
        return {"error": "Identity data could not be determined."}

def log_event(event):
    """
    Logs an event to a file, including a timestamp.

    Args:
        event (str): The event to be logged.

    Returns:
        None.

    Raises:
        Exception: If an error occurs during the logging process.
    """
    try:
        with open("illegal_action_reports.txt", "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {event}\n")
    except Exception as e:
        logging.error(f"Error logging event: {e}")
        raise

# Example usage (for testing):
if __name__ == "__main__":
    report_illegal_action(
        event_details="Suspicious activity observed near bank.",
        audio_file="audio_recording.wav",
        video_file="video_surveillance.mp4",
        electronic_log="system_log.txt",
        sensor_data={"temperature": 25.5, "humidity": 60}
    )
