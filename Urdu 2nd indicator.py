import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import plotly.graph_objs as go

# Page config
st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

# Auto-refresh every 10 sec
st_autorefresh(interval=10 * 1000, key="refresh")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators)")
st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance Futures/Spot کے Live ڈیٹا پر مبنی ہیں۔")

# Choose Spot or Futures
market_type = st.radio("📍 مارکیٹ منتخب کریں:", ["Spot", "Futures"], horizontal=True)

# Get Top 50 Symbols
@st.cache_data(ttl=600)
def get_top_50_symbols(market="Spot"):
    try:
        if market == "Spot":
            url = "https://data.binance.com/api/v3/ticker/24hr"
        else:
            url = "https://data.binance.com/fapi/v1/ticker/24hr"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.warning(f"⚠️ API Status Code: {response.status_code}")
            return []
        data = response.json()
        usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:50]]
    except Exception as e:
        st.error(f"⛔ Symbols لوڈ نہیں ہو سکے: {e}")
        return []

symbols = get_top_50_symbols(market_type)

if not symbols:
    st.stop()

# Select symbol
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols)

# Show TradingView Chart
with st.expander("📺 Live Indicator Chart"):
    chart_type = "BINANCE"
    st.components.v1.iframe(
        f"https://www.tradingview.com/chart/?symbol={chart_type}:{selected_symbol}",
        height=500, scrolling=True
    )

# Price
def get_price(symbol, market):
    if market == "Spot":
        url = f"https://data.binance.com/api/v3/ticker/price?symbol={symbol}"
    else:
        url = f"https://data.binance.com/fapi/v1/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()['price'])

# Order book
def get_order_book(symbol, market):
    if market == "Spot":
        url = f"https://data.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    else:
        url = f"https://data.binance.com/fapi/v1/depth?symbol={symbol}&limit=5"
    data = requests.get(url).json()
    bid_vol = sum([float(x[1]) for x in data['bids']])
    ask_vol = sum([float(x[1]) for x in data['asks']])
    return bid_vol, ask_vol

# Recent trades
def get_trades(symbol, market):
    if market == "Spot":
        url = f"https://data.binance.com/api/v3/trades?symbol={symbol}&limit=100"
    else:
        url = f"https://data.binance.com/fapi/v1/trades?symbol={symbol}&limit=100"
    trades = requests.get(url).json()
    buyers = sum(1 for t in trades if not t['isBuyerMaker'])
    sellers = sum(1 for t in trades if t['isBuyerMaker'])
    return buyers, sellers

# AI Signal logic
def ai_signal(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell (Short)"
    else:
        return "🟡 Wait"

# Run data
try:
    price = get_price(selected_symbol, market_type)
    bid_volume, ask_volume = get_order_book(selected_symbol, market_type)
    buyers, sellers = get_trades(selected_symbol, market_type)
    signal = ai_signal(bid_volume, ask_volume, buyers, sellers)
except:
    st.error("📡 Binance API سے ڈیٹا حاصل نہیں ہو سکا")
    st.stop()

# Show metrics
st.markdown("---")
st.subheader("📊 Real-Time Smart Money Metrics")

info = {
    "🟡 Price": f"${price:.2f}",
    "📥 Bid Volume": round(bid_volume, 2),
    "📤 Ask Volume": round(ask_volume, 2),
    "🟢 Buyers": buyers,
    "🔴 Sellers": sellers,
    "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers",
    "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2),
    "🤖 AI Signal": signal
}

for label, val in info.items():
    icon = "🔴" if "Sell" in str(val) else "🟢" if "Buy" in str(val) else "🟡"
    st.markdown(f"<div style='font-size:20px; background-color:#111; color:white; padding:8px; margin-bottom:5px;'> <b>{label}</b>: <span style='animation: blink 1s infinite'>{icon}</span> {val}</div>", unsafe_allow_html=True)

st.success("✅ ایپ مکمل طور پر فعال ہے: Live + Futures + AI Signals")
