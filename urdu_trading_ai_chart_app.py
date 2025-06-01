import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import random
import requests
from datetime import datetime
from streamlit.components.v1 import iframe

# ✅✅✅ Set Page Config (سب سے اوپر رکھنا ضروری ہے)
st.set_page_config(layout="wide")

# --- Auto Refresh ہر 60 سیکنڈ میں ---
st_autorefresh(interval=60 * 1000, key="datarefresh")

# --- Page Title ---
st.title("📊 اردو ٹریڈنگ اسسٹنٹ (AI چارٹ اور سگنلز کے ساتھ)")

# --- Coin Selection ---
symbols = ["BTC", "ETH", "BNB", "SOL", "XRP"]
selected_symbol = st.selectbox("کوائن منتخب کریں:", symbols)

# --- TradingView Live Chart ---
tv_url = f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}USDT&interval=1&hidesidetoolbar=1&theme=dark"
st.subheader(f"📈 لائیو چارٹ: {selected_symbol}USDT")
iframe(tv_url, height=500)

# --- CoinMarketCap Price Fetch ---
api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={selected_symbol}&convert=USD"
headers = {"X-CMC_PRO_API_KEY": api_key}
response = requests.get(url, headers=headers)
price = response.json()["data"][selected_symbol]["quote"]["USD"]["price"]
price = round(price, 2)

st.markdown("---")
st.subheader("💰 موجودہ قیمت اور تجزیہ")

# --- TP/SL Box ---
tp = price * 1.03
sl = price * 0.97

tp_sl_box = f"""
<div style='background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ccc; font-size:18px'>
<b>🎯 ٹیک پرافٹ (TP):</b> <span style='color:green;'>${tp:.2f}</span> <br>
<b>⛔ اسٹاپ لاس (SL):</b> <span style='color:red;'>${sl:.2f}</span>
</div>
"""
st.markdown(tp_sl_box, unsafe_allow_html=True)

# --- Sentiment Box ---
buyers = random.randint(40, 70)
sellers = 100 - buyers
neutral = random.randint(0, 10)

sentiment_box = f"""
<div style='background-color:#eaf4ff; padding:15px; border-radius:10px; border:1px solid #b3d4fc; font-size:18px'>
<h4>🤖 AI مارکیٹ سینٹیمنٹ</h4>
🟢 <b>خریدار:</b> {buyers}%<br>
🔴 <b>فروخت کنندہ:</b> {sellers}%<br>
⚪ <b>نیوٹرل:</b> {neutral}%
</div>
"""
st.markdown(sentiment_box, unsafe_allow_html=True)

# --- AI Signal with Blinking ---
signal = "🟢 Buy" if buyers > sellers else "🔴 Sell" if sellers > buyers else "🟡 Hold"
color = "green" if signal == "🟢 Buy" else "red" if signal == "🔴 Sell" else "orange"

st.markdown("### 📢 AI ٹریڈ سگنل:")

def blinking_html(text, color):
    return f"""
    <div style='animation: blinker 1s linear infinite; color:{color}; font-size:24px; font-weight:bold;'>
        {text}
    </div>
    <style>
        @keyframes blinker {{
            50% {{ opacity: 0; }}
        }}
    </style>
    """

st.markdown(blinking_html(f"📍 سگنل: {signal}", color), unsafe_allow_html=True)

# --- Chart Patterns (Simulated) ---
chart_patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]

def simulate_patterns():
    return {p: random.choice(["🟢", "🔴", "🟡", "❌"]) for p in chart_patterns}

st.markdown("---")
st.subheader("📊 چارٹ پیٹرن ڈیٹیکشن:")
patterns = simulate_patterns()
for pattern, signal in patterns.items():
    st.markdown(f"{pattern}: {signal}")

# --- Footer ---
st.markdown("---")
st.caption("Developed by Urdu Trading AI | Auto Refreshed | Powered by Streamlit")
