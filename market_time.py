from datetime import datetime, time
def market_open_now():
    now = datetime.now().time()
    return time(9, 15) <= now <= time(15, 30)
