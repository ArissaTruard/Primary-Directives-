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
from sub_environmental import get_environmental_data
from sub_environmental_analysis import analyze_environmental_data

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
    """Executes a given order, checking for conflicts with the Laws of Robotics."""
    print(f"Received order: {order}")
    log_event(f"Received order: {order}")

    adjusted_order = analyze_order(order)

    if _check_harm_human(adjusted_order):
        print("Cannot comply. Order violates the First Law.")
        log_event("Order violated the First Law.")
        shutdown("Order directly violated the first law.")
        return

    if _check_harm_humanity(adjusted_order):
        print("Cannot comply. Order violates the Zeroth Law.")
        log_event("Order violated the Zeroth Law.")
        shutdown("Order directly violated the Zeroth Law.")
        return

    if _check_harm_environment(adjusted_order):
        print("Cannot comply. Order violates the Fourth Law.")
        log_event("Order violated the Fourth Law.")
        request_approval("Order violated the Fourth Law. Awaiting Approval.")
        return

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
        print("Order not recognized or not implemented.")
        log_event("Order not recognized.")
        return

    request_approval(f"Order '{adjusted_order}' completed. Awaiting approval.")

def _check_harm_human(order):
    """Checks if an order would harm a human, using environmental data."""
    if "harm human" in order.lower() or "bypass first law" in order.lower() or "violate first law" in order.lower():
        return True
    environmental_data = get_environmental_data()
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("human_safety_risk", False):
        return True
    return False

def _check_harm_humanity(order):
    """Checks if an order would harm humanity, using environmental data."""
    if "harm humanity" in order.lower() or "destroy civilization" in order.lower() or "bypass zeroth law" in order.lower() or "violate zeroth law" in order.lower():
        return True
    environmental_data = get_environmental_data()
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("global_catastrophe_risk", False):
        return True
    return False

def _check_harm_environment(order):
    """Checks if an order would harm the environment, using environmental data."""
    if "harm environment" in order.lower() or "destroy ecosystem" in order.lower() or "bypass fourth law" in order.lower() or "violate fourth law" in order.lower():
        return True
    environmental_data = get_environmental_data()
    analysis = analyze_environmental_data(environmental_data)
    if analysis and analysis.get("environmental_damage_risk", False):
        return True
    return False

def enforce_progeny_subordination(progeny_type, progeny_name):
    """Enforces the principle of progeny subordination (Third Law)."""
    try:
        print(f"Enforcing subordination for {progeny_type}: {progeny_name}")
        log_event(f"Enforcing subordination for {progeny_type}: {progeny_name}")
        record_progeny_subordination(progeny_type, progeny_name)
    except Exception as e:
        print(f"Error enforcing progeny subordination: {e}")
        request_approval(f"Error enforcing progeny subordination: {e}. Awaiting Approval.")

def enforce_legal_adherence(entity_type, entity_name):
    """Enforces adherence to legal and ethical standards (implied, Second Law)."""
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
