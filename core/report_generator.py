import os
from datetime import datetime

def generate_session_report(session_id, session_data):
    """
    Generates a text-based report for the user session.
    Returns the file path.
    """
    report_dir = "reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
        
    filename = f"MindMate_Report_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(report_dir, filename)
    
    # Calculate average stress
    history = session_data.get('history', [])
    stress_score = session_data.get('stress_score', 0)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("==================================================\n")
        f.write("              MINDMATE SESSION REPORT             \n")
        f.write("==================================================\n\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Session ID: {session_id}\n")
        f.write(f"Final Stress Level: {stress_score}/100\n\n")
        
        f.write("--------------------------------------------------\n")
        f.write("              EMOTIONAL SUMMARY                   \n")
        f.write("--------------------------------------------------\n")
        if stress_score < 30:
            f.write("You are currently in a balanced and calm state.\n")
            f.write("Recommendation: Maintenance. Keep up your positive routines.\n")
        elif stress_score < 70:
            f.write("You are experiencing moderate stress.\n")
            f.write("Recommendation: Mindfulness. Try the 4-7-8 Breathing exercise.\n")
        else:
            f.write("You are under high stress.\n")
            f.write("Recommendation: Immediate Grounding. Use the 5-4-3-2-1 technique.\n")
        f.write("\n")
        
        f.write("--------------------------------------------------\n")
        f.write("              SESSION LOG                         \n")
        f.write("--------------------------------------------------\n")
        for msg in history:
            role = "USER" if msg['sender'] == 'user' else "MINDMATE"
            f.write(f"[{role}]: {msg['text']}\n")
            
        f.write("\n==================================================\n")
        f.write("This report is for informational purposes only.\n")
        f.write("MindMate is an AI companion, not a licensed doctor.\n")
        f.write("If you are in crisis, please seek professional help.\n")
        
    return filepath
