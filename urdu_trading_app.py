import streamlit as st
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit.components.v1 import html

# ========== Sidebar: Exchange Toggles ==========
st.sidebar.title("Select Exchanges")
exchanges = {
    "Binance": st.sidebar.checkbox("Binance", value=True),
    "Bybit": st.sidebar.checkbox("Bybit"),
    "CME": st.sidebar.checkbox("CME"),
    "Bitget": st.sidebar.checkbox("Bitget"),
    "KuCoin": st.sidebar.checkbox("KuCoin"),
    "MEXC": st.sidebar.checkbox("MEXC"),
    "OKX": st.sidebar.checkbox("OKX"),
}

# ========== Live TradingView Chart ==========
def show_tradingview_chart(symbol="BINANCE:BTCUSDT", interval="1"):
    tradingview_embed = f"""
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_widget
    &symbol={symbol}&interval={interval}&hidesidetoolbar=1&symboledit=1&saveimage=1
    &toolbarbg=f1f3f6&studies=[]&theme=dark&style=1&timezone=Etc/UTC
    &withdateranges=1&hideideas=1&hidelegend=0&allow_symbol_change=1
    &calendar=1&news=1&autosize=true"
    width="100%" height="600" frameborder="0" allowtransparency="true"
    scrolling="no" allowfullscreen>
    </iframe>
    """
    html(tradingview_embed, height=600)

# ========== Market Heatmap ==========
def show_heatmap():
    st.subheader("Market Heatmap")
    data = {
        'Coins': ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL'],
        'Change %': [1.2, -0.5, 2.4, -1.0, 3.1, 0.6]
    }
    df = pd.DataFrame(data)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(df[['Change %']].T, annot=True, fmt=".1f", cmap="RdYlGn",
                cbar=False, xticklabels=df['Coins'])
    st.pyplot(fig)

# ========== DOM Placeholder ==========
def show_dom():
    st.subheader("Depth of Market (DOM)")
    st.info("DOM data coming soon...")

# ========== Technical Indicators ==========
def calculate_indicators(df):
    df['EMA'] = df['Close'].ewm(span=10).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['Signal'] = df['MACD'].ewm(span=9).mean()
    df['BB_upper'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std()
    df['BB_lower'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std()
    df['VWAP'] = df['Close'].expanding().mean()
    return df

# ========== Traffic Signal ==========
def get_traffic_signal(rsi):
    if rsi > 70:
        return "Red"
    elif rsi < 30:
        return "Green"
    else:
        return "Yellow"

# ========== Main App ==========
st.title("Urdu Trading App - Pro Checklist")

# Live Chart
st.subheader("Live Chart")
if exchanges['Binance']:
    show_tradingview_chart("BINANCE:BTCUSDT", "1")
elif exchanges['Bybit']:
    show_tradingview_chart("BYBIT:BTCUSDT", "1")
elif exchanges['CME']:
    show_tradingview_chart("CME:ES1!", "15")
elif exchanges['Bitget']:
    show_tradingview_chart("BITGET:BTCUSDT", "1")
elif exchanges['KuCoin']:
    show_tradingview_chart("KUCOIN:BTCUSDT", "1")
elif exchanges['MEXC']:
    show_tradingview_chart("MEXC:BTCUSDT", "1")
elif exchanges['OKX']:
    show_tradingview_chart("OKX:BTCUSDT", "1")

# Heatmap
show_heatmap()

# DOM
show_dom()

# Indicators & Traffic Signal (Simulated Data)
st.subheader("Indicators & Signal")
data = {'Close': np.random.normal(loc=30000, scale=200, size=100)}
df = pd.DataFrame(data)
df = calculate_indicators(df)

rsi_value = df['RSI'].iloc[-1]
signal = get_traffic_signal(rsi_value)

st.metric(label="RSI", value=f"{rsi_value:.2f}")
if signal == "Green":
    st.markdown(f"<h2 style='color:green;'>Traffic Signal: {signal}</h2>", unsafe_allow_html=True)
elif signal == "Yellow":
    st.markdown(f"<h2 style='color:orange;'>Traffic Signal: {signal}</h2>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='color:red;'>Traffic Signal: {signal}</h2>", unsafe_allow_html=True)
