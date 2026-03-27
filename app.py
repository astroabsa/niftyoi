import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# --- CONFIGURATION ---
ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiIzTUJDMzIiLCJqdGkiOiI2OWM2ODMyOWQ5MmEyMDc1MjFkMjY4MjciLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaXNQbHVzUGxhbiI6ZmFsc2UsImlhdCI6MTc3NDYxNzM4NSwiaXNzIjoidWRhcGktZ2F0ZXdheS1zZXJ2aWNlIiwiZXhwIjoxNzc0NjQ4ODAwfQ.vOYotCHBxdEpQB2YcBvavvk1KAKE_kDu_VtIxvghs54" # Get this via Upstox Dashboard
INSTRUMENT_KEY = "NSE_INDEX|Nifty 50" # Or "NSE_INDEX|Nifty Bank"
EXPIRY_DATE = "2026-04-02" # Format: YYYY-MM-DD

def fetch_option_chain(key, expiry):
    url = "https://api.upstox.com/v2/option/chain"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    params = {'instrument_key': key, 'expiry_date': expiry}
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def process_data(json_data):
    rows = []
    for item in json_data['data']:
        strike = item['strike_price']
        
        # Call Data
        c_oi = item['call_options']['market_data']['oi']
        c_prev_oi = item['call_options']['market_data']['prev_oi']
        c_chg_oi = c_oi - c_prev_oi
        
        # Put Data
        p_oi = item['put_options']['market_data']['oi']
        p_prev_oi = item['put_options']['market_data']['prev_oi']
        p_chg_oi = p_oi - p_prev_oi
        
        rows.append({
            'Strike': strike,
            'Call_OI': c_oi, 'Call_Chg_OI': c_chg_oi,
            'Put_OI': p_oi, 'Put_Chg_OI': p_chg_oi
        })
    return pd.DataFrame(rows)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Live Smart Money Dashboard", layout="wide")
st.title("🧠 Option Chain & Smart Money Dashboard")

# 1. Fetch & Process
data = fetch_option_chain(INSTRUMENT_KEY, EXPIRY_DATE)
if data.get('status') == 'success':
    df = process_data(data)
    
    # 2. Key Metrics (The "Main Weapons")
    total_call_oi = df['Call_OI'].sum()
    total_put_oi = df['Put_OI'].sum()
    total_call_chg = df['Call_Chg_OI'].sum()
    total_put_chg = df['Put_Chg_OI'].sum()
    
    pcr_total = round(total_put_oi / total_call_oi, 2)
    pcr_coi = round(total_put_chg / total_call_chg, 2)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total PCR", pcr_total)
    col2.metric("PCR (Change in OI)", pcr_coi, help="Main Weapon: > 1 is Bullish, < 1 is Bearish")
    
    # 3. Smart Money Signal Logic
    bias = "Neutral"
    if pcr_coi > 1.2: bias = "Bullish 🚀"
    elif pcr_coi < 0.8: bias = "Bearish 📉"
    col3.metric("Trend Bias", bias)

    # 4. Strike-wise OI Buildup Chart
    st.subheader("📊 Strike-wise OI Buildup")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['Strike'], y=df['Call_Chg_OI'], name='Call Change OI', marker_color='red'))
    fig.add_trace(go.Bar(x=df['Strike'], y=df['Put_Chg_OI'], name='Put Change OI', marker_color='green'))
    fig.update_layout(barmode='group', xaxis_title="Strike Price", yaxis_title="Change in OI")
    st.plotly_chart(fig, use_container_width=True)

    # 5. Live Data Table
    st.dataframe(df.style.highlight_max(axis=0, subset=['Call_Chg_OI', 'Put_Chg_OI']))

else:
    st.error("Failed to fetch data. Check your Token or Expiry Date.")
