import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- Sidebar ---
st.sidebar.title("کوائن سیلیکشن")
top_n = st.sidebar.selectbox("ٹاپ کتنے کوائنز دیکھنا چاہتے ہیں؟", [10, 50])

st.title("AI اسسٹنٹ - اردو ٹریڈنگ تجزیہ")

# --- Get Market Data from CoinGecko ---
@st.cache_data(ttl=60)
def get_coin_data(limit=10):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1,
        "sparkline": True
    }
    response = requests.get(url, params=params)
    return response.json()

# --- Simple AI Signal Logic ---
def analyze_coin(coin):
    price = coin['current_price']
    change = coin['price_change_percentage_24h']
    volume = coin['total_volume']

    if change is None:
        return "رکیں", "پیلا"

    if change > 3 and volume > 1_000_000:
        return "خریدیں", "سبز"
    elif change < -3 and volume > 1_000_000:
        return "بیچیں", "سرخ"
    else:
        return "رکیں", "پیلا"

# --- Chart Pattern Detection (Head & Shoulders - simplified mock) ---
def detect_head_shoulders(sparkline):
    prices = np.array(sparkline)
    if len(prices) < 7:
        return False

    left = prices[1]
    head = prices[3]
    right = prices[5]

    # Simplified condition
    if head > left and head > right and abs(left - right)/head < 0.1:
        return True
    return False

# --- Main App ---
data = get_coin_data(top_n)

st.markdown("### تجزیہ: AI سگنلز اور پیٹرن ڈیٹیکشن")

for coin in data:
    name = coin['name']
    symbol = coin['symbol'].upper()
    price = coin['current_price']
    change = coin['price_change_percentage_24h']
    sparkline = coin['sparkline_in_7d']['price']
    
    signal_urdu, color = analyze_coin(coin)
    pattern_detected = detect_head_shoulders(sparkline)

    pattern_text = "🟢 Head & Shoulders پیٹرن ملا" if pattern_detected else "❌ کوئی خاص پیٹرن نہیں"

    st.markdown(
        f"""
        <div style='border:1px solid #ccc; border-radius:10px; padding:10px; margin:10px 0; background-color:#f8f8f8'>
            <b>{name} ({symbol})</b><br>
            قیمت: ${price:,} <br>
            24 گھنٹے تبدیلی: {change:.2f}% <br>
            <span style='color:{color}; font-weight:bold;'>سگنل: {signal_urdu}</span><br>
            <span style='font-size: 16px;'>{pattern_text}</span>
        </div>
        """, unsafe_allow_html=True
    )
