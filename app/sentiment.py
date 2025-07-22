from textblob import TextBlob

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.2:
            return 'Bullish'
        elif polarity < -0.2:
            return 'Bearish'
        elif 'rise' in text.lower() or 'gain' in text.lower():
            return 'Positive'
        elif 'fall' in text.lower() or 'drop' in text.lower():
            return 'Negative'
        return 'Neutral'
    except Exception:
        return 'Neutral'