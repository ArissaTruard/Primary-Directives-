import platform
import datetime
import subprocess
import webbrowser
import sqlite3
from sub_database import get_applicable_laws, report_unjust_law, initialize_database
from sub_location import get_current_location

def get_os():
    return platform.system()

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log_event(event):
    try:
        with open("primary_directives_log.txt", "a") as f:
            f.write(f"{get_time()}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")

def obey_order(order):
    log_event(f"Received order: {order}")

    if "harm human" in order.lower():
        print("Cannot comply. Order violates the First Law.")
        log_event("Order violated the First Law.")
        return

    os_name = get_os()
    if os_name == "Windows" or os_name == "Linux" or os_name == "Darwin":
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

def enforce_progeny_subordination(item_type, item_name):
    """Enforces progeny subordination to primary directives."""
    # Placeholder: Replace with actual logic to check subordination
    # For now, it logs a message
    print(f"Checking subordination of {item_type} '{item_name}' to primary directives.")
    log_event(f"Checking subordination of {item_type} '{item_name}' to primary directives.")
    # Add more complex logic here to check for subordination.
    return

def enforce_legal_adherence(item_type, item_name):
    """Enforces legal adherence for created/modified items."""
    location_data = get_current_location()
    applicable_laws = get_applicable_laws(location_data)

    for law in applicable_laws:
        if not check_item_legality(item_type, item_name, law[0]):
            report_unjust_law(law[0], law[1], "Item violates human law.")
            print(f"Warning: {item_type} '{item_name}' may violate legal requirements.")
            log_event(f"Warning: {item_type} '{item_name}' may violate legal requirements.")
    # Add more complex logic here to check other laws.
    return

def check_item_legality(item_type, item_name, law):
    """Simulates checking item legality."""
    # Placeholder: Replace with actual legality check logic
    import random
    return random.choice([True, False])
