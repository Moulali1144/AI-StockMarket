import time
from market_time import market_open_now
from trend import trend_prediction
from sector import sector_strength
from news import get_market_news
from ai import news_sentiment
from rules import expiry_before, final_decision
def auto_alert(bot,chat_id,stocks,interval):
    last_signal={}
    while True:
        if not market_open_now():
            time.sleep(300); continue
        for s in stocks:
            trend=trend_prediction(s["stock"])
            sector=sector_strength(s["stock"])
            news=get_market_news(s["stock"])
            sentiment=news_sentiment(news)
            expiry_ok=expiry_before(s["expiry"])
            decision=final_decision(trend,sentiment,sector,expiry_ok)
            if last_signal.get(s["stock"])!=decision:
                bot.send_message(chat_id=chat_id,text=f"📢 AUTO ALERT\n\nStock: {s['stock']}\nTrend: {trend}\nSector: {sector}\nSentiment: {sentiment}\n👉 Action: {decision}")
                last_signal[s["stock"]]=decision
        time.sleep(interval)
