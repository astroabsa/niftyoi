import requests
import pandas as pd
import streamlit as st

def fetch_option_chain():
    url = "https://api.upstox.com/v2/market-quote/option-greek"

    headers = {
        "Authorization": f"Bearer {st.secrets['ACCESS_TOKEN']}",
        "Accept": "application/json"
    }

    # Example instruments (you NEED to generate these dynamically later)
    instruments = [
        "NSE_FO|NIFTY24MAR22000CE",
        "NSE_FO|NIFTY24MAR22000PE",
    ]

    params = {
        "instrument_key": ",".join(instruments)
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        st.write(response.text)  # DEBUG
        return pd.DataFrame()

    data = response.json()

    records = []

    for key, value in data.get("data", {}).items():
        records.append({
            "instrument": key,
            "oi": value.get("oi", 0),
            "oi_change": value.get("oi_day_change", 0)
        })

    return pd.DataFrame(records)
