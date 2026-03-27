import requests
import pandas as pd
import streamlit as st

def fetch_option_chain():
    url = "https://api.upstox.com/v2/option/chain"

    headers = {
        "Authorization": f"Bearer {st.secrets['ACCESS_TOKEN']}"
    }

    params = {
        "symbol": st.secrets["SYMBOL"],
        "expiry_date": st.secrets["EXPIRY"]
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    records = []

    for item in data.get('data', []):
        records.append({
            "strike": item['strike_price'],
            "call_oi": item['call_options']['oi'],
            "put_oi": item['put_options']['oi'],
            "call_oi_change": item['call_options']['oi_change'],
            "put_oi_change": item['put_options']['oi_change']
        })

    return pd.DataFrame(records)
