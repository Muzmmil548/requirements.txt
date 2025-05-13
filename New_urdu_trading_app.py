import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنلز", layout="wide")

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
        st.markdown("### ٹریڈنگ سگنل:")
        if recommendation == "BUY":
            st.success("خریداری (BUY) - سبز بتی")
        elif recommendation == "SELL":
            st.error("فروخت (SELL) - سرخ بتی")
        else:
            st.warning("انتظار (NEUTRAL) - پیلی بتی")

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
