import requests
HEADERS={'User-Agent':'Mozilla/5.0','Accept-Language':'en-US,en;q=0.9'}
session=requests.Session(); session.get('https://www.nseindia.com',headers=HEADERS)
def live_price(symbol): r=session.get(f'https://www.nseindia.com/api/quote-equity?symbol={symbol}',headers=HEADERS).json(); return r['priceInfo']['lastPrice']
def all_indices(): return session.get('https://www.nseindia.com/api/allIndices',headers=HEADERS).json()['data']
