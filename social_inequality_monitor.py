# --- social_inequality_monitor.py ---
"""Simulates monitoring social inequality."""
def monitor_social_inequality(location, api_key=None):
    return {'inequality_index': random.uniform(0, 1), 'location': location}
