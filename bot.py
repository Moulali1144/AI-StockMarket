import json
from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import BOT_TOKEN
from holiday import is_holiday
from nse_live import live_price
from alert_engine import auto_alert


def load():
    with open("data.json") as f:
        return json.load(f)


def save(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=2)


def start(update, context):
    update.message.reply_text(
        "Hi 👋 How can I help you today?\n\n"
        "• Type a stock name (RELIANCE, CONCOR)\n"
        "• Use /add SYMBOL YYYY-MM-DD to track F&O"
    )


def add(update, context):
    try:
        symbol, expiry = context.args
        data = load()
        data["stocks"].append({
            "stock": symbol.upper(),
            "expiry": expiry
        })
        save(data)
        update.message.reply_text("✅ Stock added for tracking")
    except Exception:
        update.message.reply_text(
            "❌ Usage:\n/add RELIANCE 2026-02-14"
        )


def handle_text(update, context):
    text = update.message.text.strip().upper()

    # Market holiday check
    holiday, reason = is_holiday()
    if holiday:
        update.message.reply_text(
            f"📅 Market is closed today due to {reason}.\n\n"
            "You can still ask for:\n"
            "• Stock analysis\n"
            "• F&O planning"
        )
        return

    # Live NSE price check
    try:
        price = live_price(text)
        update.message.reply_text(
            f"📊 {text} — LIVE NSE PRICE\n\n"
            f"₹ {price}\n\n"
            "⏱ Near real-time NSE data"
        )
    except Exception:
        update.message.reply_text(
            "❓ I didn’t understand that.\n\n"
            "Try:\n"
            "• RELIANCE\n"
            "• CONCOR\n"
            "• /add SYMBOL YYYY-MM-DD"
        )


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_text)
    )

    updater.start_polling()

    # Start auto alert thread safely
    updates = updater.bot.get_updates()
    if updates:
        chat_id = updates[-1].message.chat.id
        Thread(
            target=auto_alert,
            args=(updater.bot, chat_id, load()["stocks"]),
            daemon=True
        ).start()

    updater.idle()


if __name__ == "__main__":
    main()
