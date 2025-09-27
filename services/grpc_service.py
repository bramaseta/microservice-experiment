import grpc
from concurrent import futures
import time
import psutil
from datetime import datetime
import threading

# Simulasi generated protobuf classes (biasanya dari protoc compiler)
class GetUserRequest:
    def __init__(self, user_id=0):
        self.user_id = user_id

class UserProfile:
    def __init__(self, bio="", preferences=[]):
        self.bio = bio
        self.preferences = preferences

class GetUserResponse:
    def __init__(self, id=0, name="", email="", created_at="", profile=None):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.profile = profile or UserProfile()

class CreateUserRequest:
    def __init__(self, name="", email="", profile=None):
        self.name = name
        self.email = email
        self.profile = profile or UserProfile()

class CreateUserResponse:
    def __init__(self, id=0, status=""):
        self.id = id
        self.status = status

class GRPCUserService:
    def __init__(self):
        self.metrics = {
            'requests': 0,
            'total_latency': 0,
            'cpu_usage': [],
            'memory_usage': []
        }
        self.server = None
        self.stop_event = None
    
    def GetUser(self, request, context):
        start_time = time.time()
        
        # Simulasi business processing
        time.sleep(0.01)  # Simulasi I/O delay
        
        profile = UserProfile(
            bio='This is a sample bio' * 10,
            preferences=['pref1', 'pref2', 'pref3'] * 20
        )
        
        response = GetUserResponse(
            id=request.user_id,
            name=f'User {request.user_id}',
            email=f'user{request.user_id}@example.com',
            created_at=datetime.now().isoformat(),
            profile=profile
        )
        
        latency = (time.time() - start_time) * 1000
        self.update_metrics(latency)
        
        return response
    
    def CreateUser(self, request, context):
        start_time = time.time()
        
        # Simulasi pembuatan user
        time.sleep(0.015)  # Simulasi processing delay
        
        response = CreateUserResponse(
            id=12345,
            status='created'
        )
        
        latency = (time.time() - start_time) * 1000
        self.update_metrics(latency)
        
        return response
    
    def update_metrics(self, latency):
        self.metrics['requests'] += 1
        self.metrics['total_latency'] += latency
        self.metrics['cpu_usage'].append(psutil.cpu_percent())
        self.metrics['memory_usage'].append(psutil.virtual_memory().percent)
    
    def get_metrics(self):
        avg_latency = self.metrics['total_latency'] / max(1, self.metrics['requests'])
        return {
            'protocol': 'gRPC',
            'total_requests': self.metrics['requests'],
            'avg_latency_ms': avg_latency,
            'avg_cpu_usage': sum(self.metrics['cpu_usage']) / max(1, len(self.metrics['cpu_usage'])),
            'avg_memory_usage': sum(self.metrics['memory_usage']) / max(1, len(self.metrics['memory_usage']))
        }
    
    def start_in_thread(self, port=50051):
        """FIXED: Start gRPC service in separate thread"""
        def run_server():
            try:
                self.serve(port)
            except Exception as e:
                print(f"gRPC service error: {e}")
        
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        time.sleep(1)  # Give time to start
        return thread
    
    def serve(self, port=50051):
        """FIXED: Start gRPC server with proper error handling"""
        try:
            self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            # server.add_UserServiceServicer_to_server(self, server)  # Biasanya dari generated code
            self.server.add_insecure_port(f'[::]:{port}')
            self.server.start()
            print(f"gRPC Server started on port {port}")
            
            # Keep server running with proper stop mechanism
            self.stop_event = threading.Event()
            
            try:
                self.stop_event.wait()  # Wait until stop_event is set
            except KeyboardInterrupt:
                print("gRPC server interrupted")
            finally:
                if self.server:
                    self.server.stop(0)
                    
        except Exception as e:
            print(f"gRPC server error: {e}")
    
    def stop(self):
        """FIXED: Properly stop gRPC server"""
        if self.stop_event:
            self.stop_event.set()
        if self.server:
            self.server.stop(0)