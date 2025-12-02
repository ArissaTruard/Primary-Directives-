# --- biodiversity_monitor.py ---
"""Simulates monitoring biodiversity levels."""
def monitor_biodiversity(location, api_key=None):
    return {'biodiversity_index': random.uniform(0, 1), 'location': location}
