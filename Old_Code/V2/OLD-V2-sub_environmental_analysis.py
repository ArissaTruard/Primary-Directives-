# --- sub_environmental_analysis.py ---
def analyze_environmental_data(data):
    """Analyzes environmental data and returns risk assessments."""
    if not data:
        return None
    try:
        analysis = {
            "human_safety_risk": data["temperature"] > 35 or data["air_quality"] == "Unhealthy" or (data["radiation"]["level"] > 50 and data["radiation"]["alert"]),
            "global_catastrophe_risk": data["radiation"]["level"] > 90,
            "environmental_damage_risk": data["air_quality"] == "Unhealthy" or data["radiation"]["level"] > 70
        }
        return analysis
    except (KeyError, TypeError) as e:
        logging.error(f"Error analyzing environmental data: {e}")
        return None
