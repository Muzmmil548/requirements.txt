import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import ccxt
import requests
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.title("اردو اسکیلپنگ چیک لسٹ ایپ | Urdu Trading Assistant")

# Sidebar navigation
menu = st.sidebar.radio("اپشن منتخب کریں", (
    "Live Chart", "Top 10 Coins", "Top 50 Coins",
    "Chart Patterns", "Buy/Sell Signals", "Exchange Toggle"
))

# Load data function
@st.cache_data
def load_data(symbol, period='1d', interval='5m'):
    data = yf.download(symbol, period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

# Live Chart section
if menu == "Live Chart":
    st.subheader("لائیو چارٹ")
    symbol = st.text_input("سکہ کا سمبل درج کریں (جیسے BTC-USD)", "BTC-USD")
    df = load_data(symbol)
    fig = go.Figure(data=[go.Candlestick(
        x=df['Datetime'],
        open=df['Open'], high=df['High'],
        low=df['Low'], close=df['Close']
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# Top 10 Coins with AI Signals
elif menu == "Top 10 Coins":
    st.subheader("ٹاپ 10 سکے - AI سگنلز")
    top10 = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
             "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "MATIC/USDT"]
    st.write("AI سگنلز: 🟢 Buy | 🟡 Hold | 🔴 Sell")
    for coin in top10:
        signal = np.random.choice(["🟢 Buy", "🟡 Hold", "🔴 Sell"])
        st.write(f"{coin}: {signal}")

# Top 50 Coins (Mock)
elif menu == "Top 50 Coins":
    st.subheader("ٹاپ 50 سکے (ڈیمو موڈ)")
    for i in range(1, 51):
        st.write(f"Coin {i}: 🟢 Buy")

# Chart Patterns Section
elif menu == "Chart Patterns":
    st.subheader("چارٹ پیٹرن تجزیہ")
    st.write("Head & Shoulders, Double Top/Bottom, Triangle, etc.")
    for pattern in ["Head & Shoulders", "Double Bottom", "Ascending Triangle"]:
        detected = np.random.choice([True, False])
        if detected:
            st.success(f"{pattern} پیٹرن ملا 🟢")
        else:
            st.warning(f"{pattern} پیٹرن نہیں ملا")

# Buy/Sell Signals (demo)
elif menu == "Buy/Sell Signals":
    st.subheader("خرید و فروخت کے سگنلز")
    coin = st.selectbox("سکہ منتخب کریں", ["BTC/USDT", "ETH/USDT"])
    signal = np.random.choice(["🟢 Strong Buy", "🟡 Neutral", "🔴 Strong Sell"])
    st.metric(label=f"{coin} سگنل", value=signal)

# Exchange Toggle
elif menu == "Exchange Toggle":
    st.subheader("ایکسچینج سیلیکٹر")
    exchanges = ["Binance", "Bybit", "CME", "Bitget", "KuCoin", "MEXC", "OKX"]
    active = []
    for ex in exchanges:
        toggle = st.checkbox(f"{ex}", value=True)
        if toggle:
            active.append(ex)
    st.success(f"چالو ایکسچینجز: {', '.join(active)}")
