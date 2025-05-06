Trading AI Assistant (Signals & Data Only)

import streamlit as st import pandas as pd import numpy as np import requests import seaborn as sns import matplotlib.pyplot as plt from streamlit.components.v1 import html

----------------- Page Config -----------------

st.set_page_config(page_title="Trading AI Assistant", layout="wide")

----------------- Sidebar Settings -----------------

st.sidebar.title("Settings & Data")

Top coins selection

top_group = st.sidebar.radio("Top Coins Group", ["Top 10", "Top 50"])

Chart timeframe

timeframe = st.sidebar.selectbox("Chart Interval", ["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"], index=2)

----------------- Helper Functions -----------------

def show_tradingview(symbol, interval): """Embed a TradingView chart via iframe.""" embed = f""" <iframe src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={interval}&theme=dark"
width="100%" height="400" frameborder="0"></iframe> """ html(embed, height=420)

Fetch OHLCV data from Binance public API

def fetch_ohlcv(symbol, interval, limit=100): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}" data = requests.get(url).json() df = pd.DataFrame(data, columns=[ 'OpenTime','Open','High','Low','Close','Volume','CloseTime', 'QuoteAssetVolume','NumTrades','TakerBuyBase','TakerBuyQuote','Ignore' ]) df['Close'] = df['Close'].astype(float) df.index = pd.to_datetime(df['OpenTime'], unit='ms') return df[['Close']]

Calculate indicators (EMA, RSI, MACD, SignalLine)

def calculate_indicators(df): df['EMA'] = df['Close'].ewm(span=10).mean() delta = df['Close'].diff() gain = delta.where(delta > 0, 0) loss = -delta.where(delta < 0, 0) avg_gain = gain.rolling(14).mean() avg_loss = loss.rolling(14).mean() rs = avg_gain / avg_loss df['RSI'] = 100 - (100 / (1 + rs)) df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean() df['SignalLine'] = df['MACD'].ewm(span=9).mean() return df

Generate traffic signal based on RSI

def traffic_signal(rsi): if rsi < 30: return '🟢 Buy' elif rsi > 70: return '🔴 Sell' else: return '🟡 Hold'

Simulated chart patterns

patterns = [ "Head & Shoulders", "Inverse Head & Shoulders", "Triangle", "Double Top", "Double Bottom", "Triple Top", "Triple Bottom", "Ascending Triangle", "Descending Triangle", "Symmetrical Triangle", "Cup and Handle", "Rising Wedge", "Falling Wedge", "Bullish Rectangle", "Bearish Rectangle", "Broadening Formation", "Diamond Top/Bottom" ]

Random detection for demo

def detect_patterns(): return {p: np.random.choice(['🟢','🟡','🔴']) for p in patterns}

Simple AI signal for Top coins section

def ai_signal(change_pct): if change_pct > 5: return '🟢 Buy' elif change_pct < -5: return '🔴 Sell' else: return '🟡 Hold'

----------------- Main App -----------------

st.title("Trading AI Assistant - Signals & Data Only")

1) Live Chart & Indicators for a selected symbol

st.header("1. Live Chart & Indicators") symbol = st.selectbox("Select Symbol (Binance):", ['BTCUSDT','ETHUSDT','BNBUSDT']) show_tradingview(f"BINANCE:{symbol}", timeframe) df = fetch_ohlcv(symbol, timeframe) df_ind = calculate_indicators(df) latest = df_ind.iloc[-1] st.metric(label="RSI", value=f"{latest['RSI']:.2f}") st.write(f"Signal: {traffic_signal(latest['RSI'])}")

2) Market Heatmap

st.header("2. Market Heatmap") heat_data = requests.get("https://api.binance.com/api/v3/ticker/24hr").json() heat_df = pd.DataFrame(heat_data) heat_df = heat_df[heat_df['symbol'].str.endswith('USDT')] heat_df['change'] = heat_df['priceChangePercent'].astype(float) top_heat = heat_df.nlargest(20, 'change') fig, ax = plt.subplots(figsize=(10,2)) sns.heatmap(top_heat[['change']].T, annot=True, fmt='.1f', cmap='RdYlGn', cbar=False, xticklabels=top_heat['symbol'], ax=ax) st.pyplot(fig)

3) Depth of Market (DOM) Placeholder

st.header("3. Depth of Market (DOM)") st.info("Live DOM integration coming soon...")

4) AI Assist: Top Coins Signals & Patterns

st.header("4. AI Assist: Top Coins Signals & Patterns") limit = 10 if top_group == 'Top 10' else 50 url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1" coins = requests.get(url).json() for coin in coins: sym = coin['symbol'].upper() change = coin.get('price_change_percentage_24h') or 0 sig = ai_signal(change) with st.expander(f"{sym} → {sig}"): st.write(f"24h Change: {change:.2f}%") patterns_detected = detect_patterns() cols = st.columns(3) for i, (pat, icon) in enumerate(patterns_detected.items()): cols[i % 3].write(f"{pat}: {icon}")

