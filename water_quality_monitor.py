# --- water_quality_monitor.py ---
import logging
import datetime

def monitor_water_quality(
    ph,
    turbidity,
    dissolved_oxygen,
    heavy_metals,
    pollutants,
    test_location,
    inquiry_location=None,  # Added inquiry_location parameter
):
    """Monitors and analyzes water quality data.

    Args:
        ph (float): pH level.
        turbidity (float): Turbidity level.
        dissolved_oxygen (float): Dissolved oxygen level.
        heavy_metals (dict): Heavy metal concentrations.
        pollutants (dict): Pollutant concentrations.
        test_location (str): Location where the water quality test was conducted.
        inquiry_location (str, optional): Location where the water quality inquiry is being made.
    """
    timestamp = datetime.datetime.now()
    log_message = f"Water quality data at {test_location}: pH={ph}, Turbidity={turbidity}, DO={dissolved_oxygen}, Heavy Metals={heavy_metals}, Pollutants={pollutants}"
    if inquiry_location:
        log_message += f", Inquiry Location: {inquiry_location}"
    logging.info(log_message)

    analysis = {"alert": False, "message": "Water quality normal", "details": {}}

    if ph < 6.5 or ph > 8.5 or turbidity > 10:
        logging.warning(f"Water quality outside acceptable range at {test_location}")
        analysis["alert"] = True
        analysis["message"] = "Unacceptable water quality"
        analysis["details"]["ph"] = ph
        analysis["details"]["turbidity"] = turbidity
        analysis["details"]["dissolved_oxygen"] = dissolved_oxygen
        analysis["details"]["heavy_metals"] = heavy_metals
        analysis["details"]["pollutants"] = pollutants

    return analysis
