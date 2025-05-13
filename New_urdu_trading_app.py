import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنلز", layout="wide")

# بیک گراؤنڈ رنگ اور کارڈ اسٹائل
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f4; /* یا اپنی مرضی کا رنگ */
        }
        .signal-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ہیڈر
st.markdown("<h1 style='text-align: center; color: #0E76A8;'>اردو ٹریڈنگ سگنلز</h1>", unsafe_allow_html=True)

# یوزر انپٹ
st.markdown("### سکہ یا اسٹاک منتخب کریں:")
symbol = st.text_input("مثال: BTCUSDT", value="BTCUSDT").upper()

# TradingView لائیو چارٹ کارڈ
with st.container():
    st.markdown("---")
    st.markdown("### لائیو چارٹ (TradingView):")
    components.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{symbol}&interval=1&theme=dark&style=1&locale=en&toolbarbg=F1F3F6",
        height=400,
        scrolling=True
    )
    st.markdown("---")

# سگنل بٹن
if st.button("سگنل چیک کریں"):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
        analysis = handler.get_analysis()
        recommendation = analysis.summary["RECOMMENDATION"]

        # سگنل کارڈ
        with st.container():
            st.markdown('<div class="signal-card">', unsafe_allow_html=True)
            if recommendation == "BUY":
                st.markdown("<h2 style='color: green;'>خریداری (BUY) - سبز بتی</h2>", unsafe_allow_html=True)
            elif recommendation == "SELL":
                st.markdown("<h2 style='color: red;'>فروخت (SELL) - سرخ بتی</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color: yellow;'>انتظار (NEUTRAL) - پیلی بتی</h2>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # خلاصہ
        st.markdown("### خلاصہ:")
        with st.expander("تفصیل دیکھیں"):
            for key, val in analysis.summary.items():
                st.write(f"{key}: {val}")

        # تکنیکی انڈیکیٹرز
        st.markdown("### تکنیکی انڈیکیٹرز:")
        with st.expander("انڈیکیٹرز دیکھیں"):
            for ind, val in analysis.indicators.items():
                st.write(f"{ind}: {val}")

    except Exception as e:
        st.error(f"کچھ غلط ہو گیا: {e}")
