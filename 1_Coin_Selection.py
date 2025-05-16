
import streamlit as st

st.title("سکہ منتخب کریں")
symbol = st.text_input("سکہ یا اسٹاک کا نام لکھیں:", "BTCUSDT")
st.success(f"منتخب شدہ سکہ: {symbol}")
