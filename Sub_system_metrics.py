"""
Sub_system_metrics Module

This module provides functionality to collect and expose system metrics using Prometheus.
It includes a class, SystemMetrics, that periodically updates Prometheus gauges with
CPU, memory, disk, and network usage statistics.

Classes:
    SystemMetrics: Collects and updates system metrics.
"""

import psutil
import time
import logging
import threading

class SystemMetrics:
    """
    Collects and updates system metrics using Prometheus gauges.

    Attributes:
        cpu_gauge (Gauge): Prometheus Gauge for CPU usage.
        memory_gauge (Gauge): Prometheus Gauge for memory usage.
        disk_gauge (Gauge): Prometheus Gauge for disk usage.
        network_sent_gauge (Gauge): Prometheus Gauge for network bytes sent.
        network_received_gauge (Gauge): Prometheus Gauge for network bytes received.
        update_interval (int): Interval in seconds to update metrics.
        stop_event (threading.Event): Event to stop the metrics updater thread.
    """

    def __init__(self, cpu_gauge, memory_gauge, disk_gauge, network_sent_gauge, network_received_gauge, update_interval=10):
        """
        Initializes SystemMetrics with Prometheus gauges and update interval.

        Args:
            cpu_gauge (Gauge): Prometheus Gauge for CPU usage.
            memory_gauge (Gauge): Prometheus Gauge for memory usage.
            disk_gauge (Gauge): Prometheus Gauge for disk usage.
            network_sent_gauge (Gauge): Prometheus Gauge for network bytes sent.
            network_received_gauge (Gauge): Prometheus Gauge for network bytes received.
            update_interval (int, optional): Interval in seconds to update metrics. Defaults to 10.
        """
        self.cpu_gauge = cpu_gauge
        self.memory_gauge = memory_gauge
        self.disk_gauge = disk_gauge
        self.network_sent_gauge = network_sent_gauge
        self.network_received_gauge = network_received_gauge
        self.update_interval = update_interval
        self.stop_event = threading.Event()

    def _update_metrics(self):
        """
        Updates Prometheus gauges with current system metrics.
        """
        try:
            self.cpu_gauge.set(psutil.cpu_percent(interval=1))
            self.memory_gauge.set(psutil.virtual_memory().percent)
            self.disk_gauge.set(psutil.disk_usage('/').percent)
            network_stats = psutil.net_io_counters()
            self.network_sent_gauge.set(network_stats.bytes_sent)
            self.network_received_gauge.set(network_stats.bytes_recv)
        except Exception as e:
            logging.error(f"Error updating system metrics: {e}")

    def _metrics_updater(self):
        """
        Periodically updates system metrics in a loop.
        """
        while not self.stop_event.is_set():
            self._update_metrics()
            time.sleep(self.update_interval)

    def start_metrics_updater(self):
        """
        Starts the metrics updater thread.
        """
        self.thread = threading.Thread(target=self._metrics_updater)
        self.thread.daemon = True  # Allow program to exit even if thread is running
        self.thread.start()

    def stop_metrics_updater(self):
        """
        Stops the metrics updater thread.
        """
        self.stop_event.set()
        if self.thread.is_alive():
            self.thread.join()
