import streamlit as st
st.set_page_config(page_title="📊 Urdu Scalping Binance Live", layout="wide")

from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd

# 🔁 Auto-refresh every 30 seconds
st_autorefresh(interval=30 * 1000, key="refresh")

# 📢 Title and description
st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Top 50 Binance Coins)")
st.markdown("تمام indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

# 🔎 Get top 50 coins from Binance (cached for 1 hour)
@st.cache_data(ttl=3600)
def get_top_50_symbols():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        data = requests.get(url, timeout=10).json()
        symbols = sorted(
            [d['symbol'] for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')],
            key=lambda x: -float(next(d for d in data if d['symbol'] == x)['quoteVolume'])
        )
        return symbols[:50]
    except:
        return ["BTCUSDT"]

symbols = get_top_50_symbols()
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols)

# 📺 TradingView Chart Embed
with st.expander("📺 Live TradingView Chart", expanded=True):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/single-quote/?symbol=BINANCE:{selected_symbol}&locale=en",
        height=260,
        scrolling=False
    )

# 📡 Live Binance data
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response['price'])

def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    response = requests.get(url).json()
    bid_vol = sum([float(bid[1]) for bid in response['bids']])
    ask_vol = sum([float(ask[1]) for ask in response['asks']])
    return bid_vol, ask_vol

def get_trades(symbol):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=50"
    response = requests.get(url).json()
    buyers = sum(1 for trade in response if not trade['isBuyerMaker'])
    sellers = sum(1 for trade in response if trade['isBuyerMaker'])
    return buyers, sellers

def calculate_effort(bid, ask):
    return round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)

# ✅ Collect Live Data
try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    effort = calculate_effort(bid_volume, ask_volume)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    demand_zone = "Yes" if bid_volume > ask_volume * 1.2 else "No"
    supply_zone = "Yes" if ask_volume > bid_volume * 1.2 else "No"
except:
    price = bid_volume = ask_volume = buyers = sellers = effort = "N/A"
    dominancy = demand_zone = supply_zone = "Error"

# 📊 Show Data
data = {
    "Price": price,
    "Bid Volume": bid_volume,
    "Ask Volume": ask_volume,
    "Buyers": buyers,
    "Sellers": sellers,
    "Effort %": effort,
    "Dominancy": dominancy,
    "Demand Zone": demand_zone,
    "Supply Zone": supply_zone
}

for label, value in data.items():
    color = "white"
    if label == "Price" and isinstance(value, (int, float)): color = "green"
    elif label in ["Bid Volume", "Buyers"] and isinstance(value, (int, float)) and value > 1000: color = "green"
    elif label in ["Ask Volume", "Sellers"] and isinstance(value, (int, float)) and value > 1000: color = "red"
    elif label == "Effort %" and isinstance(value, (int, float)) and value > 10: color = "orange"
    elif label == "Dominancy": color = "green" if value == "Buyers" else "red"
    elif label == "Demand Zone": color = "green" if value == "Yes" else "gray"
    elif label == "Supply Zone": color = "red" if value == "Yes" else "gray"

    st.markdown(f"""
        <div style='font-size:18px; background-color:#222; color:{color}; padding:10px; margin-bottom:5px; border-radius:10px;'>
        <b>{label}</b>: {value}</div>
    """, unsafe_allow_html=True)

st.success("✅ یہ Live Binance Urdu Scalping Assistant ہے۔ اگلا فیچر: AI Signal + Pattern Detection")
