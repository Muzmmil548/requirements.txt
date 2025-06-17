import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import plotly.graph_objs as go
import datetime

st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")
st_autorefresh(interval=10000, key="refresh")  # ہر 10 سیکنڈ میں ریفریش

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators)")
st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

@st.cache_data(ttl=600)
def get_top_50_symbols():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)
        data = response.json()
        usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:50]]
    except:
        return []

symbols = get_top_50_symbols()
if not symbols:
    st.error("📡 Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔")
    st.stop()

selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols)

# TradingView چارٹ
with st.expander("📺 TradingView چارٹ"):
    st.components.v1.iframe(
        f"https://www.tradingview.com/chart/?symbol=BINANCE:{selected_symbol}",
        height=500, scrolling=True
    )

# Binance APIs
def get_price(symbol):
    return float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()['price'])

def get_order_book(symbol):
    data = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5").json()
    bid_vol = sum(float(x[1]) for x in data['bids'])
    ask_vol = sum(float(x[1]) for x in data['asks'])
    return bid_vol, ask_vol

def get_trades(symbol):
    trades = requests.get(f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100").json()
    buyers = sum(1 for t in trades if not t['isBuyerMaker'])
    sellers = sum(1 for t in trades if t['isBuyerMaker'])
    return buyers, sellers

def ai_signal(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell (Short)"
    else:
        return "🟡 Wait"

try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    signal = ai_signal(bid_volume, ask_volume, buyers, sellers)
except:
    st.error("📡 Binance API سے ڈیٹا حاصل نہیں ہو سکا")
    st.stop()

# Display Real-Time Info
st.subheader("📊 Real-Time Smart Money Metrics")
col1, col2 = st.columns(2)

with col1:
    st.metric("📈 Live Price", f"${price:.2f}")
    st.metric("📥 Bid Volume", round(bid_volume, 2))
    st.metric("🟢 Buyers", buyers)

with col2:
    st.metric("📤 Ask Volume", round(ask_volume, 2))
    st.metric("🔴 Sellers", sellers)
    st.metric("🤖 AI Signal", signal)

# Demand/Supply Zone Plot
with st.expander("📊 Demand & Supply Zone Chart"):
    df = pd.DataFrame(requests.get(
        f"https://api.binance.com/api/v3/klines?symbol={selected_symbol}&interval=1m&limit=100"
    ).json(), columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume', '', '', '', '', '', ''])

    df['Time'] = pd.to_datetime(df['Time'], unit='ms')
    df['Close'] = df['Close'].astype(float)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Time'], y=df['Close'], mode='lines+markers', name='Price'))
    fig.update_layout(title=f"{selected_symbol} Demand & Supply Zones", xaxis_title="Time", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)
