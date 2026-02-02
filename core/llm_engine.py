import os
import logging
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self):
        """Initialize the Groq client."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not found in environment variables. AI features will be disabled.")
            self.client = None
        else:
            try:
                self.client = Groq(api_key=api_key)
                logger.info("Groq Client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.client = None

    def generate_response(self, user_text, medical_context=None, past_history=None):
        """
        Generates a response using Groq API.
        """
        if not self.client:
            return None # Return None to trigger fallback defaults if AI fails

        try:
            # Construct the system prompt
            system_prompt = (
                "You are MindMate, an empathetic and intelligent mental health companion. "
                "Your goal is to provide supportive, safe, and helpful responses to users. "
                "You are NOT a doctor and cannot diagnose, but you can offer guidance and coping strategies. "
                "Keep responses concise, warm, and conversational. \n"
            )

            if medical_context:
                system_prompt += f"\nRelevant Medical Context from User Reports:\n{medical_context}\n"

            messages = [
                {"role": "system", "content": system_prompt}
            ]

            # Add history if available (simplified for now)
            if past_history:
                for msg in past_history[-5:]: # Keep context window small for speed
                    messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

            # Add current user message
            messages.append({"role": "user", "content": user_text})

            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.1-8b-instant", # Updated to supported model
                temperature=0.7,
                max_tokens=300,
            )

            response_text = chat_completion.choices[0].message.content
            return response_text

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            return None # Return None to trigger fallback defaults
