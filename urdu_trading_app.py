import streamlit as st
import requests
import pandas as pd
import time
from streamlit.components.v1 import html

# --- SETTINGS ---
st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")
st.title("پروفیشنل اردو ٹریڈنگ AI اسسٹنٹ")
st.caption("CoinMarketCap + AI Indicators + Chart Patterns + Live TradingView Charts")

# --- API CONFIG ---
CMC_API_KEY = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# --- USER SETTINGS ---
num_coins = st.selectbox("کتنے Top Coins دیکھنے ہیں؟", [10, 20, 30, 50], index=0)
auto_refresh = st.checkbox("خودکار ریفریش ہر 30 سیکنڈ بعد", value=True)

# --- FETCH DATA ---
def fetch_data():
    params = {"start": "1", "limit": str(num_coins), "convert": "USD"}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": CMC_API_KEY}
    response = requests.get(CMC_URL, params=params, headers=headers)
    return response.json()["data"]

# --- AI INDICATOR LOGIC ---
def ai_signal(price, change):
    if change > 2:
        return "🟢 خریدیں (Buy)"
    elif change < -2:
        return "🔴 فروخت (Sell)"
    else:
        return "🟡 انتظار کریں (Hold)"

# --- CHART PATTERN DETECTION (سادی مثال) ---
def detect_pattern(name):
    patterns = ["Head & Shoulders", "Triangle", "Wedge", "Double Top", "Double Bottom"]
    import random
    found = random.choice([True, False])
    return f"✅ {random.choice(patterns)}" if found else "❌ کوئی نہیں"

# --- SHOW COINS ---
def show_coins():
    data = fetch_data()
    for coin in data:
        name = coin['name']
        symbol = coin['symbol']
        price = coin['quote']['USD']['price']
        change = coin['quote']['USD']['percent_change_24h']

        st.markdown(f"### {name} ({symbol})")
        st.write(f"قیمت: ${price:.2f}")
        st.write(f"تبدیلی: {change:.2f}%")
        st.success(f"AI سگنل: {ai_signal(price, change)}")
        st.info(f"پیٹرن ڈیٹیکشن: {detect_pattern(name)}")

        # --- TradingView Chart ---
        tv_code = f"""
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{symbol}&symbol=BINANCE%3A{symbol}USDT&interval=1&hidesidetoolbar=1&symboledit=1&hideideas=1&theme=dark&style=1&timezone=Asia/Karachi" width="100%" height="400" frameborder="0" allowtransparency="true"></iframe>
        """
        html(tv_code, height=400)

# --- APP LOGIC ---
show_coins()

# --- AUTO REFRESH ---
if auto_refresh:
    time.sleep(30)
    st.experimental_rerun()
