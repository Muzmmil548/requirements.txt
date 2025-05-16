
import streamlit as st
from tradingview_ta import TA_Handler, Interval

st.title("سگنلز")

symbol = st.text_input("سکہ منتخب کریں", "BTCUSDT")
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
        if recommendation == "BUY":
            st.success("خریداری (BUY) - سبز بتی")
        elif recommendation == "SELL":
            st.error("فروخت (SELL) - سرخ بتی")
        else:
            st.warning("انتظار (NEUTRAL) - پیلی بتی")
    except Exception as e:
        st.error(f"غلطی: {e}")
