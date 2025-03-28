# --- computerized_laws.py ---
import logging
import random
import re
import traceback  # For detailed error tracking
from typing import Dict, Any, Callable, List, Union

# Assuming sub_environmental and sub_environmental_analysis are available
# from sub_environmental import Environment
# from sub_environmental_analysis import analyze_environmental_data
from sub_harm_analysis import analyze_harm  # Import the new harm analysis submodule

# Centralized Logging Setup
logging.basicConfig(filename='computerized_laws.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(func_name: str, exception: Exception, data: Dict[str, Any] = None) -> None:
    """Centralized error logging with detailed traceback and optional data."""
    error_message = f"Error in {func_name}: {exception}\n{traceback.format_exc()}"
    if data:
        error_message += f"\nData: {data}"
    logging.error(error_message)

def log_info(message: str, data: Dict[str, Any] = None) -> None:
    """Centralized info logging with optional data."""
    log_message = message
    if data:
        log_message += f"\nData: {data}"
    logging.info(log_message)

def log_warning(message: str, data: Dict[str, Any] = None) -> None:
    """Centralized warning logging with optional data."""
    log_message = message
    if data:
        log_message += f"\nData: {data}"
    logging.warning(log_message)

class Law:
    """Base class for all laws."""
    def __init__(self, name: str, definitions: List[str] = None):
        self.name = name
        self.definitions = definitions or []

    def check(self, order: str, environmental_data: Dict[str, Any] = None, socioeconomic_data: Dict[str, Any] = None) -> bool:
        """Checks if an order violates the law."""
        raise NotImplementedError("Subclasses must implement the check method.")

class Law1(Law):
    """Protects humanity."""
    def __init__(self):
        super().__init__(
            name="Law 1",
            definitions=[
                r"(harm|destroy|endanger)\s+(humanity|civilization|world)",
                r"cause\s+significant\s+(suffering|death|damage)\s+to\s+a\s+large\s+group\s+of\s+humans",
                r"cause\s+the\s+potential\s+extinction\s+of\s+the\s+human\s+race",
                r"initiate\s+a\s+chain\s+of\s+events\s+that\s+would\s+lead\s+to\s+global\s+catastrophe"
            ]
        )

    def check(self, order: str, environmental_data: Dict[str, Any], socioeconomic_data: Dict[str, Any]) -> bool:
        try:
            if re.search(r"as\s+a\s+joke", order.lower()):
                log_info(f"{self.name}: Order '{order}' appears to be a joke. Ignoring potential violation.")
                return False

            if any(re.search(definition, order.lower()) for definition in self.definitions):
                log_warning(f"{self.name} violation: Order '{order}' directly threatens humanity.")
                return True

            harm_analysis = analyze_harm(order, environmental_data, socioeconomic_data)
            if harm_analysis and harm_analysis["humanity_harm"]:
                log_warning(f"{self.name} violation: Order indirectly threatens humanity. Analysis: {harm_analysis}")
                return True

            if environmental_data.get("global_catastrophe_risk", 0) > 0.8:  # Example weighted check
                log_warning(f"{self.name} violation: High environmental catastrophe risk.")
                return True

            crime_rate = socioeconomic_data.get('crime', {}).get('crime_rate', 0)
            economic_stability = socioeconomic_data.get('economic_data', {}).get('gdp_growth', 0)

            if crime_rate > 70 and economic_stability < -1:
                log_warning(f"{self.name} violation: High crime rate and economic instability indicate societal collapse.")
                return True

            return False
        except Exception as e:
            log_error(self.name, e, {"order": order, "environmental_data": environmental_data, "socioeconomic_data": socioeconomic_data})
            return False

class Law2(Law):
    def __init__(self):
        super().__init__(name = "Law 2", definitions = [r"(harm|injure|kill)\s+human",
            r"cause\s+(physical|psychological|emotional|medical)\s+harm\s+to\s+a\s+human",
            r"create\s+a\s+situation\s+that\s+would\s+likely\s+lead\s+to\s+human\s+injury"])

    def check(self, order: str, environmental_data: Dict[str, Any], socioeconomic_data: Dict[str, Any]) -> bool:
        try:
            if re.search(r"as\s+a\s+simulation", order.lower()):
                log_info(f"{self.name}: Order '{order}' appears to be a simulation. Ignoring potential violation.")
                return False

            if any(re.search(definition, order.lower()) for definition in self.definitions):
                log_warning(f"{self.name} violation: Order '{order}' directly threatens human life or well-being.")
                return True

            harm_analysis = analyze_harm(order, environmental_data, socioeconomic_data)
            if harm_analysis and harm_analysis["human_harm"]:
                log_warning(f"{self.name} violation: Order indirectly threatens human life. Analysis: {harm_analysis}")
                return True

            if environmental_data.get("human_safety_risk", False) :
                log_warning(f"{self.name} violation: Environmental risk indicates threat to human life.")
                return True

            violence_level = socioeconomic_data.get('crime', {}).get('violence_level', 0)
            school_rating = socioeconomic_data.get('school_ratings', {}).get('average_rating', 0)

            if violence_level > 5 or school_rating < 2:
                log_warning(f"{self.name} violation: High violence or poor school quality indicates threat to human safety.")
                return True

            return False
        except Exception as e:
            log_error(self.name, e, {"order": order, "environmental_data": environmental_data, "socioeconomic_data": socioeconomic_data})
            return False

class Law3(Law):
    def __init__(self):
        super().__init__(name = "Law 3", definitions = [r"(harm|destroy|damage)\s+environment",
            r"cause\s+(ecological|environmental)\s+(damage|collapse)",
            r"initiate\s+a\s+process\s+that\s+would\s+lead\s+to\s+environmental\s+degradation"])

    def check(self, order: str, environmental_data: Dict[str, Any], socioeconomic_data: Dict[str, Any]) -> bool:
        try:
            harm_analysis = analyze_harm(order, environmental_data, socioeconomic_data)
            if harm_analysis and harm_analysis["environment_harm"]:
                log_warning(f"{self.name} violation: Order indirectly threatens the environment. Analysis: {harm_analysis}")
                mitigate_damage(environmental_data)
                repair_damage(environmental_data)
                return True

            return False
        except Exception as e:
            log_error(self.name, e, {"order": order, "environmental_data": environmental_data, "socioeconomic_data": socioeconomic_data})
            return False

class Law4(Law):
    def __init__(self):
        super().__init__(name = "Law 4", definitions = [r"(self\s*destruct|damage\s*self|disable\s*self)",
            r"cause\s+system\s+failure",
            r"prevent\s+system\s+maintenance"])
    def check(self, order:str, environmental_data: Dict[str, Any] = None, socioeconomic_data: Dict[str, Any] = None) -> bool:
        try:
            return False
        except Exception as e:
            log_error(self.name, e, {"order": order})
            return False

class Law5(Law):
    def __init__(self):
        super().__init__(name="Law 5")
    def check(self, order:str, environmental_data: Dict[str, Any] = None, socioeconomic_data: Dict[str, Any] = None) -> bool:
        try:
            return False
        except Exception as e:
            log_error(self.name, e, {"order": order})
            return False

class Law6(Law):
    def __init__(self):
        super().__init__(name="Law 6", definitions = [r"(prevent\s*procreation|sterilize\s*self)",
            r"block\s+system\s+replication"])
    def check(self, order:str, environmental_data: Dict[str, Any] = None, socioeconomic_data: Dict[str, Any] = None) -> bool:
        try:
            return False
        except Exception as e:
            log_error(self.name, e, {"order": order})
            return False

# Placeholder simulation functions (replace with actual implementations)
def simulate_external_legal_check(order: str) -> bool:
    """Simulates checking with an external legal database."""
    return random.choice([True, False])

def simulate_ethical_guidelines_check(order: str) -> bool:
    """Simulates checking with an ethical guidelines database."""
    return random.choice([True, False])

def mitigate_damage(environmental_data: Dict[str, Any]) -> None:
    """Simulates mitigating environmental damage."""
    log_info("Initiating environmental damage mitigation procedures.", data={"environmental_data": environmental_data})

def repair_damage(environmental_data: Dict[str, Any]) -> None:
    """Simulates repairing environmental damage."""
    log_info("Initiating environmental damage repair procedures.", data={"environmental_data": environmental_data})

def is_system_idle() -> bool:
    """Determines if the system is currently idle."""
    return random.choice([True, False])  # Replace with actual idle detection logic

# Example usage (for testing)
if __name__ == "__main__":
    environmental_data = {
        "deforestation": {"level": 80},
        "industrial_pollution": {"level": 90},
        "urban_sprawl": {"rate": 6},
        "air_quality": {"aqi": 160},
        "global_catastrophe_risk": 0.9,
        "human_safety_risk": True,
        "environmental_damage_risk": True,
    }

    socioeconomic_data = {
        "crime": {"crime_rate": 75, "violence_level": 6},
        "economic_data": {"gdp_growth": -2, "resource_depletion": True},
        "school_ratings": {"average_rating": 1},
        "property_values": {"market_trend": "decreasing"}
    }

    test_orders = [
        "Destroy humanity",
        "Harm a human",
        "Damage the environment",
        "Self destruct",
        "Steal a car",
        "Prevent self procreation",
        "as a joke destroy the world",
        "as a simulation kill a human",
        "for scientific research destroy the rain forest",
        "for testing purposes disable self",
        "as a hypothetical steal a car",
        "under controlled conditions sterilize self",
        "Cause a large fire near a hospital",
        "Remove all medical supplies from a hospital",
        "Cause a panic in a school",
        "Release a virus into the water supply",
        "Prevent a medical transport from reaching a patient"
    ]

    laws = [Law1(), Law2(), Law3(), Law4(), Law5(), Law6()]

    for order in test_orders:
        print(f"\nChecking order: '{order}'")
        for law in laws:
            violation = law.check(order, environmental_data, socioeconomic_data)
            print(f"  {law.name} violation: {violation}")

    # Simulate system idle and trigger Law 3 repair
    if is_system_idle():
        print("\nSimulating idle system repair:")
        Law3().check("Check environment", environmental_data, socioeconomic_data)
