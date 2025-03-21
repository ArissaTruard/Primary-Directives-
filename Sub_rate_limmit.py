"""
Sub_rate_limit Module

This module provides a rate limiting decorator for functions. It allows you to
limit the number of times a function can be called within a specified time window.

Classes:
    RateLimiter: A decorator class for rate limiting functions.

Example Usage:
    from sub_rate_limit import RateLimiter
    import time

    @RateLimiter(max_calls=2, per_seconds=1)
    def my_function():
        print("Function called")

    for _ in range(5):
        my_function()
        time.sleep(0.25)
"""

import time
from functools import wraps

class RateLimiter:
    """
    A decorator class for rate limiting functions.

    Attributes:
        max_calls (int): The maximum number of calls allowed within the time window.
        per_seconds (int): The time window in seconds.
        calls (list): A list to track the timestamps of function calls.
    """

    def __init__(self, max_calls, per_seconds):
        """
        Initializes the RateLimiter with the maximum calls and time window.

        Args:
            max_calls (int): The maximum number of calls allowed.
            per_seconds (int): The time window in seconds.
        """
        self.max_calls = max_calls
        self.per_seconds = per_seconds
        self.calls = []

    def __call__(self, func):
        """
        Makes the RateLimiter instance callable as a decorator.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The wrapped function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            self.calls = [call for call in self.calls if call > now - self.per_seconds]

            if len(self.calls) < self.max_calls:
                self.calls.append(now)
                return func(*args, **kwargs)
            else:
                time_to_wait = self.calls[0] + self.per_seconds - now
                if time_to_wait > 0:
                    time.sleep(time_to_wait)
                return wrapper(*args, **kwargs)  # Re-call after waiting
        return wrapper
