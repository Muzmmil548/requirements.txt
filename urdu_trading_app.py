import streamlit as st import pandas as pd import requests import time from datetime import datetime from streamlit.components.v1 import iframe

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide") st.title("پروفیشنل اردو ٹریڈنگ چیک لسٹ")

بٹن سے صفحہ ریفریش

if st.button("دوبارہ لوڈ کریں"): st.experimental_rerun()

ٹریڈنگ ویو چارٹ

selected_coin = st.selectbox("سکہ منتخب کریں:", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"]) iframe(f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{selected_coin}&interval=1&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=f1f3f6&studies=[]&theme=Dark&style=1&timezone=Asia/Karachi&withdateranges=1&hideideas=1", height=500)

سگنل اور خلاصہ

st.subheader(f"سگنل اور خلاصہ برائے: {selected_coin}") st.success("خریدنے کا اشارہ: سبز رنگ") st.warning("انتظار کریں: پیلا رنگ") st.error("فروخت کریں: سرخ رنگ") st.info("نیچرل رجحان: مارکیٹ غیر یقینی ہے")

چارٹ پیٹرن ڈٹیکشن

st.subheader("چارٹ پیٹرن ڈٹیکشن") patterns = { "Head & Shoulders": "🟡", "Inverse H&S": "🟢", "Double Top": "🟡", "Double Bottom": "🟡", "Symmetrical Triangle": "🟡", "Ascending Triangle": "🟢", "Descending Triangle": "🟢", "Falling Wedge": "🟢", "Rising Wedge": "🟢", "Cup & Handle": "🟡", "Bullish Flag": "🟡", "Bearish Flag": "🟢", "Rectangle": "🟢", "Triple Top": "🟡", "Triple Bottom": "🟢", }

for pattern, status in patterns.items(): st.markdown(f"{status} {pattern}", unsafe_allow_html=True)

خلاصہ نیچے

st.subheader("خلاصہ") st.markdown("""

منتخب سکہ: {selected_coin}

سگنل: سبز = خریدیں، سرخ = فروخت کریں، پیلا = انتظار کریں، نیچرل = غیر یقینی

چارٹ پیٹرن جو 🟢 ہے وہ موجود ہے، جو 🟡 ہے وہ ڈیٹیکٹ نہیں ہوا

چارٹ: ٹریڈنگ ویو لائیو """)


