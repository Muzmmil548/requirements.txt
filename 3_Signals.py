import streamlit as st
from tradingview_ta import TA_Handler, Interval

st.header("سگنل تجزیہ")

symbol = st.session_state.get("symbol", "BTCUSDT")
st.info(f"منتخب سکہ: {symbol}")

if st.button("سگنل حاصل کریں"):
    try:
        handler = TA_Handler(
            symbol=symbol,
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
        analysis = handler.get_analysis()
        rec = analysis.summary["RECOMMENDATION"]

        if rec == "BUY":
            st.success("خریداری کا سگنل")
        elif rec == "SELL":
            st.error("فروخت کا سگنل")
        else:
            st.warning("انتظار کریں")

    except Exception as e:
        st.error(f"خرابی: {e}")
