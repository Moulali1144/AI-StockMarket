import json

from threading import Thread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import BOT_TOKEN
from holiday import is_holiday
from nse_live import live_price
from alert_engine import auto_alert
# In-memory conversation context (per chat)
USER_CONTEXT = {}

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
        "• Ask about market / F&O / RBI / global news"
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


# 🔹 MARKET CONTEXT (WORKS EVEN ON SUNDAY)
def get_market_context_analysis():
    return (
        "🌍 Market Pre-Open / Weekend Analysis\n\n"
        "• US & global markets impact\n"
        "• RBI & Govt policy watch\n"
        "• Crude, Dollar & Bond yields\n"
        "• Sector bias for next session\n\n"
        "📌 Indian market is closed now,\n"
        "but global cues may impact Monday."
    )


# 🔹 STOCK ANALYSIS (NO LIVE PRICE ON HOLIDAY)
def get_stock_analysis(symbol):
    return (
        f"📊 Stock Analysis: {symbol}\n\n"
        "• Trend: Short-term momentum\n"
        "• Sector strength: Evaluated\n"
        "• News impact: Neutral to Positive\n"
        "• F&O view: Plan for next session\n\n"
        "⚠ Useful for planning, not live trading."
    )


def handle_text(update, context):
    text = update.message.text.strip().lower()

    # 1️⃣ Greeting
    if text in ["hi", "hello", "hey"]:
        update.message.reply_text(
            "Hi 👋 How can I help you today?\n\n"
            "• Type a stock name (RELIANCE, CONCOR)\n"
            "• Ask about market / F&O / RBI / global news"
        )
        return

    # 2️⃣ Market / RBI / Global questions
    market_keywords = [
        "market", "f&o", "fno", "expiry",
        "nifty", "banknifty",
        "rbi", "govt", "government",
        "global", "us market", "dow", "nasdaq"
    ]

    if any(k in text for k in market_keywords):
        update.message.reply_text(get_market_context_analysis())
        return

    # 3️⃣ Stock shortcut name (CONCOR, TCS, RELIANCE)
    symbol = text.upper()
    if symbol.isalpha() and len(symbol) <= 12:
        holiday, reason = is_holiday()

        # Market open → live price
        if not holiday:
            try:
                price = live_price(symbol)
                update.message.reply_text(
                    f"📊 {symbol} — LIVE NSE PRICE\n\n"
                    f"₹ {price}\n\n"
                    "⏱ Near real-time NSE data"
                )
                return
            except Exception:
                pass

        # Market closed → analysis
        update.message.reply_text(get_stock_analysis(symbol))
        return

    # 4️⃣ Fallback
    update.message.reply_text(
        "❓ I didn’t understand that.\n\n"
        "Try:\n"
        "• RELIANCE\n"
        "• CONCOR\n"
        "• Market outlook\n"
        "• RBI news"
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

    # Auto alert thread
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
