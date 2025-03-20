import logging
import threading
import time

class thread_pool:
    """
    Implements a thread pool with a fixed number of worker threads.
    """

    def __init__(self, num_threads=4):
        """
        Initializes the thread pool.

        Args:
            num_threads (int, optional): The number of worker threads in the pool. Defaults to 4.
        """
        self.num_threads = num_threads
        self.tasks = []
        self.results = []
        self.threads = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.running = True
        self.create_threads()

    def create_threads(self):
        """
        Creates and starts the worker threads.
        """
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

    def worker(self):
        """
        The worker thread loop.
        """
        with self.condition:
            while self.running:
                if not self.tasks:
                    self.condition.wait()  # Wait for tasks
                if not self.running:
                    break
                if self.tasks:
                    task, args, kwargs = self.tasks.pop(0)
                    try:
                        result = task(*args, **kwargs)
                        with self.lock:
                            self.results.append(result)
                    except Exception as e:
                        logging.error(f"Task execution failed: {e}")

    def submit(self, task, *args, **kwargs):
        """
        Submits a task to the thread pool.

        Args:
            task (callable): The task to execute.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.
        """
        with self.condition:
            self.tasks.append((task, args, kwargs))
            self.condition.notify()  # Notify a waiting thread

    def get_results(self):
        """
        Gets the results of the executed tasks.

        Returns:
            list: A list of results.
        """
        with self.lock:
            results = self.results[:] #create a copy.
            self.results.clear()
            return results

    def shutdown(self, wait=True):
        """
        Shuts down the thread pool.

        Args:
            wait (bool, optional): Whether to wait for tasks to complete. Defaults to True.
        """
        with self.condition:
            self.running = False
            self.condition.notify_all()  # Notify all waiting threads

        if wait:
            for thread in self.threads:
                thread.join()

    def wait_for_completion(self):
        """
        Waits for all tasks to complete.
        """
        with self.condition:
            while self.tasks:
                self.condition.wait()

class bounded_thread_pool:
    """
    Implements a bounded thread pool with a fixed number of worker threads and a task queue.
    """

    def __init__(self, num_threads=4, max_queue_size=10):
        """
        Initializes the bounded thread pool.

        Args:
            num_threads (int, optional): The number of worker threads in the pool. Defaults to 4.
            max_queue_size (int, optional): The maximum number of tasks allowed in the queue. Defaults to 10.
        """
        self.num_threads = num_threads
        self.max_queue_size = max_queue_size
        self.tasks = []
        self.results = []
        self.threads = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.running = True
        self.create_threads()

    def create_threads(self):
        """
        Creates and starts the worker threads.
        """
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            self.threads.append(thread)
            thread.start()

    def worker(self):
        """
        The worker thread loop.
        """
        with self.condition:
            while self.running:
                if not self.tasks:
                    self.condition.wait()  # Wait for tasks
                if not self.running:
                    break
                if self.tasks:
                    task, args, kwargs = self.tasks.pop(0)
                    try:
                        result = task(*args, **kwargs)
                        with self.lock:
                            self.results.append(result)
                    except Exception as e:
                        logging.error(f"Task execution failed: {e}")

    def submit(self, task, *args, **kwargs):
        """
        Submits a task to the thread pool, blocking if the queue is full.

        Args:
            task (callable): The task to execute.
            *args: Positional arguments for the task.
            **kwargs: Keyword arguments for the task.
        """
        with self.condition:
            while len(self.tasks) >= self.max_queue_size and self.running:
                self.condition.wait()  # Wait for space in the queue

            if not self.running:
                return  # Don't add tasks if shutting down

            self.tasks.append((task, args, kwargs))
            self.condition.notify()  # Notify a waiting thread

    def get_results(self):
        """
        Gets the results of the executed tasks.

        Returns:
            list: A list of results.
        """
        with self.lock:
            results = self.results[:]
            self.results.clear()
            return results

    def shutdown(self, wait=True):
        """
        Shuts down the thread pool.

        Args:
            wait (bool, optional): Whether to wait for tasks to complete. Defaults to True.
        """
        with self.condition:
            self.running = False
            self.condition.notify_all()  # Notify all waiting threads

        if wait:
            for thread in self.threads:
                thread.join()

    def wait_for_completion(self):
        """
        Waits for all tasks to complete.
        """
        with self.condition:
            while self.tasks:
                self.condition.wait()
