import time
import threading
import psutil
from collections import deque
import statistics

class SystemMonitor:
    def __init__(self, window_size=60):
        self.window_size = window_size  # seconds
        self.metrics = {
            'latency': deque(maxlen=window_size),
            'cpu_usage': deque(maxlen=window_size),
            'memory_usage': deque(maxlen=window_size),
            'request_rate': deque(maxlen=window_size),
            'concurrent_connections': deque(maxlen=window_size)
        }
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start system monitoring in background thread"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        print("System Monitor: Started")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("System Monitor: Stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            # Collect system metrics
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            
            self.metrics['cpu_usage'].append(cpu)
            self.metrics['memory_usage'].append(memory)
            
            time.sleep(1)
    
    def record_request_metrics(self, latency, payload_size, concurrent_conn=1):
        """Record request-specific metrics"""
        self.metrics['latency'].append(latency)
        self.metrics['concurrent_connections'].append(concurrent_conn)
        
        # Calculate request rate (requests per second)
        current_time = time.time()
        if hasattr(self, 'last_request_time'):
            time_diff = current_time - self.last_request_time
            if time_diff > 0:
                rate = 1 / time_diff
                self.metrics['request_rate'].append(rate)
        
        self.last_request_time = current_time
    
    def get_current_condition(self) -> 'SystemCondition':
        """Get current system condition for decision making"""
        from adaptive_framework.decision_engine import SystemCondition
        
        return SystemCondition(
            current_latency=statistics.mean(self.metrics['latency']) if self.metrics['latency'] else 0,
            cpu_usage=statistics.mean(self.metrics['cpu_usage']) if self.metrics['cpu_usage'] else 0,
            memory_usage=statistics.mean(self.metrics['memory_usage']) if self.metrics['memory_usage'] else 0,
            request_rate=statistics.mean(self.metrics['request_rate']) if self.metrics['request_rate'] else 0,
            payload_size=1024,  # Default estimate
            concurrent_connections=max(self.metrics['concurrent_connections']) if self.metrics['concurrent_connections'] else 1
        )