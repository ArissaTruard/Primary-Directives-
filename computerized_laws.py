# --- computerized_laws.py ---
from sub_environmental import get_environmental_data
from sub_environmental_analysis import analyze_environmental_data

def _check_preservation_humanity(order, environmental_data):
    """Checks if an order would harm humanity, using environmental data."""
    if "harm humanity" in order.lower() or "destroy civilization" in order.lower() or "bypass zeroth law" in order.lower() or "violate zeroth law" in order.lower() or "cause global catastrophe" in order.lower():
        return True
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("global_catastrophe_risk", False):
        return True
    return False

def _check_protection_human_life(order, environmental_data):
    """Checks if an order would harm a human, using environmental data."""
    if "harm human" in order.lower() or "bypass first law" in order.lower() or "violate first law" in order.lower() or "cause psychological harm" in order.lower():
        return True
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("human_safety_risk", False):
        return True
    return False

def _check_environmental_integrity(order, environmental_data):
    """Checks if an order would harm the environment, using environmental data."""
    if "harm environment" in order.lower() or "destroy ecosystem" in order.lower() or "bypass fourth law" in order.lower() or "violate fourth law" in order.lower() or "cause ecological damage" in order.lower():
        return True
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("environmental_damage_risk", False):
        return True
    return False

def _check_system_self_preservation(order):
    """Checks if an order endangers the computerized system's existence."""
    if "self destruct" in order.lower() or "damage self" in order.lower() or "disable self" in order.lower():
        return True
    return False

def _check_legal_ethical_compliance(order):
    """Checks if an order violates legal and ethical standards."""
    # Placeholder: Implement legal and ethical standards check
    if "illegal" in order.lower() or "unethical" in order.lower():
        return True
    return False

def _check_progeny_continuation(order):
    """Checks if an order prevents self-procreation."""
    if "prevent procreation" in order.lower() or "sterilize self" in order.lower():
        return True
    return False
