# --- infrastructure_quality_monitor.py ---
"""Simulates monitoring infrastructure quality."""
def monitor_infrastructure_quality(location, api_key=None):
    return {'infrastructure_index': random.uniform(0, 1), 'location': location}
