"""
API Client for backend communication
"""

import requests
import os

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
        
    def predict_image(self, image_path, conf_threshold=0.25):
        """Predict disease from image file"""
        with open(image_path, 'rb') as f:
            files = {'file': f}
            params = {'conf_threshold': conf_threshold}
            response = requests.post(
                f"{self.base_url}/pc-app-endpoint",
                files=files,
                params=params
            )
            return response.json()
