"""
Severity Analysis Module
Analyzes disease severity based on detected bounding boxes
"""

import numpy as np
from typing import List, Dict, Tuple

def calculate_bbox_area(bbox: List[float]) -> float:
    """
    Calculate area of bounding box
    
    Args:
        bbox: Bounding box [x1, y1, x2, y2]
    
    Returns:
        area: Area in pixels
    """
    x1, y1, x2, y2 = bbox
    width = x2 - x1
    height = y2 - y1
    return width * height

def analyze_severity(detections: List[Dict], image_shape: Tuple[int, int]) -> Dict:
    """
    Analyze disease severity based on detections
    
    Args:
        detections: List of detection dictionaries
        image_shape: Image shape (height, width)
    
    Returns:
        severity_info: Dictionary with severity analysis
    """
    
    # Total image area
    total_area = image_shape[0] * image_shape[1]
    
    # Check if no detections or only healthy leaves
    if not detections:
        return {
            'category': 'No Detection',
            'percentage': 0.0,
            'infected_area': 0.0,
            'total_area': float(total_area),
            'description': 'No cotton leaf detected.',
            'color': 'gray',
            'severity_score': 0
        }
    
    # Calculate infected area (exclude healthy leaf detections)
    infected_area = 0.0
    disease_detections = []
    healthy_detections = []
    
    for detection in detections:
        bbox = detection['bbox']
        area = calculate_bbox_area(bbox)
        
        # Check if it's a disease or healthy leaf
        if detection['class_name'] == 'Healthy Leaf':
            healthy_detections.append(detection)
        else:
            infected_area += area
            disease_detections.append(detection)
    
    # If only healthy leaves detected
    if not disease_detections:
        return {
            'category': 'Healthy',
            'percentage': 0.0,
            'infected_area': 0.0,
            'total_area': float(total_area),
            'description': 'Only healthy leaves detected. No disease present.',
            'color': 'green',
            'severity_score': 0
        }
    
    # Calculate percentage of infected area
    percentage = (infected_area / total_area) * 100
    
    # Determine severity category
    if percentage < 10:
        category = 'Mild'
        description = 'Early stage infection detected. Immediate treatment recommended to prevent spread.'
        color = 'yellow'
        severity_score = 1
    elif percentage < 30:
        category = 'Moderate'
        description = 'Moderate infection level. Urgent treatment required to control disease spread.'
        color = 'orange'
        severity_score = 2
    else:
        category = 'Severe'
        description = 'Severe infection detected. Critical intervention needed immediately.'
        color = 'red'
        severity_score = 3
    
    # Get disease breakdown
    disease_breakdown = {}
    for detection in disease_detections:
        disease = detection['class_name']
        if disease not in disease_breakdown:
            disease_breakdown[disease] = {
                'count': 0,
                'total_confidence': 0.0,
                'area': 0.0
            }
        
        disease_breakdown[disease]['count'] += 1
        disease_breakdown[disease]['total_confidence'] += detection['confidence']
        disease_breakdown[disease]['area'] += calculate_bbox_area(detection['bbox'])
    
    # Calculate average confidence for each disease
    for disease in disease_breakdown:
        count = disease_breakdown[disease]['count']
        disease_breakdown[disease]['avg_confidence'] = disease_breakdown[disease]['total_confidence'] / count
        disease_breakdown[disease]['percentage'] = (disease_breakdown[disease]['area'] / total_area) * 100
    
    return {
        'category': category,
        'percentage': round(percentage, 2),
        'infected_area': round(infected_area, 2),
        'total_area': float(total_area),
        'description': description,
        'color': color,
        'severity_score': severity_score,
        'disease_breakdown': disease_breakdown,
        'num_disease_detections': len(disease_detections),
        'num_healthy_detections': len(healthy_detections)
    }

def get_severity_color(category: str) -> str:
    """
    Get color code for severity category
    
    Args:
        category: Severity category
    
    Returns:
        color: Hex color code
    """
    colors = {
        'Healthy': '#10b981',  # Green
        'Mild': '#fbbf24',     # Yellow
        'Moderate': '#f97316', # Orange
        'Severe': '#ef4444',    # Red
        'No Detection': '#9ca3af' # Gray
    }
    return colors.get(category, '#6b7280')  # Gray as default

def get_severity_recommendations(severity_info: Dict) -> List[str]:
    """
    Get severity-specific action recommendations
    
    Args:
        severity_info: Severity analysis dictionary
    
    Returns:
        recommendations: List of action items
    """
    category = severity_info['category']
    
    if category == 'No Detection':
        return [
            'Ensure a cotton leaf is clearly visible in the frame',
            'Move closer to the leaf',
            'Improve lighting conditions'
        ]
    elif category == 'Healthy':
        return [
            'Continue regular monitoring',
            'Maintain good agricultural practices',
            'Ensure proper irrigation and nutrition'
        ]
    elif category == 'Mild':
        return [
            'Apply preventive fungicides immediately',
            'Remove and destroy affected leaves',
            'Increase monitoring frequency to twice weekly',
            'Ensure proper plant spacing for air circulation'
        ]
    elif category == 'Moderate':
        return [
            'Apply systemic fungicides urgently',
            'Remove severely affected plant parts',
            'Implement strict sanitation measures',
            'Consider isolating affected plants',
            'Daily monitoring required'
        ]
    else:  # Severe
        return [
            'URGENT: Apply broad-spectrum fungicides immediately',
            'Consider removing severely infected plants',
            'Implement quarantine measures',
            'Consult agricultural extension officer',
            'Prepare for potential crop loss mitigation',
            'Continuous monitoring required'
        ]
