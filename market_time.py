from datetime import datetime,time
def market_open_now(): return time(9,15)<=datetime.now().time()<=time(15,30)
