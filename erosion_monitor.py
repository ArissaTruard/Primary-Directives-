# --- erosion_monitor.py ---
"""Simulates monitoring erosion levels."""
import random

def monitor_erosion(location, api_key=None):
    return {'level': random.uniform(0, 10), 'location': location}
