import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنلز", layout="wide")

# بیک گراؤنڈ اور کارڈ اسٹائلنگ
st.markdown("""
    <style>
        .main {
            background-color: #f0f4f8; /* نرم بلیو رنگ */
        }
        .signal-card {
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease-in-out;
        }
        .signal-card:hover {
            transform: scale(1.05);
        }
        .button {
            background-color: #0E76A8;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 18px;
            text-align: center;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #005f86;
        }
        .header {
            text-align: center;
            color: #0E76A8;
            font-size: 36px;
            font-weight: 700;
        }
        .chart-container {
            margin-top: 40px;
        }
        .expander {
            font-size: 16px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# ہیڈر
st.markdown("<h1 class='header'>اردو ٹریڈنگ سگنلز</h1>", unsafe_allow_html=True)

# یوزر انپٹ
st.markdown("### سکہ یا اسٹاک منتخب کریں:")
symbol = st.text_input("مثال: BTCUSDT", value="BTCUSDT").upper()

# TradingView لائیو چارٹ کارڈ
with st.container():
    st.markdown("### لائیو چارٹ (TradingView):", unsafe_allow_html=True)
    components.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{symbol}&interval=1&theme=dark&style=1&locale=en&toolbarbg=F1F3F6",
        height=400,
        scrolling=True
    )
    st.markdown("---")

# سگنل بٹن
if st.button("سگنل چیک کریں", key="signal_button", help="سگنل چیک کرنے کے لئے یہاں کلک کریں"):
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
        st.markdown("### خلاصہ:", unsafe_allow_html=True)
        with st.expander("تفصیل دیکھیں", expanded=True):
            for key, val in analysis.summary.items():
                st.write(f"{key}: {val}")

        # تکنیکی انڈیکیٹرز
        st.markdown("### تکنیکی انڈیکیٹرز:", unsafe_allow_html=True)
        with st.expander("انڈیکیٹرز دیکھیں", expanded=True):
            for ind, val in analysis.indicators.items():
                st.write(f"{ind}: {val}")

    except Exception as e:
        st.error(f"کچھ غلط ہو گیا: {e}")
