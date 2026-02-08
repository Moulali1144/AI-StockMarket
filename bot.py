import json
from threading import Thread
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from config import BOT_TOKEN
from holiday import is_holiday
from nse_live import live_price
from alert_engine import auto_alert

def load(): return json.load(open('data.json'))
def save(d): json.dump(d,open('data.json','w'),indent=2)

def start(u,c): u.message.reply_text('Hi 👋 How can I help you today?')
def add(u,c): s,e=c.args; d=load(); d['stocks'].append({'stock':s,'expiry':e}); save(d); u.message.reply_text('Added for tracking')
def text(u,c): t=u.message.text.upper(); h,r=is_holiday();
 if h: u.message.reply_text(f'Market closed today due to {r}'); return
 try: u.message.reply_text(f'{t} Live Price: ₹{live_price(t)}')
 except: u.message.reply_text('Please enter valid NSE symbol')

def main(): up=Updater(BOT_TOKEN,use_context=True); dp=up.dispatcher; dp.add_handler(CommandHandler('start',start)); dp.add_handler(CommandHandler('add',add)); dp.add_handler(MessageHandler(Filters.text & ~Filters.command,text)); up.start_polling(); upd=up.bot.get_updates();
 if upd: Thread(target=auto_alert,args=(up.bot,upd[-1].message.chat.id,load()['stocks']),daemon=True).start(); up.idle()

if __name__=='__main__': main()
