import streamlit as st
import datetime

st.set_page_config(layout="centered")

# اردو ہیڈنگ
st.markdown("<h1 style='text-align: center; font-size: 50px;'>اردو ٹریڈنگ اسسٹنٹ</h1>", unsafe_allow_html=True)

# ٹریڈنگ ویو چارٹ embed کرنے والا فنکشن
def show_chart(symbol):
    st.subheader(f"{symbol}")
    st.markdown(f"""
        <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:{symbol}&locale=ur" 
        width="100%" height="200" frameborder="0"></iframe>
    """, unsafe_allow_html=True)
    
    # سگنل باکس
    st.markdown(
        f"""
        <div style="background-color:#fff3cd;padding:15px;border-radius:10px;">
            <strong>Live چارٹ:</strong> براہ کرم {symbol} کیلئے سگنل دیکھیں۔
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

# کوائن لسٹ
coins = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]

# ہر کوائن کا سیکشن
for coin in coins:
    symbol = coin.replace("/", "")
    show_chart(symbol)
