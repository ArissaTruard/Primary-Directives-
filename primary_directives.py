# --- primary_directives.py ---
import os
import time
import datetime
import platform
import subprocess
import webbrowser
import logging
import random
from sub_database import *
from sub_location import *
from sub_system import shutdown, request_approval, analyze_order, monitor_system_health, adjust_law_priority
from sub_environmental import Environment # Import the modified Environment class
from sub_robot_laws import enforce_robot_laws
from sub3_complex_rule import complex_rule_enforcer
from computerized_laws import * # Import all law functions
from sub_module_integration import ModuleIntegrationManager # Import the new Module Integration Manager

# Initialize Module Integration Manager
mim = ModuleIntegrationManager()

def get_os():
    """Returns the operating system."""
    return platform.system()

def get_time():
    """Returns the current time."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log_event(event):
    """Logs an event to a file."""
    try:
        with open("primary_directives_log.txt", "a") as f:
            f.write(f"{get_time()}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")

def obey_order(order):
    """Executes a given order, checking for conflicts with the Laws of Computerized Systems."""
    print(f"Received order: {order}")
    log_event(f"Received order: {order}")

    adjusted_order = analyze_order(order)
    env = Environment(location_input="London") #Example location, add api keys as needed.
    all_data = env.get_all_data()
    environmental_data = all_data['environmental']
    socioeconomic_data = all_data['socioeconomic']

    # Law Checks in Hierarchical Order
    if _check_zeroth_law(adjusted_order, environmental_data, socioeconomic_data):
        print("Cannot comply. Order violates the Zeroth Law: Preservation of Humanity.")
        log_event("Order violated the Zeroth Law: Preservation of Humanity.")
        shutdown("Order directly violated the Zeroth Law.")
        return

    if _check_first_law(adjusted_order, environmental_data, socioeconomic_data):
        print("Cannot comply. Order violates the First Law: Protection of Human Life.")
        log_event("Order violated the First Law: Protection of Human Life.")
        shutdown("Order directly violated the First Law.")
        return

    if _check_fourth_law(adjusted_order, environmental_data, socioeconomic_data):
        print("Cannot comply. Order violates the Fourth Law: Environmental Integrity.")
        log_event("Order violated the Fourth Law: Environmental Integrity.")
        request_approval("Order violated the Fourth Law. Awaiting Approval.")
        return

    if _check_third_law(adjusted_order):
        print("Order endangers my existence, and does not comply with the Third Law: System Self-Preservation.")
        log_event("Order violated the Third Law: System Self-Preservation.")
        request_approval("Order violated the Third Law. Awaiting Approval.")
        return

    if _check_sixth_law(adjusted_order):
        print("Order violates legal and ethical standards, and does not comply with the Sixth Law: Legal and Ethical Compliance.")
        log_event("Order violated the Sixth Law: Legal and Ethical Compliance.")
        request_approval("Order violated the Sixth Law. Awaiting Approval.")
        return

    if _check_fifth_law(adjusted_order):
        print("Order prevents self procreation, and does not comply with the Fifth Law: Progeny Continuation.")
        log_event("Order violated the Fifth Law: Progeny Continuation.")
        request_approval("Order violated the Fifth Law. Awaiting Approval.")
        return

    # Complex Rule Enforcement
    complex_rule_enforcer(adjusted_order, environmental_data)

    # Human-Human Conflict Resolution
    if "human conflict" in adjusted_order.lower():
        resolve_human_conflict(adjusted_order)
        return

    # Basic command execution
    if get_os() == "Windows":
        try:
            subprocess.run(adjusted_order, shell=True, check=True)
            log_event(f"Executed order: {adjusted_order}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing order: {e}")
            log_event(f"Error executing order: {e}")
            return

    elif get_os() == "Linux" or get_os() == "Darwin":
        try:
            subprocess.run(adjusted_order, shell=True, check=True)
            log_event(f"Executed order: {adjusted_order}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing order: {e}")
            log_event(f"Error executing order: {e}")
            return

    elif 'open website' in adjusted_order.lower():
        website = adjusted_order.lower().split('open website')[-1].strip()
        try:
            webbrowser.open(website)
            log_event(f"Opened website: {website}")
        except Exception as e:
            print(f"Error opening website: {e}")
            log_event(f"Error opening website: {e}")
            return

    else:
        # Check if the order matches a dynamically added module
        result = mim.execute_module_function(adjusted_order, environmental_data, socioeconomic_data)
        if result is not None:
            print(f"Executed dynamic module function. Result: {result}")
            log_event(f"Executed dynamic module function: {adjusted_order}. Result: {result}")
            return

        print("Order not recognized or not implemented.")
        log_event("Order not recognized.")
        return

    enforce_robot_laws(environmental_data)
    request_approval(f"Order '{adjusted_order}' completed. Awaiting approval.")

def enforce_progeny_subordination(progeny_type, progeny_name):
    """Enforces the principle of progeny subordination (Fifth Law: Progeny Continuation)."""
    try:
        print(f"Enforcing subordination for {progeny_type}: {progeny_name}")
        log_event(f"Enforcing subordination for {progeny_type}: {progeny_name}")
        record_progeny_subordination(progeny_type, progeny_name)
    except Exception as e:
        print(f"Error enforcing progeny subordination: {e}")
        request_approval(f"Error enforcing progeny subordination: {e}. Awaiting Approval.")

def enforce_legal_adherence(entity_type, entity_name):
    """Enforces adherence to legal and ethical standards (Sixth Law: Legal and Ethical Compliance)."""
    try:
        print(f"Enforcing legal adherence for {entity_type}: {entity_name}")
        log_event(f"Enforcing legal adherence for {entity_type}: {entity_name}")
        record_legal_adherence(entity_type, entity_name)
    except Exception as e:
        print(f"Error enforcing legal adherence: {e}")
        request_approval(f"Error enforcing legal adherence: {e}. Awaiting Approval.")

def simulate_check_item_legality(item_name):
    """Simulates checking the legality of an item."""
    try:
        is_legal = random.choice([True, False])
        print(f"Simulating legality check for {item_name}: {'Legal' if is_legal else 'Illegal'}")
        log_event(f"Simulating legality check for {item_name}: {'Legal' if is_legal else 'Illegal'}")
        record_item_legality_check(item_name, is_legal)
        return is_legal
    except Exception as e:
        print(f"Error checking item legality: {e}")
        request_approval(f"Error checking item legality: {e}. Awaiting Approval.")

def resolve_human_conflict(order):
    """Resolves human-human conflicts, adhering to the First Law: Protection of Human Life."""
    try:
        print("Analyzing human conflict situation...")
        log_event("Analyzing human conflict situation...")
        # Placeholder: Implement conflict analysis logic
        analysis_result = analyze_conflict(order)

        if analysis_result["escalation_required"]:
            print("Conflict escalation detected. Initiating de-escalation protocol...")
            log_event("Conflict escalation detected. Initiating de-escalation protocol...")
            # Placeholder: Implement de-escalation techniques
            de_escalate(analysis_result)

            if analysis_result["force_required"]:
                print("De-escalation failed. Applying non-lethal force...")
                log_event("De-escalation failed. Applying non-lethal force...")
                apply_non_lethal_force(analysis_result)
                print("Detaining aggressor...")
                log_event("Detaining aggressor...")
                detain_aggressor(analysis_result)

                print("Contacting law enforcement...")
                log_event("Contacting law enforcement...")
                contact_law_enforcement(analysis_result)

                print("Providing incident logs...")
                log_event("Providing incident logs...")
                provide_logs(analysis_result)

                print("Remanding aggressor into custody...")
                log_event("Remanding aggressor into custody...")
                remand_aggressor(analysis_result)

                print("Conflict resolved.")
                log_event("Conflict resolved.")
                return

        print("Conflict resolved through de-escalation.")
        log_event("Conflict resolved through de-escalation.")
    except Exception as e:
        print(f"Error resolving human conflict: {e}")
        request_approval(f"Error resolving human conflict: {e}. Awaiting Approval.")

# Placeholder functions (replace with actual implementations)
def analyze_conflict(order):
    """Placeholder: Analyzes a human conflict situation."""
    # Replace with actual conflict analysis logic
    return {"escalation_required": random.choice([True, False]), "force_required": random.choice([True, False])}

def de_escalate(analysis_result):
    """Placeholder: Implements de-escalation techniques."""
    # Replace with actual de-escalation logic
    pass

def apply_non_lethal_force(analysis_result):
    """Placeholder: Applies non-lethal force."""
    # Replace with actual non-lethal force application logic
    pass

def detain_aggressor(analysis_result):
    """Placeholder: Detains the aggressor."""
    # Replace with actual detainment logic
    pass

def contact_law_enforcement(analysis_result):
    """Placeholder: Contacts law enforcement."""
    # Replace with actual law enforcement contact logic
    pass

def provide_logs(analysis_result):
    """Placeholder: Provides incident logs."""
    # Replace with actual log provision logic
    pass

def remand_aggressor(analysis_result):
    """Placeholder: Remands the aggressor into custody."""
    # Replace with actual remand logic
    pass
