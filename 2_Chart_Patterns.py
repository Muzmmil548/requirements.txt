import streamlit as st

st.header("چارٹ پیٹرن تجزیہ")
st.info("یہ صفحہ خودکار طور پر چارٹ پیٹرنز کو پہچانے گا (جیسے Head & Shoulders، Triangle وغیرہ)۔")
pattern_selected = st.selectbox("چارٹ پیٹرن منتخب کریں", ["Head & Shoulders", "Triangle", "Double Top", "Double Bottom"])
st.success(f"منتخب پیٹرن: {pattern_selected}")
