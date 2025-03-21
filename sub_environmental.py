import datetime
import logging

def assess_environment(environmental_data):
    """
    Assesses environmental factors and suggests PPE.

    Args:
        environmental_data (dict): A dictionary of environmental data.

    Returns:
        tuple: A tuple containing (safety_warnings, ppe_suggestions, environmental_log)
    """
    safety_warnings = []
    ppe_suggestions = []
    environmental_log = {}

    temperature = environmental_data.get("temperature", None)
    humidity = environmental_data.get("humidity", None)
    uv_index = environmental_data.get("uv_index", None)
    allergen_density = environmental_data.get("allergen_density", None)
    air_quality = environmental_data.get("air_quality", None)
    radiation_level = environmental_data.get("radiation_level", None)
    smog_level = environmental_data.get("smog_level", None)
    weather_overall = environmental_data.get("weather_overall", None)

    environmental_log["temperature"] = temperature
    environmental_log["humidity"] = humidity
    environmental_log["uv_index"] = uv_index
    environmental_log["allergen_density"] = allergen_density
    environmental_log["air_quality"] = air_quality
    environmental_log["radiation_level"] = radiation_level
    environmental_log["smog_level"] = smog_level
    environmental_log["weather_overall"] = weather_overall

    try:
        if temperature is not None and temperature > 30:
            safety_warnings.append("High temperature detected.")
            ppe_suggestions.append("Hydration, light clothing.")
        if humidity is not None and humidity > 70:
            safety_warnings.append("High humidity detected.")
            ppe_suggestions.append("Light, breathable clothing.")
        if uv_index is not None and uv_index > 7:
            safety_warnings.append("High UV index detected.")
            ppe_suggestions.append("Sunscreen, sunglasses, hat.")
        if allergen_density is not None and allergen_density > 5:
            safety_warnings.append("High allergen density detected.")
            ppe_suggestions.append("Mask, allergy medication.")
        if air_quality is not None and air_quality > 100:
            safety_warnings.append("Poor air quality detected.")
            ppe_suggestions.append("Mask, avoid strenuous activity.")
        if radiation_level is not None and radiation_level > 10:
            safety_warnings.append("High radiation level detected.")
            ppe_suggestions.append("Protective shielding, limit exposure.")
        if smog_level is not None and smog_level > 50:
            safety_warnings.append("High smog level detected.")
            ppe_suggestions.append("Mask, limit outdoor exposure.")
        if weather_overall is not None and "severe" in weather_overall.lower():
            safety_warnings.append("Severe weather conditions.")
            ppe_suggestions.append("Seek shelter, appropriate weather gear.")

        if not safety_warnings:
            environmental_log["status"] = "Environment safe."
        else:
            environmental_log["status"] = "Environment unsafe."
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
            with open("system_directives_log.txt", "a") as f:
                f.write(f"{timestamp}: Logging error: {e}\n")
        except:
            print("Double logging error. Logging system critical failure.")
