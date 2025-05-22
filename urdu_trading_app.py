urdu_trading_app.py
import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from streamlit.components.v1 import iframe
--- Page Config ---

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

--- App Title ---

st.markdown("""

پروفیشنل اردو ٹریڈنگ اسسٹنٹ

""", unsafe_allow_html=True)

--- Select Top Coins ---

option = st.selectbox("ٹاپ کوائنز منتخب کریں:", ["Top 10", "Top 50"]) limit = 10 if option == "Top 10" else 50

--- Fetch Coin Data ---

def fetch_coin_data(): url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false" response = requests.get(url) return response.json() if response.status_code == 200 else []

data = fetch_coin_data()

--- Coin Selection ---

coin_names = [f"{coin['name']} ({coin['symbol'].upper()})" for coin in data] selected_coin = st.selectbox("کوائن منتخب کریں:", coin_names)

--- Get Selected Coin Data ---

coin_data = next((coin for coin in data if f"{coin['name']} ({coin['symbol'].upper()})" == selected_coin), None)

--- Live TradingView Chart ---

if coin_data: symbol = coin_data['symbol'].upper() + "USDT" tv_symbol = f"BINANCE:{symbol}" st.markdown("### لائیو چارٹ (TradingView)") tv_url = f"https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{symbol}&symbol={tv_symbol}&interval=1&theme=dark&style=1" iframe(tv_url, height=400, scrolling=True)

# --- AI Signal + TP/SL ---
price = coin_data['current_price']
change = coin_data['price_change_percentage_24h']
volume = coin_data['total_volume']

def ai_signal(change):
    if change > 1:
        return "🟢", "BUY", True
    elif change < -1:
        return "🔴", "SELL", True
    else:
        return "🟡", "HOLD", False

def get_tp_sl(price):
    return round(price * 1.02, 2), round(price * 0.98, 2)

signal, signal_text, blink = ai_signal(change)
tp, sl = get_tp_sl(price)

style = f"color:white;padding:8px;border-radius:6px;background-color:{'green' if signal=='🟢' else 'red' if signal=='🔴' else 'orange'};animation:{'blinker 1s linear infinite' if blink else 'none'};"

st.markdown(f"""
    <div style="margin-bottom:10px;">
        <b>{coin_data['name']} ({symbol})</b><br>
        <span style="{style}">{signal} {signal_text}</span><br>
        قیمت: ${price} | TP: ${tp} | SL: ${sl}<br>
        والیوم: {volume}
    </div>
""", unsafe_allow_html=True)

# --- Summary ---
st.markdown(f""" 
#### خلاصہ:

منتخب شدہ کوائن: **{coin_data['name']} ({symbol})**

موجودہ قیمت: **${price}** | TP: **${tp}** | SL: **${sl}**
""", unsafe_allow_html=True)

# --- Dummy Chart Pattern Detection ---
patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Rising Wedge", "Falling Wedge", "Ascending Triangle", "Descending Triangle",
    "Symmetrical Triangle", "Bull Flag", "Bear Flag", "Cup & Handle",
    "Triple Top", "Triple Bottom", "Rectangle"
]

st.markdown("#### چارٹ پیٹرن ڈیٹیکشن:")
for pattern in patterns:
    detected = hash(pattern + symbol) % 3 == 0
    icon = "🟢" if detected else "🟡"
    anim = "blinker 1s linear infinite" if True else "none"
    pattern_style = f"color:white;padding:5px;margin:3px;border-radius:4px;background-color:{'green' if detected else 'orange'};animation:{'blinker 1s linear infinite' if True else 'none'}"
    st.markdown(f"<span style='{pattern_style}'>{icon} {pattern}</span>", unsafe_allow_html=True)

--- CSS Blinker ---

st.markdown("""

<style>
@keyframes blinker {
  50% { opacity: 0; }
}
</style>""", unsafe_allow_html=True)

--- Footer ---

st.markdown("پروفیشنل اردو ٹریڈنگ اسسٹنٹ - Powered by OpenAI & Streamlit", unsafe_allow_html=True)

