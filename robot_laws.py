# --- sub_robot_laws.py ---
import logging
import json

def enforce_robot_laws(environmental_data, social_health_data=None, robot_actions=None):
    """
    Enforces robot laws related to environmental and social health.

    Args:
        environmental_data (dict): Environmental data from sub_environmental.
        social_health_data (dict, optional): Social health data.
        robot_actions (dict, optional): Dictionary to store robot actions.

    Returns:
        dict: A dictionary containing the robot actions taken.
    """
    logging.info("Enforcing robot laws related to environment and social health.")

    if robot_actions is None:
        robot_actions = {}

    if environmental_data:
        if environmental_data.get('air_quality') and environmental_data['air_quality'].get('alert'):
            logging.warning("Robot intervention: High air pollution detected.")
            robot_actions['air_pollution_action'] = "Adjusting industrial activity."

        if environmental_data.get('water_quality') and environmental_data['water_quality'].get('alert'):
            logging.warning("Robot intervention: Water quality issue detected.")
            robot_actions['water_quality_action'] = "Diverting industrial waste."

        if environmental_data.get('noise_level') and environmental_data['noise_level'].get('alert'):
            logging.warning("Robot intervention: Excessive noise pollution detected.")
            robot_actions['noise_action'] = "Adjusting machinery."

    if social_health_data:
        if social_health_data.get('population_density', 0) > 1000:
            logging.warning("Robot intervention: High population density detected.")
            robot_actions['population_action'] = "Optimizing resource allocation."

        if social_health_data.get('crime_rate', 0) > 10:
            logging.warning("Robot intervention: High crime rate detected.")
            robot_actions['crime_action'] = "Increasing surveillance and security."

    return robot_actions
