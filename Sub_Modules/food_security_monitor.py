# --- food_security_monitor.py ---
"""Simulates monitoring food security."""
def monitor_food_security(location, api_key=None):
    return {'food_security_index': random.uniform(0, 1), 'location': location}
