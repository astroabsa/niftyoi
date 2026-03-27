# signal_engine.py

def generate_signal(pcr, delta_pcr):
    
    if delta_pcr > 1.2:
        return "🟢 BULLISH (Put Writing Dominant)"
    
    elif delta_pcr < 0.8:
        return "🔴 BEARISH (Call Writing Dominant)"
    
    elif pcr > 1.5:
        return "⚠️ OVERSOLD (Possible Bounce)"
    
    elif pcr < 0.5:
        return "⚠️ OVERBOUGHT (Possible Reversal)"
    
    else:
        return "🟡 NEUTRAL"
