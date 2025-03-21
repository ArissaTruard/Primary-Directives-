# --- sub_radiation.py ---
import logging
import datetime
import os  # For file operations (simulating data storage)
import random # For simulating facial recognition

# Radiation level thresholds and PPE recommendations (Sieverts)
RADIATION_LEVELS = {
    "background": {"threshold": 0.0000001, "warning": "Normal background radiation.", "ppe": "No PPE required."},
    "elevated": {"threshold": 0.000001, "warning": "Slightly elevated radiation detected. Note: Monitor exposure time.", "ppe": "Monitor exposure time."},
    "low": {"threshold": 0.001, "warning": "Low-level radiation detected. Note: Limit exposure time, basic shielding if prolonged.", "ppe": "Limit exposure time, basic shielding if prolonged."},
    "moderate": {"threshold": 0.01, "warning": "Moderate radiation detected. Note: Use lead apron, limit exposure.", "ppe": "Lead apron, limit exposure."},
    "high": {"threshold": 0.1, "warning": "High radiation detected. Note: Use full body radiation suit, potassium iodide, limit exposure.", "ppe": "Full body radiation suit, potassium iodide, limit exposure."},
    "very_high": {"threshold": 1, "warning": "Very high radiation detected. Note: Use full body radiation suit, potassium iodide, immediate evacuation recommended.", "ppe": "Full body radiation suit, potassium iodide, immediate evacuation recommended."},
    "lethal": {"threshold": 5, "warning": "Lethal radiation detected. Note: Immediate evacuation, maximum shielding, survival unlikely.", "ppe": "Immediate evacuation, maximum shielding, survival unlikely."},
}

def _simulate_data_capture(location):
    """
    Simulates data capture (audio, video, sensor, facial images) and returns the data directory.

    Placeholders:
        - audio_data.txt: Actual audio recordings.
        - video_data.txt: Actual video recordings.
        - sensor_data.txt: Real-time sensor readings (radiation, temperature, etc.).
        - facial_images.txt: Images of all persons present in the area.
        - facial_identification.txt: Identified individuals (if available).
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = f"radiation_data_{timestamp}"
    os.makedirs(data_dir, exist_ok=True) #creates a folder to store the data
    with open(os.path.join(data_dir, "sensor_data.txt"), "w") as f:
        f.write(f"Simulated sensor data at {location}: {random.random()}") #Placeholder: Real-time sensor readings.
    with open(os.path.join(data_dir, "audio_data.txt"), "w") as f:
        f.write(f"Simulated audio data at {location}: Noise level {random.randint(0,100)}") #Placeholder: Audio recording.
    with open(os.path.join(data_dir, "video_data.txt"), "w") as f:
        f.write(f"Simulated video data at {location}: Motion detected {random.choice([True, False])}") #Placeholder: Video recording.
    with open(os.path.join(data_dir, "facial_images.txt"), "w") as f:
        f.write(f"Simulated facial image data: Person {random.randint(1,5)} detected") #Placeholder: Facial images.
    with open(os.path.join(data_dir, "facial_identification.txt"), "w") as f:
        f.write(f"Simulated identification data: Person ID {random.randint(1000, 9999)} detected") #Placeholder: Person identification.
    return data_dir

def _alert_authorities(radiation_level, location):
    """
    Simulates alerting authorities and emergency services, including data capture.

    Placeholders:
        - Authorities: API calls or direct communication with law enforcement.
        - Emergency services: API calls or direct communication with fire/medical services.
        - Medical establishments: API calls or notifications to nearby hospitals.
        - Data transmission: Secure transmission of captured data to relevant parties.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"ALERT: Radiation level {radiation_level} detected at {location} at {timestamp}.")
    print("Alerting authorities, emergency services, and medical establishments.")
    data_dir = _simulate_data_capture(location)
    print(f"Data captured and stored in: {data_dir}")
    # Placeholder: Send alerts to authorities, emergency services, and medical establishments.
    # Placeholder: Transmit captured data securely.
    logging.warning(f"Radiation alert at {location}: Level {radiation_level}, data in {data_dir}")

def assess_radiation(radiation_level, location="Unknown"):
    """
    Assesses radiation levels and returns warnings and PPE suggestions based on graded exposure.
    Also alerts authorities if a spike is detected.

    Placeholders:
        - location: GPS coordinates or address of the detection.
    """
    if radiation_level is not None:
        if radiation_level > RADIATION_LEVELS["lethal"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["lethal"]["warning"], RADIATION_LEVELS["lethal"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["very_high"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["very_high"]["warning"], RADIATION_LEVELS["very_high"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["high"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["high"]["warning"], RADIATION_LEVELS["high"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["moderate"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["moderate"]["warning"], RADIATION_LEVELS["moderate"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["low"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["low"]["warning"], RADIATION_LEVELS["low"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["elevated"]["threshold"]:
            _alert_authorities(radiation_level, location)
            return RADIATION_LEVELS["elevated"]["warning"], RADIATION_LEVELS["elevated"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["background"]["threshold"]:
            return RADIATION_LEVELS["background"]["warning"], RADIATION_LEVELS["background"]["ppe"]
        else:
            return RADIATION_LEVELS["background"]["warning"], RADIATION_LEVELS["background"]["ppe"]

    return None, None
