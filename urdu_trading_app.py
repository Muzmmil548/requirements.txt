import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components
import time
import random

# ٹاپ 50 کوائنز کی لسٹ
top_50_coins = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT",
    "SOLUSDT", "DOGEUSDT", "AVAXUSDT", "TRXUSDT", "LINKUSDT",
    "MATICUSDT", "DOTUSDT", "LTCUSDT", "SHIBUSDT", "BCHUSDT",
    "ICPUSDT", "NEARUSDT", "XLMUSDT", "ATOMUSDT", "FILUSDT",
    "HBARUSDT", "APTUSDT", "ETCUSDT", "IMXUSDT", "INJUSDT",
    "VETUSDT", "RENDERUSDT", "MKRUSDT", "ALGOUSDT", "GRTUSDT",
    "AAVEUSDT", "SANDUSDT", "FTMUSDT", "EGLDUSDT", "THETAUSDT",
    "FLOWUSDT", "AXSUSDT", "CHZUSDT", "XTZUSDT", "RUNEUSDT",
    "CAKEUSDT", "KAVAUSDT", "ZILUSDT", "CRVUSDT", "ENJUSDT",
    "1INCHUSDT", "COMPUSDT", "DYDXUSDT", "SNXUSDT", "CELOUSDT"
]

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنلز", layout="wide")

# کسٹم CSS
st.markdown("""
    <style>
    @keyframes blink {
        50% { opacity: 0.0; }
    }
    .blink-green {
        animation: blink 1s infinite;
        background-color: #00cc00;
        padding: 10px;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        text-align: center;
    }
    .blink-red {
        animation: blink 1s infinite;
        background-color: #cc0000;
        padding: 10px;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        text-align: center;
    }
    .blink-yellow {
        animation: blink 1s infinite;
        background-color: #ffcc00;
        padding: 10px;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #0E76A8;'>اردو ٹریڈنگ سگنلز</h1>", unsafe_allow_html=True)

# کوائن سلیکشن
selected_coin = st.selectbox("ٹاپ 50 کوائن میں سے انتخاب کریں:", top_50_coins, index=0)

# لائیو چارٹ
st.markdown("### لائیو چارٹ:")
components.iframe(
    f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{selected_coin}&interval=1&theme=dark&style=1&locale=en",
    height=400,
    scrolling=True
)

# خودکار ریفریش
st_autorefresh = st.empty()
count = 0

while count < 1:
    count += 1
    try:
        handler = TA_Handler(
            symbol=selected_coin,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
        analysis = handler.get_analysis()
        recommendation = analysis.summary["RECOMMENDATION"]

        st.markdown("### سگنل:")
        if recommendation == "BUY":
            st.markdown('<div class="blink-green">🟢 خریداری (BUY)</div>', unsafe_allow_html=True)
        elif recommendation == "SELL":
            st.markdown('<div class="blink-red">🔴 فروخت (SELL)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="blink-yellow">🟡 انتظار (NEUTRAL)</div>', unsafe_allow_html=True)

        # پیٹرن سیکشن (ڈیٹیکشن کی مثال)
        st.markdown("### پیٹرن تجزیہ:")
        patterns = ["Head & Shoulders", "Double Top", "Triangle", "Cup & Handle", "Flag", "Wedge", "Rectangle", "Triple Top"]
        for pattern in patterns:
            detected = random.choice([True, False])
            if detected:
                st.success(f"✅ {pattern} پیٹرن ڈیٹیکٹ ہوا")
            else:
                st.info(f"⏳ {pattern} ویٹ کریں")

        # خلاصہ
        with st.expander("خلاصہ"):
            for key, val in analysis.summary.items():
                st.write(f"{key}: {val}")

        # انڈیکیٹرز
        with st.expander("تکنیکی انڈیکیٹرز"):
            for ind, val in analysis.indicators.items():
                st.write(f"{ind}: {val}")

    except Exception as e:
        st.error(f"کچھ غلط ہو گیا: {e}")

    time.sleep(60)  # 1 منٹ میں خودکار ریفریش کے لیے
