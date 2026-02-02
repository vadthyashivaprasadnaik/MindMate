from db.database import db_session
from db.models import Task

def generate_todos(session, stress_score):
    """
    Generates suggested tasks based on stress level and role.
    """
    todos = []
    
    # Generic low stress
    if stress_score < 30:
        todos.append("Drink a glass of water")
        todos.append("Take a 5 minute walk")
    
    # High stress
    elif stress_score > 70:
        todos.append("Practice 4-7-8 breathing")
        todos.append("Step away from the screen for 10 minutes")
        todos.append("Write down 3 things you are grateful for")
        
    return todos

def save_todos(session_id, todo_list):
    for item in todo_list:
        task = Task(session_id=session_id, description=item)
        db_session.add(task)
    db_session.commit()
