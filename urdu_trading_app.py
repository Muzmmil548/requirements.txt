Urdu Trading AI Assistant App with Pattern Detection and Traffic Signals

import streamlit as st import requests import pandas as pd import numpy as np import matplotlib.pyplot as plt import seaborn as sns from streamlit.components.v1 import html

===== Sidebar Exchange Toggles & Coin Selection =====

st.sidebar.title("Select Exchanges & Top Coins") exchanges = { "Binance": st.sidebar.checkbox("Binance", value=True), "Bybit": st.sidebar.checkbox("Bybit"), "CME": st.sidebar.checkbox("CME"), "Bitget": st.sidebar.checkbox("Bitget"), "KuCoin": st.sidebar.checkbox("KuCoin"), "MEXC": st.sidebar.checkbox("MEXC"), "OKX": st.sidebar.checkbox("OKX") }

coin_set = st.sidebar.radio("Top Coins", ["Top 10", "Top 50"])

====== Simulated Coin List (Use live CoinGecko or exchange data in real app) ======

coin_list = [f"Coin{i+1}" for i in range(10 if coin_set == "Top 10" else 50)]

====== Technical Indicators Calculation ======

def calculate_indicators(df): df['EMA'] = df['Close'].ewm(span=10).mean() delta = df['Close'].diff() gain = delta.where(delta > 0, 0) loss = -delta.where(delta < 0, 0) avg_gain = gain.rolling(14).mean() avg_loss = loss.rolling(14).mean() rs = avg_gain / avg_loss df['RSI'] = 100 - (100 / (1 + rs)) df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean() df['Signal'] = df['MACD'].ewm(span=9).mean() df['BB_upper'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std() df['BB_lower'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std() return df

====== AI Traffic Signal ======

def get_traffic_signal(rsi): if rsi > 70: return ("🔴", "Sell") elif rsi < 30: return ("🟢", "Buy") else: return ("🟡", "Hold")

====== Pattern Detector (simulated logic) ======

pattern_list = [ "Head & Shoulders", "Inverse Head & Shoulders", "Double Top", "Double Bottom", "Triple Top", "Triple Bottom", "Cup and Handle", "Ascending Triangle", "Descending Triangle", "Symmetrical Triangle", "Flag", "Pennant", "Rising Wedge", "Falling Wedge", "Bullish Rectangle", "Bearish Rectangle", "Broadening Formation", "Diamond Top/Bottom" ]

def detect_patterns(): # Simulated random detection return {pat: np.random.choice(["🟢", "❌"]) for pat in pattern_list}

====== Show Coin Cards with Signals and Patterns ======

st.title("AI Urdu Trading Dashboard") st.markdown("#### Coin Signal Summary")

for coin in coin_list: with st.expander(f"{coin} Analysis"): # Simulated Close Prices df = pd.DataFrame({'Close': np.random.normal(loc=30000, scale=500, size=100)}) df = calculate_indicators(df) rsi = df['RSI'].iloc[-1] signal_icon, signal_text = get_traffic_signal(rsi)

st.metric(label=f"RSI", value=f"{round(rsi, 2)}", delta=signal_text)
    st.markdown(f"**Signal:** {signal_icon} {signal_text}")

    st.markdown("---")
    st.markdown("**Detected Patterns**")
    detected = detect_patterns()

    cols = st.columns(3)
    for idx, (pat, icon) in enumerate(detected.items()):
        cols[idx % 3].markdown(f"{pat}: {icon}")

====== Notes ======

st.info("Note: Signals and pattern detections are simulated. For live data, integrate with exchange APIs or CoinGecko.")

