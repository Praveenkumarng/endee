"""
Logging and History Management Module
Stores prediction history and provides retrieval functions
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# Default log file path
LOG_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prediction_logs', 'predictions.json')

def ensure_log_directory():
    """Ensure log directory exists"""
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)

def log_prediction(
    filename: str,
    predictions: List[Dict],
    severity: Dict,
    additional_info: Optional[Dict] = None
):
    """
    Log a prediction to the history file
    
    Args:
        filename: Name of the processed file
        predictions: List of detection dictionaries
        severity: Severity analysis dictionary
        additional_info: Optional additional information
    """
    
    ensure_log_directory()
    
    # Create log entry
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'filename': filename,
        'predictions': predictions,
        'severity': severity,
        'num_detections': len(predictions)
    }
    
    if additional_info:
        log_entry.update(additional_info)
    
    # Load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    
    # Append new log
    logs.append(log_entry)
    
    # Keep only last 1000 entries to prevent file from growing too large
    if len(logs) > 1000:
        logs = logs[-1000:]
    
    # Save logs
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def get_prediction_history(limit: int = 50) -> List[Dict]:
    """
    Retrieve prediction history
    
    Args:
        limit: Maximum number of records to return
    
    Returns:
        history: List of historical predictions
    """
    
    ensure_log_directory()
    
    if not os.path.exists(LOG_FILE):
        return []
    
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
        
        # Return most recent entries
        return logs[-limit:] if len(logs) > limit else logs
        
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def get_statistics() -> Dict:
    """
    Calculate statistics from prediction history
    
    Returns:
        stats: Dictionary with various statistics
    """
    
    history = get_prediction_history(limit=1000)
    
    if not history:
        return {
            'total_predictions': 0,
            'disease_counts': {},
            'severity_distribution': {},
            'avg_detections_per_image': 0
        }
    
    # Initialize counters
    disease_counts = {}
    severity_counts = {}
    total_detections = 0
    
    for record in history:
        # Count diseases
        for prediction in record.get('predictions', []):
            disease = prediction.get('class_name', 'Unknown')
            disease_counts[disease] = disease_counts.get(disease, 0) + 1
            total_detections += 1
        
        # Count severity
        severity = record.get('severity', {}).get('category', 'Unknown')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    return {
        'total_predictions': len(history),
        'disease_counts': disease_counts,
        'severity_distribution': severity_counts,
        'avg_detections_per_image': total_detections / len(history) if history else 0,
        'total_detections': total_detections
    }

def clear_history():
    """Clear all prediction history"""
    ensure_log_directory()
    
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

def export_history_csv(output_path: str):
    """
    Export prediction history to CSV
    
    Args:
        output_path: Path to save CSV file
    """
    
    import csv
    
    history = get_prediction_history(limit=10000)
    
    if not history:
        return
    
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'filename', 'num_detections', 'severity_category', 
                     'severity_percentage', 'diseases_detected']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for record in history:
            # Get unique diseases
            diseases = set()
            for pred in record.get('predictions', []):
                if pred.get('class_name') != 'Healthy Leaf':
                    diseases.add(pred.get('class_name'))
            
            writer.writerow({
                'timestamp': record.get('timestamp'),
                'filename': record.get('filename'),
                'num_detections': record.get('num_detections', 0),
                'severity_category': record.get('severity', {}).get('category', 'Unknown'),
                'severity_percentage': record.get('severity', {}).get('percentage', 0),
                'diseases_detected': ', '.join(diseases) if diseases else 'None'
            })

def get_recent_files(limit: int = 10) -> List[str]:
    """
    Get list of recently processed files
    
    Args:
        limit: Number of recent files to return
    
    Returns:
        files: List of filenames
    """
    
    history = get_prediction_history(limit=limit)
    return [record.get('filename') for record in history]
