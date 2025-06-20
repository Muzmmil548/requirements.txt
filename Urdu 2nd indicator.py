import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd

# --- Page Config ---
st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

# --- Auto Refresh Every 30 Seconds ---
st_autorefresh(interval=30 * 1000, key="refresh")

# --- App Header ---
st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators)")
st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

# --- Get Top 50 Binance Symbols ---
@st.cache_data(ttl=600)
def get_top_50_symbols():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            st.warning(f"⚠️ Binance API Status Code: {response.status_code}")
            return []
        data = response.json()
        usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:50]]
    except Exception as e:
        st.error(f"⛔ Error loading symbols: {e}")
        return []

symbols = get_top_50_symbols()
if not symbols:
    st.error("📡 Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔")
    st.stop()

# --- Coin Selector ---
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

# --- TradingView Chart Embed ---
with st.expander("📺 Live Indicator Chart (TradingView)"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/advanced-chart/?symbol=BINANCE:{selected_symbol}&interval=1",
        height=500,
        scrolling=True
    )

# --- Get Live Data Functions ---
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()['price'])

def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    data = requests.get(url).json()
    bid_vol = sum([float(x[1]) for x in data['bids']])
    ask_vol = sum([float(x[1]) for x in data['asks']])
    return bid_vol, ask_vol

def get_trades(symbol):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100"
    trades = requests.get(url).json()
    buyers = sum(1 for t in trades if not t['isBuyerMaker'])
    sellers = sum(1 for t in trades if t['isBuyerMaker'])
    return buyers, sellers

def ai_signal(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell"
    else:
        return "🟡 Wait"

# --- Get and Display Data ---
try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    signal = ai_signal(bid_volume, ask_volume, buyers, sellers)
except:
    st.error("📡 Binance API سے ڈیٹا حاصل نہیں ہو سکا")
    st.stop()

# --- Display Metrics ---
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
    st.markdown(
        f"<div style='font-size:20px; background-color:#111; color:white; padding:8px; margin-bottom:5px;'>"
        f"<b>{label}</b>: {val}</div>", unsafe_allow_html=True
    )

st.success("✅ سب کچھ Live اور کامیابی سے چل رہا ہے۔ AI سگنلز آ رہے ہیں۔")
