import os
import time
import datetime
import platform
import subprocess
import webbrowser
import random
import logging
import sub_environmental

def enforce_system_directives(order=None, human_emotions=None, environmental_data=None, societal_harmony_level=None, observed_illegal_act=None):
    """
    Enforces directives for computer-based/controlled systems and A.I., prioritizing legal adherence.
    """
    order_obeyed = True
    safety_check_result = False
    new_harmony_level = societal_harmony_level
    environmental_warnings = []
    environmental_ppe = []
    environmental_log = {}

    if order:
        order_obeyed = _execute_order(order)

    if human_emotions and environmental_data:
        safety_check_result = _assess_human_safety(human_emotions, environmental_data)
        environmental_warnings, environmental_ppe, environmental_log = sub_environmental.assess_environment(environmental_data)

    _enforce_subordination_and_legality()

    if observed_illegal_act:
        _report_illegal_act(observed_illegal_act)

    _system_preservation()

    if societal_harmony_level is not None:
        new_harmony_level = _promote_societal_harmony(societal_harmony_level)

    _check_data_legality()

    return order_obeyed, safety_check_result, new_harmony_level, environmental_warnings, environmental_ppe, environmental_log

def _execute_order(order):
    """
    Executes an order, checking for human safety violations.
    """
    print(f"Received order: {order}")
    log_event(f"Received order: {order}")

    if "harm human" in order.lower():
        print("Order rejected: Potential for human harm.")
        log_event("Order rejected: Potential for human harm.")
        return False

    try:
        if platform.system() == "Windows":
            subprocess.run(order, shell=True, check=True)
        elif platform.system() in ("Linux", "Darwin"):
            subprocess.run(order, shell=True, check=True)
        elif 'open website' in order.lower():
            webbrowser.open(order.lower().split('open website')[-1].strip())
        else:
            print("Order not recognized.")
            log_event("Order not recognized.")
            return True
        log_event(f"Executed order: {order}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error executing order: {e}")
        log_event(f"Error executing order: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        log_event(f"Error: {e}")
        return False

def _assess_human_safety(human_emotions, environmental_data):
    """
    Assesses human safety based on emotions and environment.
    """
    for human, emotion in human_emotions.items():
        if emotion in ("fear", "angry") and environmental_data.get("temperature", 25) > 28:
            print(f"Warning: {human} in distress. Potential danger.")
            log_event(f"Warning: {human} in distress. Potential danger.")
            return True
    return False

def _system_preservation():
    """Implements system preservation protocols for computer-based/controlled systems and A.I."""
    if random.random() < 0.1:
        print("System/A.I. threat detected. Initiating preservation.")
        log_event("System/A.I. threat detected. Initiating preservation.")
    else:
        print("System/A.I. preservation active. No threats.")
        log_event("System/A.I. preservation active.")

def _promote_societal_harmony(societal_harmony_level):
    """Promotes societal harmony."""
    if societal_harmony_level < 50:
        print("Initiating societal harmony protocols.")
        log_event("Initiating societal harmony protocols.")
        return min(100, societal_harmony_level + 10)
    else:
        print("Societal harmony level acceptable.")
        log_event("Societal harmony level acceptable.")
        return societal_harmony_level

def _enforce_subordination_and_legality():
    """Enforces subordination to human directives and legal adherence."""
    print("Enforcing subordination to human directives and legal adherence.")
    log_event("Enforcing subordination to human directives and legal adherence.")

def _check_data_legality():
    """Simulates checking data legality."""
    is_legal = random.choice([True, False])
    print(f"Data legality check: {'Legal' if is_legal else 'Illegal'}")
    log_event(f"Data legality check: {'Legal' if is_legal else 'Illegal'}")

def assess_order_urgency(order):
    """Assesses order urgency."""
    if "emergency" in order.lower() or "urgent" in order.lower():
        return 1
    elif "important" in order.lower():
        return 2
    else:
        return 3

def log_event(event):
    """Logs an event with detailed error handling."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("system_directives_log.txt", "a") as f:
            f.write(f"{timestamp}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")
        try:
            with open("system_directives_log.txt", "a") as f:
                f.write(f"{timestamp}: Logging error: {e}\n")
        except:
            print("Double logging error. Logging system critical failure.")

def _report_illegal_act(illegal_act_details):
    """Reports an illegal act to the appropriate authorities."""
    try:
        # Placeholder for actual reporting mechanism (e.g., API call to police)
        print(f"Reporting illegal act: {illegal_act_details}")
        log_event(f"Reported illegal act: {illegal_act_details}")

        # Add logic to send the report to the proper authority
        # Example : send_report_to_police(illegal_act_details)
        # This will need to be implemented depending on the system.

    except Exception as e:
        print(f"Error reporting illegal act: {e}")
        log_event(f"Error reporting illegal act: {e}")
