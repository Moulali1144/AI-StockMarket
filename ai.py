from transformers import pipeline
model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
def news_sentiment(news):
    score = 0
    for n in news:
        r = model(n)[0]["label"]
        if r == "positive": score += 1
        elif r == "negative": score -= 1
    return score
