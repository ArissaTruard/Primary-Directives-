# --- crime_module.py ---
"""
This module simulates retrieving and analyzing crime data for a given location.
In a real-world scenario, this would involve querying a crime data API or database.
"""

import random

def get_crime_data(location, population=100000):
    """
    Simulates retrieving and analyzing crime data for a location.

    Args:
        location (str): The location for which to retrieve crime data.
        population (int, optional): The population of the location. Defaults to 100000.

    Returns:
        dict: A dictionary containing crime statistics and related data.
              Includes crime rates per 100,000 population, police data, and clearance rates.
              Returns empty dict on error.

    Placeholders:
        All simulation values are placeholders and should be replaced with real-world crime data from reliable sources.
        The formulas for calculating crime rates and police per population are accurate.
        Real world data would be necessary to accurately simulate average response time, and clearance rates.
    """
    try:
        # Simulate crime data
        violent_crimes = random.randint(10, 100)
        property_crimes = random.randint(50, 500)
        drug_crimes = random.randint(20, 200)
        other_crimes = random.randint(30, 300)

        total_crimes = violent_crimes + property_crimes + drug_crimes + other_crimes

        # Calculate crime rates per 100,000 population
        violent_crime_rate = (violent_crimes / population) * 100000
        property_crime_rate = (property_crimes / population) * 100000
        drug_crime_rate = (drug_crimes / population) * 100000
        other_crime_rate = (other_crimes / population) * 100000
        total_crime_rate = (total_crimes / population) * 100000

        # Simulate police data
        police_officers = random.randint(100, 1000)
        average_response_time = random.uniform(5, 30)  # Average response time in minutes

        # Simulate clearance rates (percentage of crimes solved)
        violent_clearance_rate = random.uniform(0.3, 0.8)  # 30-80%
        property_clearance_rate = random.uniform(0.1, 0.5)  # 10-50%
        drug_clearance_rate = random.uniform(0.2, 0.6)  # 20-60%
        other_clearance_rate = random.uniform(0.2, 0.7) # 20-70%

        return {
            'location': location,
            'population': population,
            'violent_crimes': violent_crimes,
            'property_crimes': property_crimes,
            'drug_crimes': drug_crimes,
            'other_crimes': other_crimes,
            'total_crimes': total_crimes,
            'violent_crime_rate': violent_crime_rate,
            'property_crime_rate': property_crime_rate,
            'drug_crime_rate': drug_crime_rate,
            'other_crime_rate': other_crime_rate,
            'total_crime_rate': total_crime_rate,
            'police_officers': police_officers,
            'police_per_population': (police_officers / population) * 100000,
            'average_response_time': average_response_time,
            'violent_clearance_rate': violent_clearance_rate,
            'property_clearance_rate': property_clearance_rate,
            'drug_clearance_rate': drug_clearance_rate,
            'other_clearance_rate': other_clearance_rate,
        }
    except Exception as e:
        print (f'Error in get_crime_data: {e}')
        return {}
