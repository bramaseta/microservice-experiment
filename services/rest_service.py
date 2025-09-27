from flask import Flask, request, jsonify
import time
import json
import psutil
import threading
from datetime import datetime

class RESTUserService:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.metrics = {
            'requests': 0,
            'total_latency': 0,
            'cpu_usage': [],
            'memory_usage': []
        }
        
    def setup_routes(self):
        @self.app.route('/user/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            start_time = time.time()
            
            # Simulasi business processing
            user_data = self.get_user_data(user_id)
            
            # Tracking metrics
            latency = (time.time() - start_time) * 1000
            self.update_metrics(latency)
            
            return jsonify(user_data)
        
        @self.app.route('/users', methods=['POST'])
        def create_user():
            start_time = time.time()
            
            user_data = request.get_json()
            result = self.create_user_data(user_data)
            
            latency = (time.time() - start_time) * 1000
            self.update_metrics(latency)
            
            return jsonify(result)
        
        # FIXED: Added health endpoint
        @self.app.route('/health', methods=['GET'])
        def health():
            return jsonify({
                "status": "healthy", 
                "service": "REST",
                "requests_processed": self.metrics['requests']
            })
    
    def get_user_data(self, user_id):
        # Simulasi query database
        time.sleep(0.01)  # Simulasi I/O delay
        return {
            'id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com',
            'created_at': datetime.now().isoformat(),
            'profile': {
                'bio': 'This is a sample bio' * 10,  # Data yang cukup besar
                'preferences': ['pref1', 'pref2', 'pref3'] * 20
            }
        }
    
    def create_user_data(self, user_data):
        # Simulasi pembuatan user
        time.sleep(0.015)  # Simulasi processing delay
        return {
            'id': 12345,
            'status': 'created',
            'data': user_data
        }
    
    def update_metrics(self, latency):
        self.metrics['requests'] += 1
        self.metrics['total_latency'] += latency
        self.metrics['cpu_usage'].append(psutil.cpu_percent())
        self.metrics['memory_usage'].append(psutil.virtual_memory().percent)
    
    def get_metrics(self):
        avg_latency = self.metrics['total_latency'] / max(1, self.metrics['requests'])
        return {
            'protocol': 'REST',
            'total_requests': self.metrics['requests'],
            'avg_latency_ms': avg_latency,
            'avg_cpu_usage': sum(self.metrics['cpu_usage']) / max(1, len(self.metrics['cpu_usage'])),
            'avg_memory_usage': sum(self.metrics['memory_usage']) / max(1, len(self.metrics['memory_usage']))
        }
    
    def run(self, host='0.0.0.0', port=5000):
        # FIXED: Removed debug parameter that was causing the error
        self.app.run(host=host, port=port, threaded=True, use_reloader=False)
    
    def start_in_thread(self, host='127.0.0.1', port=5000):
        """Start REST service in separate thread for better control"""
        def run_service():
            try:
                self.run(host=host, port=port)
            except Exception as e:
                print(f"REST service thread error: {e}")
        
        thread = threading.Thread(target=run_service, daemon=True)
        thread.start()
        time.sleep(2)  # Give more time for Flask to start
        return thread

    def run_clean(self, host='0.0.0.0', port=5000):
        """Clean run method without any problematic parameters"""
        self.app.run(
            host=host,
            port=port,
            threaded=True,
            use_reloader=False
        )