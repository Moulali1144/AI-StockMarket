import time
from market_time import market_open_now
from nse_live import live_price
from news import market_news
from sentiment import sentiment_score
from sector_rank import sector_rank
from rules import expiry_ok
from confidence import confidence


def auto_alert(bot, chat_id, stocks):
    """
    Background auto-alert loop.
    Runs forever INSIDE a thread.
    """

    last_signal = {}

    while True:
        try:
            # Run only during market hours
            if not market_open_now():
                time.sleep(300)
                continue

            for item in stocks:
                symbol = item["stock"]
                expiry = item["expiry"]

                # Live price
                price = live_price(symbol)

                # News sentiment
                news = market_news(symbol)
                sentiment = sentiment_score(news)

                # Sector strength (top sector % change)
                top_sector_change = sector_rank()[0][1]

                # Expiry window
                expiry_valid = expiry_ok(expiry)

                # Confidence
                conf = confidence(
                    trend="MOVE",
                    sector=top_sector_change,
                    sentiment=sentiment,
                    expiry_ok=expiry_valid
                )

                # Send alert only if changed
                if last_signal.get(symbol) != conf:
                    bot.send_message(
                        chat_id=chat_id,
                        text=(
                            f"📢 LIVE AUTO ALERT\n\n"
                            f"Stock: {symbol}\n"
                            f"Price: ₹{price}\n"
                            f"Sentiment: {sentiment}\n"
                            f"Confidence: {conf}\n\n"
                            f"⚠ Manual trading only"
                        )
                    )
                    last_signal[symbol] = conf

            time.sleep(300)

        except Exception as e:
            # Never crash the bot
            print("Alert engine error:", e)
            time.sleep(300)
