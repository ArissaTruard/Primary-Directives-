# --- radiation_config.py ---
import json
import logging
from enum import Enum

class RadiationLevel(Enum):
    BACKGROUND = "background"
    ELEVATED = "elevated"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    LETHAL = "lethal"

class RadiationType(Enum):
    ALPHA = "alpha"
    BETA = "beta"
    GAMMA = "gamma"
    NEUTRON = "neutron"
    XRAY = "x-ray"

def load_radiation_levels(filepath="radiation_levels.json"):
    """Loads radiation levels from a JSON file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Radiation levels file not found: {filepath}")
        return None
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in radiation levels file: {filepath}")
        return None
