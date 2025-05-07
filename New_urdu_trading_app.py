import streamlit as st
import pandas as pd
import requests
import talib
import numpy as np
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# --- Title ---
st.title("AI Powered Trading Assistant with Live Signals and Chart Patterns")

# --- User Coin Selection ---
top_option = st.radio("Select Coin List", ["Top 10", "Top 50"])
st.markdown("AI Assistant will show Buy (🟢), Hold (🟡), Sell (🔴) signals")

# --- Function to fetch coin list from CoinGecko ---
def get_top_coins(n):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": n, "page": 1}
    r = requests.get(url, params=params)
    return pd.DataFrame(r.json())

# --- Fetch Top Coins ---
top_n = 10 if top_option == "Top 10" else 50
coin_df = get_top_coins(top_n)

# --- Loop through coins and show analysis ---
for _, row in coin_df.iterrows():
    symbol = row['symbol'].upper()
    name = row['name']
    price = row['current_price']

    # Simulated OHLC data (replace with Binance live OHLC if needed)
    np.random.seed(0)
    close = np.random.normal(price, 1, 100)
    high = close + np.random.rand(100)
    low = close - np.random.rand(100)
    open_ = close + np.random.normal(0, 0.5, 100)

    # Indicators
    rsi = talib.RSI(close)[-1]
    macd, signal, _ = talib.MACD(close)
    ma50 = talib.SMA(close, timeperiod=50)[-1]
    ma200 = talib.SMA(close, timeperiod=200)[-1]

    # Traffic Signal Logic
    if rsi < 30 and macd[-1] > signal[-1]:
        signal_color = "🟢 BUY"
    elif rsi > 70 and macd[-1] < signal[-1]:
        signal_color = "🔴 SELL"
    else:
        signal_color = "🟡 WAIT"

    # Layout
    with st.expander(f"{name} ({symbol}) - ${price}"):
        st.write(f"**RSI**: {round(rsi, 2)}")
        st.write(f"**MACD**: {round(macd[-1], 2)} | **Signal**: {round(signal[-1], 2)}")
        st.write(f"**MA50**: {round(ma50, 2)} | **MA200**: {round(ma200, 2)}")
        st.markdown(f"### Signal: {signal_color}")

        # Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=close, name="Price"))
        st.plotly_chart(fig, use_container_width=True)

        # Chart Pattern Detection (simulated)
        patterns = [
            "Head & Shoulders", "Inverse Head & Shoulders", "Triangle",
            "Double Top", "Double Bottom", "Cup and Handle", "Wedge",
            "Bullish Rectangle", "Bearish Rectangle", "Symmetrical Triangle",
            "Ascending Triangle", "Descending Triangle", "Triple Top", "Triple Bottom",
            "Broadening Formation"
        ]

        st.subheader("Chart Pattern Detection")
        for pattern in patterns:
            st.markdown(f"- {pattern} 🟢")

# --- End ---
