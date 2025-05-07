import streamlit as st import pandas as pd import yfinance as yf import numpy as np import plotly.graph_objs as go

--- App Title ---

st.set_page_config(page_title="Urdu Trading AI Assistant", layout="wide") st.title("Urdu Trading AI Assistant with Pattern Detection and Signals")

--- Sidebar Coin Selection ---

option = st.sidebar.selectbox("Select Coin Group:", ("Top 10", "Top 50"))

if option == "Top 10": coins = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "TRX-USD"] elif option == "Top 50": coins = ["BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD", "ADA-USD", "DOGE-USD", "AVAX-USD", "DOT-USD", "TRX-USD", "MATIC-USD", "LINK-USD", "LTC-USD", "SHIB-USD", "ATOM-USD", "ETC-USD", "XMR-USD", "XLM-USD", "FIL-USD", "ICP-USD"]

selected_coin = st.sidebar.selectbox("Select Coin:", coins) data = yf.download(selected_coin, period="7d", interval="1h")

--- Indicators Calculation ---

def calculate_indicators(df): df['RSI'] = compute_rsi(df['Close'], 14) df['EMA20'] = df['Close'].ewm(span=20).mean() df['EMA50'] = df['Close'].ewm(span=50).mean() return df

def compute_rsi(series, period=14): delta = series.diff() gain = (delta.where(delta > 0, 0)).rolling(window=period).mean() loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean() rs = gain / loss return 100 - (100 / (1 + rs))

data = calculate_indicators(data)

--- Signal Logic ---

def signal_logic(rsi): if rsi < 30: return ("Buy", "🟢") elif rsi > 70: return ("Sell", "🔴") else: return ("Wait", "🟡")

last_rsi = data['RSI'].iloc[-1] signal, color = signal_logic(last_rsi)

--- Live Chart ---

st.subheader(f"Live Chart: {selected_coin}") fig = go.Figure() fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Candlesticks')) fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='blue', width=1), name='EMA20')) fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], line=dict(color='orange', width=1), name='EMA50')) fig.update_layout(xaxis_rangeslider_visible=False, height=500) st.plotly_chart(fig, use_container_width=True)

--- Signal Display ---

st.markdown(f"### Signal: {signal} {color}") st.markdown(f"RSI: {last_rsi:.2f}")

--- Pattern Detection (Mocked for Now) ---

pattern_dict = { "Head & Shoulders": "🟢", "Triangle": "🟢", "Double Top/Bottom": "🟢", "Flag/Pennant": "🟢", "Cup and Handle": "🟢", "Ascending Triangle": "🟢", "Descending Triangle": "🟢", "Symmetrical Triangle": "🟢", "Rising Wedge": "🟢", "Falling Wedge": "🟢", "Bullish Rectangle": "🟢", "Bearish Rectangle": "🟢", "Double Top": "🟢", "Double Bottom": "🟢", "Triple Top": "🟢", "Triple Bottom": "🟢", "Inverse Head & Shoulders": "🟢", "Broadening Formation": "🟢", "Diamond Top/Bottom": "🟢" }

st.markdown("### Detected Patterns") for pattern, symbol in pattern_dict.items(): st.markdown(f"- {pattern} {symbol}")

--- Binance Future Feature Placeholder ---

st.sidebar.markdown("---") st.sidebar.markdown("[Future Option] Connect Binance for Live Trade & Order Placement") st.sidebar.markdown("This will require your API Key and Secret in a secure place.")

