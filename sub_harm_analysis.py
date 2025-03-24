# --- sub_harm_analysis.py ---
import re
import logging
from typing import Dict, Any

logging.basicConfig(filename='harm_analysis.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_harm(order: str, environmental_data: Dict[str, Any], socioeconomic_data: Dict[str, Any]) -> Dict[str, bool]:
    """Analyzes an order to determine if it could cause harm, directly or indirectly."""
    harm_analysis = {
        "humanity_harm": False,
        "human_harm": False,
        "environment_harm": False,
    }

    try:
        # Check for direct harm indicators
        if re.search(r"(harm|destroy|kill|injure|damage)", order.lower()):
            harm_analysis["humanity_harm"] = True
            harm_analysis["human_harm"] = True
            harm_analysis["environment_harm"] = True
            return harm_analysis

        # Check for indirect harm indicators based on order, environmental, and socioeconomic data
        # Humanity harm checks
        if re.search(r"(war|genocide|mass destruction|global catastrophe)", order.lower()):
            harm_analysis["humanity_harm"] = True

        if environmental_data.get("global_catastrophe_risk", 0) > 0.7 or \
           socioeconomic_data.get("economic_data", {}).get("resource_depletion", False):
            harm_analysis["humanity_harm"] = True

        # Human harm checks
        if re.search(r"(attack|assault|poison|medical emergency|cause panic)", order.lower()):
            harm_analysis["human_harm"] = True

        if environmental_data.get("human_safety_risk", False) or \
           socioeconomic_data.get("crime", {}).get("violence_level", 0) > 4:
            harm_analysis["human_harm"] = True

        # Environment harm checks
        if re.search(r"(deforestation|pollution|chemical spill|ecological damage)", order.lower()):
            harm_analysis["environment_harm"] = True

        if environmental_data.get("environmental_damage_risk", False) or \
           environmental_data.get("deforestation", {}).get("level", 0) > 60:
            harm_analysis["environment_harm"] = True

        # Medical Harm Checks
        if re.search(r"(medical emergency|prevent medical transport|remove medical supplies|release virus)", order.lower()):
            harm_analysis["human_harm"] = True

        return harm_analysis

    except Exception as e:
        logging.error(f"Error in analyze_harm: {e}")
        return harm_analysis
