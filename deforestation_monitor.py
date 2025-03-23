# --- deforestation_monitor.py ---
"""
This module simulates monitoring deforestation levels for a given location.
In a real-world scenario, this would involve querying a remote sensing API or database.
"""

import random

def monitor_deforestation(location, api_key=None):
    """Simulates monitoring deforestation levels for a location."""
    deforestation_level = random.randint(0, 100)  # Simulate deforestation level (0-100)
    return {
        'level': deforestation_level,
        'location': location,
    }
