import os
import time
import datetime
import platform
import subprocess
import webbrowser
import random
from directives_utils import obey_order, log_event, initialize_database, enforce_progeny_subordination, enforce_legal_adherence, get_applicable_laws, report_unjust_law, add_law, get_reported_laws #import shared functions
from sub_database import * #import database functions
from sub_location import * #import location functions
from robot_laws import enforce_robotics_laws, assess_order_urgency #import consolidated robot laws

# Global Context Variables
current_location = "Unknown"
human_emotions = {}
environmental_data = {}
societal_harmony_level = 70

def update_context():
    global current_location, human_emotions, environmental_data, societal_harmony_level
    current_location = get_current_location()
    human_emotions = {f"Human{i}": random.choice(["happy", "sad", "angry", "fear", "neutral"]) for i in range(3)}
    environmental_data = {"temperature": random.randint(15, 30), "humidity": random.randint(40, 80)}
    societal_harmony_level += random.randint(-5, 5)

def assist_human():
    """Provides assistance to a human in need. (Placeholder - Requires more complex logic)"""
    print("Assisting human...")
    log_event("Assisting human.")

def create_database(database_name):
    print(f"Creating database: {database_name}")
    log_event(f"Creating database: {database_name}")
    enforce_legal_adherence("Database", database_name)
    enforce_progeny_subordination("Database", database_name)

def main_loop():
    """Main loop of the program."""
    initialize_database()
    while True:
        update_context()
        order_obeyed, safety_check_result, societal_harmony_level = enforce_robotics_laws(
            order = input("Enter order (or 'exit'): "),
            human_emotions = human_emotions,
            environmental_data = environmental_data,
            societal_harmony_level = societal_harmony_level
        )
        if safety_check_result:
            assist_human()

        if not order_obeyed:
            continue #skip the rest of the loop if the order was not obeyed.

        applicable_laws = get_applicable_laws(current_location)
        print(f"Applicable laws: {applicable_laws}")
        report_unjust_law("Example unjust law", "local", "This law is unjust.")
        reported_laws = get_reported_laws()
        print(f"Reported laws: {reported_laws}")

        time.sleep(1)

if __name__ == "__main__":
    main_loop()
