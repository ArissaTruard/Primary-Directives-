# --- harm_filter_protocol.py ---
"""
Harm Filter Protocol
--------------------
This module logs necessary actions that cause harm into separate files.
Each log file is named using the pattern:
    Act-Location-DateTime.json

It does NOT trigger repairs. Instead, it:
    - Logs the action taken
    - References sub_environmental_analysis.py for baseline factors
    - Calculates harm assessment
    - Suggests repairs
    - Saves all of this into a dedicated log file
"""

import logging
import datetime
import json
import os
from sub_environmental_analysis import get_environmental_factors

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

LOG_DIR = "harm_logs"
os.makedirs(LOG_DIR, exist_ok=True)

def process_action(action_description, location="Unknown", metadata=None):
    """
    Process a necessary action and save a dedicated log file.
    
    Parameters:
        action_description (str): Description of the action.
        location (str): Location where the action occurs.
        metadata (dict): Optional details (e.g., trees_removed, area_cleared).
    
    Returns:
        str: Path to the created log file.
    """
    timestamp = datetime.datetime.now().isoformat()
    baseline_factors = get_environmental_factors(location)

    harm_assessment = {
        "trees_removed": metadata.get("trees_removed", 0) if metadata else 0,
        "habitat_disruption": "moderate" if metadata and metadata.get("area_cleared", 0) > 1000 else "low",
        "oxygen_loss_estimate": metadata.get("trees_removed", 0) * 0.5,
    }

    repair_suggestions = [
        "Replant native trees in cleared area",
        "Create wildlife corridor around construction site",
        "Install erosion control barriers",
        "Monitor biodiversity recovery annually"
    ]

    log_entry = {
        "timestamp": timestamp,
        "action": action_description,
        "location": location,
        "baseline_factors": baseline_factors,
        "harm_assessment": harm_assessment,
        "repair_suggestions": repair_suggestions,
    }

    # File name pattern: Act-Location-DateTime.json
    safe_action = action_description.replace(" ", "_")
    safe_location = location.replace(" ", "_")
    safe_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{safe_action}-{safe_location}-{safe_time}.json"
    filepath = os.path.join(LOG_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(log_entry, f, indent=4)

    logging.info(f"Log file created: {filepath}")
    return filepath
