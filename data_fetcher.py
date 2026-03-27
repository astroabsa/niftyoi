# data_fetcher.py

import requests
import pandas as pd
from config import *

def fetch_option_chain():
    url = f"https://api.upstox.com/v2/option/chain"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    params = {
        "symbol": SYMBOL,
        "expiry_date": EXPIRY
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    records = []

    for item in data['data']:
        records.append({
            "strike": item['strike_price'],
            "call_oi": item['call_options']['oi'],
            "put_oi": item['put_options']['oi'],
            "call_oi_change": item['call_options']['oi_change'],
            "put_oi_change": item['put_options']['oi_change']
        })

    return pd.DataFrame(records)
