# --- resource_monitor.py ---
"""Simulates monitoring specific resource levels."""
def monitor_specific_resources(location, api_key=None):
    return {'resource_level': random.uniform(0, 100), 'location': location}
