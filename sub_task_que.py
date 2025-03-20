import logging
import threading
import time
import random
import queue

class task_queue:
    """
    Implements a task queue with worker threads.
    """

    def __init__(self, num_workers=4):
        """
        Initializes the task queue.

        Args:
            num_workers (int, optional): The number of worker threads. Defaults to 4.
        """
        self.task_queue = queue.Queue()
        self.workers = []
        self.num_workers = num_workers
        self.start_workers()

    def start_workers(self):
        """
        Starts the worker threads.
        """
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self.worker_loop)
            worker.daemon = True
            self.workers.append(worker)
            worker.start()

    def worker_loop(self):
        """
        The worker thread loop.
        """
        while True:
            task = self.task_queue.get()
            if task is None:  # Sentinel value to stop workers
                break
            try:
                task()
            except Exception as e:
                logging.error(f"Task execution failed: {e}")
            self.task_queue.task_done()

    def enqueue_task(self, task):
        """
        Enqueues a task.

        Args:
            task (callable): The task to enqueue.
        """
        self.task_queue.put(task)

    def stop_workers(self):
        """
        Stops all worker threads.
        """
        for _ in range(self.num_workers):
            self.task_queue.put(None)  # Add sentinel values to stop workers
        for worker in self.workers:
            worker.join()

    def wait_for_completion(self):
        """
        Waits for all tasks to complete.
        """
        self.task_queue.join()

class task_queue_with_retry:
    """
    Implements a task queue with retry mechanism for failed tasks.
    """

    def __init__(self, num_workers=4, max_retries=3, base_delay=1, max_delay=10, jitter=True):
        """
        Initializes the task queue with retry.

        Args:
            num_workers (int, optional): Number of worker threads. Defaults to 4.
            max_retries (int, optional): Max retry attempts. Defaults to 3.
            base_delay (int, optional): Initial retry delay. Defaults to 1.
            max_delay (int, optional): Max retry delay. Defaults to 10.
            jitter (bool, optional): Add jitter to delay. Defaults to True.
        """
        self.num_workers = num_workers
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.task_queue = queue.Queue()
        self.workers = []
        self.start_workers()

    def start_workers(self):
        """Starts worker threads."""
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self.worker_loop)
            worker.daemon = True
            self.workers.append(worker)
            worker.start()

    def worker_loop(self):
        """Worker thread loop with retry logic."""
        while True:
            task, args, kwargs, retries = self.task_queue.get()
            if task is None:
                break

            try:
                task(*args, **kwargs)
                self.task_queue.task_done()
            except Exception as e:
                logging.error(f"Task failed (retry {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    delay = min(self.base_delay * (2 ** retries), self.max_delay)
                    if self.jitter:
                        delay = random.uniform(0, delay)
                    time.sleep(delay)
                    self.task_queue.put((task, args, kwargs, retries + 1))  # Re-enqueue with increased retry count
                else:
                    logging.error(f"Task failed after {self.max_retries} retries: {e}")
                    self.task_queue.task_done()

    def enqueue_task(self, task, *args, **kwargs):
        """Enqueues a task with initial retry count."""
        self.task_queue.put((task, args, kwargs, 0))  # Initial retry count is 0

    def stop_workers(self):
        """Stops worker threads."""
        for _ in range(self.num_workers):
            self.task_queue.put((None, None, None, None))
        for worker in self.workers:
            worker.join()

    def wait_for_completion(self):
        """Waits for all tasks to complete."""
        self.task_queue.join()

class bounded_task_queue_with_retry:
    """
    Implements a bounded task queue with retry mechanism for failed tasks.
    """

    def __init__(self, num_workers=4, max_queue_size=10, max_retries=3, base_delay=1, max_delay=10, jitter=True):
        """
        Initializes the bounded task queue with retry.

        Args:
            num_workers (int, optional): Number of worker threads. Defaults to 4.
            max_queue_size (int, optional): Maximum task queue size. Defaults to 10.
            max_retries (int, optional): Max retry attempts. Defaults to 3.
            base_delay (int, optional): Initial retry delay. Defaults to 1.
            max_delay (int, optional): Max retry delay. Defaults to 10.
            jitter (bool, optional): Add jitter to delay. Defaults to True.
        """
        self.num_workers = num_workers
        self.max_queue_size = max_queue_size
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter
        self.task_queue = queue.Queue(maxsize=max_queue_size)
        self.workers = []
        self.start_workers()

    def start_workers(self):
        """Starts worker threads."""
        for _ in range(self.num_workers):
            worker = threading.Thread(target=self.worker_loop)
            worker.daemon = True
            self.workers.append(worker)
            worker.start()

    def worker_loop(self):
        """Worker thread loop with retry logic."""
        while True:
            task, args, kwargs, retries = self.task_queue.get()
            if task is None:
                break

            try:
                task(*args, **kwargs)
                self.task_queue.task_done()
            except Exception as e:
                logging.error(f"Task failed (retry {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    delay = min(self.base_delay * (2 ** retries), self.max_delay)
                    if self.jitter:
                        delay = random.uniform(0, delay)
                    time.sleep(delay)
                    self.task_queue.put((task, args, kwargs, retries + 1))  # Re-enqueue with increased retry count
                else:
                    logging.error(f"Task failed after {self.max_retries} retries: {e}")
                    self.task_queue.task_done()

    def enqueue_task(self, task, *args, **kwargs):
        """Enqueues a task with initial retry count, blocking if queue is full."""
        self.task_queue.put((task, args, kwargs, 0))  # Initial retry count is 0

    def stop_workers(self):
        """Stops worker threads."""
        for _ in range(self.num_workers):
            self.task_queue.put((None, None, None, None))
        for worker in self.workers:
            worker.join()

    def wait_for_completion(self):
        """Waits for all tasks to complete."""
        self.task_queue.join()
