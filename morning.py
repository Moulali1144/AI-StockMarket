from nse_live import all_indices
def outlook(): i=all_indices(); n=[x for x in i if x['index']=='NIFTY 50'][0]['percentChange']; b=[x for x in i if x['index']=='NIFTY BANK'][0]['percentChange']; bias='BULLISH' if n>0 and b>0 else 'BEARISH' if n<0 and b<0 else 'SIDEWAYS'; return f'🌅 Morning Outlook\nNIFTY:{n}%\nBANKNIFTY:{b}%\nBias:{bias}'
