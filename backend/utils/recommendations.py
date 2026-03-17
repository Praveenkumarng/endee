"""
Treatment Recommendations Module
Provides disease-specific treatment recommendations
"""

from typing import List, Dict

# Comprehensive recommendation database
RECOMMENDATIONS_DB = {
    'Bacterial Blight': {
        'chemical': [
            {
                'id': 'chem_copper_bactericide',
                'type': 'chemical',
                'title': 'Copper-based Bactericide',
                'description': 'Apply copper hydroxide or copper oxychloride at 2-3 g/L. Spray at 10-15 day intervals.',
                'priority': 'high',
                'dosage': '2-3 g/L',
                'frequency': 'Every 10-15 days',
                'precautions': 'Avoid spraying during flowering. Use protective equipment.'
            },
            {
                'id': 'chem_streptocycline',
                'type': 'chemical',
                'title': 'Streptocycline',
                'description': 'Mix 1g Streptocycline + 25g Copper oxychloride per 10L water. Effective against bacterial infections.',
                'priority': 'high',
                'dosage': '1g + 25g per 10L water',
                'frequency': 'Weekly application',
                'precautions': 'Do not exceed recommended dosage. Maintain spray interval.'
            }
        ],
        'organic': [
            {
                'id': 'org_neem_oil',
                'type': 'organic',
                'title': 'Neem Oil Spray',
                'description': 'Mix 5ml neem oil per liter of water. Add 1ml liquid soap as emulsifier. Spray on affected areas.',
                'priority': 'medium',
                'dosage': '5ml/L water',
                'frequency': 'Twice weekly',
                'precautions': 'Apply in early morning or evening. Avoid direct sunlight.'
            },
            {
                'id': 'org_pseudomonas',
                'type': 'organic',
                'title': 'Pseudomonas fluorescens',
                'description': 'Biocontrol agent. Apply 10g/L as foliar spray. Helps suppress bacterial growth.',
                'priority': 'medium',
                'dosage': '10g/L',
                'frequency': 'Every 15 days',
                'precautions': 'Store in cool place. Use within shelf life.'
            }
        ],
        'prevention': [
            {
                'id': 'prev_disease_free_seeds',
                'type': 'prevention',
                'title': 'Use Disease-Free Seeds',
                'description': 'Always use certified, disease-free seeds from reliable sources.',
                'priority': 'high'
            },
            {
                'id': 'prev_crop_rotation',
                'type': 'prevention',
                'title': 'Crop Rotation',
                'description': 'Practice 2-3 year crop rotation with non-host crops like cereals.',
                'priority': 'high'
            },
            {
                'id': 'prev_field_sanitation',
                'type': 'prevention',
                'title': 'Field Sanitation',
                'description': 'Remove and burn infected plant debris. Maintain clean field conditions.',
                'priority': 'medium'
            },
            {
                'id': 'prev_balanced_fertilization',
                'type': 'prevention',
                'title': 'Balanced Fertilization',
                'description': 'Avoid excessive nitrogen. Maintain balanced NPK ratio.',
                'priority': 'medium'
            }
        ]
    },
    
    'Fusarium Wilt': {
        'chemical': [
            {
                'id': 'chem_carbendazim',
                'type': 'chemical',
                'title': 'Carbendazim',
                'description': 'Soil drench with Carbendazim 50% WP at 2g/L. Apply at root zone.',
                'priority': 'high',
                'dosage': '2g/L',
                'frequency': 'At first symptom, repeat after 15 days',
                'precautions': 'Avoid contact with skin. Use protective gear.'
            },
            {
                'id': 'chem_thiophanate',
                'type': 'chemical',
                'title': 'Thiophanate Methyl',
                'description': 'Apply as soil drench at 1.5g/L. Effective systemic fungicide.',
                'priority': 'high',
                'dosage': '1.5g/L',
                'frequency': 'Every 20 days',
                'precautions': 'Follow recommended dosage strictly.'
            }
        ],
        'organic': [
            {
                'id': 'org_trichoderma',
                'type': 'organic',
                'title': 'Trichoderma viride',
                'description': 'Biocontrol fungus. Apply 5g/kg seed treatment or 5kg/ha soil application.',
                'priority': 'high',
                'dosage': '5g/kg seed or 5kg/ha soil',
                'frequency': 'At sowing and 30 days after',
                'precautions': 'Store in cool, dry place. Check viability before use.'
            },
            {
                'id': 'org_neem_cake',
                'type': 'organic',
                'title': 'Neem Cake',
                'description': 'Apply neem cake at 250kg/ha. Helps suppress soil-borne pathogens.',
                'priority': 'medium',
                'dosage': '250kg/ha',
                'frequency': 'Once at sowing',
                'precautions': 'Mix well with soil.'
            }
        ],
        'prevention': [
            {
                'id': 'prev_resistant_varieties',
                'type': 'prevention',
                'title': 'Resistant Varieties',
                'description': 'Plant wilt-resistant cotton varieties like Bt cotton hybrids.',
                'priority': 'high'
            },
            {
                'id': 'prev_soil_solarization',
                'type': 'prevention',
                'title': 'Soil Solarization',
                'description': 'Cover soil with transparent plastic for 4-6 weeks in summer to kill pathogens.',
                'priority': 'high'
            },
            {
                'id': 'prev_proper_drainage',
                'type': 'prevention',
                'title': 'Proper Drainage',
                'description': 'Ensure good drainage. Avoid waterlogging which favors Fusarium.',
                'priority': 'medium'
            },
            {
                'id': 'prev_ph_management',
                'type': 'prevention',
                'title': 'pH Management',
                'description': 'Maintain soil pH 6.5-7.5. Fusarium thrives in acidic soils.',
                'priority': 'medium'
            }
        ]
    },
    
    'Leaf Curl Virus': {
        'chemical': [
            {
                'id': 'chem_imidacloprid',
                'type': 'chemical',
                'title': 'Imidacloprid',
                'description': 'Control whitefly vector with Imidacloprid 17.8% SL at 0.5ml/L.',
                'priority': 'high',
                'dosage': '0.5ml/L',
                'frequency': 'Every 10-12 days',
                'precautions': 'Target whitefly population. Rotate with other insecticides.'
            },
            {
                'id': 'chem_thiamethoxam',
                'type': 'chemical',
                'title': 'Thiamethoxam',
                'description': 'Systemic insecticide for whitefly control. Apply at 0.2g/L.',
                'priority': 'high',
                'dosage': '0.2g/L',
                'frequency': 'Every 15 days',
                'precautions': 'Avoid spraying during bee activity hours.'
            }
        ],
        'organic': [
            {
                'id': 'org_neem_garlic',
                'type': 'organic',
                'title': 'Neem Oil + Garlic Extract',
                'description': 'Mix 5ml neem oil + 10ml garlic extract per liter. Repels whiteflies.',
                'priority': 'medium',
                'dosage': '5ml + 10ml per liter',
                'frequency': 'Twice weekly',
                'precautions': 'Prepare fresh solution. Apply in evening.'
            },
            {
                'id': 'org_yellow_traps',
                'type': 'organic',
                'title': 'Yellow Sticky Traps',
                'description': 'Install yellow sticky traps at 15-20 traps/acre to monitor and trap whiteflies.',
                'priority': 'high',
                'dosage': '15-20 traps/acre',
                'frequency': 'Replace weekly',
                'precautions': 'Place at canopy height.'
            }
        ],
        'prevention': [
            {
                'id': 'prev_virus_free_seedlings',
                'type': 'prevention',
                'title': 'Virus-Free Seedlings',
                'description': 'Use certified virus-free planting material from authorized nurseries.',
                'priority': 'high'
            },
            {
                'id': 'prev_remove_infected',
                'type': 'prevention',
                'title': 'Remove Infected Plants',
                'description': 'Rogue out and destroy infected plants immediately to prevent spread.',
                'priority': 'high'
            },
            {
                'id': 'prev_barrier_crops',
                'type': 'prevention',
                'title': 'Barrier Crops',
                'description': 'Plant maize or sorghum as barrier crops around cotton fields.',
                'priority': 'medium'
            },
            {
                'id': 'prev_weed_management',
                'type': 'prevention',
                'title': 'Weed Management',
                'description': 'Control weeds that serve as alternate hosts for whiteflies.',
                'priority': 'medium'
            }
        ]
    },
    
    'Healthy Leaf': {
        'chemical': [],
        'organic': [],
        'prevention': [
            {
                'id': 'prev_good_practices',
                'type': 'prevention',
                'title': 'Continue Good Practices',
                'description': 'Maintain current agricultural practices. Regular monitoring is key.',
                'priority': 'low'
            },
            {
                'id': 'prev_preventive_sprays',
                'type': 'prevention',
                'title': 'Preventive Sprays',
                'description': 'Apply preventive fungicides during disease-prone seasons.',
                'priority': 'low'
            },
            {
                'id': 'prev_nutrient_management',
                'type': 'prevention',
                'title': 'Nutrient Management',
                'description': 'Ensure balanced nutrition to maintain plant health and disease resistance.',
                'priority': 'medium'
            }
        ]
    }
}

def get_recommendations(detections: List[Dict], severity_info: Dict) -> List[Dict]:
    """
    Get treatment recommendations based on detections and severity
    
    Args:
        detections: List of detection dictionaries
        severity_info: Severity analysis information
    
    Returns:
        recommendations: List of recommendation dictionaries
    """
    
    recommendations = []
    
    # If healthy, return maintenance recommendations
    if severity_info['category'] == 'Healthy':
        return RECOMMENDATIONS_DB['Healthy Leaf']['prevention']
    
    # Get unique diseases detected
    diseases = set()
    for detection in detections:
        if detection['class_name'] != 'Healthy Leaf':
            diseases.add(detection['class_name'])
    
    # Collect recommendations for each disease
    for disease in diseases:
        if disease in RECOMMENDATIONS_DB:
            disease_recs = RECOMMENDATIONS_DB[disease]
            
            # Add chemical recommendations (high priority for severe cases)
            if severity_info['severity_score'] >= 2:
                recommendations.extend(disease_recs['chemical'][:2])  # Top 2 chemical
            
            # Add organic recommendations
            recommendations.extend(disease_recs['organic'][:2])  # Top 2 organic
            
            # Add prevention recommendations
            recommendations.extend(disease_recs['prevention'][:3])  # Top 3 prevention
    
    # Remove duplicates while preserving order
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        rec_key = rec['title']
        if rec_key not in seen:
            seen.add(rec_key)
            unique_recommendations.append(rec)
    
    return unique_recommendations

def get_disease_info(disease_name: str) -> Dict:
    """
    Get detailed information about a specific disease
    
    Args:
        disease_name: Name of the disease
    
    Returns:
        info: Disease information dictionary
    """
    
    disease_info = {
        'Bacterial Blight': {
            'scientific_name': 'Xanthomonas citri pv. malvacearum',
            'symptoms': [
                'Water-soaked lesions on leaves',
                'Angular leaf spots with yellow halos',
                'Vein necrosis',
                'Boll rot in severe cases'
            ],
            'favorable_conditions': [
                'High humidity (>80%)',
                'Temperature 25-30°C',
                'Overhead irrigation',
                'Wounds or injuries on plants'
            ],
            'economic_impact': 'Can cause 20-30% yield loss in severe outbreaks'
        },
        'Fusarium Wilt': {
            'scientific_name': 'Fusarium oxysporum f.sp. vasinfectum',
            'symptoms': [
                'Yellowing of lower leaves',
                'Wilting of entire plant',
                'Vascular browning in stem',
                'Stunted growth'
            ],
            'favorable_conditions': [
                'Soil temperature 25-32°C',
                'Acidic soil pH',
                'Poor drainage',
                'Root-knot nematode presence'
            ],
            'economic_impact': 'Can cause complete crop failure in susceptible varieties'
        },
        'Leaf Curl Virus': {
            'scientific_name': 'Cotton Leaf Curl Virus (CLCuV)',
            'symptoms': [
                'Upward curling of leaves',
                'Leaf thickening and vein swelling',
                'Stunted plant growth',
                'Reduced boll formation'
            ],
            'favorable_conditions': [
                'High whitefly population',
                'Temperature 25-35°C',
                'Dry weather',
                'Presence of alternate hosts'
            ],
            'economic_impact': 'Can cause 30-70% yield loss depending on infection stage'
        }
    }
    
    return disease_info.get(disease_name, {})
