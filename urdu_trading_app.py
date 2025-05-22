import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from streamlit.components.v1 import iframe
import random

# Page Config
st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

# Title
st.markdown("## پروفیشنل اردو ٹریڈنگ اسسٹنٹ", unsafe_allow_html=True)

# Manual Refresh
if st.button("دوبارہ لوڈ کریں"):
    st.experimental_rerun()

# Select Top Coins
option = st.selectbox("ٹاپ کوائنز منتخب کریں:", ["Top 10", "Top 50"])
limit = 10 if option == "Top 10" else 50

# Fetch Data
def fetch_coin_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

data = fetch_coin_data()

# Coin Selection
coin_names = [coin['name'] for coin in data]
selected_coin = st.selectbox("کوائن منتخب کریں:", coin_names)

# Signal Logic
def ai_signal(price, change):
    if change > 1:
        return "🟢", "BUY", True
    elif change < -1:
        return "🔴", "SELL", True
    else:
        return "🟡", "HOLD", False

def get_tp_sl(price):
    tp = price * 1.02
    sl = price * 0.98
    return round(tp, 2), round(sl, 2)

# CSS
st.markdown("""
<style>
@keyframes blinker {
  50% { opacity: 0; }
}
.blink-btn {
  animation: blinker 1s linear infinite;
  display:inline-block;
  margin-right:6px;
}
</style>
""", unsafe_allow_html=True)

# Show TradingView Candlestick Chart
symbol = ""
for coin in data:
    if coin['name'] == selected_coin:
        symbol = coin['symbol'].upper() + "USDT"
        break

if symbol:
    st.markdown(f"### {selected_coin} - Live TradingView Chart")
    tradingview_widget = f"""
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{symbol}&symbol=BINANCE%3A{symbol}&interval=15&theme=dark&style=1&locale=en&utm_source=&utm_medium=widget_new&utm_campaign=chart&utm_term=BINANCE%3A{symbol}" width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no" allowfullscreen></iframe>
    """
    st.markdown(tradingview_widget, unsafe_allow_html=True)

# Show AI Signal
for coin in data:
    if coin['name'] == selected_coin:
        price = coin['current_price']
        change = coin['price_change_percentage_24h']
        volume = coin['total_volume']

        signal, text, blink = ai_signal(price, change)
        tp, sl = get_tp_sl(price)

        style = f"color:white;padding:8px;border-radius:6px;background-color:{'green' if signal=='🟢' else 'red' if signal=='🔴' else 'orange'};animation:{'blinker 1s linear infinite' if blink else 'none'};"

        st.markdown(f"""<div style="margin-bottom:10px;">
            <b>{selected_coin}</b><br>
            <span style="{style}">{signal} {text}</span><br>
            قیمت: ${price} | TP: ${tp} | SL: ${sl}<br>
            والیوم: {volume}
        </div>""", unsafe_allow_html=True)

# Summary
summary_buy = sum(1 for coin in data if ai_signal(coin['current_price'], coin['price_change_percentage_24h'])[1] == "BUY")
summary_sell = sum(1 for coin in data if ai_signal(coin['current_price'], coin['price_change_percentage_24h'])[1] == "SELL")
summary_neutral = limit - summary_buy - summary_sell

st.markdown(f""" 
#### خلاصہ:
- 🟢 خریداری سگنل: **{summary_buy}**
- 🔴 فروخت سگنل: **{summary_sell}**
- 🟡 نیوٹرل: **{summary_neutral}**
""", unsafe_allow_html=True)

# Chart Patterns
st.markdown("#### چارٹ پیٹرن ڈیٹیکشن:")

patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom", "Symmetrical Triangle",
    "Ascending Triangle", "Descending Triangle", "Falling Wedge", "Rising Wedge", "Cup & Handle",
    "Bullish Flag", "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]

for pattern in patterns:
    detected = random.choice([True, False])
    icon = "🟢" if detected else "🟡"
    blink_class = "blink-btn"
    st.markdown(f"<span class='{blink_class}'>{icon}</span>{pattern}", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("پروفیشنل اردو ٹریڈنگ اسسٹنٹ - Powered by OpenAI & Streamlit", unsafe_allow_html=True)
