import streamlit as st import pandas as pd import numpy as np import requests import seaborn as sns import matplotlib.pyplot as plt from streamlit.components.v1 import html from binance.client import Client from binance.exceptions import BinanceAPIException

========== Sidebar ==========

st.sidebar.title("Settings")

Exchange Toggles\st.sidebar.subheader("Select Exchanges")

exchanges = { "Binance": st.sidebar.checkbox("Binance", value=True), "Bybit": st.sidebar.checkbox("Bybit"), "CME": st.sidebar.checkbox("CME"), "Bitget": st.sidebar.checkbox("Bitget"), "KuCoin": st.sidebar.checkbox("KuCoin"), "MEXC": st.sidebar.checkbox("MEXC"), "OKX": st.sidebar.checkbox("OKX"), }

Trading & API Settings

st.sidebar.subheader("Trading Settings (Binance)") enable_trading = st.sidebar.checkbox("Enable Binance Trading", value=False) binance_api_key = st.sidebar.text_input("Binance API Key", type="password") binance_api_secret = st.sidebar.text_input("Binance API Secret", type="password")

Coin Selection

st.sidebar.subheader("Top Coin Selection") top_n = st.sidebar.selectbox("Select Top N Coins:", [10, 50], index=0)

Timeframe

st.sidebar.subheader("Chart Timeframe") timeframe = st.sidebar.selectbox("Chart Interval", ["1m","5m","15m","1h","4h","1d","1w","1M"], index=0)

Initialize Binance Client

if enable_trading and binance_api_key and binance_api_secret: client = Client(binance_api_key, binance_api_secret) else: client = None

========== Functions ==========

def show_tradingview_chart(symbol, interval): embed = f""" <iframe src="https://s.tradingview.com/widgetembed/?symbol={symbol}&interval={interval}&theme=dark" 
width="100%" height="400" frameborder="0"></iframe> """ html(embed, height=420)

def show_heatmap(): st.subheader("Market Heatmap (Top 20)") data = requests.get("https://api.binance.com/api/v3/ticker/24hr").json() df = pd.DataFrame(data) df = df[df['symbol'].str.endswith('USDT')] df['pct'] = df['priceChangePercent'].astype(float) top = df.nlargest(20, 'pct') fig, ax = plt.subplots(figsize=(8,3)) sns.heatmap(top[['pct']].T, annot=True, fmt=".1f", cmap="RdYlGn", cbar=False, xticklabels=top['symbol'], ax=ax) ax.set_ylabel('Change %') st.pyplot(fig)

def show_dom_placeholder(): st.subheader("Depth of Market (DOM)") st.info("Live DOM integration coming soon...")

def fetch_binance_ohlcv(symbol, interval): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100" data = requests.get(url).json() df = pd.DataFrame(data, columns=['_time','open','high','low','close','volume',*range(6)]) df.index = pd.to_datetime(df['time'], unit='ms') df['Close'] = df['close'].astype(float) return df[['Close']]

def calculate_indicators(df): df['EMA'] = df['Close'].ewm(span=10).mean() delta = df['Close'].diff() gain = delta.where(delta>0, 0) loss = -delta.where(delta<0, 0) avg_gain = gain.rolling(14).mean() avg_loss = loss.rolling(14).mean() rs = avg_gain/avg_loss df['RSI'] = 100 - (100/(1+rs)) df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean() df['Signal'] = df['MACD'].ewm(span=9).mean() df['BB_upper'] = df['Close'].rolling(20).mean()+2df['Close'].rolling(20).std() df['BB_lower'] = df['Close'].rolling(20).mean()-2df['Close'].rolling(20).std() df['VWAP'] = (df['Close']*df['Close']).cumsum()/df['Close'].cumsum() return df

def get_signal(rsi): if rsi<30: return '🟢 Buy' elif rsi>70: return '🔴 Sell' else: return '🟡 Hold'

def execute_order(symbol, side, quantity): if not client: st.error("Trading disabled or API not configured.") return try: order = client.create_order(symbol=symbol, side=side, type='MARKET', quantity=quantity) st.success(f"Order executed: {order}") except BinanceAPIException as e: st.error(f"Order failed: {e}")

========== Main Layout ==========

st.title("Urdu Trading App - Pro Checklist")

1) Live Chart

st.header("1. Live Chart & Signals") if exchanges['Binance'] and client: symbol='BTCUSDT' show_tradingview_chart(f"BINANCE:{symbol}", timeframe) df_ohlc = fetch_binance_ohlcv(symbol, timeframe) df_ind = calculate_indicators(df_ohlc) rsi_val = df_ind['RSI'].iloc[-1] signal = get_signal(rsi_val) st.metric(label='RSI', value=f"{rsi_val:.2f}") st.markdown(f"## {signal}") # Order buttons col1, col2 = st.columns(2) with col1: if st.button('Buy Market'): execute_order(symbol, 'BUY', quantity=0.001) with col2: if st.button('Sell Market'): execute_order(symbol, 'SELL', quantity=0.001) else: show_tradingview_chart('BINANCE:BTCUSDT', timeframe) if exchanges['Binance'] else None

2) Heatmap

st.header("2. Market Heatmap") show_heatmap()

3) DOM

st.header("3. Depth of Market") show_dom_placeholder()

4) Top N AI Signals

st.header("4. Top Coins Signals (AI)") top_limit = top_n url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={top_limit}&page=1" coins = requests.get(url).json() for coin in coins: name, sym = coin['name'], coin['symbol'].upper() chg = coin['price_change_percentage_24h'] sig = '🟢 Buy' if chg<-1 else '🔴 Sell' if chg>1 else '🟡 Hold' st.write(f"{name} ({sym}): {chg:.2f}% → {sig}")

End of app code

