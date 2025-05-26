import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit.components.v1 import iframe

# CoinMarketCap API Configuration
API_KEY = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {"X-CMC_PRO_API_KEY": API_KEY}

# TradingView Chart Embed Function
def show_tradingview_chart(symbol):
    base = "https://s.tradingview.com/widgetembed/?frameElementId=tradingview_x&symbol="
    url = f"{base}{symbol}&interval=15&hidesidetoolbar=1&symboledit=1&saveimage=1"
    st.markdown(f'<iframe src="{url}" width="100%" height="400"></iframe>', unsafe_allow_html=True)

# Fetch CoinMarketCap data
@st.cache_data(ttl=600)
def fetch_market_data():
    try:
        response = requests.get(CMC_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()["data"]
            return pd.DataFrame([{
                "name": item["name"],
                "symbol": item["symbol"],
                "price": item["quote"]["USD"]["price"],
                "change_24h": item["quote"]["USD"]["percent_change_24h"]
            } for item in data])
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# Chart Pattern Detection Mock
def get_pattern_status(symbol):
    import random
    patterns = [
        "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
        "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
        "Falling Wedge", "Rising Wedge", "Cup & Handle",
        "Bullish Flag", "Bearish Flag", "Rectangle",
        "Triple Top", "Triple Bottom"
    ]
    return {p: random.choice(["🟢", "🟡"]) for p in patterns}

# Urdu Summary Generator (AI-style Mock)
def generate_summary(name, price, change):
    if change > 0:
        mood = "مارکیٹ مثبت رجحان میں ہے"
    elif change < 0:
        mood = "مارکیٹ منفی رجحان میں ہے"
    else:
        mood = "مارکیٹ مستحکم ہے"
    return f"کرپٹو کوائن {name} کی موجودہ قیمت {round(price, 2)} ڈالر ہے۔ {mood}۔"

# App UI
st.title("اردو اسکیلپنگ ٹریڈنگ اسسٹنٹ")
st.markdown("### کرپٹو کوائن منتخب کریں:")

data = fetch_market_data()
if not data.empty:
    selected_coin = st.selectbox("کوائن منتخب کریں", data["symbol"])
    coin_row = data[data["symbol"] == selected_coin].iloc[0]

    # TradingView Chart
    st.markdown("### لائیو چارٹ")
    show_tradingview_chart(selected_coin + "USD")

    # Summary
    st.markdown("### خلاصہ")
    st.info(generate_summary(coin_row['name'], coin_row['price'], coin_row['change_24h']))

    # Signal
    st.markdown("### سگنل")
    change = coin_row['change_24h']
    if change > 2:
        st.success("🟢 خریدنے کا اشارہ")
    elif change < -2:
        st.error("🔴 فروخت کا اشارہ")
    else:
        st.warning("🟡 انتظار کریں")

    # Chart Patterns with blinking emoji
    st.markdown("### چارٹ پیٹرنز کی شناخت:")
    pattern_status = get_pattern_status(selected_coin)
    for pattern, status in pattern_status.items():
        st.markdown(f"<span style='animation: blinker 1s linear infinite;'>{status}</span> {pattern}", unsafe_allow_html=True)

    st.markdown('''
        <style>
        @keyframes blinker {
            50% { opacity: 0; }
        }
        </style>
    ''', unsafe_allow_html=True)

else:
    st.error("ڈیٹا حاصل نہیں ہو سکا۔ برائے مہربانی دوبارہ کوشش کریں۔")
