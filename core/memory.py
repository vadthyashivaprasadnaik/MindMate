from db.database import db_session
from db.models import Session, Message
import uuid

def get_or_create_session(session_id=None):
    if not session_id:
        session_id = str(uuid.uuid4())
    
    session = Session.query.filter_by(session_id=session_id).first()
    if not session:
        session = Session(session_id=session_id)
        db_session.add(session)
        db_session.commit()
    
    return session

def log_message(session_id, sender, text, sentiment_score=None):
    message = Message(
        session_id=session_id,
        sender=sender,
        text=text,
        sentiment_score=sentiment_score
    )
    db_session.add(message)
    db_session.commit()

def update_session_state(session_id, **kwargs):
    session = Session.query.filter_by(session_id=session_id).first()
    if session:
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        db_session.commit()
