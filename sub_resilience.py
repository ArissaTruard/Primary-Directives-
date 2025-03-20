import logging
import threading
import time
import random

def retry(operation, max_retries=3, retry_delay=1):
    """
    Retries an operation a specified number of times with a fixed delay.

    Args:
        operation (callable): The operation to retry.
        max_retries (int, optional): The maximum number of retry attempts. Defaults to 3.
        retry_delay (int, optional): The delay in seconds between retries. Defaults to 1.

    Returns:
        The result of the operation if successful, or None if all retries fail.
    """
    retries = 0
    while retries < max_retries:
        try:
            return operation()
        except Exception as e:
            retries += 1
            if retries < max_retries:
                logging.warning(f"Operation failed (retry {retries}/{max_retries}): {e}. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Operation failed after {max_retries} retries: {e}")
                return None

def retry_with_timeout(operation, max_retries=3, retry_delay=1, timeout=5):
    """
    Retries an operation with a timeout.

    Args:
        operation (callable): The operation to retry.
        max_retries (int, optional): The maximum number of retry attempts. Defaults to 3.
        retry_delay (int, optional): The delay in seconds between retries. Defaults to 1.
        timeout (int, optional): The maximum time in seconds to wait for the operation to complete. Defaults to 5.

    Returns:
        The result of the operation if successful, or None if all retries fail or timeout occurs.
    """
    retries = 0
    start_time = time.time()
    while retries < max_retries:
        try:
            result = operation()
            return result
        except Exception as e:
            retries += 1
            if retries < max_retries and time.time() - start_time + retry_delay <= timeout:
                logging.warning(f"Operation failed (retry {retries}/{max_retries}): {e}. Retrying in {retry_delay} seconds.")
                time.sleep(retry_delay)
            else:
                logging.error(f"Operation failed after {max_retries} retries or timeout occurred: {e}")
                return None

def retry_with_backoff(func, max_retries=5, base_delay=1, max_delay=60, jitter=True):
    """
    Retries a function with exponential backoff and optional jitter.

    Args:
        func (callable): The function to retry.
        max_retries (int, optional): The maximum number of retries. Defaults to 5.
        base_delay (int, optional): The initial delay in seconds. Defaults to 1.
        max_delay (int, optional): The maximum delay in seconds. Defaults to 60.
        jitter (bool, optional): Whether to add jitter to the delay. Defaults to True.

    Returns:
        The result of the function if successful, or None if all retries fail.
    """
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries == max_retries:
                logging.error(f"Function failed after {max_retries} retries: {e}")
                return None  # Or raise the exception if desired

            delay = min(base_delay * (2 ** (retries - 1)), max_delay)
            if jitter:
                delay = random.uniform(0, delay)
            logging.warning(f"Function failed (retry {retries}/{max_retries}): {e}. Retrying in {delay:.2f} seconds.")
            time.sleep(delay)
    return None  # Should not be reached

class circuit_breaker_with_retry:
    """
    Combines circuit breaker and retry with backoff patterns.
    """

    def __init__(self, failure_threshold=5, recovery_timeout=30, max_retries=3, base_delay=1, max_delay=10, jitter=True):
        """
        Initializes the circuit breaker with retry.

        Args:
            failure_threshold (int, optional): Number of failures to open circuit. Defaults to 5.
            recovery_timeout (int, optional): Timeout to transition to HALF_OPEN. Defaults to 30.
            max_retries (int, optional): Max retry attempts. Defaults to 3.
            base_delay (int, optional): Initial retry delay. Defaults to 1.
            max_delay (int, optional): Max retry delay. Defaults to 10.
            jitter (bool, optional): Add jitter to delay. Defaults to True.
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.failure_count = 0
        self.state = "CLOSED"  # States: CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = 0
        self.lock = threading.Lock()

    def call(self, func, *args, **kwargs):
        """
        Calls the function with circuit breaker and retry logic.

        Args:
            func (callable): The function to call.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The function's result, or None if circuit is open and retries fail.
        """
        with self.lock:
            if self.state == "OPEN":
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                else:
                    logging.warning("Circuit is OPEN. Call prevented.")
                    return None

        retries = 0
        while retries <= self.max_retries:
            try:
                result = func(*args, **kwargs)
                self.reset()
                return result
            except Exception as e:
                retries += 1
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"
                    logging.critical("Circuit OPENED.")

                if retries <= self.max_retries:
                    delay = min(self.base_delay * (2 ** (retries - 1)), self.max_delay)
                    if self.jitter:
                        delay = random.uniform(0, delay)
                    logging.warning(f"Function failed (retry {retries}/{self.max_retries}): {e}. Retrying in {delay:.2f} seconds.")
                    time.sleep(delay)
                else:
                    logging.error(f"Function failed after {self.max_retries} retries: {e}")
                    raise #re-raise the error.

    def reset(self):
        """Resets the circuit breaker."""
        with self.lock:
            self.failure_count = 0
            self.state = "CLOSED"
            logging.info("Circuit CLOSED.")

    def half_open_attempt(self, func, *args, **kwargs):
        """
        Attempts a call in HALF_OPEN state.

        Args:
            func (callable): The function to call.
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            The function's result, or None if still open.
        """
        with self.lock:
            if self.state != "HALF_OPEN":
                logging.warning("Circuit is not HALF_OPEN.")
                return None

            try:
                result = func(*args, **kwargs)
                self.reset()
                return result
            except Exception as e:
                self.state = "OPEN"
                self.last_failure_time = time.time()
                self.failure_count = self.failure_threshold
                logging.error(f"Half-open attempt failed: {e}. Circuit OPENED.")
                raise #reraise the exception.
