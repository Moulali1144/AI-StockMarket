from datetime import datetime
def expiry_before(expiry):
    exp=datetime.strptime(expiry,"%Y-%m-%d")
    return (exp-datetime.now()).days in [1,2]
def final_decision(trend,sentiment,sector,expiry_ok):
    if not expiry_ok: return "AVOID (EXPIRY DAY)"
    if "BREAKOUT" in trend and sentiment>=0 and sector=="STRONG": return "BUY CE (1–2 DAYS)"
    if "BREAKDOWN" in trend and sentiment<=0 and sector=="WEAK": return "BUY PE (1–2 DAYS)"
    return "WAIT"
