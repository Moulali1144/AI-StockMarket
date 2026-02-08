from datetime import datetime
def is_holiday(): wd=datetime.now().weekday(); return (True,'Saturday') if wd==5 else (True,'Sunday') if wd==6 else (False,None)
