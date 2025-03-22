# --- sub_robot_laws.py ---
import logging
import json
from incident_reporter import report_illegal_action  # Import incident_reporter

def enforce_robot_laws(environmental_data, social_health_data=None, robot_actions=None):
    """
    Enforces robot laws related to environmental and social health.
    """
    logging.info("Enforcing robot laws related to environment and social health.")

    if robot_actions is None:
        robot_actions = {}

    if environmental_data:
        # ... (environmental data checks remain the same) ...
        if environmental_data.get('radiation') and environmental_data['radiation'].get('alert'):
             logging.warning("Robot intervention: Radiation detected.")
             robot_actions['radiation_action'] = "Sealing off area and deploying cleanup robots."
             robot_actions['radiation_detail'] = "Sealing off zone E and deploying rad-cleaner bots"
             report_illegal_action( #Call to incident_reporter
                 event_details="Radiation Alert Triggered.",
                 sensor_data=environmental_data,
             )

    if social_health_data:
        # ... (social health data checks remain the same) ...
        if social_health_data.get('crime_rate', 0) > 10:
            logging.warning("Robot intervention: High crime rate detected.")
            robot_actions['crime_action'] = "Increasing surveillance and security."
            robot_actions['crime_detail'] = "Deploying additional security drones and increasing patrol frequency in sector G."
            report_illegal_action( #Call to incident_reporter
                event_details="High Crime Rate Detected.",
                sensor_data=social_health_data,
            )

    return robot_actions
