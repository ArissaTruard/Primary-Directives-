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
            subprocess.run(adjusted_order, shell=True, check=True
