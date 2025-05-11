import streamlit as st
import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange

st.set_page_config(page_title="TradingView Urdu Signals", layout="wide")
st.title("Urdu Trading Assistant – Live Signals")

# Coin list
coins = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]

# Timeframe selection
timeframes = {
    "1 Minute": Interval.INTERVAL_1_MINUTE,
    "5 Minutes": Interval.INTERVAL_5_MINUTES,
    "15 Minutes": Interval.INTERVAL_15_MINUTES,
    "1 Hour": Interval.INTERVAL_1_HOUR,
    "4 Hours": Interval.INTERVAL_4_HOURS,
    "1 Day": Interval.INTERVAL_1_DAY
}
selected_tf = st.selectbox("ٹائم فریم منتخب کریں", list(timeframes.keys()))

# Function to get TradingView signal
def get_signal(symbol, tf):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BINANCE",
            interval=timeframes[tf]
        )
        analysis = handler.get_analysis()
        return analysis.summary["RECOMMENDATION"]
    except:
        return "NO DATA"

# Function to display colored signal
def show_signal(signal):
    if signal == "BUY":
        return "🟢 BUY"
    elif signal == "SELL":
        return "🔴 SELL"
    elif signal == "NEUTRAL":
        return "🟡 WAIT"
    else:
        return "❓ NO DATA"

# Create signal table
st.header("تمام سکہ جات کے سگنلز")
data = []
for coin in coins:
    signal = get_signal(coin, selected_tf)
    data.append({
        "Coin": coin,
        "Signal": show_signal(signal)
    })

df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)
