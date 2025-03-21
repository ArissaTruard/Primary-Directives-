# --- sub_environmental.py ---
import datetime
import logging
import sub_radiation

# Configuration Dictionaries (Move outside the function for efficiency)
TOLERANCES = {
    "temperature": 20,  # Degrees Celsius (comfortable spring)
    "humidity": 50,     # Percentage (comfortable spring)
    "uv_index": 4,      # Moderate UV index
    "allergen_density": 2, # Low allergen levels
    "air_quality": 30,  # Good air quality (AQI)
    "smog_level": 50,
}

CONDITIONS = {
    "temperature": {
        "high": {"threshold": TOLERANCES["temperature"] + 5, "warning": "High temperature detected.", "ppe": "Hydration, light clothing, wide-brimmed hat."},
        "low": {"threshold": TOLERANCES["temperature"] - 10, "warning": "Low temperature detected.", "ppe": "Insulated clothing, layers, gloves, hat."},
    },
    "humidity": {
        "high": {"threshold": TOLERANCES["humidity"] + 25, "warning": "High humidity detected.", "ppe": "Breathable clothing, moisture-wicking fabrics."},
        "low": {"threshold": TOLERANCES["humidity"] - 25, "warning": "Low humidity detected.", "ppe": "Moisturizer, lip balm, increased hydration."},
    },
    "uv_index": {"high": {"threshold": TOLERANCES["uv_index"] + 3, "warning": "High UV index detected.", "ppe": "Sunscreen, sunglasses, long sleeves, hat."}},
    "allergen_density": {"high": {"threshold": TOLERANCES["allergen_density"] + 3, "warning": "High allergen density detected.", "ppe": "Mask, allergy medication, eye protection."}},
    "air_quality": {"high": {"threshold": TOLERANCES["air_quality"] + 70, "warning": "Poor air quality detected.", "ppe": "N95 mask, avoid strenuous activity."}},
    "smog_level": {"high": {"threshold": TOLERANCES["smog_level"], "warning": "High smog level detected.", "ppe": "Mask, limit outdoor exposure."}},
    "weather_overall": {"severe": {"threshold": "severe", "warning": "Severe weather conditions.", "ppe": "Seek shelter, appropriate weather gear."}},
}

def _check_condition(factor, data, conditions):
    """Internal function to check a single environmental condition."""
    if data is not None and factor in conditions:
        if isinstance(data, (int, float)):
            if data > conditions[factor]["high"]["threshold"]:
                return conditions[factor]["high"]["warning"], conditions[factor]["high"]["ppe"]
            elif factor in ("temperature", "humidity") and data < conditions[factor]["low"]["threshold"]:
                return conditions[factor]["low"]["warning"], conditions[factor]["low"]["ppe"]
        elif isinstance(data, str) and factor == "weather_overall" and conditions[factor]["severe"]["threshold"] in data.lower():
            return conditions[factor]["severe"]["warning"], conditions[factor]["severe"]["ppe"]
    return None, None

def assess_environment(environmental_data):
    """
    Assesses environmental factors with improved clarity and context, suggesting appropriate PPE.
    """
    safety_warnings = []
    ppe_suggestions = []
    environmental_log = environmental_data.copy() # copy to avoid changing input data

    try:
        for factor, data in environmental_data.items():
            if factor == "radiation_level":
                warning, ppe = sub_radiation.assess_radiation(data)
                if warning:
                    safety_warnings.append(warning)
                    ppe_suggestions.append(ppe)
            else:
                warning, ppe = _check_condition(factor, data, CONDITIONS)
                if warning:
                    safety_warnings.append(warning)
                    ppe_suggestions.append(ppe)

        environmental_log["status"] = "Environment safe." if not safety_warnings else "Environment unsafe."

    except Exception as e:
        log_event(f"Error in assess_environment: {e}")
        environmental_log["error"] = str(e)

    return safety_warnings, ppe_suggestions, environmental_log

def log_event(event):
    """Logs an event with detailed error handling."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("system_directives_log.txt", "a") as f:
            f.write(f"{timestamp}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("system_directives_log.txt", "a") as f:
                f.write(f"{timestamp}: Logging error: {e}\n")
        except:
            print("Double logging error. Logging system critical failure.")

# --- sub_radiation.py ---
import logging

RADIATION_LEVELS = {
    "elevated": {"threshold": 0.001, "warning": "Elevated radiation detected.", "ppe": "Lead shielding, limit exposure."},
    "significant": {"threshold": 0.1, "warning": "Significant radiation detected.", "ppe": "Full body radiation suit, potassium iodide."},
    "lethal": {"threshold": 1, "warning": "Lethal radiation detected.", "ppe": "Immediate evacuation, maximum shielding."},
}

def assess_radiation(radiation_level):
    """Assesses radiation levels and returns warnings and PPE suggestions."""
    if radiation_level is not None:
        if radiation_level > RADIATION_LEVELS["lethal"]["threshold"]:
            return RADIATION_LEVELS["lethal"]["warning"], RADIATION_LEVELS["lethal"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["significant"]["threshold"]:
            return RADIATION_LEVELS["significant"]["warning"], RADIATION_LEVELS["significant"]["ppe"]
        elif radiation_level > RADIATION_LEVELS["elevated"]["threshold"]:
            return RADIATION_LEVELS["elevated"]["warning"], RADIATION_LEVELS["elevated"]["ppe"]
    return None, None
