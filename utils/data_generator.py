import random
import json
from datetime import datetime, timedelta

class TestDataGenerator:
    """Generate test data for benchmarking"""
    
    @staticmethod
    def generate_user_data(size='medium'):
        """Generate user data of different sizes"""
        
        sizes = {
            'small': {'bio_multiplier': 1, 'prefs_count': 3},
            'medium': {'bio_multiplier': 10, 'prefs_count': 20},
            'large': {'bio_multiplier': 50, 'prefs_count': 100}
        }
        
        config = sizes.get(size, sizes['medium'])
        
        return {
            'id': random.randint(1, 10000),
            'name': f'User {random.randint(1, 1000)}',
            'email': f'user{random.randint(1, 1000)}@example.com',
            'created_at': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
            'profile': {
                'bio': 'This is a sample bio ' * config['bio_multiplier'],
                'preferences': [f'pref{i}' for i in range(config['prefs_count'])],
                'settings': {
                    'theme': 'dark',
                    'notifications': True,
                    'privacy_level': random.choice(['public', 'private', 'friends'])
                }
            }
        }
    
    @staticmethod
    def generate_load_scenarios():
        """Generate different load testing scenarios"""
        return [
            {'name': 'Light Load', 'requests': 100, 'concurrent': 1, 'payload': 'small'},
            {'name': 'Medium Load', 'requests': 500, 'concurrent': 10, 'payload': 'medium'},
            {'name': 'Heavy Load', 'requests': 1000, 'concurrent': 50, 'payload': 'large'},
            {'name': 'Stress Test', 'requests': 2000, 'concurrent': 100, 'payload': 'large'},
        ]