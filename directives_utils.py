import os
import time
import datetime
import platform
import subprocess
import webbrowser
import logging
import random
from sub_database import * #import database functions
from sub_location import * #import location functions

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
    """Executes a given order, checking for conflicts with the First Law."""
    print(f"Received order: {order}")
    log_event(f"Received order: {order}")

    if "harm human" in order.lower():
        print("Cannot comply. Order violates the First Law.")
        log_event("Order violated the First Law.")
        return

    # Basic command execution (very limited and unsafe in real world applications)
    if get_os() == "Windows":
        try:
            subprocess.run(order, shell=True, check=True)
            log_event(f"Executed order: {order}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing order: {e}")
            log_event(f"Error executing order: {e}")

    elif get_os() == "Linux" or get_os() == "Darwin": # Darwin is macOS
        try:
            subprocess.run(order, shell=True, check=True)
            log_event(f"Executed order: {order}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing order: {e}")
            log_event(f"Error executing order: {e}")

    elif 'open website' in order.lower():
        website = order.lower().split('open website')[-1].strip()
        try:
            webbrowser.open(website)
            log_event(f"Opened website: {website}")
        except Exception as e:
            print(f"Error opening website: {e}")
            log_event(f"Error opening website: {e}")

    else:
        print("Order not recognized or not implemented.")
        log_event("Order not recognized.")

def enforce_progeny_subordination(progeny_type, progeny_name):
    """Enforces the principle of progeny subordination."""
    print(f"Enforcing subordination for {progeny_type}: {progeny_name}")
    log_event(f"Enforcing subordination for {progeny_type}: {progeny_name}")

def enforce_legal_adherence(entity_type, entity_name):
    """Enforces adherence to legal and ethical standards."""
    print(f"Enforcing legal adherence for {entity_type}: {entity_name}")
    log_event(f"Enforcing legal adherence for {entity_type}: {entity_name}")

def simulate_check_item_legality(item_name):
    """Simulates checking the legality of an item."""
    is_legal = random.choice([True, False])
    print(f"Simulating legality check for {item_name}: {'Legal' if is_legal else 'Illegal'}")
    log_event(f"Simulating legality check for {item_name}: {'Legal' if is_legal else 'Illegal'}")
    return is_legal
