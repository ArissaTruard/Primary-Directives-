--- political_stability_monitor.py ---
"""Simulates monitoring political stability."""
def monitor_political_stability(location, api_key=None):
    return {'stability_index': random.uniform(0, 1), 'location': location}
