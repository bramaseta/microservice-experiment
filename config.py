class Config:
    # Service Configuration
    REST_HOST = '0.0.0.0'
    REST_PORT = 5000
    GRPC_HOST = '0.0.0.0'
    GRPC_PORT = 50051
    
    # Benchmark Configuration
    DEFAULT_REQUESTS = 1000
    DEFAULT_CONCURRENT_USERS = 10
    BENCHMARK_TIMEOUT = 300  # seconds
    
    # Monitoring Configuration
    MONITOR_WINDOW_SIZE = 60  # seconds
    METRICS_COLLECTION_INTERVAL = 1  # seconds
    
    # Adaptive Framework Configuration
    SWITCH_COOLDOWN = 30  # seconds
    DECISION_CONFIDENCE_THRESHOLD = 0.7
    
    # MECE Framework Thresholds
    HIGH_LATENCY_THRESHOLD = 100  # ms
    HIGH_CPU_THRESHOLD = 80  # percent
    HIGH_MEMORY_THRESHOLD = 75  # percent
    HIGH_CONCURRENCY_THRESHOLD = 100  # concurrent connections
    LARGE_PAYLOAD_THRESHOLD = 1024  # bytes