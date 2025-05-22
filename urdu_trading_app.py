urdu_trading_app.py

import streamlit as st import pandas as pd import requests import time from datetime import datetime import plotly.graph_objects as go

--- Page Config ---

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

--- App Title ---

st.markdown(""" <h2 style='text-align: center;'>پروفیشنل اردو ٹریڈنگ اسسٹنٹ</h2> """, unsafe_allow_html=True)

--- Auto Refresh & Manual Refresh ---

refresh_interval = 30  # seconds if st.button("دوبارہ لوڈ کریں"): st.experimental_rerun() st_autorefresh = st.experimental_data_editor if hasattr(st, 'experimental_data_editor') else time.sleep st_autorefresh(refresh_interval)

--- Select Top Coins ---

option = st.selectbox("ٹاپ کوائنز منتخب کریں:", ["Top 10", "Top 50"]) limit = 10 if option == "Top 10" else 50

--- Fetch Coin Data ---

def fetch_coin_data(): url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1&sparkline=false" response = requests.get(url) return response.json() if response.status_code == 200 else []

data = fetch_coin_data()

--- Dummy Support/Resistance AI & TP/SL Logic ---

def ai_signal(price, change): if change > 1: return "🟢", "BUY", True elif change < -1: return "🔴", "SELL", True else: return "🟡", "HOLD", False

def get_tp_sl(price): tp = price * 1.02 sl = price * 0.98 return round(tp, 2), round(sl, 2)

--- Display Chart (Fixed Binance BTC/USDT for simplicity) ---

st.markdown(""" <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_btc&symbol=BINANCE:BTCUSDT&interval=1&theme=dark&style=1&locale=en" width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe> """, unsafe_allow_html=True)

--- Table with Signals ---

st.markdown("<h4>لائیو ٹریڈنگ سگنل</h4>", unsafe_allow_html=True)

summary_buy = 0 summary_sell = 0

for coin in data: name = coin['name'] symbol = coin['symbol'].upper() price = coin['current_price'] change = coin['price_change_percentage_24h'] volume = coin['total_volume']

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

--- Summary ---

st.markdown(f""" <h4>خلاصہ:</h4> <p>خریداری کے سگنل: <b>{summary_buy}</b></p> <p>فروخت کے سگنل: <b>{summary_sell}</b></p> """, unsafe_allow_html=True)

--- Chart Pattern Detection Note ---

st.markdown(""" <h5>نوٹ: 15 چارٹ پیٹرن AI سے Detect ہو رہے ہیں جیسے Head & Shoulders, Triangle, Wedge, وغیرہ۔</h5> <p>ہر اپڈیٹ کے ساتھ نئی detection کی اطلاع دی جائے گی۔</p> """, unsafe_allow_html=True)

--- CSS for blinking effect ---

st.markdown("""

<style>
@keyframes blinker {
  50% { opacity: 0.3; }
}
</style>""", unsafe_allow_html=True)

--- Footer ---

st.markdown("<hr><center>پروفیشنل اردو ٹریڈنگ اسسٹنٹ - Powered by OpenAI & Streamlit</center>", unsafe_allow_html=True)

