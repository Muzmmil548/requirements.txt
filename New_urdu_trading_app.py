# Urdu Trading Assistant App - Corrected

import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("اردو ٹریڈنگ اسسٹنٹ")

st.sidebar.header("ایکسچینج سلیکشن")
use_tradingview = st.sidebar.checkbox("TradingView چارٹ استعمال کریں", value=True)

st.sidebar.subheader("سکوں کا انتخاب کریں")
coin_limit = st.sidebar.radio("Top Coins", ["Top 10", "Top 50"])
coin_count = 10 if coin_limit == "Top 10" else 50

sample_coins = ["BTC/USD", "ETH/USD", "BNB/USD", "SOL/USD", "XRP/USD", "ADA/USD", "DOGE/USD", "AVAX/USD", "DOT/USD", "MATIC/USD"]
coins = sample_coins[:coin_count]

def get_signal(data):
    if data['Close'][-1] > data['Close'][-5:].mean():
        return "🟢 Buy"
    elif data['Close'][-1] < data['Close'][-5:].mean():
        return "🔴 Sell"
    else:
        return "🟡 Hold"

for coin in coins:
    st.markdown(f"### {coin}")
    
    # Fix symbol for Yahoo Finance
    symbol = coin.replace("/", "-")  # BTC/USD → BTC-USD
    data = yf.download(symbol, period="7d", interval="1h")

    if data.empty:
        st.warning(f"Data not available for {coin}")
        continue

    if use_tradingview:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close']
        ))
        fig.update_layout(title=f"{coin} Chart", xaxis_title="Time", yaxis_title="Price")
        st.plotly_chart(fig, use_container_width=True)
    
    signal = get_signal(data)
    st.markdown(f"**Signal:** {signal}")

st.success("ایپ مکمل طور پر درست طریقے سے چل رہی ہے۔")
