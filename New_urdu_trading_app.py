import streamlit as st import pandas as pd import yfinance as yf import numpy as np import plotly.graph_objs as go import ccxt import requests from datetime import datetime, timedelta

Title

st.set_page_config(layout="wide") st.title("Urdu Trading Assistant")

Sidebar: Exchange Selection

st.sidebar.header("Select Exchange") selected_exchange = st.sidebar.radio("Exchange:", ["Binance", "Bybit", "OKX", "MEXC", "Bitget", "KuCoin", "CME"])

Sidebar: Chart Source Toggle

chart_source = st.sidebar.radio("Chart Source:", ["TradingView", "Exchange"])

Sidebar: Top Coins

top_coins_option = st.sidebar.radio("Select Coins:", ["Top 10", "Top 50"])

Sample coin list (can be updated with live API later)

coin_list = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT", "ADA/USDT"] if top_coins_option == "Top 10" else ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT", "ADA/USDT", "DOT/USDT", "TRX/USDT", "MATIC/USDT", "LTC/USDT", "LINK/USDT", "SHIB/USDT", "AVAX/USDT", "UNI/USDT", "XLM/USDT"]

Function to generate a basic trading signal based on indicators

def generate_signal(df): if df is None or df.empty: return "No data" rsi = df['RSI'].iloc[-1] macd = df['MACD'].iloc[-1] signal = df['Signal'].iloc[-1] if rsi < 30 and macd > signal: return "Buy" elif rsi > 70 and macd < signal: return "Sell" else: return "Hold"

Function to fetch historical data and calculate indicators

def fetch_data(symbol): try: df = yf.download(symbol.replace("/", ""), period="7d", interval="1h") df['EMA'] = df['Close'].ewm(span=20).mean() df['SMA'] = df['Close'].rolling(window=20).mean() df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean())) df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean() df['Signal'] = df['MACD'].ewm(span=9).mean() return df except Exception as e: return pd.DataFrame()

Main Chart Display

st.subheader(f"Live Chart for {selected_exchange}") for symbol in coin_list: df = fetch_data(symbol) if not df.empty: signal = generate_signal(df) color = "green" if signal == "Buy" else "red" if signal == "Sell" else "yellow"

with st.expander(f"{symbol} | Signal: {signal}"):
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df.index,
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],
                                     name='Candles'))
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], line=dict(color='blue', width=1), name='EMA'))
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], line=dict(color='orange', width=1), name='SMA'))
        fig.update_layout(title=f"{symbol} Chart", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

TradingView iframe example

if chart_source == "TradingView": st.markdown(""" <iframe src="https://www.tradingview.com/widgetembed/?frameElementId=tradingview_xxxxx&symbol=BINANCE:BTCUSDT&interval=1&theme=dark&style=1&timezone=Etc/UTC" 
width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe> """, unsafe_allow_html=True)

Footer

st.markdown("---") st.markdown("Developed by ChatGPT for Urdu Professional Traders")

