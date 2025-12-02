"""
Sub_task_queue Module

This module provides a TaskQueue class for managing and executing asynchronous tasks.

Classes:
    TaskQueue: Manages and executes asynchronous tasks.
"""

import asyncio
import logging
from collections import deque

class TaskQueue:
    """
    Manages and executes asynchronous tasks.

    Attributes:
        queue (deque): A deque to store tasks.
        max_size (int): The maximum size of the queue.
        running (bool): Indicates if the queue is running.
    """

    def __init__(self, max_size=100):
        """
        Initializes the TaskQueue.

        Args:
            max_size (int, optional): The maximum size of the queue. Defaults to 100.
        """
        self.queue = deque()
        self.max_size = max_size
        self.running = False

    def add_task(self, task):
        """
        Adds a task to the queue.

        Args:
            task (callable): The asynchronous task to add.

        Raises:
            ValueError: If the queue is full.
        """
        if len(self.queue) < self.max_size:
            self.queue.append(task)
            if not self.running:
                asyncio.create_task(self._process_tasks())
        else:
            raise ValueError("Task queue is full.")

    async def _process_tasks(self):
        """
        Processes tasks from the queue.
        """
        self.running = True
        while self.queue:
            task = self.queue.popleft()
            try:
                await task()
            except Exception as e:
                logging.error(f"Error processing task: {e}")
        self.running = False

    async def wait_for_completion(self):
        """
        Waits for all tasks in the queue to complete.
        """
        while self.running or self.queue:
            await asyncio.sleep(0.1)  # Small delay to avoid busy-waiting

if __name__ == "__main__":
    # Example usage
    async def my_task(task_id):
        logging.info(f"Task {task_id} started.")
        await asyncio.sleep(1)  # Simulate some async work
        logging.info(f"Task {task_id} completed.")

    async def main():
        queue = TaskQueue(max_size=5)
        for i in range(3):
            queue.add_task(my_task(i))

        await queue.wait_for_completion()
        logging.info("All tasks completed.")

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
