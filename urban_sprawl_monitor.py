# --- urban_sprawl_monitor.py ---
"""
This module simulates monitoring urban sprawl rates for a given location.
In a real-world scenario, this would involve querying a land use API or database.
"""

import random

def monitor_urban_sprawl(location, api_key=None):
    """Simulates monitoring urban sprawl rates for a location."""
    urban_sprawl_rate = round(random.uniform(0, 10), 2)  # Simulate urban sprawl rate (0-10)
    return {
        'rate': urban_sprawl_rate,
        'location': location,
    }
