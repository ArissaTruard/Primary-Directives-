# --- invasive_species_monitor.py ---
"""Simulates monitoring invasive species presence."""
def monitor_invasive_species(location, api_key=None):
    return {'species_present': random.choice([True, False]), 'location': location}
