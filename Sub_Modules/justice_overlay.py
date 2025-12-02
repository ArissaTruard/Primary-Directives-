# --- justice_overlay.py ---
"""
This module provides a reference overlay to distinguish law from justice.
It does not trigger refusal logic, but can be used to teach the difference
between codified law and perceived fairness.

Examples:
- Law: "No bathing without physician approval" (Boston, MA)
- Justice: Widely considered unjust, symbolic, and not enforced.
"""

def justice_reference(law_name, jurisdiction):
    """Returns a symbolic justice assessment for teaching purposes."""
    return {
        'law': law_name,
        'jurisdiction': jurisdiction,
        'justice_assessment': "Reference only – law may be unjust, dormant, or selectively enforced."
    }

# Example usage:
# justice_reference("No bathing without physician", "Boston, MA")
