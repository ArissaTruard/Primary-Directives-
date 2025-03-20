import logging
import threading
import time

def rate_limit(func, calls_per_second=1):
    """
    Rate-limits a function to a specified number of calls per second.

    Args:
        func (callable): The function to rate-limit.
        calls_per_second (int, optional): The maximum number of calls allowed per second. Defaults to 1.

    Returns:
        callable: A wrapped function that enforces the rate limit.
    """
    last_call_time = 0
    lock = threading.Lock() #Add a lock to make thread safe.
    def wrapper(*args, **kwargs):
        nonlocal last_call_time

        with lock:
            current_time = time.time()
            elapsed_time = current_time - last_call_time

            if elapsed_time < 1 / calls_per_second:
                time.sleep(1 / calls_per_second - elapsed_time)

            last_call_time = time.time()
            return func(*args, **kwargs)

    return wrapper
