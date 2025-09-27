import time
import requests
import threading
import json
from dataclasses import dataclass
from typing import Dict, List, Any
import statistics

@dataclass
class MECEMetrics:
    # Business Processing Metrics
    avg_response_time: float
    cpu_per_request: float
    
    # Data Transmission Metrics
    payload_size: int
    network_overhead: float
    
    # Request Queuing Metrics
    concurrent_requests: int
    queue_wait_time: float
    
    # System Management Metrics
    memory_usage: float
    gc_overhead: float

class MECEAnalyzer:
    def __init__(self):
        self.results = {}
    
    def analyze_business_processing(self, service_metrics):
        """MECE Dimension 1: Business Processing"""
        return {
            'avg_response_time': service_metrics.get('avg_latency_ms', 0),
            'cpu_per_request': service_metrics.get('avg_cpu_usage', 0) / max(1, service_metrics.get('total_requests', 1)),
            'processing_efficiency': 1000 / max(1, service_metrics.get('avg_latency_ms', 1))
        }
    
    def analyze_data_transmission(self, protocol, payload_data):
        """MECE Dimension 2: Data Transmission"""
        if protocol == 'REST':
            json_size = len(json.dumps(payload_data).encode('utf-8'))
            overhead = json_size * 0.3  # JSON overhead estimation
            return {
                'payload_size': json_size,
                'network_overhead': overhead,
                'compression_ratio': 1.0
            }
        else:  # gRPC
            # Protocol Buffers lebih efisien
            estimated_protobuf_size = len(json.dumps(payload_data).encode('utf-8')) * 0.6
            overhead = estimated_protobuf_size * 0.1
            return {
                'payload_size': estimated_protobuf_size,
                'network_overhead': overhead,
                'compression_ratio': 0.6
            }
    
    def analyze_request_queuing(self, concurrent_tests_results):
        """MECE Dimension 3: Request Queuing - FIXED empty iterable error"""
        if not concurrent_tests_results:
            # Return default values when no test results available
            return {
                'max_concurrent_requests': 1,
                'avg_queue_wait_time': 0,
                'throughput_rps': 0
            }
        
        try:
            max_concurrent = max(concurrent_tests_results.keys()) if concurrent_tests_results.keys() else 1
            
            # Safely calculate averages with error handling
            latencies = [result.get('avg_latency', 0) for result in concurrent_tests_results.values() if result]
            rps_values = [result.get('requests_per_second', 0) for result in concurrent_tests_results.values() if result]
            
            avg_wait_time = statistics.mean(latencies) if latencies else 0
            total_rps = sum(rps_values) / len(rps_values) if rps_values else 0
            
            return {
                'max_concurrent_requests': max_concurrent,
                'avg_queue_wait_time': avg_wait_time,
                'throughput_rps': total_rps
            }
        except Exception as e:
            print(f"Warning: Error in request queuing analysis: {e}")
            return {
                'max_concurrent_requests': 1,
                'avg_queue_wait_time': 0,
                'throughput_rps': 0
            }
    
    def analyze_system_management(self, service_metrics):
        """MECE Dimension 4: System Management"""
        return {
            'avg_memory_usage': service_metrics.get('avg_memory_usage', 0),
            'memory_per_request': service_metrics.get('avg_memory_usage', 0) / max(1, service_metrics.get('total_requests', 1)),
            'gc_overhead_estimate': service_metrics.get('avg_cpu_usage', 0) * 0.1  # Estimasi GC overhead
        }
    
    def generate_mece_report(self, rest_metrics, grpc_metrics, test_data):
        """Generate comprehensive MECE analysis report"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'protocols_compared': ['REST', 'gRPC'],
            'mece_analysis': {}
        }
        
        for protocol, metrics in [('REST', rest_metrics), ('gRPC', grpc_metrics)]:
            report['mece_analysis'][protocol] = {
                'business_processing': self.analyze_business_processing(metrics),
                'data_transmission': self.analyze_data_transmission(protocol, test_data),
                'request_queuing': self.analyze_request_queuing({}),  # Akan diisi dari benchmark
                'system_management': self.analyze_system_management(metrics)
            }
        
        # Comparative Analysis
        report['comparison'] = self.compare_protocols(
            report['mece_analysis']['REST'],
            report['mece_analysis']['gRPC']
        )
        
        return report
    
    def compare_protocols(self, rest_analysis, grpc_analysis):
        """Compare protocols across MECE dimensions - FIXED division by zero error"""
        comparison = {}
        
        dimensions = ['business_processing', 'data_transmission', 'request_queuing', 'system_management']
        
        for dimension in dimensions:
            comparison[dimension] = {}
            rest_data = rest_analysis.get(dimension, {})
            grpc_data = grpc_analysis.get(dimension, {})
            
            for metric in rest_data:
                if metric in grpc_data:
                    rest_val = rest_data[metric]
                    grpc_val = grpc_data[metric]
                    
                    # Handle zero and None values safely
                    if rest_val is None or grpc_val is None:
                        continue
                    
                    if rest_val == 0 and grpc_val == 0:
                        comparison[dimension][metric] = {
                            'winner': 'Tie',
                            'improvement_percent': 0,
                            'rest_value': rest_val,
                            'grpc_value': grpc_val
                        }
                        continue
                    
                    # Safe comparison with proper division by zero handling
                    if rest_val > grpc_val:
                        winner = 'REST'
                        if grpc_val > 0:
                            improvement = ((rest_val - grpc_val) / grpc_val) * 100
                        else:
                            improvement = 100  # If grpc_val is 0, REST is infinitely better
                    else:
                        winner = 'gRPC'
                        if rest_val > 0:
                            improvement = ((grpc_val - rest_val) / rest_val) * 100
                        else:
                            improvement = 100  # If rest_val is 0, gRPC is infinitely better
                    
                    comparison[dimension][metric] = {
                        'winner': winner,
                        'improvement_percent': improvement,
                        'rest_value': rest_val,
                        'grpc_value': grpc_val
                    }
        
        return comparison