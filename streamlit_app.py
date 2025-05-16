import streamlit as st

st.set_page_config(
    page_title="اردو پروفیشنل ٹریڈنگ ایپ",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <h1 style='text-align: center; color: green;'>اردو پروفیشنل ٹریڈنگ اسسٹنٹ</h1>
    <hr style='border:1px solid #ddd'>
    <div style='text-align:center;'>براہ کرم بائیں طرف موجود مینوز سے صفحہ منتخب کریں</div>
""", unsafe_allow_html=True)

st.image("https://assets.tradingview.com/banners/crypto.svg", use_container_width=True)

st.success("سکرین کے بائیں جانب سے ایک آپشن منتخب کریں: سکہ منتخب کریں، پیٹرن، سگنلز یا سیٹنگز")
