
import streamlit as st

st.title("چارٹ پیٹرن تجزیہ")
pattern = st.selectbox("چارٹ پیٹرن منتخب کریں", ["Head & Shoulders", "Double Top", "Triangle"])
if pattern:
    st.info(f"آپ نے منتخب کیا ہے: {pattern}")
