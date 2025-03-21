# --- soil_quality_monitor.py ---
import logging
import datetime
from typing import Optional, Dict

def monitor_soil_quality(
    moisture: Optional[float] = None,
    temperature: Optional[float] = None,
    location: str = "unknown",
    ph: Optional[float] = None,
    nitrogen: Optional[float] = None,
    phosphorus: Optional[float] = None,
    potassium: Optional[float] = None,
    heavy_metals: Optional[Dict[str, float]] = None,
    pesticides: Optional[Dict[str, float]] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
) -> Dict[str, any]:
    """
    Monitors and analyzes soil moisture, temperature, pH, nutrients, heavy metals, and pesticides.

    Args:
        moisture: Soil moisture percentage (optional).
        temperature: Soil temperature in Celsius (optional).
        location: Location of the soil sensor (default: "unknown").
        ph: Soil pH level (optional).
        nitrogen: Nitrogen content in the soil (mg/kg) (optional).
        phosphorus: Phosphorus content in the soil (mg/kg) (optional).
        potassium: Potassium content in the soil (mg/kg) (optional).
        heavy_metals: Dictionary of heavy metal concentrations (e.g., {"lead": 10, "arsenic": 5}) (optional).
        pesticides: Dictionary of pesticide concentrations (optional).
        latitude: Latitude of the soil testing location (optional).
        longitude: Longitude of the soil testing location (optional).

    Returns:
        A dictionary containing the analysis results, including location data. Example:
        {
            "alert": True,
            "message": "Low soil moisture detected. High lead concentration detected.",
            "details": {
                "moisture": "Moisture: 15%",
                "lead": "lead: 12"
            },
            "location": {"latitude": 34.0522, "longitude": -118.2437"} #or {"location_name": "My Garden"}
        }
    """
    timestamp = datetime.datetime.now()
    logging.info(
        f"Soil data at {location}: Moisture={moisture}, Temperature={temperature}, pH={ph}, "
        f"Nitrogen={nitrogen}, Phosphorus={phosphorus}, Potassium={potassium}, "
        f"Heavy Metals={heavy_metals}, Pesticides={pesticides}, Latitude={latitude}, Longitude={longitude}"
    )

    analysis = {"alert": False, "message": "Soil conditions normal", "details": {}}
    alerts = []

    if moisture is not None and moisture < 20:
        alerts.append("Low soil moisture detected.")
        analysis["details"]["moisture"] = f"Moisture: {moisture}%"

    if temperature is not None and temperature > 35:
        alerts.append("High soil temperature detected.")
        analysis["details"]["temperature"] = f"Temperature: {temperature}°C"

    if ph is not None and (ph < 5.5 or ph > 7.5):
        alerts.append("Soil pH level is outside the optimal range.")
        analysis["details"]["ph"] = f"pH: {ph}"

    if nitrogen is not None and nitrogen < 50:
        alerts.append("Low nitrogen content detected.")
        analysis["details"]["nitrogen"] = f"Nitrogen: {nitrogen} mg/kg"

    if phosphorus is not None and phosphorus < 20:
        alerts.append("Low phosphorus content detected.")
        analysis["details"]["phosphorus"] = f"Phosphorus: {phosphorus} mg/kg"

    if potassium is not None and potassium < 100:
        alerts.append("Low potassium content detected.")
        analysis["details"]["potassium"] = f"Potassium: {potassium} mg/kg"

    if heavy_metals:
        for metal, concentration in heavy_metals.items():
            if concentration is not None and concentration > 10:
                alerts.append(f"High {metal} concentration detected.")
                analysis["details"][metal] = f"{metal}: {concentration}"

    if pesticides:
        for pesticide, concentration in pesticides.items():
            if concentration is not None and concentration > 5:
                alerts.append(f"High {pesticide} concentration detected.")
                analysis["details"][pesticide] = f"{pesticide}: {concentration}"

    if alerts:
        analysis["alert"] = True
        analysis["message"] = " ".join(alerts)

    if latitude is not None and longitude is not None:
        analysis["location"] = {"latitude": latitude, "longitude": longitude}
    elif location != "unknown":
        analysis["location"] = {"location_name": location}

    return analysis
