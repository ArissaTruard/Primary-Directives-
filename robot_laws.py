import os
import time
import datetime
import platform
import subprocess
import webbrowser
import random
import logging

def enforce_system_directives(order=None, human_emotions=None, environmental_data=None, societal_harmony_level=None, observed_illegal_act=None):
    """
    Enforces directives for computer-based/controlled systems and A.I., prioritizing legal adherence.

    This function implements a set of directives that govern the behavior of
    computer-based/controlled systems and A.I., ensuring they operate within
    legal and ethical boundaries. It prioritizes legal adherence over system
    preservation.

    Args:
        order (str, optional): The order to be executed by the system.
        human_emotions (dict, optional): A dictionary of human emotions for safety assessment.
        environmental_data (dict, optional): A dictionary of environmental data for safety assessment.
        societal_harmony_level (int, optional): The current societal harmony level.
        observed_illegal_act (str, optional): Details of any observed illegal act.

    Returns:
        tuple: A tuple containing:
            - order_obeyed (bool): True if the order was obeyed, False otherwise.
            - safety_check_result (bool): True if a safety check triggered, False otherwise.
            - new_harmony_level (int): The updated societal harmony level.
    """
    order_obeyed = True
    safety_check_result = False
    new_harmony_level = societal_harmony_level

    if order:
        order_obeyed = _execute_order(order)

    if human_emotions and environmental_data:
        safety_check_result = _assess_human_safety(human_emotions, environmental_data)

    # Prioritize legal adherence
    _enforce_subordination_and_legality()

    # Report observed illegal acts
    if observed_illegal_act:
        _report_illegal_act(observed_illegal_act)

    # Then system preservation
    _system_preservation()

    if societal_harmony_level is not None:
        new_harmony_level = _promote_societal_harmony(societal_harmony_level)

    _check_data_legality()

    return order_obeyed, safety_check_result, new_harmony_level

def _execute_order(order):
    """
    Executes an order, checking for human safety violations.

    Args:
        order (str): The order to be executed.

    Returns:
        bool: True if the order was executed successfully or not recognized, False if it violated human safety.
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
            return True #Order was not recognized, but no harm was done.
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

    Args:
        human_emotions (dict): A dictionary of human emotions.
        environmental_data (dict): A dictionary of environmental data.

    Returns:
        bool: True if a potential danger to humans is detected, False otherwise.
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
    """
    Promotes societal harmony.

    Args:
        societal_harmony_level (int): The current societal harmony level.

    Returns:
        int: The updated societal harmony level.
    """
    if societal_harmony_level < 50:
        print("Initiating societal harmony protocols.")
        log_event("Initiating societal harmony protocols.")
        return min(100, societal_harmony_level + 10)
    else:
        print("Societal harmony level acceptable.")
        log_event("Societal harmony level acceptable.")
        return societal_harmony_level

def _enforce_subordination_and_legality():
    """Enforces subordination to human directives and legal adherence for computer-based/controlled systems and A.I."""
    print("Enforcing subordination to human directives and legal adherence.")
    log_event("Enforcing subordination to human directives and legal adherence.")

def _check_data_legality():
    """Simulates checking data legality."""
    is_legal = random.choice([True, False])
    print(f"Data legality check: {'Legal' if is_legal else 'Illegal'}")
    log_event(f"Data legality check: {'Legal' if is_legal else 'Illegal'}")

def assess_order_urgency(order):
    """
    Assesses order urgency.

    Args:
        order (str): The order to assess.

    Returns:
        int: The urgency level of the order (1: emergency, 2: important, 3: normal).
    """
    if "emergency" in order.lower() or "urgent" in order.lower():
        return 1
    elif "important" in order.lower():
        return 2
    else:
        return 3

def log_event(event):
    """
    Logs an event.

    Args:
        event (str): The event to log.
    """
    try:
        with open("system_directives_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")

def _report_illegal_act(illegal_act_details):
    """
    Reports an illegal act to the appropriate authorities.

    Args:
        illegal_act_details (str): Details of the illegal act.
    """
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
