import feedparser
KEYWORDS = ["RBI","interest","inflation","Fed","crude","war","election"]
def get_market_news(stock):
    feeds = [
        f"https://news.google.com/rss/search?q={stock}+india+stock",
        "https://www.reuters.com/rssFeed/marketsNews"
    ]
    news=[]
    for url in feeds:
        feed=feedparser.parse(url)
        for e in feed.entries[:5]:
            if any(k.lower() in e.title.lower() for k in KEYWORDS):
                news.append(e.title)
    return news
