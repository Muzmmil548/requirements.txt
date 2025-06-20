import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import time

# ✅ Page config (یہ سب سے اوپر ہونا ضروری ہے)
st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

# ✅ Auto-refresh ہر 10 سیکنڈ میں
st_autorefresh(interval=10 * 1000, key="refresh")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators)")
st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

# ✅ Retry Logic
def safe_request(url, retries=3, delay=2):
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            time.sleep(delay)
    return None

# ✅ Top 50 Binance Symbols
@st.cache_data(ttl=600)
def get_top_50_symbols():
    data = safe_request("https://api.binance.com/api/v3/ticker/24hr")
    if not data:
        return []
    usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')]
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
    return [pair['symbol'] for pair in sorted_pairs[:50]]

symbols = get_top_50_symbols()

if not symbols:
    st.error("📡 Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔")
    st.stop()

# ✅ Select coin
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols)

# ✅ TradingView Indicator Chart (Better version)
with st.expander("📺 Indicator چارٹ - TradingView"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:{selected_symbol}&locale=en&dateRange=1D&colorTheme=dark&trendLineColor=rgba(0, 255, 0, 1)&underLineColor=rgba(0, 255, 0, 0.1)",
        height=400, scrolling=False
    )

# ✅ Live Data Functions
def get_price(symbol):
    data = safe_request(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    return float(data['price']) if data else None

def get_order_book(symbol):
    data = safe_request(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5")
    if not data:
        return 0, 0
    bid_vol = sum(float(x[1]) for x in data['bids'])
    ask_vol = sum(float(x[1]) for x in data['asks'])
    return bid_vol, ask_vol

def get_trades(symbol):
    data = safe_request(f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100")
    if not data:
        return 0, 0
    buyers = sum(1 for t in data if not t['isBuyerMaker'])
    sellers = sum(1 for t in data if t['isBuyerMaker'])
    return buyers, sellers

# ✅ AI Signal Logic
def ai_signal_logic(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell (Short)"
    else:
        return "🟡 Wait"

# ✅ Fetch Live Data
price = get_price(selected_symbol)
bid_volume, ask_volume = get_order_book(selected_symbol)
buyers, sellers = get_trades(selected_symbol)
signal = ai_signal_logic(bid_volume, ask_volume, buyers, sellers)

# ✅ Show Results
st.markdown("---")
st.subheader("📊 Live Market Metrics + AI Signal")

data = {
    "💰 Price": f"${price:.2f}" if price else "N/A",
    "📥 Bid Volume": round(bid_volume, 2),
    "📤 Ask Volume": round(ask_volume, 2),
    "🟢 Buyers": buyers,
    "🔴 Sellers": sellers,
    "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2),
    "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers",
    "🤖 AI Signal": signal
}

for label, val in data.items():
    blink = "blink" if "🟢" in label or "🔴" in label or "🟡" in label or "🤖" in label else ""
    st.markdown(f"""
        <div class="{blink}" style='font-size:20px; background:#111; color:white; padding:10px; margin-bottom:5px; border-left: 5px solid lime;'>
            <b>{label}</b>: {val}
        </div>
    """, unsafe_allow_html=True)

# ✅ CSS for Blinking
st.markdown("""
<style>
@keyframes blink {
  0% {opacity: 1;}
  50% {opacity: 0.2;}
  100% {opacity: 1;}
}
.blink {
  animation: blink 1.5s infinite;
}
</style>
""", unsafe_allow_html=True)

st.success("✅ App مکمل طور پر Live چل رہا ہے (VPN کے ساتھ Binance API)")
