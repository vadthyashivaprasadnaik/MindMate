def calculate_stress(session_data, sentiment_score):
    """
    Calculates a stress score (0-100) based on user inputs and current sentiment.
    """
    base_stress = 20 # Baseline
    
    # Adjust based on role (simple heuristic)
    role = session_data.get('role', '').lower()
    if 'student' in role:
        base_stress += 10
    elif 'working' in role:
        base_stress += 15
        
    # Adjust based on mindset
    mindset = session_data.get('mindset', '').lower()
    if 'anxious' in mindset or 'worried' in mindset:
        base_stress += 20
    elif 'sad' in mindset or 'depressed' in mindset:
        base_stress += 15
    elif 'calm' in mindset:
        base_stress -= 10
        
    # Adjust based on current sentiment (immediate reaction)
    # sentiment is -1 to 1.
    # If negative (-0.5), we add stress. If positive (0.5), we reduce stress.
    sentiment_impact = sentiment_score * -20 # -0.8 becomes +16 stress
    
    current_score = base_stress + sentiment_impact
    
    # Clamp
    return max(0, min(100, current_score))
