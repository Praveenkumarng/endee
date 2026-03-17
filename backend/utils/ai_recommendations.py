"""
AI-Powered Treatment Recommendations using Google Gemini
Generates dynamic, severity-based treatment recommendations with robust error handling
"""

import os
import json
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Only import and configure if API key is available
model = None
if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash')  # Updated to available model
        print("✓ Gemini API configured successfully")
    except Exception as e:
        print(f"⚠ Warning: Failed to configure Gemini API: {str(e)}")
        model = None
else:
    print("⚠ Warning: GEMINI_API_KEY not set. Using hardcoded recommendations.")


def generate_ai_recommendations(
    detections: List[Dict],
    severity_info: Dict,
    language: str = 'en'
) -> List[Dict]:
    """
    Generate AI-powered treatment recommendations using Gemini
    Falls back to hardcoded recommendations if AI fails
    
    Args:
        detections: List of disease detections
        severity_info: Severity analysis information
        language: Language code (en, hi, te, kn)
    
    Returns:
        List of recommendation dictionaries
    """
    
    # If no model available, use hardcoded recommendations
    if not model:
        from utils.recommendations import get_recommendations
        return get_recommendations(detections, severity_info)
    
    try:
        # Extract disease information
        diseases = []
        for detection in detections:
            if detection['class_name'] != 'Healthy Leaf':
                diseases.append({
                    'name': detection['class_name'],
                    'confidence': detection['confidence']
                })
        
        # If no diseases detected, return healthy or no detection recommendations
        if not diseases or severity_info['category'] in ['Healthy', 'No Detection']:
            if severity_info['category'] == 'No Detection':
                return _get_no_detection_recommendations(language)
            return _get_healthy_recommendations(language)
        
        # Build prompt for Gemini
        prompt = _build_prompt(diseases, severity_info, language)
        
        # Generate recommendations with timeout
        print(f"Generating AI recommendations for {len(diseases)} disease(s) in {language}...")
        
        generation_config = {
            'temperature': 0.7,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 1024,
        }
        
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Parse and return recommendations
        recommendations = _parse_response(response.text, language)
        print(f"✓ Generated {len(recommendations)} AI recommendations")
        return recommendations
        
    except Exception as e:
        print(f"⚠ AI recommendation generation failed: {str(e)}")
        # Fallback to hardcoded recommendations
        from utils.recommendations import get_recommendations
        return get_recommendations(detections, severity_info)


def _build_prompt(diseases: List[Dict], severity_info: Dict, language: str) -> str:
    """Build optimized prompt for Gemini"""
    
    lang_map = {'en': 'English', 'hi': 'Hindi', 'te': 'Telugu', 'kn': 'Kannada'}
    lang_name = lang_map.get(language, 'English')
    
    disease_list = ', '.join([d['name'] for d in diseases])
    severity = severity_info['category']
    percentage = severity_info.get('percentage', 0)
    
    return f"""Generate 5 cotton disease treatment recommendations in {lang_name}.

Disease: {disease_list}
Severity: {severity} ({percentage:.1f}% affected)

Requirements:
- Mix of chemical, organic, and preventive treatments
- Prioritize based on severity (severe = more chemical, mild = more organic)
- Include specific dosages
- Keep titles under 50 chars, descriptions under 150 chars

Format as JSON array:
[
  {{
    "id": "treatment_name_lowercase",
    "type": "chemical|organic|prevention",
    "title": "Treatment Name in {lang_name}",
    "description": "Detailed instructions in {lang_name}",
    "priority": "high|medium|low"
  }}
]

Return ONLY valid JSON, no markdown or extra text."""


def _parse_response(response_text: str, language: str) -> List[Dict]:
    """Parse Gemini response with robust error handling"""
    
    try:
        # Clean response
        text = response_text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        
        text = text.strip()
        
        # Parse JSON
        recommendations = json.loads(text)
        
        # Validate and format
        formatted = []
        for i, rec in enumerate(recommendations[:7]):  # Max 7 recommendations
            formatted.append({
                'id': rec.get('id', f'ai_rec_{i+1}'),
                'type': rec.get('type', 'prevention'),
                'title': rec.get('title', 'Treatment Recommendation')[:100],
                'description': rec.get('description', '')[:200],
                'priority': rec.get('priority', 'medium')
            })
        
        return formatted if formatted else _get_fallback_recommendations(language)
        
    except json.JSONDecodeError as e:
        print(f"⚠ JSON parse error: {str(e)}")
        return _get_fallback_recommendations(language)
    except Exception as e:
        print(f"⚠ Response parse error: {str(e)}")
        return _get_fallback_recommendations(language)


def _get_healthy_recommendations(language: str) -> List[Dict]:
    """Get recommendations for healthy plants"""
    
    recs = {
        'en': [
            {'id': 'monitor', 'type': 'prevention', 'title': 'Regular Monitoring', 
             'description': 'Inspect plants weekly for early disease signs.', 'priority': 'high'},
            {'id': 'nutrition', 'type': 'prevention', 'title': 'Balanced Nutrition',
             'description': 'Apply NPK fertilizer as per soil test.', 'priority': 'medium'},
            {'id': 'preventive', 'type': 'prevention', 'title': 'Preventive Sprays',
             'description': 'Apply fungicides during disease-prone seasons.', 'priority': 'low'}
        ],
        'hi': [
            {'id': 'monitor', 'type': 'prevention', 'title': 'नियमित निगरानी',
             'description': 'रोग के शुरुआती संकेतों के लिए साप्ताहिक निरीक्षण करें।', 'priority': 'high'},
            {'id': 'nutrition', 'type': 'prevention', 'title': 'संतुलित पोषण',
             'description': 'मिट्टी परीक्षण के अनुसार NPK उर्वरक लागू करें।', 'priority': 'medium'},
            {'id': 'preventive', 'type': 'prevention', 'title': 'निवारक स्प्रे',
             'description': 'रोग-प्रवण मौसम में कवकनाशी लागू करें।', 'priority': 'low'}
        ],
        'te': [
            {'id': 'monitor', 'type': 'prevention', 'title': 'నియమిత పర్యవేక్షణ',
             'description': 'వ్యాధి సంకేతాల కోసం వారానికోసారి తనిఖీ చేయండి।', 'priority': 'high'},
            {'id': 'nutrition', 'type': 'prevention', 'title': 'సమతుల్య పోషణ',
             'description': 'మట్టి పరీక్ష ప్రకారం NPK ఎరువులు వర్తించండి।', 'priority': 'medium'},
            {'id': 'preventive', 'type': 'prevention', 'title': 'నివారణ స్ప్రేలు',
             'description': 'వ్యాధి సీజన్లలో శిలీంద్రనాశకాలను వర్తించండి।', 'priority': 'low'}
        ],
        'kn': [
            {'id': 'monitor', 'type': 'prevention', 'title': 'ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ',
             'description': 'ರೋಗ ಚಿಹ್ನೆಗಳಿಗಾಗಿ ವಾರಕ್ಕೊಮ್ಮೆ ಪರಿಶೀಲಿಸಿ।', 'priority': 'high'},
            {'id': 'nutrition', 'type': 'prevention', 'title': 'ಸಮತೋಲಿತ ಪೋಷಣೆ',
             'description': 'ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ ಪ್ರಕಾರ NPK ರಸಗೊಬ್ಬರ ಅನ್ವಯಿಸಿ।', 'priority': 'medium'},
            {'id': 'preventive', 'type': 'prevention', 'title': 'ತಡೆಗಟ್ಟುವ ಸಿಂಪಡಣೆ',
             'description': 'ರೋಗ ಋತುಗಳಲ್ಲಿ ಶಿಲೀಂಧ್ರನಾಶಕಗಳನ್ನು ಅನ್ವಯಿಸಿ।', 'priority': 'low'}
        ]
    }
    
    return recs.get(language, recs['en'])


def _get_fallback_recommendations(language: str) -> List[Dict]:
    """Fallback recommendations if AI fails"""
    
    return [
        {
            'id': 'consult_expert',
            'type': 'prevention',
            'title': 'Consult Agricultural Expert' if language == 'en' else 'कृषि विशेषज्ञ से परामर्श करें',
            'description': 'Contact local agricultural extension officer for treatment advice.',
            'priority': 'high'
        },
        {
            'id': 'monitor_spread',
            'type': 'prevention',
            'title': 'Monitor Disease Spread' if language == 'en' else 'रोग प्रसार की निगरानी करें',
            'description': 'Track disease progression daily and document changes.',
            'priority': 'high'
        }
    ]


def _get_no_detection_recommendations(language: str) -> List[Dict]:
    """Get recommendations when no leaf is detected"""
    
    recs = {
        'en': [
            {'id': 'visibility', 'type': 'prevention', 'title': 'Improve Visibility',
             'description': 'Ensure the cotton leaf is clearly visible and well-lit.', 'priority': 'high'},
            {'id': 'distance', 'type': 'prevention', 'title': 'Adjust Distance',
             'description': 'Move the camera closer to the leaf.', 'priority': 'medium'}
        ],
        'hi': [
            {'id': 'visibility', 'type': 'prevention', 'title': 'दृश्यता में सुधार करें',
             'description': 'सुनिश्चित करें कि कपास की पत्ती स्पष्ट रूप से दिखाई दे रही है।', 'priority': 'high'},
            {'id': 'distance', 'type': 'prevention', 'title': 'दूरी समायोजित करें',
             'description': 'कैमरे को पत्ती के करीब ले जाएं।', 'priority': 'medium'}
        ],
        'te': [
            {'id': 'visibility', 'type': 'prevention', 'title': 'దృశ్యమానతను మెరుగుపరచండి',
             'description': 'పత్తి ఆకు స్పష్టంగా కనిపించేలా చూసుకోండి।', 'priority': 'high'},
            {'id': 'distance', 'type': 'prevention', 'title': 'దూరాన్ని సర్దుబాటు చేయండి',
             'description': 'కెమెరాను ఆకుకు దగ్గరగా జరపండి।', 'priority': 'medium'}
        ],
        'kn': [
            {'id': 'visibility', 'type': 'prevention', 'title': 'ಗೋಚರತೆಯನ್ನು ಸುಧಾರಿಸಿ',
             'description': 'ಹತ್ತಿ ಎಲೆ ಸ್ಪಷ್ಟವಾಗಿ ಗೋಚರಿಸುವುದನ್ನು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ।', 'priority': 'high'},
            {'id': 'distance', 'type': 'prevention', 'title': 'ದೂರವನ್ನು ಹೊಂದಿಸಿ',
             'description': 'ಕ್ಯಾಮೆರಾವನ್ನು ಎಲೆಗೆ ಹತ್ತಿರ ಸರಿಸಿ।', 'priority': 'medium'}
        ]
    }
    
    return recs.get(language, recs['en'])
