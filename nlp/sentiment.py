from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyzes sentiment of the text.
    Returns a float from -1.0 (negative) to 1.0 (positive).
    """
    analysis = TextBlob(text)
    return analysis.sentiment.polarity
