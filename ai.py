from textblob import TextBlob

def news_sentiment(news):
    score = 0
    for n in news:
        polarity = TextBlob(n).sentiment.polarity
        if polarity > 0.1:
            score += 1
        elif polarity < -0.1:
            score -= 1
    return score
