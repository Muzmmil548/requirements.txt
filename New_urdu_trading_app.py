import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objs as go

# Title
st.set_page_config(layout="wide")
st.title("AI-Based Urdu Trading Assistant (Top 10/50 Coins, Live Signals, Chart Patterns)")

# Sidebar: User options
st.sidebar.header("Settings")
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC-USD, ETH-USD):", value="BTC-USD")
top_selection = st.sidebar.selectbox("Top Coins to Scan:", ["Top 10", "Top 50"])
timeframe = st.sidebar.selectbox("Select Timeframe:", ["1d", "1h", "15m", "5m", "1m"])
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))

# Load data
@st.cache_data(ttl=3600)
def get_data(symbol, start):
    df = yf.download(symbol, start=start)
    return df

df = get_data(symbol, start_date)

if df.empty:
    st.warning("No data found. Please check the symbol.")
    st.stop()

# EMA and RSI
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["EMA50"] = df["Close"].ewm(span=50).mean()
delta = df["Close"].diff()
gain = (delta.where(delta > 0, 0)).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
df["RSI"] = 100 - (100 / (1 + rs))

# Signal logic
latest_rsi = df["RSI"].iloc[-1]
if latest_rsi > 70:
    signal = "Sell"
    color = "🔴"
elif latest_rsi < 30:
    signal = "Buy"
    color = "🟢"
else:
    signal = "Wait"
    color = "🟡"

# Chart
st.subheader(f"{symbol} Price Chart with EMA & RSI")

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name='Candlesticks'))

fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color='blue', width=1), name="EMA20"))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], line=dict(color='orange', width=1), name="EMA50"))

fig.update_layout(xaxis_rangeslider_visible=False, height=600)

st.plotly_chart(fig, use_container_width=True)

# RSI & Traffic Signal
st.subheader("Indicators & Signal")
st.metric("RSI", f"{latest_rsi:.2f}")
st.write(f"**Traffic Signal**: {color} **{signal}** (based on RSI)")

# Chart Pattern Detection Section
st.subheader("Chart Pattern Detection (Coming Soon)")
pattern_placeholders = [
    "1. Head & Shoulders",
    "2. Inverse Head & Shoulders",
    "3. Triangle",
    "4. Double Top",
    "5. Double Bottom",
    "6. Flag / Pennant",
    "7. Rising Wedge",
    "8. Falling Wedge"
]

for pattern in pattern_placeholders:
    st.write(f"{pattern} — [🟢 Detected] or [🔴 Not Detected] (AI logic coming soon)")
