import time
from market_time import market_open_now
from nse_live import live_price
from news import market_news
from sentiment import sentiment_score
from sector_rank import sector_rank
from rules import expiry_ok
from confidence import confidence

def auto_alert(bot,chat_id,stocks): last={}
 while True:
  if not market_open_now(): time.sleep(300); continue
  for s in stocks:
   p=live_price(s['stock']); sent=sentiment_score(market_news(s['stock'])); sec=sector_rank()[0][1]; conf=confidence('MOVE',sec,sent,expiry_ok(s['expiry']))
   if last.get(s['stock'])!=conf:
    bot.send_message(chat_id=chat_id,text=f'📢 LIVE ALERT\n{s['stock']} ₹{p}\nSentiment:{sent}\nConfidence:{conf}')
    last[s['stock']]=conf
  time.sleep(300)
