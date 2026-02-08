import yfinance as yf
def trend_prediction(stock):
    df=yf.download(stock+".NS",period="7d",interval="1d",progress=False)
    h,l,c=df["High"].max(),df["Low"].min(),df["Close"].iloc[-1]
    if c>=h*0.98: return "BREAKOUT_SOON (2D–1W)"
    if c<=l*1.02: return "BREAKDOWN_SOON (2D–1W)"
    return "SIDEWAYS"
