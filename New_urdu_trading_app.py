import streamlit as st from tradingview_ta import TA_Handler, Interval

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide") st.markdown("""

<h1 style='text-align: center;'>اردو ٹریڈنگ ویو سگنل + لائیو چارٹ</h1>
""", unsafe_allow_html=True)Layout

col1, col2 = st.columns([1, 2])

Light Color Function

signal_color = { "STRONG_BUY": "🟢 خریداری کا مضبوط سگنل", "BUY": "🟢 خریداری کا سگنل", "NEUTRAL": "🟡 انتظار کریں", "SELL": "🔴 فروخت کا سگنل", "STRONG_SELL": "🔴 فروخت کا مضبوط سگنل" }

Left Column: Input & Signal

with col1: symbol_input = st.text_input("سکہ یا اسٹاک (مثال: BTCUSDT)", value="BTCUSDT") interval_option = st.selectbox("ٹائم فریم منتخب کریں", [ "1m", "5m", "15m", "1h", "4h", "1d" ])

interval_map = {
    "1m": Interval.INTERVAL_1_MINUTE,
    "5m": Interval.INTERVAL_5_MINUTES,
    "15m": Interval.INTERVAL_15_MINUTES,
    "1h": Interval.INTERVAL_1_HOUR,
    "4h": Interval.INTERVAL_4_HOURS,
    "1d": Interval.INTERVAL_1_DAY
}

if st.button("سگنل چیک کریں"):
    try:
        handler = TA_Handler(
            symbol=symbol_input,
            screener="crypto",
            exchange="BINANCE",
            interval=interval_map[interval_option]
        )
        analysis = handler.get_analysis()

        st.subheader("خلاصہ:")
        signal = analysis.summary.get("RECOMMENDATION", "NEUTRAL")
        st.success(signal_color.get(signal, "🟡 انتظار کریں"))

        st.subheader("تکنیکی انڈیکیٹرز:")
        for ind, value in analysis.indicators.items():
            st.write(f"{ind}: {value}")

    except Exception as e:
        st.error("کچھ غلط ہو گیا:")
        st.exception(e)

Right Column: Live TradingView Chart

with col2: st.subheader("Live TradingView Chart") tv_symbol = symbol_input.upper() st.components.v1.html(f""" <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:{tv_symbol}&interval={interval_option}&hidesidetoolbar=1&theme=dark&style=1&locale=en" width="100%" height="600" frameborder="0" allowtransparency="true" scrolling="no"> </iframe> """, height=650, scrolling=True)

