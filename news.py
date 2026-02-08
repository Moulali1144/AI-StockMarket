import feedparser
KEYWORDS=['RBI','rate','inflation','Fed','crude','war','budget','govt']
def market_news(stock):
 news=[]
 for f in [f'https://news.google.com/rss/search?q={stock}+india+stock','https://www.reuters.com/rssFeed/marketsNews']:
  feed=feedparser.parse(f)
  for e in feed.entries[:5]:
   if any(k.lower() in e.title.lower() for k in KEYWORDS): news.append(e.title)
 return news
