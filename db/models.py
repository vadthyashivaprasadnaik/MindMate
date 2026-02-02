from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, PickleType
from db.database import Base
from datetime import datetime
import uuid

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # User state
    age = Column(String(10))
    role = Column(String(50))
    mindset = Column(String(100))
    stress_score = Column(Float, default=0.0)
    intake_complete = Column(Integer, default=0) # 0: No, 1: Yes
    
    # Context (serialized dict)
    context_data = Column(PickleType, default={})

    def __repr__(self):
        return f'<Session {self.session_id}>'

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), ForeignKey('sessions.session_id'), nullable=False)
    sender = Column(String(10), nullable=False) # 'user' or 'bot'
    text = Column(Text, nullable=False)
    sentiment_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), ForeignKey('sessions.session_id'), nullable=False)
    description = Column(String(200), nullable=False)
    status = Column(String(20), default='pending') # pending, completed
    created_at = Column(DateTime, default=datetime.utcnow)
