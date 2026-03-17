"""
Test AI recommendations with a sample detection
"""

from utils.ai_recommendations import generate_ai_recommendations

# Sample detection data
detections = [
    {
        'class_name': 'Bacterial Blight',
        'confidence': 0.85,
        'bbox': [100, 100, 200, 200]
    }
]

# Sample severity info
severity_info = {
    'category': 'Moderate',
    'severity_score': 3,
    'percentage': 35.5,
    'description': 'Moderate infection detected'
}

print("Testing AI Recommendations...")
print("="*60)
print(f"Disease: {detections[0]['class_name']}")
print(f"Severity: {severity_info['category']} ({severity_info['percentage']}%)")
print("="*60)
print()

# Test English
print("🇬🇧 English Recommendations:")
print("-"*60)
recs_en = generate_ai_recommendations(detections, severity_info, language='en')
for i, rec in enumerate(recs_en, 1):
    print(f"{i}. [{rec['type'].upper()}] {rec['title']}")
    print(f"   {rec['description']}")
    print(f"   Priority: {rec['priority']}")
    print()

print("="*60)
print()

# Test Hindi
print("🇮🇳 Hindi Recommendations:")
print("-"*60)
recs_hi = generate_ai_recommendations(detections, severity_info, language='hi')
for i, rec in enumerate(recs_hi, 1):
    print(f"{i}. [{rec['type'].upper()}] {rec['title']}")
    print(f"   {rec['description']}")
    print(f"   Priority: {rec['priority']}")
    print()

print("="*60)
print("✓ Test completed!")
