import streamlit as st from streamlit_autorefresh import st_autorefresh import pandas as pd import random import requests from datetime import datetime from streamlit.components.v1 import iframe

✅ ✅ ✅ Set Page Config (سب سے اوپر رکھنا ضروری ہے)

st.set_page_config(layout="wide")

--- Auto Refresh ہر 10 سیکنڈ میں ---

st_autorefresh(interval=10 * 1000, key="datarefresh")

--- Page Title ---

st.title("📊 اردو ٹریڈنگ اسسٹنٹ (AI چارٹ اور سگنلز کے ساتھ)")

--- Coin Selection ---

symbols = ["BTC", "ETH", "BNB", "SOL", "XRP"] selected_symbol = st.selectbox("کوائن منتخب کریں:", symbols)

--- TradingView Live Chart ---

tv_url = f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}USDT&interval=1&hidesidetoolbar=1&theme=dark" st.subheader(f"📈 لائیو چارٹ: {selected_symbol}USDT") iframe(tv_url, height=500)

--- CoinMarketCap Price Fetch ---

api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8" url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={selected_symbol}&convert=USD" headers = {"X-CMC_PRO_API_KEY": api_key} response = requests.get(url, headers=headers) price = response.json()["data"][selected_symbol]["quote"]["USD"]["price"] price = round(price, 2)

st.markdown("---") st.subheader("💰 موجودہ قیمت اور تجزیہ") st.info(f"🔸 موجودہ قیمت: ${price}")

--- TP/SL Calculation ---

tp = price * 1.03 sl = price * 0.97 st.success(f"🎯 ٹیک پرافٹ (TP): ${tp:.2f} | ⛔ اسٹاپ لاس (SL): ${sl:.2f}")

--- Sentiment (Simulated) ---

buyers = random.randint(40, 70) sellers = 100 - buyers neutral = random.randint(0, 10) st.subheader("🤖 AI مارکیٹ سینٹیمنٹ") st.info(f"🟢 خریدار: {buyers}% | 🔴 فروخت کنندہ: {sellers}% | ⚪ نیوٹرل: {neutral}%")

--- AI Signal with Blinking ---

signal = "🟢 Buy" if buyers > sellers else "🔴 Sell" if sellers > buyers else "🟡 Hold" color = "green" if signal == "🟢 Buy" else "red" if signal == "🔴 Sell" else "orange"

st.markdown("### 📢 AI ٹریڈ سگنل:")

def blinking_html(text, color): return f""" <div style='animation: blinker 1s linear infinite; color:{color}; font-size:24px; font-weight:bold;'> {text} </div> <style> @keyframes blinker {{ 50% {{ opacity: 0; }} }} </style> """

st.markdown(blinking_html(f"📍 سگنل: {signal}", color), unsafe_allow_html=True)

--- Chart Patterns (Simulated) ---

chart_patterns = [ "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom", "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle", "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag", "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom" ]

def simulate_patterns(): return {p: random.choice(["🟢", "🔴", "🟡", "❌"]) for p in chart_patterns}

st.markdown("---") st.subheader("📊 چارٹ پیٹرن ڈیٹیکشن:") patterns = simulate_patterns() for pattern, signal in patterns.items(): st.markdown(f"{pattern}: {signal}")

--- Pattern Summary ---

summary_counts = {"🟢": 0, "🔴": 0, "🟡": 0, "❌": 0} for s in patterns.values(): summary_counts[s] += 1

st.markdown("---") st.subheader("📌 پیٹرن کا خلاصہ:") st.markdown(f"🟢 مضبوط بُلش: {summary_counts['🟢']} | 🔴 مضبوط بیئرش: {summary_counts['🔴']} | 🟡 غیر یقینی: {summary_counts['🟡']} | ❌ کوئی سگنل نہیں: {summary_counts['❌']}")

--- Footer ---

st.markdown("---") st.caption("Developed by Urdu Trading AI | Auto Refreshed | Powered by Streamlit")

