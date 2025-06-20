import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import time
import random

# ✅ Page config
st.set_page_config(page_title="📊 Urdu Scalping AI (No VPN)", layout="wide")

# ✅ Auto-refresh
st_autorefresh(interval=10 * 1000, key="refresh")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (CoinGecko Based)")
st.markdown("یہ ورژن VPN کے بغیر CoinGecko API پر مبنی ہے۔")

# ✅ Get Top 50 Coins (CoinGecko)
@st.cache_data(ttl=600)
def get_top_50_coins():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "volume_desc",
            "per_page": 50,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params)
        data = response.json()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame([])

coins_df = get_top_50_coins()

if coins_df.empty:
    st.error("📡 CoinGecko API سے ڈیٹا حاصل نہیں ہو سکا، دوبارہ کوشش کریں۔")
    st.stop()

# ✅ Coin Selector
selected = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", coins_df["symbol"].str.upper())

selected_row = coins_df[coins_df["symbol"].str.upper() == selected].iloc[0]

# ✅ Price Info
st.subheader(f"💰 {selected_row['name']} ({selected_row['symbol'].upper()})")
st.markdown(f"**Current Price:** ${selected_row['current_price']}")

# ✅ Fake Order Flow (for demo only)
bid_volume = random.randint(500, 3000)
ask_volume = random.randint(500, 3000)
buyers = random.randint(200, 1500)
sellers = random.randint(200, 1500)

# ✅ AI Signal
def ai_signal(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell (Short)"
    else:
        return "🟡 Wait"

signal = ai_signal(bid_volume, ask_volume, buyers, sellers)

# ✅ Display Info
info = {
    "📥 Bid Volume": bid_volume,
    "📤 Ask Volume": ask_volume,
    "🟢 Buyers": buyers,
    "🔴 Sellers": sellers,
    "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2),
    "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers",
    "🤖 AI Signal": signal
}

for label, val in info.items():
    blink = "blink" if "🟢" in label or "🔴" in label or "🟡" in label or "🤖" in label else ""
    st.markdown(f"""
        <div class="{blink}" style='font-size:20px; background:#111; color:white; padding:10px; margin-bottom:5px; border-left: 5px solid lime;'>
            <b>{label}</b>: {val}
        </div>
    """, unsafe_allow_html=True)

# ✅ Blinking CSS
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

st.success("✅ CoinGecko ورژن بغیر VPN کے کامیابی سے چل رہا ہے!")
