import re

SUICIDE_KEYWORDS = [
    r'\b(kill myself|suicide|end my life|want to die|no reason to live)\b',
    r'\b(cutting myself|hurt myself)\b'
]

HELPLINE_MESSAGE = (
    "I hear that you're in a lot of pain right now. "
    "Please know that you are not alone, and there is support available. "
    "In India, you can call the iCall Helpline at 9152987821 or AASRA at 91-9820466726. "
    "Would you like me to help you find more local resources?"
)

def check_safety_risk(text):
    """
    Checks for high-risk content.
    Returns (is_risky, response_text)
    """
    text_lower = text.lower()
    for pattern in SUICIDE_KEYWORDS:
        if re.search(pattern, text_lower):
            return True, HELPLINE_MESSAGE
            
    return False, None

def ethical_check(text):
    """
    General ethical check to ensure bot doesn't encourage harm or toxic behavior.
    """
    # Simple placeholder: In a real app, this would detect bullying, etc.
    return True
