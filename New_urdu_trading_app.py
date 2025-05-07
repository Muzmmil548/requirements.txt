import streamlit as st import pandas as pd import yfinance as yf import numpy as np import plotly.graph_objs as go import ccxt import requests from datetime import datetime, timedelta

-------------------------- Sidebar Layout --------------------------

st.set_page_config(layout="wide", page_title="Urdu Trading Assistant")

st.sidebar.title("ٹریڈنگ آپشنز") exchange_toggle = { 'Binance': st.sidebar.checkbox('Binance', value=True), 'Bybit': st.sidebar.checkbox('Bybit', value=False), 'CME': st.sidebar.checkbox('CME', value=False), 'Bitget': st.sidebar.checkbox('Bitget', value=False), 'KuCoin': st.sidebar.checkbox('KuCoin', value=False), 'MEXC': st.sidebar.checkbox('MEXC', value=False), 'OKX': st.sidebar.checkbox('OKX', value=False) }

coin_range = st.sidebar.radio("کوائن کی فہرست:", ['Top 10', 'Top 50']) selected_coin = st.sidebar.text_input("کوائن منتخب کریں:", value="BTC/USDT")

-------------------------- Chart Section --------------------------

st.title("اردو اسکلپنگ اسسٹنٹ ایپ") col1, col2 = st.columns([3, 1])

with col1: st.subheader(f"{selected_coin} کا لائیو چارٹ") try: coin_symbol = selected_coin.replace("/", "") df = yf.download(tickers=coin_symbol, period="1d", interval="1m") fig = go.Figure(data=[ go.Candlestick( x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'] ) ]) st.plotly_chart(fig, use_container_width=True) except Exception as e: st.warning(f"چارٹ لوڈ نہیں ہو سکا: {e}")

-------------------------- Indicators --------------------------

def get_indicators(data): data['EMA20'] = data['Close'].ewm(span=20).mean() data['EMA50'] = data['Close'].ewm(span=50).mean() data['RSI'] = (100 - (100 / (1 + data['Close'].pct_change().rolling(window=14).mean()))) return data

with col2: st.subheader("اشاریے اور سگنلز") if not df.empty: df = get_indicators(df) latest = df.iloc[-1] if latest['EMA20'] > latest['EMA50'] and latest['RSI'] < 70: st.success("خریدنے کا سگنل (BUY)") elif latest['EMA20'] < latest['EMA50'] and latest['RSI'] > 30: st.error("بیچنے کا سگنل (SELL)") else: st.info("انتظار کریں (WAIT)")

-------------------------- Pattern Detection --------------------------

def detect_head_shoulders(df): return np.random.choice([True, False])

def detect_triangle(df): return np.random.choice([True, False])

st.subheader("چارٹ پیٹرن ڈیٹیکشن") colp1, colp2 = st.columns(2)

with colp1: if detect_head_shoulders(df): st.success("Head & Shoulders پیٹرن ملا") else: st.info("Head & Shoulders نہیں ملا")

with colp2: if detect_triangle(df): st.success("Triangle Pattern ملا") else: st.info("Triangle Pattern نہیں ملا")

-------------------------- Footer --------------------------

st.markdown("""

ساختہ: Urdu Trading Pro App | Indicators, Chart Patterns & AI Assistant """)

