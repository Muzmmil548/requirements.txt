import streamlit as st import pandas as pd import yfinance as yf import numpy as np import plotly.graph_objs as go import ccxt import requests from datetime import datetime, timedelta

st.set_page_config(page_title="Urdu Trading Assistant", layout="wide")

st.markdown("<h1 style='text-align: center; color: green;'>اردو ٹریڈنگ اسسٹنٹ</h1>", unsafe_allow_html=True)

Sidebar Exchange Toggle

st.sidebar.header("ایکسچینج منتخب کریں") show_tradingview = st.sidebar.checkbox("TradingView چارٹ", value=True) show_exchange_chart = st.sidebar.checkbox("ایکسچینج چارٹ", value=False)

Sidebar Top Coin Selection

st.sidebar.header("کرپٹو سکّے") coin_option = st.sidebar.selectbox("سکہ منتخب کریں", ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "ADA/USDT"])

Sidebar Timeframe

st.sidebar.header("ٹائم فریم") timeframe = st.sidebar.selectbox("ٹائم فریم منتخب کریں", ["1m", "5m", "15m", "1h", "4h", "1d"])

Load Data Function

def load_data(symbol, interval): exchange = ccxt.binance() bars = exchange.fetch_ohlcv(symbol, timeframe=interval, limit=100) df = pd.DataFrame(bars, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume']) df['Time'] = pd.to_datetime(df['Time'], unit='ms') return df

Chart Rendering

def plot_chart(df): fig = go.Figure() fig.add_trace(go.Candlestick(x=df['Time'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Candlesticks')) fig.update_layout(title='Live Chart', xaxis_title='Time', yaxis_title='Price') st.plotly_chart(fig, use_container_width=True)

Display TradingView iframe

if show_tradingview: st.markdown(""" <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_8fe7c&symbol=BINANCE:{0}&interval=1&theme=light&style=1&locale=en&toolbar_bg=F1F3F6&enable_publishing=false&hide_top_toolbar=true&save_image=false&hide_legend=true&studies=[]" width="100%" height="500" frameborder="0"></iframe> """.format(coin_option.replace("/", "")), unsafe_allow_html=True)

Display Exchange Chart

if show_exchange_chart: try: df = load_data(coin_option, timeframe) plot_chart(df) except Exception as e: st.error(f"ڈیٹا لوڈ کرنے میں مسئلہ: {e}")

Footer

st.markdown("<hr><center>ڈیزائن: اردو ٹریڈنگ چیک لسٹ ایپ (2025)</center>", unsafe_allow_html=True)

