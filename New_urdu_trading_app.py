import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنلز", layout="wide")

# بیک گراؤنڈ اور کارڈ اسٹائلنگ
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #6A11CB, #2575FC); /* پروفیشنل اور رنگین بیک گراؤنڈ */
        }
        .signal-card {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.4s ease-in-out, box-shadow 0.4s ease-in-out;
        }
        .signal-card:hover {
            transform: scale(1.05);
            box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.2);
        }
        .button {
            background-color: #0099FF;
            color: white;
            padding: 18px 30px;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            width: 100%;
            text-align: center;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #0066cc;
        }
        .header {
            text-align: center;
            color: white;
            font-size: 48px;
            font-weight: 800;
            text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
        }
        .chart-container {
            margin-top: 40px;
            background: rgba(255, 255, 255, 0.2);
            padding: 20px;
            border-radius: 12px;
        }
        .expander {
            font-size: 16px;
            font-weight: 500;
        }
        .indicator-section {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
        }
        .indicator-box {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
            width: 48%;
            min-width: 200px;
        }
    </style>
""", unsafe_allow_html=True)

# ہیڈر
st.markdown("<h1 class='header'>اردو ٹریڈنگ سگنلز</h1>", unsafe_allow_html=True)

# یوزر انپٹ
st.markdown("### سکہ یا اسٹاک منتخب کریں:")
symbol = st.text_input("مثال: BTCUSDT", value="BTCUSDT").upper()

# TradingView لائیو چارٹ
with st.container():
    st.markdown("### لائیو چارٹ (TradingView):", unsafe_allow_html=True)
    components.iframe(
        f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{symbol}&interval=1&theme=dark&style=1&locale=en&toolbarbg=F1F3F6",
        height=450,
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
        with st.container():
            st.markdown('<div class="indicator-section">', unsafe_allow_html=True)
            for ind, val in analysis.indicators.items():
                st.markdown(f"<div class='indicator-box'><b>{ind}</b>: {val}</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"کچھ غلط ہو گیا: {e}")
