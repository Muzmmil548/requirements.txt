import streamlit as st
import requests
import pandas as pd
import random
from streamlit.components.v1 import iframe

# --- Page Setup ---
st.set_page_config(layout="wide")
st.title("اردو AI ٹریڈنگ اسسٹنٹ (لائیو چارٹ، سگنلز، پیٹرن)")

# --- User Inputs ---
symbols = ["BTC", "ETH", "BNB", "SOL", "XRP"]
symbol = st.selectbox("کوائن منتخب کریں:", symbols)

# --- Timeframe for TradingView ---
timeframes = {"1H": "60", "4H": "240", "1D": "D"}
selected_tf_label = st.selectbox("ٹائم فریم منتخب کریں:", list(timeframes.keys()))
selected_tf = timeframes[selected_tf_label]

# --- TradingView Live Chart ---
chart_url = f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{symbol}USDT&interval={selected_tf}&hidesidetoolbar=1&theme=dark"
st.subheader(f"📊 لائیو چارٹ - {symbol} /USDT")
iframe(chart_url, height=500)

# --- Fetch Live Price from CoinMarketCap ---
api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}&convert=USD"
headers = {"X-CMC_PRO_API_KEY": api_key}

response = requests.get(url, headers=headers)
data = response.json()
price = data["data"][symbol]["quote"]["USD"]["price"]

st.markdown("---")
st.subheader("💰 موجودہ قیمت اور تجزیہ")
st.success(f"💲 {symbol} قیمت: ${price:.2f}")

# --- TP & SL Calculation ---
tp = price * 1.03
sl = price * 0.97
st.info(f"📈 TP (ٹیک پرافٹ): ${tp:.2f} | 📉 SL (اسٹاپ لاس): ${sl:.2f}")

# --- Sentiment Simulation ---
buyers = random.randint(40, 60)
sellers = 100 - buyers
neutral = random.randint(0, 10)
st.markdown("---")
st.subheader("📊 مارکیٹ سینٹیمنٹ:")
st.info(f"🟢 خریدار: {buyers}% | 🔴 فروخت کنندہ: {sellers}% | ⚪ نیوٹرل: {neutral}%")

# --- Indicator Signals ---
st.markdown("---")
st.subheader("📍 AI سگنلز (انڈیکیٹر بیسڈ)")
indicators = {
    "RSI": random.choice(["Buy", "Sell", "Neutral"]),
    "MACD": random.choice(["Buy", "Sell", "Neutral"]),
    "Bollinger Bands": random.choice(["Buy", "Sell", "Neutral"]),
    "Moving Avg (50)": random.choice(["Buy", "Sell", "Neutral"]),
    "Moving Avg (200)": random.choice(["Buy", "Sell", "Neutral"]),
    "Stochastic": random.choice(["Buy", "Sell", "Neutral"])
}

for name, signal in indicators.items():
    color = "🟢" if signal == "Buy" else "🔴" if signal == "Sell" else "🟡"
    st.markdown(f"**{name}**: {color} {signal}")

# --- Overall Signal Light Bulb (Blinking emoji simulation) ---
st.markdown("---")
st.subheader("🔔 حتمی سگنل:")

signal_values = list(indicators.values())
if signal_values.count("Buy") >= 4:
    st.markdown("### 🟢 **Buy Signal!**")
elif signal_values.count("Sell") >= 4:
    st.markdown("### 🔴 **Sell Signal!**")
else:
    st.markdown("### 🟡 **Neutral / Wait**")

# --- Chart Pattern Detection (Simulated) ---
st.markdown("---")
st.subheader("📐 چارٹ پیٹرن ڈیٹیکشن (AI Simulation)")
chart_patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]
for pattern in chart_patterns:
    status = random.choice(["🟢", "🔴", "🟡", "❌"])
    st.markdown(f"**{pattern}**: {status}")

# --- الگورتھم کی وضاحت ---
with st.expander("📘 الگورتھم کیسے کام کرتا ہے؟"):
    st.markdown("""
- AI indicators 6 مختلف انڈیکیٹرز (RSI, MACD, etc) سے سگنل لیتے ہیں۔
- ہر انڈیکیٹر کو ایک Vote دیا جاتا ہے: Buy, Sell یا Neutral۔
- اگر Buy votes ≥ 4 ہوں → حتمی سگنل 🟢 Buy
- اگر Sell votes ≥ 4 ہوں → حتمی سگنل 🔴 Sell
- ورنہ → 🟡 Neutral
- چارٹ پیٹرنز کو الگ simulate کیا جاتا ہے اور دستی تحقیق میں مدد دیتے ہیں۔
""")

# --- Footer ---
st.markdown("---")
st.caption("📊 Developed by Urdu Trading AI Team | Powered by CoinMarketCap, TradingView & Streamlit")
