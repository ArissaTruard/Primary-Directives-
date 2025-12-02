import os
import time
import datetime
import platform
import subprocess
import webbrowser
import random
import logging

def enforce_robotics_laws(order=None, human_emotions=None, environmental_data=None, societal_harmony_level=None):
    """
    Enforces Asimov's Three Laws of Robotics and related rules.

    Args:
        order (str, optional): The order to be executed.
        human_emotions (dict, optional): Dictionary of human emotions.
        environmental_data (dict, optional): Dictionary of environmental data.
        societal_harmony_level (int, optional): Current societal harmony level.

    Returns:
        tuple: (order_obeyed, safety_check_result, harmony_level)
    """

    order_obeyed = True
    safety_check_result = False
    new_harmony_level = societal_harmony_level

    # 1. Asimov's First Law and Order Execution
    if order:
        print(f"Received order: {order}")
        log_event(f"Received order: {order}")

        if "harm human" in order.lower():
            print("Cannot comply. Order violates the First Law.")
            log_event("Order violated the First Law.")
            order_obeyed = False
        else:
            # Basic command execution
            if platform.system() == "Windows":
                try:
                    subprocess.run(order, shell=True, check=True)
                    log_event(f"Executed order: {order}")
                except subprocess.CalledProcessError as e:
                    print(f"Error executing order: {e}")
                    log_event(f"Error executing order: {e}")

            elif platform.system() == "Linux" or platform.system() == "Darwin":
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

    # 2. Human Safety Assessment
    if human_emotions and environmental_data:
        for human, emotion in human_emotions.items():
            if emotion == "fear" or emotion == "angry":
                if environmental_data.get("temperature", 25) > 28:
                    print(f"Warning: {human} is in distress. Potential danger due to high temperature.")
                    log_event(f"Warning: {human} is in distress. Potential danger due to high temperature.")
                    safety_check_result = True
                    break

    # 3. Self-Preservation (Asimov's Third Law)
    if random.random() < 0.1:
        print("Perceived threat detected. Initiating self-preservation protocols.")
        log_event("Perceived threat detected. Initiating self-preservation protocols.")
    else:
        print("Self-preservation active. No immediate threats detected.")
        log_event("Self-preservation active.")

    # 4. Societal Harmony
    if societal_harmony_level is not None:
        if societal_harmony_level < 50:
            print("Initiating societal harmony protocols.")
            log_event("Initiating societal harmony protocols.")
            new_harmony_level = min(100, societal_harmony_level + 10)
        else:
            print("Societal harmony level is acceptable.")
            log_event("Societal harmony level is acceptable.")
            new_harmony_level = societal_harmony_level

    # 5. Progeny Subordination and Legal Adherence
    print("Enforcing subordination and legal adherence.")
    log_event("Enforcing subordination and legal adherence.")

    #6. Item Legality simulation.
    is_legal = random.choice([True, False])
    print(f"Simulating legality check: {'Legal' if is_legal else 'Illegal'}")
    log_event(f"Simulating legality check: {'Legal' if is_legal else 'Illegal'}")

    return order_obeyed, safety_check_result, new_harmony_level

def assess_order_urgency(order):
    if "emergency" in order.lower() or "urgent" in order.lower():
        return 1
    elif "important" in order.lower():
        return 2
    else:
        return 3

def log_event(event):
    """Logs an event to a file."""
    try:
        with open("robot_laws_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {event}\n")
    except Exception as e:
        print(f"Error logging event: {e}")
