"""
Configuration Module for Backend API
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Model configuration
MODEL_WEIGHTS = os.getenv('MODEL_WEIGHTS', str(BASE_DIR / 'weights' / 'best.pt'))
MODEL_TYPE = os.getenv('MODEL_TYPE', 'pytorch')  # 'pytorch' or 'onnx'

# Inference configuration
CONF_THRESHOLD = float(os.getenv('CONF_THRESHOLD', '0.25'))
IOU_THRESHOLD = float(os.getenv('IOU_THRESHOLD', '0.7'))
IMG_SIZE = int(os.getenv('IMG_SIZE', '640'))

# Device configuration
DEVICE = os.getenv('DEVICE', '')  # '' for auto, 'cpu', or '0' for GPU 0

# API configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))
API_WORKERS = int(os.getenv('API_WORKERS', '1'))

# CORS configuration
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')

# File upload configuration
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', '10485760'))  # 10MB default
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

# Logging configuration
LOG_DIR = BASE_DIR.parent / 'data' / 'prediction_logs'
LOG_FILE = LOG_DIR / 'predictions.json'

# Class names
CLASS_NAMES = [
    'Bacterial Blight',
    'Fusarium Wilt',
    'Healthy Leaf',
    'Leaf Curl Virus'
]

# Ensure directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(BASE_DIR / 'weights', exist_ok=True)
