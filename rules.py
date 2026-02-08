from datetime import datetime
def expiry_ok(e): return (datetime.strptime(e,'%Y-%m-%d')-datetime.now()).days in [1,2]
