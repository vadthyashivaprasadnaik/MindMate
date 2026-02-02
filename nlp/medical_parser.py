
import PyPDF2
import io
import re

def extract_text_from_pdf(file_stream):
    """
    Extracts text from a PDF file stream.
    """
    try:
        reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def analyze_report_text(text):
    """
    Analyzes medical report text for common markers and returns a structured logic dict.
    This is HEURISTIC based. In production, use a real medical NLP API.
    """
    findings = []
    text_lower = text.lower()
    
    # --- 1. VITAMINS & MINERALS ---
    if "iron" in text_lower or "ferritin" in text_lower or "haemoglobin" in text_lower:
        if "low" in text_lower or "deficien" in text_lower or "anemia" in text_lower:
            findings.append("Potential Iron Deficiency (Anemia)")
            
    if "vitamin d" in text_lower or "25-oh" in text_lower:
        if "low" in text_lower or "deficien" in text_lower or "insufficien" in text_lower:
            findings.append("Low Vitamin D Levels")
            
    if "b12" in text_lower or "cobalamin" in text_lower:
         if "low" in text_lower:
            findings.append("Low Vitamin B12")

    # --- 2. THYROID ---
    if "tsh" in text_lower or "thyroid" in text_lower:
        if "high" in text_lower:
            findings.append("Elevated TSH (Possible Hypothyroidism)")
        elif "low" in text_lower:
             findings.append("Low TSH (Possible Hyperthyroidism)")

    # --- 3. BLOOD SUGAR ---
    if "glucose" in text_lower or "hba1c" in text_lower or "blood sugar" in text_lower:
        if "high" in text_lower or "prediayet" in text_lower or "diabet" in text_lower:
             findings.append("Elevated Blood Glucose Markers")

    # --- 4. BLOOD PRESSURE ---
    # Regex for BP like "140/90"
    bp_match = re.search(r'(\d{2,3})\/(\d{2,3})', text)
    if bp_match:
        sys = int(bp_match.group(1))
        dia = int(bp_match.group(2))
        if sys > 130 or dia > 85:
            findings.append(f"Recorded High Blood Pressure: {sys}/{dia}")
        if sys < 90 or dia < 60:
            findings.append(f"Recorded Low Blood Pressure: {sys}/{dia}")

    return {
        "raw_text_snippet": text[:200] + "...",
        "findings": findings,
        "advice_context": generate_advice_context(findings)
    }

def generate_advice_context(findings):
    """
    Generates a system prompt string or bullet points for the Chatbot to use.
    """
    if not findings:
        return "No specific medical anomalies detected in the provided snippet."
    
    context = "USER HEALTH CONTEXT (From Uploaded Report):\n"
    for finding in findings:
        context += f"- {finding}\n"
        
        # Add quick actionable advice for the system prompt
        if "Iron" in finding:
            context += "  * Suggestion: Eat leafy greens, red meat, or take supplements if prescribed. Deficiency causes fatigue.\n"
        elif "Vitamin D" in finding:
             context += "  * Suggestion: Get sunlight, eat fortified foods. Deficiency causes low mood and fatigue.\n"
        elif "Thyroid" in finding:
             context += "  * Suggestion: Thyroid impacts mood and energy regulation significantly.\n"
        elif "Glucose" in finding:
             context += "  * Suggestion: Manage diet (low sugar) and exercise.\n"
             
    return context
