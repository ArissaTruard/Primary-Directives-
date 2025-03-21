# --- sub_radiation.py ---
import logging
import datetime
import os
import random
from enum import Enum
import json
RADIATION_LEVELS = load_radiation_levels()
if RADIATION_LEVELS is None:
    # Default radiation levels if loading fails
    RADIATION_LEVELS = {
        "background_threshold": 0.0000001,
        "background_warning": "Normal background radiation.",
        "alpha_background_ppe": "No PPE required.",
        "beta_background_ppe": "No PPE required.",
        "gamma_background_ppe": "No PPE required.",
        "neutron_background_ppe": "No PPE required.",
        "x-ray_background_ppe": "No PPE required.",
        "elevated_threshold": 0.000001,
        "elevated_warning": "Slightly elevated radiation detected. Note: Monitor exposure time.",
        "alpha_elevated_ppe": "Monitor exposure time.",
        "beta_elevated_ppe": "Monitor exposure time.",
        "gamma_elevated_ppe": "Monitor exposure time.",
        "neutron_elevated_ppe": "Monitor exposure time.",
        "x-ray_elevated_ppe": "Monitor exposure time.",
        "low_threshold": 0.001,
        "low_warning": "Low-level radiation detected. Note: Limit exposure time, basic shielding if prolonged.",
        "alpha_low_ppe": "Basic shielding (paper, clothing).",
        "beta_low_ppe": "Basic shielding (thick plastic, aluminum).",
        "gamma_low_ppe": "Lead shielding, limit exposure.",
        "neutron_low_ppe": "Concrete, water shielding.",
        "x-ray_low_ppe": "Lead shielding, limit exposure.",
        "moderate_threshold": 0.01,
        "moderate_warning": "Moderate radiation detected. Note: Use lead apron, limit exposure.",
        "alpha_moderate_ppe": "Lead apron, limit exposure.",
        "beta_moderate_ppe": "Lead apron, limit exposure.",
        "gamma_moderate_ppe": "Thick lead shielding, limit exposure.",
        "neutron_moderate_ppe": "Specialized neutron shielding, limit exposure.",
        "x-ray_moderate_ppe": "Thick lead shielding, limit exposure.",
        "high_threshold": 0.1,
        "high_warning": "High radiation detected. Note: Use full body radiation suit, potassium iodide, limit exposure.",
        "alpha_high_ppe": "Full body radiation suit, limit exposure.",
        "beta_high_ppe": "Full body radiation suit, limit exposure.",
        "gamma_high_ppe": "Full body radiation suit, potassium iodide, limit exposure.",
        "neutron_high_ppe": "Full body neutron suit, limit exposure.",
        "x-ray_high_ppe": "Full body radiation suit, potassium iodide, limit exposure.",
        "very_high_threshold": 1,
        "very_high_warning": "Very high radiation detected. Note: Use full body radiation suit, potassium iodide, immediate evacuation recommended.",
        "alpha_very_high_ppe": "Full body radiation suit, immediate evacuation.",
        "beta_very_high_ppe": "Full body radiation suit, immediate evacuation.",
        "gamma_very_high_ppe": "Full body radiation suit, potassium iodide, immediate evacuation.",
        "neutron_very_high_ppe": "Full body neutron suit, immediate evacuation.",
        "x-ray_very_high_ppe": "Full body radiation suit, potassium iodide, immediate evacuation.",
        "lethal_threshold": 5,
        "lethal_warning": "Lethal radiation detected. Note: Immediate evacuation, maximum shielding, survival unlikely.",
        "alpha_lethal_ppe": "Maximum shielding, immediate evacuation.",
        "beta_lethal_ppe": "Maximum shielding, immediate evacuation.",
        "gamma_lethal_ppe": "Maximum shielding, potassium iodide, immediate evacuation.",
        "neutron_lethal_ppe": "Maximum neutron shielding, immediate evacuation.",
        "x-ray_lethal_ppe": "Maximum shielding, potassium iodide, immediate evacuation."
    }

def assess_radiation(radiation_level, radiation_type="gamma", location="Unknown"):
    """
    Assesses radiation levels and returns warnings and PPE suggestions based on graded exposure.
    Also alerts authorities if a spike is detected.
    """
    if radiation_level is not None:
        for level in RadiationLevel:
            if radiation_level > RADIATION_LEVELS[f"{level.value}_threshold"]:
                alert_authorities(radiation_level, radiation_type, location)
                return RADIATION_LEVELS[f"{level.value}_warning"], RADIATION_LEVELS[f"{radiation_type}_{level.value}_ppe"]
        return RADIATION_LEVELS["background_warning"], RADIATION_LEVELS[f"{radiation_type}_background_ppe"]
    return None, None
