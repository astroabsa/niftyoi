# pcr_engine.py

def calculate_pcr(df):
    total_put_oi = df['put_oi'].sum()
    total_call_oi = df['call_oi'].sum()

    total_put_change = df['put_oi_change'].sum()
    total_call_change = df['call_oi_change'].sum()

    pcr = total_put_oi / total_call_oi if total_call_oi != 0 else 0
    delta_pcr = total_put_change / total_call_change if total_call_change != 0 else 0

    return pcr, delta_pcr
