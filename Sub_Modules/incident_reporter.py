# --- incident_reporter.py ---
import os
import time
import datetime
import logging
import json
import geocoder
import platform
import uuid
from sub_database import add_incident_report, get_applicable_laws
from sub_system import request_approval

def _get_location_data():
    """Retrieves location data using geocoding."""
    try:
        g = geocoder.ip('me')
        if g.latlng:
            return {"latitude": g.lat, "longitude": g.lng, "address": g.address}
        else:
            logging.warning("Location data not available.")
            return {"latitude": None, "longitude": None, "address": None}
    except Exception as e:
        logging.error(f"Error retrieving location data: {e}")
        return {"latitude": None, "longitude": None, "address": None}

def _get_identity_data():
    """Retrieves identity data (placeholder)."""
    # Placeholder: Implement actual identity retrieval logic
    return {"robot_id": "RBT-1234", "model": "Advanced AI Model"}

def log_event(event):
    """Logs an event to a file."""
    try:
        with open("incident_reporter_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")

def report_illegal_action(event_details, audio_file=None, video_file=None, electronic_log=None, sensor_data=None):
    """Reports an illegal action to the appropriate authorities."""
    try:
        timestamp = datetime.datetime.now().isoformat()
        location_data = _get_location_data()
        identity_data = _get_identity_data()
        report_id = str(uuid.uuid4())
        report_data = {"report_id": report_id, "timestamp": timestamp, "location": location_data, "event_details": event_details, "identity_data": identity_data,}
        if audio_file and os.path.exists(audio_file): report_data["audio_file"] = audio_file
        if video_file and os.path.exists(video_file): report_data["video_file"] = video_file
        if electronic_log and os.path.exists(electronic_log): report_data["electronic_log"] = electronic_log
        if sensor_data: report_data["sensor_data"] = sensor_data
        print(f"Reporting illegal action: {json.dumps(report_data, indent=4)}")
        log_event(f"Reported illegal action: {json.dumps(report_data)}")
        add_incident_report(report_data)
        applicable_laws = get_applicable_laws(location_data)
        print(f"Applicable Laws: {applicable_laws}")
    except Exception as e:
        logging.error(f"Error reporting illegal action: {e}")
        log_event(f"Error reporting illegal action: {e}")
        request_approval(f"Error reporting illegal action: {e}. Awaiting approval.")
