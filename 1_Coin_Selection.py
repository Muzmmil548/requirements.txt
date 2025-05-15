import streamlit as st

st.header("سکہ منتخب کریں")
symbol = st.text_input("سکہ منتخب کریں (مثال: BTCUSDT)", value="BTCUSDT").upper()
st.session_state["symbol"] = symbol
st.success(f"منتخب سکہ: {symbol}")
