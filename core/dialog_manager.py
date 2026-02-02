from core.memory import update_session_state

INTAKE_QUESTIONS = [
    {"key": "age", "text": "To help me understand you better, could you tell me your age? (You can skip if you prefer)", "type": "int"},
    {"key": "gender", "text": "What is your gender? (optional)", "type": "str"},
    {"key": "role", "text": "Are you currently a Student, Working Professional, or something else?", "type": "str"},
    {"key": "mindset", "text": "How would you describe your current mindset? (e.g., Anxious, Sad, Overwhelmed, Calm)", "type": "str"},
    {"key": "stress_area", "text": "What is causing you the most stress right now? (e.g., Exams, Job, Relationships)", "type": "str"}
]

class DialogManager:
    def __init__(self, session):
        self.session = session
        context = session.context_data or {}
        self.step = context.get('intake_step', 0)
    
    def get_next_response(self, user_input):
        # If intake is already complete, just chat
        if self.session.intake_complete:
            return None # Hand off to general chat logic
            
        # If just starting
        if self.step == 0 and not user_input:
            return INTAKE_QUESTIONS[0]['text']
            
        # Process answer to previous question
        current_q = INTAKE_QUESTIONS[self.step]
        
        # Store answer
        # In a real app, we'd validate here.
        update_session_state(self.session.session_id, **{current_q['key']: user_input})
        
        # Move to next
        self.step += 1
        
        # Save step
        # We need a way to update the pickle dict. For now, we just update the specific column if it matches
        # or we re-save the context.
        context = self.session.context_data or {}
        context['intake_step'] = self.step
        update_session_state(self.session.session_id, context_data=context)
        
        if self.step < len(INTAKE_QUESTIONS):
            return INTAKE_QUESTIONS[self.step]['text']
        else:
            update_session_state(self.session.session_id, intake_complete=1)
            return "Thank you for sharing. I have a better understanding now. How are you feeling right at this moment?"
