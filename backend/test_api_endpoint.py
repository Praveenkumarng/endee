"""
Test the actual API endpoint to see the response format
"""

import requests
import json
from pathlib import Path

# Find a test image
test_images = list(Path('.').glob('**/*.jpg')) + list(Path('.').glob('**/*.png'))
if test_images:
    test_image = test_images[0]
    print(f"Using test image: {test_image}")
    
    # Make API request
    url = 'http://localhost:8000/predict-image'
    params = {
        'conf_threshold': 0.25,
        'language': 'en'
    }
    
    files = {'file': open(test_image, 'rb')}
    
    try:
        response = requests.post(url, params=params, files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("\n" + "="*60)
            print("API Response:")
            print("="*60)
            print(f"Success: {data.get('success')}")
            print(f"Num detections: {data.get('num_detections')}")
            print(f"Severity: {data.get('severity', {}).get('category')}")
            print(f"\nRecommendations ({len(data.get('recommendations', []))}):")
            print("-"*60)
            for i, rec in enumerate(data.get('recommendations', []), 1):
                print(f"\n{i}. {rec.get('title')}")
                print(f"   Type: {rec.get('type')}")
                print(f"   ID: {rec.get('id')}")
                print(f"   Priority: {rec.get('priority')}")
                print(f"   Description: {rec.get('description')[:100]}...")
            print("="*60)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Request failed: {e}")
else:
    print("No test images found")
