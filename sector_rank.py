from nse_live import all_indices
def sector_rank(): d=all_indices(); s={i['index']:i['percentChange'] for i in d if 'NIFTY' in i['index']}; return sorted(s.items(),key=lambda x:x[1],reverse=True)[:5]
