"""
Sub_thread_pool Module

This module provides a ThreadPool class for managing and executing tasks using a pool of threads.

Classes:
    ThreadPool: Manages and executes tasks using a pool of threads.
"""

import logging
import threading
import queue
import time

class ThreadPool:
    """
    Manages and executes tasks using a pool of threads.

    Attributes:
        num_threads (int): The number of threads in the pool.
        task_queue (queue.Queue): A queue to store tasks.
        threads (list): A list of threads in the pool.
        running (bool): Indicates if the thread pool is running.
    """

    def __init__(self, num_threads=5):
        """
        Initializes the ThreadPool.

        Args:
            num_threads (int, optional): The number of threads in the pool. Defaults to 5.
        """
        self.num_threads = num_threads
        self.task_queue = queue.Queue()
        self.threads = []
        self.running = True
        self._create_threads()

    def _create_threads(self):
        """
        Creates and starts the threads in the pool.
        """
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True  # Allow program to exit even if threads are running
            self.threads.append(thread)
            thread.start()

    def _worker(self):
        """
        Worker function that executes tasks from the queue.
        """
        while self.running:
            try:
                task, args, kwargs = self.task_queue.get(timeout=1)  # Timeout to allow checking self.running
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error executing task: {e}")
                self.task_queue.task_done()
            except queue.Empty:
                pass  # No task available, check if pool should stop

    def submit(self, task, *args, **kwargs):
        """
        Submits a task to the queue for execution.

        Args:
            task (callable): The task to execute.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.
        """
        self.task_queue.put((task, args, kwargs))

    def wait_completion(self):
        """
        Waits for all tasks in the queue to complete.
        """
        self.task_queue.join()

    def stop(self):
        """
        Stops the thread pool and waits for all threads to finish.
        """
        self.running = False
        for thread in self.threads:
            thread.join()

if __name__ == "__main__":
    # Example usage
    def my_task(task_id):
        logging.info(f"Task {task_id} started.")
        time.sleep(1)  # Simulate some work
        logging.info(f"Task {task_id} completed.")

    logging.basicConfig(level=logging.INFO)
    pool = ThreadPool(num_threads=3)

    for i in range(5):
        pool.submit(my_task, i)

    pool.wait_completion()
    pool.stop()
    logging.info("All tasks completed.")
