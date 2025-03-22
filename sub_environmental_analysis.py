# --- sub_environmental_analysis.py ---

import json
import random

def analyze_environmental_risks(environmental_data=None):
    """
    Analyzes environmental data (either provided or simulated) and identifies potential risks.

    Args:
        environmental_data (dict, optional): A dictionary containing environmental data. If None, simulated data is used.

    Returns:
        dict: A dictionary of identified risks and their severity.
    """
    if environmental_data is None:
        # Simulate data if not provided
        environmental_data = {
            'weather': {'air_quality': {'value': random.randint(0, 100)}, 'temperature': {'value': random.randint(0, 40)}},
            'seismic_activity': {'magnitude': random.uniform(0, 5)},
            'water_quality': {'pollutants': {'value': random.uniform(0, 5)}}
        }

    risks = {}

    if environmental_data.get('weather', {}).get('air_quality', {}).get('value', 100) > 80:
        risks['high_air_pollution'] = 'High'
    if environmental_data.get('seismic_activity', {}).get('magnitude', 0) > 3:
        risks['seismic_risk'] = 'Medium'
    if environmental_data.get('water_quality', {}).get('pollutants', {}).get('value', 0) > 3:
        risks['water_contamination'] = 'High'

    return risks

def assess_habitat_suitability(environmental_data=None):
    """
    Assesses the suitability of the environment for life using data (provided or simulated).

    Args:
        environmental_data (dict, optional): A dictionary containing environmental data. If None, simulated data is used.

    Returns:
        str: A string describing the habitat suitability.
    """
    if environmental_data is None:
        # Simulate data if not provided
        environmental_data = {
            'weather': {'temperature': {'value': random.randint(0, 40)}},
            'water_quality': {'ph': {'value': random.uniform(5, 9)}}
        }

    suitability = "Moderate"

    if environmental_data.get('weather', {}).get('temperature', {}).get('value', 20) < 10 or environmental_data.get('weather', {}).get('temperature', {}).get('value', 20) > 35:
        suitability = "Unsuitable"
    elif environmental_data.get('water_quality', {}).get('ph', {}).get('value', 7) < 6 or environmental_data.get('water_quality', {}).get('ph', {}).get('value', 7) > 8:
        suitability = "Marginal"

    return suitability

def predict_environmental_changes(environmental_data=None):
    """
    Predicts future environmental changes based on data (provided or simulated).

    Args:
        environmental_data (dict, optional): A dictionary containing environmental data. If None, simulated data is used.

    Returns:
        dict: A dictionary of predicted changes.
    """
    if environmental_data is None:
        # Simulate data if not provided
        environmental_data = {
            'weather': {'temperature': {'value': random.randint(20, 30)}},
            'soil_quality': {'moisture': {'value': random.randint(20, 60)}}
        }

    predictions = {}

    if environmental_data.get('weather', {}).get('temperature', {}).get('value', 20) > 25:
        predictions['temperature_increase'] = "Likely"
    if environmental_data.get('soil_quality', {}).get('moisture', {}).get('value', 50) < 30:
        predictions['soil_drying'] = "Possible"

    return predictions

def generate_environmental_report(environmental_data=None):
    """
    Generates a comprehensive environmental report using data (provided or simulated).

    Args:
        environmental_data (dict, optional): A dictionary containing environmental data. If None, simulated data is used.

    Returns:
        str: A JSON formatted string representing the environmental report.
    """
    if environmental_data is None:
        # Simulate data if not provided
        environmental_data = {
            'weather': {'air_quality': {'value': random.randint(0, 100)}, 'temperature': {'value': random.randint(0, 40)}},
            'seismic_activity': {'magnitude': random.uniform(0, 5)},
            'water_quality': {'pollutants': {'value': random.uniform(0, 5)}, 'ph': {'value': random.uniform(5, 9)}},
            'soil_quality': {'moisture': {'value': random.randint(20, 60)}}
        }

    report = {
        'risks': analyze_environmental_risks(environmental_data),
        'suitability': assess_habitat_suitability(environmental_data),
        'predictions': predict_environmental_changes(environmental_data),
        'data': environmental_data
    }
    return json.dumps(report, indent=4)
