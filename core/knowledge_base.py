# A comprehensive knowledge base of mental health and emotional issues
# This acts as the "Universe" of known issues for exact matching.

UNIVERSE_KB = {
    # --- ANXIETY & PANIC ---
    "gad": "Generalized Anxiety Disorder (GAD) involves persistent, excessive worry about various things. It's exhausting. Grounding techniques and CBT are very effective.",
    "social anxiety": "Social anxiety is the intense fear of being judged or rejected in social situations. It's not just shyness. Exposure therapy and cognitive reframing help significantly.",
    "panic attack": "A panic attack feels like a sudden surge of overwhelming fear. You might feel like you're dying, but you are not. It will pass in minutes. Breathe deeply.",
    "phobia": "A phobia is an irrational fear of a specific object or situation. If it's affecting your life, systematic desensitization is a proven treatment.",
    "agoraphobia": "Agoraphobia is the fear of situations where escape might be difficult. It often leads to avoidance. Small steps and safe zones are key to recovery.",

    # --- MOOD DISORDERS ---
    "depression": "Depression isn't just sadness; it's a persistent feeling of emptiness or loss of interest. It's a medical condition, not a weakness. Therapy and medication are standard treatments.",
    "bipolar": "Bipolar disorder involves extreme mood swings, from emotional highs (mania) to lows (depression). Mood stabilizers and tracking triggers are essential for management.",
    "sad": "Seasonal Affective Disorder (SAD) is depression related to changes in seasons. Light therapy and Vitamin D often help.",
    
    # --- TRAUMA ---
    "ptsd": "PTSD (Post-Traumatic Stress Disorder) can occur after experiencing a terrifying event. Flashbacks and avoidance are common. EMDR and trauma-focused therapy are very effective.",
    "cptsd": "Complex PTSD often comes from prolonged trauma (like childhood neglect). It affects your self-concept and emotional regulation. Healing happens in safe relationships.",
    "trauma": "Trauma is the emotional response to a terrible event. It can physically change the brain. Be gentle with yourself; healing is a non-linear journey.",

    # --- OBSESSIVE-COMPULSIVE ---
    "ocd": "OCD involves unwanted thoughts (obsessions) and repetitive behaviors (compulsions). The goal isn't to stop the thoughts, but to change your reaction to them (ERP therapy).",
    "hoarding": "Hoarding disorder is a persistent difficulty discarding possessions. It's often linked to anxiety or grief.",
    "body dysmorphia": "Body Dysmorphic Disorder (BDD) is an obsession with a perceived flaw in appearance. Mirror framing and CBT can help reduce the distress.",
    "trichotillomania": "Trichotillomania is a hair-pulling disorder, often a mechanism to soothe anxiety. Awareness training and habit reversal therapy are helpful.",

    # --- NEURODEVELOPMENTAL ---
    "adhd": "ADHD affects executive function—focus, impulse control, and organization. It's a brain difference, not a lack of willpower. Structure and dopamine management help.",
    "autism": "Autism Spectrum Disorder involves differences in social, communication, and sensory processing. It's a neurotype, not a disease that needs 'curing'.",
    "dyslexia": "Dyslexia is a learning difference affecting reading. It has nothing to do with intelligence. Multi-sensory learning approaches are best.",

    # --- PERSONALITY PATTERNS ---
    "bpd": "Borderline Personality Disorder involves intense mood swings, fear of abandonment, and unstable relationships. DBT (Dialectical Behavior Therapy) was created specifically for this.",
    "narcissism": "Narcissistic traits often mask deep insecurity. Dealing with this involves setting firm boundaries.",
    "avoidant": "Avoidant Personality Disorder involves extreme social inhibition and feelings of inadequacy. Building self-trust slowly is the path forward.",
    
    # --- EATING ISSUES ---
    "anorexia": "Anorexia involves restricting intake due to fear of weight gain. It is a serious condition requiring medical and psychological support.",
    "bulimia": "Bulimia involves cycles of bingeing and purging. It is physically dangerous but treatable with therapy and nutritional counseling.",
    "binge eating": "Binge Eating Disorder is using food to cope with emotions. It's often linked to restriction cycles. Intuitive eating is a helpful framework.",

    # --- EMOTIONS (The Spectrum) ---
    "grief": "Grief is the price we pay for love. It comes in waves. There is no 'right' timeline to grieve.",
    "guilt": "Guilt is the feeling that you *did* something wrong. It can be useful if it leads to repair, but toxic if it's chronic.",
    "shame": "Shame is the feeling that you *are* wrong. It thrives in secrecy. Empathy is the antidote to shame.",
    "envy": "Envy tells you what you want for yourself. Instead of letting it rot you, let it show you your hidden desires.",
    "jealousy": "Jealousy is the fear of losing something you have. It usually points to an insecurity in the relationship.",
    "apathy": "Apathy or numbness is often a defense mechanism against overwhelming stress. It's your brain pulling the emergency brake.",
    "loneliness": "Loneliness is a signal that your social needs aren't being met. It hurts because we represent a tribal species.",
    "rejection": "Rejection triggers the same brain centers as physical pain. It hurts, but it does not define your worth.",
    "impostor syndrome": "Impostor syndrome is feeling like a fraud despite evidence of success. It's very common among high achievers.",
    "burnout": "Burnout is emotional, physical, and mental exhaustion caused by excessive and prolonged stress. You cannot 'push through' burnout; you must rest.",

    # --- EXISTENTIAL ---
    "purpose": "A sense of purposelessness is common. Purpose isn't found; it's built through action and connection.",
    "death anxiety": "Thanatophobia or death anxiety is a fundamental human fear. Focusing on present meaningfulness often alleviates it.",
    "identity": "Identity crisis happens when our roles change. It's an opportunity to redefine who you are on your own terms.",
    
    # --- LIFE SITUATIONS ---
    "breakup": "Heartbreak is a form of withdrawal. Your brain is missing the dopamine of the partner. No contact is often the best medicine.",
    "divorce": "Divorce is the death of a future you imagined. Grieve it fully before trying to rebuild.",
    "job loss": "Losing a job strikes at our security and identity. Remember: you are not your work.",
    "bullying": "Bullying leaves deep scars. It reflects the bully's pain, not your value.",
    "exams": "Exam stress is temporary. Your grades do not determine your destiny.",
    "public speaking": "Glossophobia is the most common fear. Visualization and preparation are your best tools.",
    "insomnia": "Insomnia feeds on the fear of not sleeping. Paradoxically, accepting that you might just rest instead of sleep can help you sleep."
}

import re

def find_best_match(user_text):
    """
    Scans the user text for keywords matching the KB.
    Returns the specific response if a match is found, else None.
    Uses Regex word boundaries to avoid partial matches.
    """
    text = user_text.lower()
    
    # Check specifically for exact phrases first
    for key, response in UNIVERSE_KB.items():
        # Escape key for regex special chars just in case (though keys are simple usually)
        # Use \b boundries
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, text):
            return response
            
    # Check for split keywords (e.g. "social" and "anxiety" together)
    # Using word boundaries for these too
    if re.search(r'\bsocial\b', text) and re.search(r'\banxiety\b', text):
        return UNIVERSE_KB["social anxiety"]
    if re.search(r'\bbinge\b', text) and re.search(r'\beating\b', text):
        return UNIVERSE_KB["binge eating"]
    if re.search(r'\bpanic\b', text) and re.search(r'\battack\b', text):
        return UNIVERSE_KB["panic attack"]
    if re.search(r'\bpost\b', text) and re.search(r'\btraumatic\b', text):
        return UNIVERSE_KB["ptsd"]
    
    return None
