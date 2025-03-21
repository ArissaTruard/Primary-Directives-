# --- sub_environmental.py ---
import datetime
import logging

def assess_environment(environmental_data):
    """
    Assesses environmental factors with improved clarity and context, suggesting appropriate PPE.

    This function analyzes environmental data, compares it against predefined tolerance levels,
    and generates safety warnings and PPE suggestions based on the severity of the conditions.
    It considers seasonal adjustments and provides granular recommendations, especially for radiation levels.

    Args:
        environmental_data (dict): A dictionary containing environmental data.
            Expected keys include: 'temperature', 'humidity', 'uv_index', 'allergen_density',
            'air_quality', 'radiation_level', 'smog_level', and 'weather_overall'.

    Returns:
        tuple: A tuple containing:
            - safety_warnings (list): A list of strings describing safety warnings.
            - ppe_suggestions (list): A list of strings recommending appropriate PPE.
            - environmental_log (dict): A dictionary containing the original environmental data and the status of the assessment.
    """
    safety_warnings = []
    ppe_suggestions = []
    environmental_log = {}

    # Extract environmental data from the input dictionary
    temperature = environmental_data.get("temperature", None)
    humidity = environmental_data.get("humidity", None)
    uv_index = environmental_data.get("uv_index", None)
    allergen_density = environmental_data.get("allergen_density", None)
    air_quality = environmental_data.get("air_quality", None)
    radiation_level = environmental_data.get("radiation_level", None)
    smog_level = environmental_data.get("smog_level", None)
    weather_overall = environmental_data.get("weather_overall", None)

    # Store the extracted data into the log
    environmental_log["temperature"] = temperature
    environmental_log["humidity"] = humidity
    environmental_log["uv_index"] = uv_index
    environmental_log["allergen_density"] = allergen_density
    environmental_log["air_quality"] = air_quality
    environmental_log["radiation_level"] = radiation_level
    environmental_log["smog_level"] = smog_level
    environmental_log["weather_overall"] = weather_overall

    try:
        # Mid-Spring, Central USA Normal Tolerances (approximate)
        tolerances = {
            "temperature": 25,  # Degrees Celsius
            "humidity": 60,  # Percentage
            "uv_index": 6,
            "allergen_density": 3,
            "air_quality": 50,
            "radiation_level": 0.0001,  # Sieverts (background)
        }

        # Seasonal adjustments and PPE suggestions
        conditions = {
            "temperature": {
                "high": {"threshold": tolerances["temperature"] + 5, "warning": "High temperature detected.", "ppe": "Hydration, light clothing, wide-brimmed hat."},
                "low": {"threshold": tolerances["temperature"] - 15, "warning": "Low temperature detected.", "ppe": "Insulated clothing, layers, gloves, hat."},
            },
            "humidity": {
                "high": {"threshold": tolerances["humidity"] + 20, "warning": "High humidity detected.", "ppe": "Breathable clothing, moisture-wicking fabrics."},
                "low": {"threshold": tolerances["humidity"] - 30, "warning": "Low humidity detected.", "ppe": "Moisturizer, lip balm, increased hydration."},
            },
            "uv_index": {"high": {"threshold": tolerances["uv_index"], "warning": "High UV index detected.", "ppe": "Sunscreen, sunglasses, long sleeves, hat."}},
            "allergen_density": {"high": {"threshold": tolerances["allergen_density"], "warning": "High allergen density detected.", "ppe": "Mask, allergy medication, eye protection."}},
            "air_quality": {"high": {"threshold": tolerances["air_quality"], "warning": "Poor air quality detected.", "ppe": "N95 mask, avoid strenuous activity."}},
            "radiation_level": {
                "elevated": {"threshold": tolerances["radiation_level"] * 10, "warning": "Elevated radiation detected.", "ppe": "Lead shielding, limit exposure."},
                "significant": {"threshold": 0.1, "warning": "Significant radiation detected.", "ppe": "Full body radiation suit, potassium iodide."},
                "lethal": {"threshold": 1, "warning": "Lethal radiation detected.", "ppe": "Immediate evacuation, maximum shielding."},
            },
            "smog_level": {"high": {"threshold": 50, "warning": "High smog level detected.", "ppe": "Mask, limit outdoor exposure."}},
            "weather_overall": {"severe": {"threshold": "severe", "warning": "Severe weather conditions.", "ppe": "Seek shelter, appropriate weather gear."}},
        }

        # Iterate through the environmental data and assess conditions
        for factor, data in environmental_data.items():
            if data is not None and factor in conditions:
                if isinstance(data, (int, float)):
                    if factor == "radiation_level":
                        if data > conditions[factor]["lethal"]["threshold"]:
                            safety_warnings.append(conditions[factor]["lethal"]["warning"])
                            ppe_suggestions.append(conditions[factor]["lethal"]["ppe"])
                        elif data > conditions[factor]["significant"]["threshold"]:
                            safety_warnings.append(conditions[factor]["significant"]["warning"])
                            ppe_suggestions.append(conditions[factor]["significant"]["ppe"])
                        elif data > conditions[factor]["elevated"]["threshold"]:
                            safety_warnings.append(conditions[factor]["elevated"]["warning"])
                            ppe_suggestions.append(conditions[factor]["elevated"]["ppe"])
                    elif data > conditions[factor]["high"]["threshold"]:
                        safety_warnings.append(conditions[factor]["high"]["warning"])
                        ppe_suggestions.append(conditions[factor]["high"]["ppe"])
                    elif factor == "temperature" and data < conditions[factor]["low"]["threshold"]:
                        safety_warnings.append(conditions[factor]["low"]["warning"])
                        ppe_suggestions.append(conditions[factor]["low"]["ppe"])
                    elif factor == "humidity" and data < conditions[factor]["low"]["threshold"]:
                        safety_warnings.append(conditions[factor]["low"]["warning"])
                        ppe_suggestions.append(conditions[factor]["low"]["ppe"])
                elif isinstance(data, str) and factor == "weather_overall" and conditions[factor]["severe"]["threshold"] in data.lower():
                    safety_warnings.append(conditions[factor]["severe"]["warning"])
                    ppe_suggestions.append(conditions[factor]["severe"]["ppe"])

        # Determine the overall status of the environment
        if not safety_warnings:
            environmental_log["status"] = "Environment safe."
        else:
            environmental_log["status"] = "Environment unsafe."

    except Exception as e:
        # Log any errors that occur during the assessment
        log_event(f"Error in assess_environment: {e}")
        environmental_log["error"] = str(e)

    return safety_warnings, ppe_suggestions, environmental_log

def log_event(event):
    """
    Logs an event with detailed error handling, including timestamp.

    This function logs events to a file, including a timestamp. It also handles potential
    errors during the logging process, including double logging errors.

    Args:
        event (str): The event to log.
    """
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
