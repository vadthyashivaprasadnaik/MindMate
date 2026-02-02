from flask import Flask, render_template, request, jsonify, session
from db.database import init_db, db_session
from core.memory import get_or_create_session, log_message, update_session_state
from core.dialog_manager import DialogManager
from core.ethics_engine import check_safety_risk
from core.emotion_engine import get_emotional_response
from core.todo_engine import generate_todos, save_todos
from core.report_generator import generate_session_report
from nlp.sentiment import analyze_sentiment
from nlp.stress import calculate_stress
from flask import Flask, render_template, request, jsonify, session, send_file
import uuid

app = Flask(__name__)
app.secret_key = 'mindmate_secret_key' # Change for production

# Import Medical Parser
import io
from nlp.medical_parser import extract_text_from_pdf, analyze_report_text


# Initialize DB
init_db()

# Initialize LLM Client (Groq)
from core.llm_engine import LLMClient
llm_client = LLMClient()

@app.route('/')
def home():
    # Generate a session ID for the frontend if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html', session_id=session['session_id'])

@app.route('/upload_report', methods=['POST'])
def upload_report():
    try:
        session_id = request.form.get('session_id')
        file = request.files.get('file')
        
        if not file or not session_id:
            return jsonify({"status": "error", "message": "No file or session ID"}), 400
            
        # Parse Text
        text = ""
        filename = file.filename.lower()
        
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file.stream)
        elif filename.endswith('.txt'):
            file_content = file.read().decode('utf-8')
            text = file_content
        else:
            return jsonify({"status": "error", "message": "Unsupported file type. Use PDF or TXT."}), 400
            
        # Analyze
        analysis = analyze_report_text(text)
        
        # Save to Session (In-Memory or DB)
        user_session = get_or_create_session(session_id)
        
        # Store analysis in session object (requires updating Memory class or just dynamic attr)
        # Using dynamic attribute for hackathon speed
        user_session.medical_context = analysis
        
        # Also log this event
        log_message(session_id, 'system', f"Uploaded Health Report: {len(analysis['findings'])} findings.", 0.0)
        
        return jsonify({
            "status": "success", 
            "findings": analysis['findings'],
            "advice": analysis['advice_context']
        })
        
    except Exception as e:
        print(f"Upload Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_text = data.get('message')
    session_id = data.get('session_id')
    
    if not user_text or not session_id:
        return jsonify({"error": "Invalid data"}), 400
        
    # Get Session Object
    user_session = get_or_create_session(session_id)
    
    # Check for Medical Context
    medical_context_str = ""
    if hasattr(user_session, 'medical_context'):
        findings = user_session.medical_context.get('findings', [])
        if findings:
            medical_context_str = f" [MEDICAL CONTEXT: The user has {', '.join(findings)}. Tailor advice accordingly.]"

    
    # 1. Safety Check
    is_risky, safety_response = check_safety_risk(user_text)
    if is_risky:
        log_message(session_id, 'user', user_text, -1.0)
        log_message(session_id, 'bot', safety_response, 0.0)
        return jsonify({
            "response": safety_response,
            "stress_score": 100,
            "emotion": "concerned"
        })
        
    # Initialize Intent Classifier
    from core.intent_classifier import IntentClassifier
    # REMOVED LLM CLIENT AS REQUESTED
    
    classifier = IntentClassifier()
    
    try:
        # 1. UNIVERSE KNOWLEDGE BASE CHECK (Exact Matches - High Priority)
        from core.knowledge_base import find_best_match
        kb_response = find_best_match(user_text)
        
        sentiment = analyze_sentiment(user_text) if 'analyze_sentiment' in globals() else 0.0
        text_lower = user_text.lower()
        import random 
        
        base_reply = ""
        intent = classifier.detect_intent(user_text)
        
        # LOGIC FLOW:
        # 1. If KB Match -> Use it (Definition/Explanation)
        # 2. Else -> Rule-Based Intent Responses
        
        if kb_response:
             base_reply = kb_response
        elif intent:
            # Handle Detected Intents
            if intent == 'greeting':
                base_reply = random.choice([
                    "Hello there. I am MindMate. How are you feeling right now?",
                    "Hi. I'm here to listen. What's on your mind today?",
                    "Greetings. I am your storm shelter. Do you want to chat or use a tool?"
                ])
            elif intent == 'help':
                base_reply = random.choice([
                    "I am MindMate, your intelligent mental health partner. I can help with anxiety, focus, or just listening.",
                    "Think of me as a grounding rod. I have tools for breathing and focus, or I can just chat."
                ])
            elif intent == 'sadness':
                base_reply = random.choice([
                    "I'm sorry you're feeling this weight. It takes strength to speak it. Do you want to vent?",
                    "It sounds like a heavy day. I'm listening. Emotional storms always pass.",
                    "I hear you. It's okay not to be okay. Would you like to try a breathing exercise?"
                ])
            elif intent == 'anxiety':
                base_reply = random.choice([
                    "I hear the tension in your words. You are safe here. Let's take it one breath at a time.",
                    "Anxiety is just a physical wave. It will peak and then recede. Can we try a grounding technique?",
                    "That sounds stressful. Just breathe with me."
                ])
            elif intent == 'loneliness':
                base_reply = random.choice([
                    "Solitude can be difficult, but you are connected to me right now.",
                    "I'm here. I may be an AI, but my care is real. Tell me more about what you're thinking.",
                    "Loneliness is a universal human storm. It means you have love to give."
                ])     
            elif intent == 'tiredness':
                 base_reply = random.choice([
                    "Rest is productive. If your body is asking for a pause, it's okay to listen.",
                    "It sounds like you need a recharge. Have you been sleeping well?",
                    "Exhaustion makes everything feel harder. Be gentle with yourself today."
                ])
            elif intent == 'anger':
                base_reply = random.choice([
                    "It's valid to be angry. It's an energy that needs to be released. You can vent here safely.",
                    "I hear your frustration. Let it out. I won't judge you.",
                    "Anger often protects us. What is making you feel this way right now?"
                ])
            elif intent == 'tool_timer':
                 base_reply = random.choice([
                    "Focus is a superpower. Check the dashboard card to start a 25-minute storm session.",
                    "Let's get things done. Use the 'Focus & Clarity' tool on the right."
                ])
            elif intent == 'tool_breathe':
                 base_reply = random.choice([
                    "Good idea. Click the 'Emotional Health' card to open the guided breathing tool.",
                    "Taking a breath is the best reset. Use the breathing tool on the dashboard."
                ])
            elif intent == 'gratitude':
                base_reply = "You are welcome. I'm glad I could be here for you."
            elif intent == 'closing':
                base_reply = "Take care. Remember, after every storm comes a calm. Goodbye for now."
            
        else:
            # HYBRID FALLBACK: Try AI (Groq) First
            ai_response = None
            
            # Construct simplified history for AI context
            past_history = []
            # (Optional: fetch recent history from DB if needed, but for speed keeping it light or using session context if implemented)
            
            # Call AI
            try:
                # Pass medical context if available
                med_ctx_str = None
                if hasattr(user_session, 'medical_context') and user_session.medical_context:
                    med_ctx_str = str(user_session.medical_context.get('findings', []))
                    
                ai_response = llm_client.generate_response(user_text, medical_context=med_ctx_str)
            except Exception as e:
                print(f"AI Call failed: {e}")
                ai_response = None
            
            if ai_response:
                base_reply = ai_response
                source = "Groq AI"
            else:
                # ORIGINAL FALLBACK (If AI fails or is disabled)
                if sentiment < -0.3:
                    base_reply = random.choice([
                        "It sounds like you're going through a tough moment. I'm listening. Tell me more.",
                        "I can sense some negativity in that. I'm here to support you. What happened?"
                    ])
                elif sentiment > 0.3:
                     base_reply = random.choice([
                        "That sounds really positive! I love that energy. Tell me more.",
                        "It's great to hear something good. Updates like that make my circuits happy."
                    ])
                else:
                    # Mirroring
                    if len(user_text.split()) > 3:
                        base_reply = random.choice([
                            "I understand. Please, tell me more about that.",
                            "That's interesting. How does that make you feel?",
                            "I'm listening. Go on."
                        ])
                    else:
                        base_reply = f"I hear you saying '{user_text}'. Can you elaborate?"

        # 3. MEDICAL CONTEXT INJECTION (Smart Overlay)
        if hasattr(user_session, 'medical_context'):
            findings_str = str(user_session.medical_context.get('findings', []))
            
            check_tired = (intent == 'tiredness' or "tired" in text_lower or "fatigue" in text_lower)
            check_mood = (intent in ['sadness', 'anxiety'] or "sad" in text_lower or "depress" in text_lower)
            
            if "Iron" in findings_str and check_tired:
                base_reply += "\n\n(Medical Insight: Your report indicated Low Iron. This is a common cause of the fatigue you're feeling. Are you taking your supplements?)"
            elif "Vitamin D" in findings_str and (check_mood or check_tired):
                base_reply += "\n\n(Medical Insight: Low Vitamin D from your report can actually worsen your mood and energy. Have you seen sunlight today?)"
            elif "Blood Pressure" in findings_str and (intent == 'stress' or "stress" in text_lower):
                base_reply += "\n\n(Medical Insight: Since you have high blood pressure recorded, managing this stress is physically important for you. Let's try breathing.)"
            elif "TSH" in findings_str and (check_mood or check_tired):
                base_reply += "\n\n(Medical Insight: Your Thyroid levels might be amplifying these emotions. Be patient with your body.)"

        # 4. ADVANCED MUSIC RECOMMENDATION
        music_recommendation = None
        play_music = False
        
        # Analyze emotion for music mapping
        music_mood = None
        if intent == 'anxiety' or "anxi" in text_lower or "panic" in text_lower:
            music_mood = "calm_binaural"
        elif intent == 'sadness' or "sad" in text_lower or "cry" in text_lower:
            music_mood = "gentle_piano" # Uplifting but gentle
        elif intent == 'stress' or "stress" in text_lower or "tired" in text_lower:
            music_mood = "rain_sounds"
        elif intent == 'anger':
            music_mood = "lofi_beats" # Distraction
        elif intent == 'tool_focus' or "focus" in text_lower:
            music_mood = "focus_noise"
            
        if music_mood:
             play_music = True
             music_recommendation = {
                 "type": music_mood,
                 "autoplay": True if sentiment < -0.6 else False # Only autoplay if very distressed
             }
        elif sentiment < -0.4:
             play_music = True
             music_recommendation = {"type": "healing_freq", "autoplay": False}

        response_text = base_reply
        
        # Log Bot Response
        log_message(session_id, 'bot', response_text, 0.0)
        
        return jsonify({
            "response": response_text,
            "stress_score": user_session.stress_score,
            "sentiment": sentiment,
            "offer_music": play_music,
            "music_data": music_recommendation,
            "source": "Rules"
        })

    except Exception as e:
        print(f"ERROR in chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "response": "I am having a momentary connection issue. Please try saying 'hi' again.",
            "stress_score": 50,
            "sentiment": 0,
            "offer_music": False
        })

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    data = request.json
    session_id = data.get('session_id')
    
    # Use DB logic
    from core.memory import get_or_create_session
    from db.models import Message
    
    user_session = get_or_create_session(session_id)
    if user_session:
        # Clear history in DB
        Message.query.filter_by(session_id=session_id).delete()
        user_session.stress_score = 20
        db_session.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

@app.route('/download_report', methods=['GET'])
def download_report():
    session_id = request.args.get('session_id')
    # Mock session data retrieval if not in memory (for hackathon simplify)
    # In real app, we fetch from DB. Here we check memory cache 'sessions'
    # Wait, 'sessions' dict is not imported/defined in global scope in view_file output?
    # Ah, need to check where 'sessions' variable is.
    # It seems I missed checking where 'sessions' is stored. core.memory has get_or_create_session.
    # Let's inspect core/memory.py or just use the DB session if possible.
    # For now, let's assume get_or_create_session returns an object we can use.
    # Actually, the memory module handles it.
    
    # Quick hack: We need to access the session object. 
    # If app.py doesn't have a global sessions dict, we might need to rely on DB or 'memory' module.
    
    # Re-reading app.py view... 'user_session = get_or_create_session(session_id)'
    # trace get_or_create_session in core/memory.py...
    # It returns a Session model object.
    
    # So we should use get_or_create_session here.
    from core.memory import get_or_create_session
    user_session = get_or_create_session(session_id)
    
    # We need to construct a dict for the report generator
    session_data = {
        'history': [], # Need to fetch messages
        'stress_score': user_session.stress_score if hasattr(user_session, 'stress_score') else 50
    }
    # Retrieve messages from DB
    from db.models import Message
    msgs = Message.query.filter_by(session_id=user_session.id).all()
    session_data['history'] = [{'sender': m.sender, 'text': m.text} for m in msgs]
    
    filepath = generate_session_report(session_id, session_data)
    return send_file(filepath, as_attachment=True, download_name="MindMate_Report.txt")

@app.route('/get_flashcards', methods=['GET'])
def get_flashcards():
    cards = [
        {"type": "tip", "front": "Breathe", "back": "Inhale for 4 seconds, hold for 7, exhale for 8."},
        {"type": "affirmation", "front": "You are enough", "back": "Your productivity does not define your worth."},
        {"type": "fact", "front": "Did you know?", "back": "Walking outside for 10 minutes can reduce cortisol levels by 20%."},
        {"type": "challenge", "front": "Tiny Challenge", "back": "Drink a glass of water right now."},
        {"type": "tip", "front": "Grounding", "back": "Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste."}
    ]
    return jsonify(cards)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)
