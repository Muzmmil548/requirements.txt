import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.graph_objs as go
import ccxt
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Urdu Trading Assistant", layout="wide")

st.title("Urdu Trading Assistant App")

# Sidebar toggles
st.sidebar.header("Chart Options")
chart_option = st.sidebar.radio("Select Chart Type", ("TradingView Chart", "Exchange Live Chart"))

st.sidebar.header("Exchange Options")
selected_exchange = st.sidebar.selectbox("Select Exchange", ["Binance", "Bybit", "CME", "Bitget", "KuCoin", "MEXC", "OKX"])

# Coin selection
st.sidebar.header("Coin Selection")
symbol = st.sidebar.text_input("Enter Symbol (e.g., BTC/USDT)", "BTC/USDT")
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])

# --- Chart Display Section --- #
st.subheader(f"Chart View: {chart_option}")

if chart_option == "TradingView Chart":
    symbol_tv = symbol.replace("/", "")
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/single-quote/?symbol=BINANCE:{symbol_tv}&interval=1",
        height=600, scrolling=True)
else:
    try:
        exchange = ccxt.binance()
        bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=100)
        df = pd.DataFrame(bars, columns=["Time", "Open", "High", "Low", "Close", "Volume"])
        df["Time"] = pd.to_datetime(df["Time"], unit="ms")

        fig = go.Figure(data=[go.Candlestick(
            x=df["Time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])
        fig.update_layout(title=f"{symbol} Candlestick Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error loading chart: {e}")
