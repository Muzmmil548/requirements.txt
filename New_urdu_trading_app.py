# app.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ================== پیج کنفیگریشن ================== #
st.set_page_config(
    page_title="Urdu Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== کسٹم CSS ================== #
st.markdown("""
<style>
    /* سائیڈبار سٹائلنگ */
    [data-testid="stSidebar"] {
        background: #2c3e50 !important;
        color: white !important;
    }
    
    /* قیمتیں باکس */
    .price-box {
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ================== کوین گیکو API فنکشنز ================== #
@st.cache_data(ttl=30) # ہر 30 سیکنڈ میں ڈیٹا اپڈیٹ
def get_crypto_prices():
    coins = {
        'bitcoin': 'BTC/USDT',
        'ethereum': 'ETH/USDT', 
        'binancecoin': 'BNB/USDT'
    }
    prices = {}
    for coin_id, pair in coins.items():
        try:
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
            prices[pair] = response.json()[coin_id]['usd']
        except:
            prices[pair] = "N/A"
    return prices

# ================== ٹریڈنگ ویو ویجٹ ================== #
def tradingview_widget():
    return f"""
    <div class="tradingview-widget-container" style="height:600px; margin:20px">
        <div id="tradingview_chart"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
            new TradingView.widget({{
                "autosize": true,
                "symbol": "BINANCE:BTCUSDT",
                "interval": "15",
                "timezone": "Asia/Karachi",
                "theme": "dark",
                "style": "1",
                "locale": "en",
                "toolbar_bg": "#2c3e50",
                "enable_publishing": false,
                "hide_side_toolbar": false,
                "allow_symbol_change": true,
                "container_id": "tradingview_chart"
            }});
        </script>
    </div>
    """

# ================== مین ایپ ================== #
with st.sidebar:
    st.header("مینو")
    menu = st.radio("", ["ہوم", "لائیو", "چارٹ", "ٹاپ 50", "AI سگنلز"])

if menu == "ہوم":
    st.header("کرپٹو ٹریڈنگ ڈیش بورڈ")
    
    # ٹاپ سیکشن
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("ٹاپ کوائنز")
        st.write("BTC/USDT\nETH/USDT\nBNB/USDT")
    
    # AI سگنلز
    with col2:
        st.subheader("AI تجاویز")
        st.button("خریدیں")
        st.button("فروخت کریں")
    
    # پیٹرنز
    with col3:
        st.subheader("چارٹ پیٹرنز")
        st.write("ہیڈ اینڈ شولڈرز\nڈبل ٹاپ")

elif menu == "لائیو":
    st.header("لائیو مارکیٹ ڈیٹا")
    
    # ٹریڈنگ ویو چارٹ
    st.markdown(tradingview_widget(), unsafe_allow_html=True)
    
    # لائیو قیمتیں
    st.subheader("موجودہ قیمتیں")
    prices = get_crypto_prices()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='price-box'><h3>BTC/USDT</h3><h2>${prices['BTC/USDT']}</h2></div>", 
                    unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"<div class='price-box'><h3>ETH/USDT</h3><h2>${prices['ETH/USDT']}</h2></div>", 
                    unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"<div class='price-box'><h3>BNB/USDT</h3><h2>${prices['BNB/USDT']}</h2></div>", 
                    unsafe_allow_html=True)

# ================== انسٹالیشن فائل ================== #
''' requirements.txt
streamlit==1.32.0
pandas==2.1.4
requests==2.31.0
'''
