# --- sub_environmental.py ---
import random
import logging

def get_environmental_data():
    """Retrieves environmental data (simulated)."""
    try:
        data = {
            "temperature": random.uniform(15, 30),
            "humidity": random.uniform(40, 80),
            "air_quality": random.choice(["Good", "Moderate", "Unhealthy"]),
            "radiation": {
                "level": random.uniform(0, 100),
                "alert": random.choice([True, False])
            }
        }
        logging.info("Environmental data retrieved.")
        return data
    except Exception as e:
        logging.error(f"Error retrieving environmental data: {e}")
        return None
