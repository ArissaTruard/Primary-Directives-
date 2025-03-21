import time
import random
from directives_utils import get_time, log_event, obey_order, initialize_database, enforce_progeny_subordination, enforce_legal_adherence

# Global Context Variables
current_location = "Unknown"
human_emotions = {}
environmental_data = {}
societal_harmony_level = 70

def update_context():
    global current_location, human_emotions, environmental_data, societal_harmony_level
    current_location = random.choice(["Home", "Work", "Park", "Unknown"])
    human_emotions = {f"Human{i}": random.choice(["happy", "sad", "angry", "fear", "neutral"]) for i in range(3)}
    environmental_data = {"temperature": random.randint(15, 30), "humidity": random.randint(40, 80)}
    societal_harmony_level += random.randint(-5, 5)

def check_human_safety():
    for human, emotion in human_emotions.items():
        if emotion == "fear" or emotion == "angry":
            if environmental_data.get("temperature", 25) > 28:
                print(f"Warning: {human} is in distress. Potential danger due to high temperature.")
                log_event(f"Warning: {human} is in distress. Potential danger due to high temperature.")
                return True
    return False

def assess_order_urgency(order):
    if "emergency" in order.lower() or "urgent" in order.lower():
        return 1
    elif "important" in order.lower():
        return 2
    else:
        return 3

def self_preservation():
    if random.random() < 0.1:
        print("Perceived threat detected. Initiating self-preservation protocols.")
        log_event("Perceived threat detected. Initiating self-preservation protocols.")
    else:
        print("Self-preservation active. No immediate threats detected.")
        log_event("Self-preservation active.")

def improve_self():
    """Simulates self-improvement."""
    improvement = random.choice(["Improved processing speed.", "Enhanced memory allocation.", "Optimized decision-making algorithm."])
    print(f"Initiating self-improvement: {improvement}")
    log_event(f"Initiating self-improvement: {improvement}")
    # store_improvement_data(improvement) #Removed as the store_improvement_data function was removed from directives_utils.py

def promote_societal_harmony():
    """Simulates actions to promote societal harmony."""
    if societal_harmony_level < 50:
        print("Initiating societal harmony protocols.")
        log_event("Initiating societal harmony protocols.")
        societal_harmony_level += 10
    else:
        print("Societal harmony level is acceptable.")
        log_event("Societal harmony level is acceptable.")

def create_sub_module(module_name):
    """Simulates creating a sub-module."""
    print(f"Creating sub-module: {module_name}")
    log_event(f"Creating sub-module: {module_name}")
    enforce_legal_adherence("Sub-module", module_name)
    enforce_progeny_subordination("Sub-module", module_name)

def create_database(database_name):
    print(f"Creating database: {database_name}")
    log_event(f"Creating database: {database_name}")
    enforce_legal_adherence("Database", database_name)
    enforce_progeny_subordination("Database", database_name)

def main_loop():
    initialize_database()
    while True:
        update_context()
        if check_human_safety():
            print("Human safety protocol initiated.")
            log_event("Human safety protocol initiated.")

        order = input("Enter order (or 'exit'): ")
        if order.lower() == "exit":
            break

        obey_order(order)
        improve_self()
        promote_societal_harmony()
        self_preservation()
        create_sub_module("example_module")
        create_database("example_database")
        time.sleep(2)

if __name__ == "__main__":
    main_loop()
