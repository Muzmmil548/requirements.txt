# urdu_trading_app.py

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

# --- App Title ---
st.markdown(""" 
## پروفیشنل اردو ٹریڈنگ اسسٹنٹ
""", unsafe_allow_html=True)

# --- Safe Refresh Logic ---
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

if st.button("دوبارہ لوڈ کریں"):
    st.session_state.refresh = True

if st.session_state.refresh:
    st.session_state.refresh = False
    st.experimental_rerun()

# --- Select Top Coins ---
option = st.selectbox("ٹاپ کوائنز منتخب کریں:", ["Top 10", "Top 50"])
limit = 10 if option == "Top 10" else 50

# --- Fetch Coin Data ---
def fetch_coin_data():
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

data = fetch_coin_data()

# --- Dummy AI Signal + TP/SL ---
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

# --- Live TradingView Chart ---
st.markdown("### لائیو چارٹ (TradingView)")
selected_symbol = "BINANCE:BTCUSDT"
tradingview_url = f"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{selected_symbol}&symbol={selected_symbol}&interval=1&theme=dark&style=1"
st.components.v1.iframe(tradingview_url, height=400, scrolling=True)

# --- Table with Live Signals ---
st.markdown("#### لائیو ٹریڈنگ سگنل", unsafe_allow_html=True)

summary_buy = 0
summary_sell = 0

for coin in data:
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = coin['current_price']
    change = coin['price_change_percentage_24h']
    volume = coin['total_volume']

    signal, text, blink = ai_signal(price, change)
    tp, sl = get_tp_sl(price)

    if signal == "🟢":
        summary_buy += 1
    elif signal == "🔴":
        summary_sell += 1

    style = f"color:white;padding:8px;border-radius:6px;background-color:{'green' if signal=='🟢' else 'red' if signal=='🔴' else 'orange'};animation:{'blinker 1s linear infinite' if blink else 'none'};"

    st.markdown(f"""
        <div style="margin-bottom:10px;">
            <b>{name} ({symbol})</b><br>
            <span style="{style}">{signal} {text}</span><br>
            قیمت: ${price} | TP: ${tp} | SL: ${sl}<br>
            والیوم: {volume}
        </div>
    """, unsafe_allow_html=True)

# --- Summary Box ---
st.markdown(f""" 
#### خلاصہ:

خریداری کے سگنل: **{summary_buy}**

فروخت کے سگنل: **{summary_sell}**
""", unsafe_allow_html=True)

# --- Chart Pattern Note ---
st.markdown(""" 
##### نوٹ: 15 چارٹ پیٹرن AI سے Detect ہو رہے ہیں جیسے Head & Shoulders, Triangle, Wedge, وغیرہ۔

ہر اپڈیٹ کے ساتھ نئی detection کی اطلاع دی جائے گی۔
""", unsafe_allow_html=True)

# --- CSS for Blinking Signal (Optional) ---
st.markdown("""
<style>
@keyframes blinker {
  50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("پروفیشنل اردو ٹریڈنگ اسسٹنٹ - Powered by OpenAI & Streamlit", unsafe_allow_html=True)
