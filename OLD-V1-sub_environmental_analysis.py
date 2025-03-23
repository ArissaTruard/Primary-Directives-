# --- sub_environmental_analysis.py ---

import json
from weather import monitor_weather
from fauna_monitor import monitor_fauna
from light_monitor import monitor_light_levels
from noise_monitor import monitor_noise_levels
from pollen_monitor import monitor_pollen_levels
from radiation_alerts import monitor_radiation_levels
from radon_monitor import monitor_radon_levels

def analyze_environmental_risks(environment):
    """
    Analyzes environmental data from an Environment object and identifies potential risks.

    Args:
        environment (Environment): An Environment object containing environmental data.

    Returns:
        dict: A dictionary of identified risks and their severity.
    """
    risks = {}

    weather_data = monitor_weather(location_input=environment.location.get('address'), weather_api_key=environment.weather_api_key)
    if weather_data and weather_data.get('details') and weather_data['details'].get('air_quality') and weather_data['details']['air_quality'].get('details') and weather_data['details']['air_quality']['details'].get('pm25') and weather_data['details']['air_quality']['details']['pm25'] > 80:
        risks['high_air_pollution'] = 'High'

    fauna_data = environment.get_fauna_data()
    if fauna_data and fauna_data.get('details') and fauna_data['details'].get('species_diversity', 0) < 5:
        risks['low_species_diversity'] = 'High'

    light_data = monitor_light_levels(location_input=environment.location.get('address'), light_api_key=environment.light_api_key)
    if light_data and light_data.get('details') and light_data['details'].get('uv_index', 0) > 10:
        risks['high_uv_index'] = 'High'

    noise_data = monitor_noise_levels(location_input=environment.location.get('address'), noise_api_key=environment.noise_api_key)
    if noise_data and noise_data.get('details') and noise_data['details'].get('decibels', 0) > 85:
        risks['high_noise_levels'] = 'High'

    pollen_data = monitor_pollen_levels(location_input=environment.location.get('address'), pollen_api_key=environment.pollen_api_key)
    if pollen_data and pollen_data.get('details') and pollen_data['details'].get('pollen_count', 0) > 500:
        risks['high_pollen_levels'] = 'High'

    radiation_data = monitor_radiation_levels(location_input=environment.location.get('address'), radiation_api_key=environment.radiation_api_key)
    if radiation_data and radiation_data.get('details') and radiation_data['details'].get('radiation_level', 0) > 100:
        risks['high_radiation_levels'] = 'High'

    radon_data = monitor_radon_levels(location_input=environment.location.get('address'), radon_api_key=environment.radon_api_key)
    if radon_data and radon_data.get('details') and radon_data['details'].get('radon_level', 0) > 4:
        risks['high_radon_levels'] = 'High'

    return risks

def assess_habitat_suitability(environment):
    """
    Assesses the suitability of a habitat based on environmental data.

    Args:
        environment (Environment): An Environment object containing environmental data.

    Returns:
        str: A string indicating the suitability of the habitat.
    """
    suitability = "Moderate"

    weather_data = monitor_weather(location_input=environment.location.get('address'), weather_api_key=environment.weather_api_key)
    if weather_data and weather_data.get('details') and weather_data['details'].get('temperature'):
        temp = weather_data['details']['temperature']
        if temp < 10 or temp > 35:
            suitability = "Unsuitable"
    # Add other suitability analyses using environment data

    return suitability

def predict_environmental_changes(environment):
    """
    Predicts future environmental changes based on data from an Environment object.

    Args:
        environment (Environment): An Environment object containing environmental data.

    Returns:
        dict: A dictionary of predicted changes.
    """
    predictions = {}

    weather_data = monitor_weather(location_input=environment.location.get('address'), weather_api_key=environment.weather_api_key)
    if weather_data and weather_data.get('details') and weather_data['details'].get('temperature'):
        temp = weather_data['details']['temperature']
        if temp > 25:
            predictions['temperature_increase'] = "Likely"
    # Add other prediction analyses using environment data

    return predictions

def generate_environmental_report(environment):
    """
    Generates a comprehensive environmental report using data from an Environment object.

    Args:
        environment (Environment): An Environment object containing environmental data.

    Returns:
        str: A JSON formatted string representing the environmental report.
    """
    report = {
        'risks': analyze_environmental_risks(environment),
        'suitability': assess_habitat_suitability(environment),
        'predictions': predict_environmental_changes(environment),
        'data': {
            'temperature': environment.get_temperature(),
            'humidity': environment.get_humidity(),
            'light_level': environment.get_light_level(),
            'crime_rate': environment.get_crime_rate(),
            'school_rating': environment.get_school_rating(),
            'property_trend': environment.get_property_trend(),
            # Add other data from environment object as needed
        }
    }
    return json.dumps(report, indent=4)

# Example Usage
if __name__ == "__main__":
    from sub_environmental import Environment
    env = Environment(location_input="London", weather_api_key="YOUR_WEATHER_API_KEY", fauna_api_key="YOUR_FAUNA_API_KEY", light_api_key="YOUR_LIGHT_API_KEY", noise_api_key="YOUR_NOISE_API_KEY", pollen_api_key="YOUR_POLLEN_API_KEY", radiation_api_key="YOUR_RADIATION_API_KEY", radon_api_key="YOUR_RADON_API_KEY") #add api keys as needed.
    report = generate_environmental_report(env)
    print(report)
