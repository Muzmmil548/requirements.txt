# Urdu Trading Assistant App - Full Functional Version

import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import ccxt
import requests
from datetime import datetime, timedelta

# Title
st.title("اردو ٹریڈنگ اسسٹنٹ")

# Sidebar Exchange Toggle
st.sidebar.header("ایکسچینج سلیکشن")
use_tradingview = st.sidebar.checkbox("TradingView چارٹ استعمال کریں", value=True)
use_exchange_chart = st.sidebar.checkbox("ایکسچینج چارٹ استعمال کریں", value=False)

# Coin Selection
st.sidebar.subheader("سکوں کا انتخاب کریں")
coin_limit = st.sidebar.radio("Top Coins", ["Top 10", "Top 50"])
coin_count = 10 if coin_limit == "Top 10" else 50

# Sample coin list (replace with real-time top coins if needed)
sample_coins = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "MATIC/USDT"]
coins = sample_coins[:coin_count]

# Function to get simple buy/sell/hold signal
def get_signal(data):
    if data['Close'][-1] > data['Close'][-5:].mean():
        return "🟢 Buy"
    elif data['Close'][-1] < data['Close'][-5:].mean():
        return "🔴 Sell"
    else:
        return "🟡 Hold"

# Chart and Signal Display
for coin in coins:
    st.markdown(f"### {coin}")
    
    # Use YFinance for historical data
    symbol = coin.replace("/", "")
    data = yf.download(symbol, period="7d", interval="1h")

    if data.empty:
        st.warning(f"Data not available for {coin}")
        continue

    # Show Chart
    if use_tradingview:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name="Candlesticks"
        ))
        fig.update_layout(title=f"{coin} Chart", xaxis_title="Time", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)
    
    # Show Signal
    signal = get_signal(data)
    st.markdown(f"**Signal:** {signal}")

st.success("ایپ مکمل طور پر کامیابی سے لوڈ ہو گئی ہے۔")
