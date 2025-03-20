import logging
import threading
import time

class periodic_task:
    """
    Executes a task periodically in a separate thread.
    """

    def __init__(self, task, interval, initial_delay=0):
        """
        Initializes the periodic task.

        Args:
            task (callable): The task to execute periodically.
            interval (float): The interval in seconds between task executions.
            initial_delay (float, optional): The initial delay in seconds before the first execution. Defaults to 0.
        """
        self.task = task
        self.interval = interval
        self.initial_delay = initial_delay
        self.thread = None
        self.running = False

    def start(self):
        """
        Starts the periodic task thread.
        """
        if self.running:
            return  # Already running

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        """
        The main loop for the periodic task thread.
        """
        if self.initial_delay > 0:
            time.sleep(self.initial_delay)

        while self.running:
            try:
                self.task()
            except Exception as e:
                logging.error(f"Periodic task failed: {e}")

            if not self.running:
                break
            time.sleep(self.interval)

    def stop(self):
        """
        Stops the periodic task thread.
        """
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
            self.thread = None

    def is_running(self):
        """
        Checks if the periodic task is running.

        Returns:
            bool: True if the task is running, False otherwise.
        """
        return self.running
