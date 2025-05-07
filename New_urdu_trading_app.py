Urdu Trading Assistant App with TradingView and Exchange Chart Toggle

import streamlit as st import pandas as pd import yfinance as yf import numpy as np import plotly.graph_objs as go import ccxt import requests from datetime import datetime, timedelta

st.set_page_config(layout="wide") st.title("Urdu Trading Assistant - Scalping Checklist App")

Sidebar toggle for chart type

chart_option = st.sidebar.radio("Select Chart Type:", ["TradingView Chart", "Exchange (Binance) Chart"])

Sidebar for coin selection

symbol = st.sidebar.selectbox("Select Coin:", ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]) symbol_yf = symbol.replace("/", "") + "-USD"

st.markdown("---")

if chart_option == "TradingView Chart": st.subheader(f"Live TradingView Chart - {symbol}") tradingview_symbol = symbol.replace("/USDT", "USDT").upper() tradingview_widget = f""" <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_3a0fc&symbol=BINANCE%3A{tradingview_symbol}&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Etc%2FUTC&withdateranges=1&hidevolume=0&hideideas=1&studies_overrides=%7B%7D&overrides=%7B%7D&enabled_features=[]&disabled_features=[]&locale=en&utm_source=localhost&utm_medium=widget_new&utm_campaign=chart&utm_term=BINANCE%3ABTCUSDT" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe> """ st.components.v1.html(tradingview_widget, height=500)

elif chart_option == "Exchange (Binance) Chart": st.subheader(f"Live Binance Chart (1m candles) - {symbol}") exchange = ccxt.binance() bars = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100) df = pd.DataFrame(bars, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume']) df['Time'] = pd.to_datetime(df['Time'], unit='ms')

fig = go.Figure(data=[go.Candlestick(x=df['Time'],
            open=df['Open'], high=df['High'],
            low=df['Low'], close=df['Close'])])
fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---") st.success("Chart loaded successfully! Choose other options from the sidebar to explore more.")

