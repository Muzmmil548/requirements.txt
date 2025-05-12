import streamlit as st
from tradingview_ta import TA_Handler, Interval, Exchange

# صفحے کی ترتیب
st.set_page_config(page_title="اردو ٹریڈنگ سگنل", layout="centered")
st.title("اردو ٹریڈنگ ویو سگنل ایپ")

# یوزر سے سکہ کا نام لینا
symbol_input = st.text_input("سکہ یا اسٹاک کا نام لکھیں (مثال: BTCUSDT)", value="BTCUSDT")

# سگنل چیک بٹن
if st.button("سگنل چیک کریں"):
    try:
        handler = TA_Handler(
            symbol=symbol_input,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
        analysis = handler.get_analysis()

        st.subheader("خلاصہ:")
        st.write(analysis.summary)

        st.subheader("تکنیکی انڈیکیٹرز:")
        for ind, value in analysis.indicators.items():
            st.write(f"{ind}: {value}")

    except Exception as e:
        st.error("کچھ غلط ہو گیا:")
        st.exception(e)  # تفصیلی ایرر دکھانے کے لیے
