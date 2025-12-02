--- ocean_health_monitor.py ---
"""Simulates monitoring ocean health."""
def monitor_ocean_health(location, api_key=None):
    return {'ocean_health_index': random.uniform(0, 1), 'location': location}
