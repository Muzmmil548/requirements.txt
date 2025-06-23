import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import hmac
import hashlib
import time

# ✅ Config
st.set_page_config(page_title="📈 Urdu Scalping AI (Binance + API Key)", layout="wide")
st_autorefresh(interval=30 * 1000, key="refresh")
st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Binance API Key Version)")
st.markdown("AI سگنل اور انسٹی ٹیوشنل ڈیٹیکشن Binance Live API Key پر مبنی ہے۔")

# ✅ Binance API Key & Secret
API_KEY = st.secrets["BINANCE"]["api_key"]
API_SECRET = st.secrets["BINANCE"]["api_secret"]

headers = {
    "X-MBX-APIKEY": API_KEY
}

# ✅ Top 50 Coins
@st.cache_data(ttl=600)
def get_top_50_symbols():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url, headers=headers)
    data = response.json()
    usdt_pairs = [d for d in data if d['symbol'].endswith("USDT") and not d['symbol'].endswith("BUSD")]
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
    return [pair['symbol'] for pair in sorted_pairs[:50]]

symbols = get_top_50_symbols()
if not symbols:
    st.error("📡 Binance API Key سے Symbols لوڈ نہیں ہو سکے!")
    st.stop()

selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

# ✅ TradingView Chart
with st.expander("📺 TradingView Indicator Chart"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}&interval=1&theme=dark&style=1&locale=en",
        height=500, scrolling=True
    )

# ✅ Live Data Fetch (Price, Orderbook, Trades)
def get_live_metrics(symbol):
    price = float(requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()["price"])
    orderbook = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5").json()
    trades = requests.get(f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100").json()

    bid_volume = sum(float(b[1]) for b in orderbook['bids'])
    ask_volume = sum(float(a[1]) for a in orderbook['asks'])
    buyers = sum(1 for t in trades if not t['isBuyerMaker'])
    sellers = sum(1 for t in trades if t['isBuyerMaker'])

    effort = round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"

    # ✅ Institutional Logic
    inst_buying = "High" if bid_volume > ask_volume * 1.8 else "Moderate" if bid_volume > ask_volume * 1.2 else "Low"
    inst_selling = "High" if ask_volume > bid_volume * 1.8 else "Moderate" if ask_volume > bid_volume * 1.2 else "Low"
    demand = "Yes" if bid_volume > ask_volume * 1.3 else "No"
    supply = "Yes" if ask_volume > bid_volume * 1.3 else "No"

    # ✅ AI Signal
    if dominancy == "Buyers" and effort < 10:
        signal = "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        signal = "🔴 Sell (Short)"
    else:
        signal = "🟡 Wait"

    return {
        "Price": f"${price:.2f}",
        "Bid Volume": round(bid_volume, 2),
        "Ask Volume": round(ask_volume, 2),
        "Buyers": buyers,
        "Sellers": sellers,
        "Effort %": effort,
        "Dominancy": dominancy,
        "Institutional Buying": inst_buying,
        "Institutional Selling": inst_selling,
        "Demand Zone": demand,
        "Supply Zone": supply,
        "🤖 AI Signal": signal
    }

# ✅ Show Metrics
try:
    data = get_live_metrics(selected_symbol)
    st.subheader("📊 AI Metrics + Detection")
    for k, v in data.items():
        blink = "blink" if "Signal" in k or "🟢" in v or "🔴" in v or "🟡" in v else ""
        st.markdown(f"""
        <div class="{blink}" style='font-size:20px; background-color:#111; color:white; padding:10px; margin-bottom:5px;'>
        <b>{k}</b>: {v}
        </div>
        """, unsafe_allow_html=True)
except:
    st.error("❌ Binance API Key سے ڈیٹا حاصل نہ ہو سکا")

# ✅ Blinking CSS
st.markdown("""
<style>
@keyframes blink {
  0% {opacity: 1;}
  50% {opacity: 0.3;}
  100% {opacity: 1;}
}
.blink {
  animation: blink 1s infinite;
}
</style>
""", unsafe_allow_html=True)

st.success("✅ Binance API Key Version کامیابی سے چل رہا ہے!")
