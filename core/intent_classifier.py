
import re

class IntentClassifier:
    def __init__(self):
        # Define patterns with regex for word boundaries (\b) to avoid partial matches
        self.intents = {
            'greeting': [r'\bhi\b', r'\bhello\b', r'\bhey\b', r'\bstart\b', r'\bgreetings\b', r'\bmorning\b', r'\bevening\b'],
            'help': [r'\bhelp\b', r'\bwhat can you do\b', r'\bwho are you\b', r'\bfeatures\b', r'\bguide\b'],
            
            # EMOTIONS
            'sadness': [r'\bsad\b', r'\bunhappy\b', r'\bdepressed\b', r'\bdown\b', r'\bcry\b', r'\bcrying\b', r'\bhopeless\b', r'\bgrief\b'],
            'anxiety': [r'\banxi', r'\bpanic\b', r'\bworr', r'\bscared\b', r'\bfear\b', r'\bnervous\b', r'\bstress'],
            'loneliness': [r'\blonely\b', r'\balone\b', r'\bisolat', r'\bnobody\b'],
            'tiredness': [r'\btired\b', r'\bexhausted\b', r'\bsleep\b', r'\binsomnia\b', r'\bdrained\b', r'\bfatigue\b'],
            'anger': [r'\bangry\b', r'\bmad\b', r'\bhate\b', r'\bfurious\b', r'\bupset\b', r'\birritat'],
            
            # MEDICAL / PHYSICAL
            'medical_symptom': [r'\bpain\b', r'\bache\b', r'\bhurt\b', r'\bsick\b', r'\bvomit\b', r'\bdizzy\b', r'\bheadache\b', r'\bstomach'],
            
            # TOOLS
            'tool_timer': [r'\btimer\b', r'\bfocus\b', r'\bwork\b', r'\bstudy\b', r'\bconcentrate\b', r'\bproduction\b'],
            'tool_breathe': [r'\bbreathe\b', r'\bbreath\b', r'\bmeditate\b', r'\bcalm\b', r'\brelax\b', r'\binhale\b'],
            
            # CLOSING
            'closing': [r'\bbye\b', r'\bgoodbye\b', r'\bexit\b', r'\bleave\b', r'\bstop\b', r'\bsee you\b'],
            'gratitude': [r'\bthank', r'\bcool\b', r'\bnice\b', r'\bgreat\b']
        }

    def detect_intent(self, user_text):
        """
        Returns the primary detected intent key, or None.
        Handles basic negation (e.g. 'not sad').
        """
        text_lower = user_text.lower()
        
        # Check for negation first
        # Simple heuristic: if "not" or "don't" is within 2 words of a keyword match, ignore or flip it.
        # For simplicity in this regex implementation, we'll return a special 'negated' intent if strongly detected, or just filtering.
        
        detected_intents = []

        for intent, patterns in self.intents.items():
            for pattern in patterns:
                # Search for pattern
                match = re.search(pattern, text_lower)
                if match:
                    # Check for negation window (word before)
                    # This is a basic implementation. 
                    # We look at the 15 characters preceding the match.
                    start_index = match.start()
                    preceding_text = text_lower[max(0, start_index - 15):start_index]
                    
                    if re.search(r'\b(not|no|never|don\'t|dont)\b', preceding_text):
                         # It is negated, e.g. "I am NOT sad"
                         pass 
                    else:
                        detected_intents.append(intent)
                        break # Found this intent, move to next intent category

        if not detected_intents:
            return None
            
        # Prioritize specific over general
        if 'medical_symptom' in detected_intents and 'tiredness' in detected_intents:
            return 'tiredness' # More specific emotion/state
            
        # Return the first one for now, or use a priority list
        # Priority: Closing > Help > Tool > Medical > Emotion > Greeting
        priority = ['closing', 'tool_timer', 'tool_breathe', 'help', 'medical_symptom', 'anxiety', 'sadness', 'anger', 'loneliness', 'tiredness', 'gratitude', 'greeting']
        
        for p in priority:
            if p in detected_intents:
                return p
                
        return detected_intents[0]
