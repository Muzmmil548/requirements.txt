import streamlit as st
from tradingview_ta import TA_Handler, Interval
import streamlit.components.v1 as components

# صفحہ سیٹنگ
st.set_page_config(page_title="اردو ٹریڈنگ سگنل", layout="centered")
st.title("اردو ٹریڈنگ سگنلز - لائیو چارٹ اور سگنلز کے ساتھ")

# یوزر ان پٹ
symbol = st.text_input("سکہ یا اسٹاک لکھیں (مثال: BTCUSDT)", value="BTCUSDT").upper()

# لائیو TradingView چارٹ
st.subheader("لائیو چارٹ:")
components.iframe(
    f"https://s.tradingview.com/widgetembed/?symbol=BINANCE%3A{symbol}&interval=1&theme=dark&style=1&locale=en&toolbarbg=F1F3F6",
    height=400,
    scrolling=True
)

# سگنل چیکر
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

        st.subheader("تجویز:")

        # سگنل کے مطابق رنگی بتی
        if recommendation == "BUY":
            st.success("خریداری (BUY) - سبز بتی")
        elif recommendation == "SELL":
            st.error("فروخت (SELL) - سرخ بتی")
        else:
            st.warning("انتظار (NEUTRAL) - پیلی بتی")

        # خلاصہ
        st.subheader("خلاصہ:")
        for key, val in analysis.summary.items():
            st.write(f"{key}: {val}")

        # تکنیکی انڈیکیٹرز
        st.subheader("تکنیکی انڈیکیٹرز:")
        for ind, val in analysis.indicators.items():
            st.write(f"{ind}: {val}")

    except Exception as e:
        st.error(f"کچھ غلط ہو گیا: {e}")
