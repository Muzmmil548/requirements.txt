import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import numpy as np
from datetime import datetime

# ---- CONFIG ----
st.set_page_config(page_title="AI Trading Assistant", layout="wide")

# ---- CSS ----
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
        color: white;
    }
    .green-light {
        height: 20px;
        width: 20px;
        background-color: #00FF00;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 15px #00FF00;
    }
    .red-light {
        height: 20px;
        width: 20px;
        background-color: #FF0000;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 15px #FF0000;
    }
    .gray-light {
        height: 20px;
        width: 20px;
        background-color: #2e2e2e;
        border-radius: 50%;
        display: inline-block;
        box-shadow: none;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----
st.sidebar.markdown("## 📊 نیویگیشن")
st.sidebar.button("Live")
st.sidebar.button("Chart")
st.sidebar.button("Top 50")
st.sidebar.button("AI Signals")
st.sidebar.selectbox("Select Coin List", ["TOP 10", "TOP 50"])

# ---- Live Chart ----
st.markdown("# 📈 Live Chart")
components.html("""
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_f2d0d&symbol=BINANCE:BTCUSDT&interval=1&theme=dark&style=1&locale=en&toolbarbg=rgba(0, 0, 0, 1)&hide_side_toolbar=false&allow_symbol_change=true&details=true&studies=[]" 
        width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", height=500)

# ---- Fetch Binance Kline Data ----
def fetch_candles(symbol="BTCUSDT", interval="1m", limit=200):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data, columns=[
        "Open Time", "Open", "High", "Low", "Close", "Volume",
        "Close Time", "Quote Asset Volume", "Number of Trades",
        "Taker buy base", "Taker buy quote", "Ignore"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Volume"] = pd.to_numeric(df["Volume"])
    return df

data = fetch_candles()

# ---- Indicator Functions ----
def rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    return ema12 - ema26

def ema(df, period=20):
    return df['Close'].ewm(span=period, adjust=False).mean()

def bollinger_bands(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)
    return upper, lower

def vwap(df):
    return (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()

# ---- Signal Logic ----
def signal_status(df):
    status = {}
    df['RSI'] = rsi(df)
    df['MACD'] = macd(df)
    df['EMA20'] = ema(df, 20)
    df['Upper'], df['Lower'] = bollinger_bands(df)
    df['VWAP'] = vwap(df)

    last = df.iloc[-1]

    status['RSI'] = last['RSI'] < 30  # Buy if oversold
    status['MACD'] = last['MACD'] > 0  # Buy if MACD positive
    status['EMA'] = last['Close'] > last['EMA20']
    status['Bollinger'] = last['Close'] < last['Lower']
    status['Volume'] = last['Volume'] > df['Volume'].mean()
    status['VWAP'] = last['Close'] > last['VWAP']

    return status

indicators = signal_status(data)

# ---- Indicators UI ----
st.markdown("## 📌 6 Indicators (Live Signals)")
cols = st.columns(3)
for i, (name, signal) in enumerate(indicators.items()):
    col = cols[i % 3]
    light = '<span class="green-light"></span>' if signal else '<span class="red-light"></span>'
    with col:
        st.markdown(f"{light} {name}", unsafe_allow_html=True)

# ---- Dummy Pattern Detection ----
def detect_pattern(df):
    last_close = df["Close"].iloc[-1]
    return {
        "Head & Shoulders": last_close % 2 < 1,
        "Inverse Head & Shoulders": last_close % 3 < 1,
        "Double Top": last_close % 5 < 2,
        "Double Bottom": last_close % 4 < 1,
        "Ascending Triangle": last_close % 6 < 3,
        "Descending Triangle": last_close % 7 < 2,
        "Symmetrical Triangle": last_close % 8 < 4,
        "Bullish Flag": last_close % 3 == 0,
        "Bearish Flag": last_close % 2 == 0,
        "Pennant": last_close % 4 == 0,
        "Rising Wedge": last_close % 5 == 0,
        "Falling Wedge": last_close % 6 == 0,
        "Cup and Handle": last_close % 7 == 0,
        "Rounding Bottom": last_close % 8 == 0,
        "Rectangle (Range)": last_close % 9 == 0,
    }

pattern_status = detect_pattern(data)

# ---- Chart Pattern UI ----
st.markdown("## 🧠 Chart Patterns (Live Detected)")
cols3 = st.columns(3)
for i, (pattern, is_on) in enumerate(pattern_status.items()):
    col = cols3[i % 3]
    light = '<span class="green-light"></span>' if is_on else '<span class="gray-light"></span>'
    with col:
        st.markdown(f"{light} {pattern}", unsafe_allow_html=True)
