import time
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional

class Protocol(Enum):
    REST = "REST"
    GRPC = "gRPC"

@dataclass
class SystemCondition:
    current_latency: float
    cpu_usage: float
    memory_usage: float
    request_rate: float
    payload_size: int
    concurrent_connections: int

@dataclass
class DecisionRule:
    condition_name: str
    threshold_values: Dict[str, Any]
    recommended_protocol: Protocol
    confidence_score: float

class AdaptiveDecisionEngine:
    def __init__(self):
        self.decision_rules = self.initialize_decision_rules()
        self.current_protocol = Protocol.REST
        self.switch_cooldown = 30  # seconds
        self.last_switch_time = 0
    
    def initialize_decision_rules(self):
        """Initialize decision rules based on MECE framework analysis"""
        return [
            # Rule 1: High latency dengan payload besar -> gRPC
            DecisionRule(
                condition_name="high_latency_large_payload",
                threshold_values={
                    "min_latency": 100,  # ms
                    "min_payload_size": 1024,  # bytes
                },
                recommended_protocol=Protocol.GRPC,
                confidence_score=0.8
            ),
            
            # Rule 2: Low latency dengan small payload -> REST
            DecisionRule(
                condition_name="low_latency_small_payload",
                threshold_values={
                    "max_latency": 50,  # ms
                    "max_payload_size": 512,  # bytes
                },
                recommended_protocol=Protocol.REST,
                confidence_score=0.7
            ),
            
            # Rule 3: High concurrency -> gRPC
            DecisionRule(
                condition_name="high_concurrency",
                threshold_values={
                    "min_concurrent_connections": 100,
                    "min_request_rate": 1000,  # requests per second
                },
                recommended_protocol=Protocol.GRPC,
                confidence_score=0.9
            ),
            
            # Rule 4: High CPU usage -> REST (simpler processing)
            DecisionRule(
                condition_name="high_cpu_usage",
                threshold_values={
                    "min_cpu_usage": 80,  # percent
                },
                recommended_protocol=Protocol.REST,
                confidence_score=0.6
            ),
            
            # Rule 5: Memory pressure -> gRPC (more efficient)
            DecisionRule(
                condition_name="memory_pressure",
                threshold_values={
                    "min_memory_usage": 75,  # percent
                },
                recommended_protocol=Protocol.GRPC,
                confidence_score=0.75
            )
        ]
    
    def evaluate_condition(self, system_condition: SystemCondition) -> Optional[Protocol]:
        """Evaluate system condition and recommend protocol"""
        
        # Check cooldown period
        current_time = time.time()
        if current_time - self.last_switch_time < self.switch_cooldown:
            return self.current_protocol
        
        best_rule = None
        highest_confidence = 0
        
        for rule in self.decision_rules:
            if self.matches_rule(system_condition, rule):
                if rule.confidence_score > highest_confidence:
                    highest_confidence = rule.confidence_score
                    best_rule = rule
        
        if best_rule and best_rule.recommended_protocol != self.current_protocol:
            print(f"Decision Engine: Switching to {best_rule.recommended_protocol.value}")
            print(f"Reason: {best_rule.condition_name} (confidence: {best_rule.confidence_score})")
            
            self.current_protocol = best_rule.recommended_protocol
            self.last_switch_time = current_time
            return best_rule.recommended_protocol
        
        return self.current_protocol
    
    def matches_rule(self, condition: SystemCondition, rule: DecisionRule) -> bool:
        """Check if system condition matches a decision rule"""
        
        if rule.condition_name == "high_latency_large_payload":
            return (condition.current_latency >= rule.threshold_values["min_latency"] and
                   condition.payload_size >= rule.threshold_values["min_payload_size"])
        
        elif rule.condition_name == "low_latency_small_payload":
            return (condition.current_latency <= rule.threshold_values["max_latency"] and
                   condition.payload_size <= rule.threshold_values["max_payload_size"])
        
        elif rule.condition_name == "high_concurrency":
            return (condition.concurrent_connections >= rule.threshold_values["min_concurrent_connections"] or
                   condition.request_rate >= rule.threshold_values["min_request_rate"])
        
        elif rule.condition_name == "high_cpu_usage":
            return condition.cpu_usage >= rule.threshold_values["min_cpu_usage"]
        
        elif rule.condition_name == "memory_pressure":
            return condition.memory_usage >= rule.threshold_values["min_memory_usage"]
        
        return False