import random

def get_emotional_response(intent, context, sentiment_score, stress_score):
    """
    Modifies the response based on the users emotional state.
    """
    # If high stress, be more grounding
    if stress_score > 70:
        return _get_grounding_response(intent)
    
    # If negative sentiment, be empathetic
    if sentiment_score < -0.3:
        return _get_empathetic_response(intent)
        
    return _get_neutral_response(intent)

def _get_grounding_response(intent):
    responses = [
        "Take a deep breath. I'm here with you. ",
        "It feels overwhelming right now, but let's take it one step at a time. ",
        "I hear you. Let's slow down for a moment. "
    ]
    return random.choice(responses)

def _get_empathetic_response(intent):
    responses = [
        "I'm sorry you're feeling this way. ",
        "That sounds really tough. ",
        "It's okay to feel this way. "
    ]
    return random.choice(responses)

def _get_neutral_response(intent):
    return "" # Append nothing, just standard response
