from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os

# Create database directory if it doesn't exist (handled by os.makedirs in write_to_file usually, but good practice here)
DB_PATH = os.path.join(os.getcwd(), 'mindmate.db')
engine = create_engine(f'sqlite:///{DB_PATH}')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import db.models
    Base.metadata.create_all(bind=engine)
