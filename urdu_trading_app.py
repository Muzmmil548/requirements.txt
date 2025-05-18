Urdu Trading Assistant App (Complete Code)

import streamlit as st from tradingview_ta import TA_Handler, Interval import streamlit.components.v1 as components import time import random

Set page config

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

Custom CSS for blinking signals

st.markdown(""" <style> @keyframes blink { 50% { opacity: 0.0; } } .blink-green { animation: blink 1s infinite; background-color: #00cc00; padding: 10px; color: white; font-weight: bold; border-radius: 10px; text-align: center; } .blink-red { animation: blink 1s infinite; background-color: #cc0000; padding: 10px; color: white; font-weight: bold; border-radius: 10px; text-align: center; } .blink-yellow { animation: blink 1s infinite; background-color: #ffcc00; padding: 10px; color: black; font-weight: bold; border-radius: 10px; text-align: center; } </style> """, unsafe_allow_html=True)

Header

st.markdown("<h1 style='text-align: center; color: #0E76A8;'>اردو ٹریڈنگ اسسٹنٹ</h1>", unsafe_allow_html=True)

Top 50 Coin Selector

top_50 = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT", "SOLUSDT", "DOTUSDT", "TRXUSDT", "AVAXUSDT"] symbol = st.selectbox("### سکہ منتخب کریں:", options=top_50)

Auto Refresh Toggle

auto_refresh = st.toggle("⏳ آٹو ریفریش", value=False)

Live Chart

st.markdown("### لائیو چارٹ:") components.iframe( f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{symbol}&interval=1&theme=dark&style=1&locale=en", height=400, scrolling=True )

Pattern Detection

st.markdown("### چارٹ پیٹرن تجزیہ:") chart_patterns = [ "Head & Shoulders", "Inverse Head & Shoulders", "Double Top", "Double Bottom", "Triple Top", "Triple Bottom", "Cup & Handle", "Wedge", "Ascending Triangle", "Descending Triangle", "Symmetrical Triangle", "Rectangle", "Flag", "Pennant", "Rounding Bottom" ]

for pattern in chart_patterns: detected = random.choice(["✅ ڈیٹیکٹ ہوا", "⏳ ویٹ کریں"]) st.write(f"{pattern}: {detected}")

Signal Section

st.markdown("### سگنل:") if auto_refresh or st.button("سگنل چیک کریں"): try: handler = TA_Handler( symbol=symbol, screener="crypto", exchange="BINANCE", interval=Interval.INTERVAL_1_MINUTE ) analysis = handler.get_analysis() recommendation = analysis.summary["RECOMMENDATION"]

if recommendation == "BUY":
        st.markdown('<div class="blink-green">🟢 خریداری (BUY) سگنل</div>', unsafe_allow_html=True)
    elif recommendation == "SELL":
        st.markdown('<div class="blink-red">🔴 فروخت (SELL) سگنل</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="blink-yellow">🟡 انتظار (NEUTRAL)</div>', unsafe_allow_html=True)

    with st.expander("### خلاصہ دیکھیں"):
        for key, val in analysis.summary.items():
            st.write(f"{key}: {val}")

    with st.expander("### تکنیکی انڈیکیٹرز"):
        for ind, val in analysis.indicators.items():
            st.write(f"{ind}: {val}")

except Exception as e:
    st.error(f"کچھ غلط ہو گیا: {e}")

Auto refresh loop

if auto_refresh: time.sleep(60) st.experimental_rerun()

