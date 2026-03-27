# app.py

import streamlit as st
from data_fetcher import fetch_option_chain
from pcr_engine import calculate_pcr
from signal_engine import generate_signal

st.set_page_config(layout="wide")
st.title("🔥 Real-Time ΔPCR Dashboard")

df = fetch_option_chain()

pcr, delta_pcr = calculate_pcr(df)
signal = generate_signal(pcr, delta_pcr)

col1, col2, col3 = st.columns(3)

col1.metric("PCR (Total OI)", round(pcr, 2))
col2.metric("ΔPCR (Change in OI)", round(delta_pcr, 2))
col3.metric("Market Signal", signal)

st.subheader("Option Chain Snapshot")
st.dataframe(df)

st.subheader("Top OI Build-Up")

top_calls = df.sort_values("call_oi_change", ascending=False).head(5)
top_puts = df.sort_values("put_oi_change", ascending=False).head(5)

col1, col2 = st.columns(2)
col1.write("🔴 Call Writing")
col1.dataframe(top_calls)

col2.write("🟢 Put Writing")
col2.dataframe(top_puts)
