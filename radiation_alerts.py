# --- radiation_alerts.py ---
import logging
import datetime
import os
import random

def _simulate_data_capture(location):
    """Simulates data capture (audio, video, sensor, facial images)."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data_dir = f"radiation_data_{timestamp}"
    os.makedirs(data_dir, exist_ok=True)
    with open(os.path.join(data_dir, "sensor_data.txt"), "w") as f:
        f.write(f"Simulated sensor data at {location}: {random.random()}")
    with open(os.path.join(data_dir, "audio_data.txt"), "w") as f:
        f.write(f"Simulated audio data at {location}: Noise level {random.randint(0, 100)}")
    with open(os.path.join(data_dir, "video_data.txt"), "w") as f:
        f.write(f"Simulated video data at {location}: Motion detected {random.choice([True, False])}")
    with open(os.path.join(data_dir, "facial_images.txt"), "w") as f:
        f.write(f"Simulated facial image data: Person {random.randint(1, 5)} detected")
    with open(os.path.join(data_dir, "facial_identification.txt"), "w") as f:
        f.write(f"Simulated identification data: Person ID {random.randint(1000, 9999)} detected")
    return data_dir

def alert_authorities(radiation_level, radiation_type, location):
    """Simulates alerting authorities and emergency services."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"ALERT: {radiation_type} radiation level {radiation_level} detected at {location} at {timestamp}.")
    print("Alerting authorities, emergency services, and medical establishments.")
    data_dir = _simulate_data_capture(location)
    print(f"Data captured and stored in: {data_dir}")
    logging.warning(f"Radiation alert at {location}: {radiation_type} Level {radiation_level}, data in {data_dir}")
