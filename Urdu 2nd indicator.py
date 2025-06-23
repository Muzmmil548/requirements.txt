import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd

# ✅ Page Config (یہ سب سے اوپر ہونا ضروری ہے)
st.set_page_config(page_title="📈 Urdu Scalping AI (Binance)", layout="wide")

# ✅ Auto-refresh (ہر 30 سیکنڈ میں)
st_autorefresh(interval=30 * 1000, key="refresh")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Binance Live + AI)")
st.markdown("تمام indicators Binance Live API اور AI سسٹم پر مبنی ہیں۔")

# ✅ Get Top 50 Symbols from Binance
@st.cache_data(ttl=600)
def get_top_50_symbols():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            st.error(f"⚠️ Binance API Status Code: {response.status_code}")
            return []

        data = response.json()
        usdt_pairs = [
            d for d in data 
            if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')
        ]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:50]]
    except Exception as e:
        st.error(f"❌ Binance API Error: {e}")
        return []

symbols = get_top_50_symbols()
if not symbols:
    st.stop()

# ✅ Coin Selector
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

# ✅ TradingView Chart Embed
with st.expander("📺 Live Indicator Chart (TradingView)"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}&interval=1&theme=dark&style=1&locale=en",
        height=500, scrolling=True
    )

# ✅ Live Data Collection
def get_live_data(symbol):
    try:
        price_data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
        order_book = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5").json()
        trades = requests.get(f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100").json()

        price = float(price_data['price'])
        bid_volume = sum([float(x[1]) for x in order_book['bids']])
        ask_volume = sum([float(x[1]) for x in order_book['asks']])
        buyers = sum(1 for t in trades if not t['isBuyerMaker'])
        sellers = sum(1 for t in trades if t['isBuyerMaker'])

        effort = round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2)
        dominancy = "Buyers" if buyers > sellers else "Sellers"

        # ✅ Institutional Volume Logic
        inst_buy = "High" if bid_volume > ask_volume * 1.8 else "Medium" if bid_volume > ask_volume * 1.2 else "Low"
        inst_sell = "High" if ask_volume > bid_volume * 1.8 else "Medium" if ask_volume > bid_volume * 1.2 else "Low"

        demand = "Yes" if bid_volume > ask_volume * 1.3 else "No"
        supply = "Yes" if ask_volume > bid_volume * 1.3 else "No"

        # ✅ AI Signal Logic
        if dominancy == "Buyers" and effort < 10:
            signal = "🟢 Buy (Long)"
        elif dominancy == "Sellers" and effort < 10:
            signal = "🔴 Sell (Short)"
        else:
            signal = "🟡 Wait"

        return {
            "💰 Price": f"${price:.2f}",
            "📥 Bid Volume": round(bid_volume, 2),
            "📤 Ask Volume": round(ask_volume, 2),
            "🟢 Buyers": buyers,
            "🔴 Sellers": sellers,
            "⚖️ Effort %": effort,
            "🎯 Dominancy": dominancy,
            "🏦 Inst. Buying": inst_buy,
            "🏦 Inst. Selling": inst_sell,
            "📈 Demand Zone": demand,
            "📉 Supply Zone": supply,
            "🤖 AI Signal": signal
        }
    except Exception as e:
        st.error(f"❌ Live data fetch error: {e}")
        return {}

# ✅ Show Live AI Data
live_data = get_live_data(selected_symbol)
if live_data:
    st.subheader("📊 Live AI Metrics + Institutional Logic")
    for label, val in live_data.items():
        blink = "blink" if any(x in val for x in ["🟢", "🟡", "🔴"]) else ""
        st.markdown(f"""
            <div class="{blink}" style='font-size:20px; background-color:#111; color:white; padding:10px; margin-bottom:5px; border-left: 5px solid lime;'>
                <b>{label}</b>: {val}
            </div>
        """, unsafe_allow_html=True)

# ✅ Blinking Animation Style
st.markdown("""
<style>
@keyframes blink {
  0% {opacity: 1;}
  50% {opacity: 0.2;}
  100% {opacity: 1;}
}
.blink {
  animation: blink 1.2s infinite;
}
</style>
""", unsafe_allow_html=True)

st.success("✅ Binance لائیو ورژن کامیابی سے چل رہا ہے، تمام فیچرز ایکٹیو ہیں۔")
