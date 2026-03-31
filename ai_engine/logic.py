from textblob import TextBlob

def analyze_sentiment(text):
    """
    Analyzes text and returns (Sentiment Label, Score).
    Label: POSITIVE, NEUTRAL, NEGATIVE
    Score: -1.0 to 1.0 (Polarity)
    """
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    
    # Classification logic based on polarity score
    if polarity > 0.15:
        return 'POSITIVE', round(polarity, 2)
    elif polarity < -0.15:
        return 'NEGATIVE', round(polarity, 2)
    else:
        return 'NEUTRAL', round(polarity, 2)

def calculate_recommendation_score(avg_rating, sentiment_score, review_count):
    """
    Weighted scoring formula:
    (Rating * 0.4) + (Sentiment * 0.4) + (Popularity * 0.2)
    """
    # Normalize review count to a 0-1 scale (capped at 100 reviews)
    popularity = min(review_count / 100, 1.0)
    
    # Normalize rating (1-5) to a 0-1 scale
    norm_rating = (avg_rating - 1) / 4 if avg_rating > 0 else 0
    
    # Sentiment score is already roughly -1 to 1, shift to 0-1
    norm_sentiment = (sentiment_score + 1) / 2
    
    final_score = (norm_rating * 0.4) + (norm_sentiment * 0.4) + (popularity * 0.2)
    return round(final_score * 100, 1) # Returns score out of 100