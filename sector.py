import yfinance as yf
SECTOR_MAP={"HDFCBANK":"^NSEBANK","ICICIBANK":"^NSEBANK","SBIN":"^NSEBANK","INFY":"^CNXIT","TCS":"^CNXIT","TATASTEEL":"^CNXMETAL"}
def sector_strength(stock):
    idx=SECTOR_MAP.get(stock,"^NSEI")
    df=yf.download(idx,period="5d",interval="1d",progress=False)
    ch=(df["Close"].iloc[-1]-df["Close"].iloc[0])/df["Close"].iloc[0]
    if ch>0.01: return "STRONG"
    if ch<-0.01: return "WEAK"
    return "NEUTRAL"
