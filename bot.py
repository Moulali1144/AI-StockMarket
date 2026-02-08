import json
from threading import Thread
from telegram.ext import Updater, CommandHandler
from config import BOT_TOKEN, CHECK_INTERVAL
from alert_engine import auto_alert
def load():
    with open("data.json") as f: return json.load(f)
def save(d):
    with open("data.json","w") as f: json.dump(d,f,indent=2)
def start(update,ctx):
    update.message.reply_text("📊 Personal AI F&O Bot\n/add STOCK YYYY-MM-DD\n/remove STOCK")
def add(update,ctx):
    stock,expiry=ctx.args
    d=load(); d["stocks"].append({"stock":stock,"expiry":expiry}); save(d)
    update.message.reply_text("✅ Added")
def remove(update,ctx):
    stock=ctx.args[0]
    d=load(); d["stocks"]=[s for s in d["stocks"] if s["stock"]!=stock]; save(d)
    update.message.reply_text("❌ Removed")
def main():
    up=Updater(BOT_TOKEN,use_context=True)
    dp=up.dispatcher
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("add",add))
    dp.add_handler(CommandHandler("remove",remove))
    up.start_polling()
    updates=up.bot.get_updates()
    if updates:
        chat_id=updates[-1].message.chat.id
        Thread(target=auto_alert,args=(up.bot,chat_id,load()["stocks"],CHECK_INTERVAL),daemon=True).start()
    up.idle()
if __name__=="__main__": main()
