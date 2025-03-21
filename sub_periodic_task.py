"""
Sub_periodic_task Module

This module provides a decorator for running functions periodically.

Classes:
    periodic_task: A decorator for running functions periodically.

Functions:
    periodic_task(interval): Decorator to run a function periodically.
"""

import asyncio
import logging
from functools import wraps

def periodic_task(interval):
    """
    Decorator to run a function periodically.

    Args:
        interval (int): The interval in seconds to run the function.

    Returns:
        callable: The decorated function.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async def periodic_runner():
                while True:
                    try:
                        await func(*args, **kwargs)
                    except Exception as e:
                        logging.error(f"Error in periodic task {func.__name__}: {e}")
                    await asyncio.sleep(interval)

            asyncio.create_task(periodic_runner())
            return func  # Return the original function for other purposes

        return wrapper

    return decorator

if __name__ == "__main__":
    # Example usage
    @periodic_task(interval=5)
    async def my_periodic_task():
        logging.info("Periodic task executed.")

    async def main():
        # Simulate some other async operations
        await asyncio.sleep(15)
        logging.info("Main task finished.")

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
