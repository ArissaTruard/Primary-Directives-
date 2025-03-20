import psutil
import time
import logging

class SystemMetrics:
    def __init__(self, cpu_gauge, memory_gauge, disk_gauge, network_sent_gauge, network_received_gauge):
        self.cpu_gauge = cpu_gauge
        self.memory_gauge = memory_gauge
        self.disk_gauge = disk_gauge
        self.network_sent
