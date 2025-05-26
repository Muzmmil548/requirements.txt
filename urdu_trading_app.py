import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit.components.v1 import iframe
import random

st.set_page_config(layout="wide")
st.title("اردو ٹریڈنگ اسسٹنٹ ایپ (AI سسٹم کے ساتھ)")

# CoinMarketCap API
api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
headers = {"X-CMC_PRO_API_KEY": api_key}
cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Fetch market data
def get_market_data(limit=50):
    params = {"start": "1", "limit": limit, "convert": "USD"}
    response = requests.get(cmc_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["data"]
        return pd.DataFrame([{
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Price": coin["quote"]["USD"]["price"],
            "Change(24h)": coin["quote"]["USD"]["percent_change_24h"]
        } for coin in data])
    else:
        return pd.DataFrame()

# Chart pattern AI detection (Simulated)
patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]

def detect_patterns():
    return {p: random.choice(["🟢", "🟡"]) for p in patterns}

# Simulated Buyer/Seller Ratio
def buyer_seller_ratio():
    buyers = random.randint(45, 95)
    sellers = 100 - buyers
    return buyers, sellers

# Blinking icon
def blinking_icon(icon):
    return f"<span style='animation: blink 1s infinite;'>{icon}</span>"

# CSS for blinking effect
st.markdown("""
<style>
@keyframes blink {
0% {opacity: 1;}
50% {opacity: 0.1;}
100% {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# Auto Refresh Button
refresh = st.button("ڈیٹا دوبارہ لوڈ کریں (Auto Refresh)")
if refresh or "df" not in st.session_state:
    st.session_state.df = get_market_data(50)

# Layout
col1, col2 = st.columns([1, 2])
with col1:
    df = st.session_state.df
    selected = st.selectbox("کوائن منتخب کریں:", df["Name"] if not df.empty else [])
    if selected:
        coin_info = df[df["Name"] == selected].iloc[0]
        symbol = coin_info["Symbol"]
        price = coin_info["Price"]
        change = coin_info["Change(24h)"]

with col2:
    if selected:
        st.subheader(f"{selected} کا لائیو چارٹ:")
        iframe(f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{symbol}USDT&interval=15&hidesidetoolbar=1", height=420)

# Summary & AI Info
if selected:
    st.markdown("---")
    st.subheader("خلاصہ:")
    st.markdown(f"- موجودہ قیمت: ${price:.4f}")
    st.markdown(f"- 24 گھنٹے تبدیلی: {change:.2f}%")

    tp = price * 1.03
    sl = price * 0.97
    st.success(f"TP (ٹیک پرافٹ): ${tp:.2f}  |  SL (اسٹاپ لاس): ${sl:.2f}")

    # AI Section: Buyer/Seller
    with st.container():
        st.subheader("AI مارکیٹ سینٹیمنٹ (Buyer/Seller Ratio):")
        buyers, sellers = buyer_seller_ratio()
        st.info(f"خریدار (Buyers): {buyers}%  |  فروخت کنندہ (Sellers): {sellers}%")

    # AI Section: Chart Patterns
    with st.container():
        st.markdown("---")
        st.subheader("AI چارٹ پیٹرن ڈیٹیکشن:")
        detected = detect_patterns()
        for name, icon in detected.items():
            st.markdown(f"**{name}**: {blinking_icon(icon)}", unsafe_allow_html=True)
