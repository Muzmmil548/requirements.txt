# app.py
import streamlit as st
import requests

# ========== پیج کنفیگریشن ========== #
st.set_page_config(
    page_title="پیشہ ور ٹریڈنگ ایپ",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💹"
)

# ========== کسٹم CSS ========== #
st.markdown("""
<style>
    /* بنیادی سٹائلز */
    .main {background: #1a1a1a !important; color: #ffffff}
    
    /* ہیڈرز */
    h1 {color: #00ff88 !important; border-bottom: 3px solid #00ff88; padding-bottom: 10px}
    
    /* قیمتیں باکس */
    .price-card {
        background: #2d2d2d;
        border-radius: 12px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* بٹنز */
    .stButton>button {
        background: #00ff88 !important;
        color: #1a1a1a !important;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {transform: scale(1.05)}
    
    /* ٹریڈنگ ویو کنٹینر */
    .tv-container {
        height: 600px;
        border-radius: 15px;
        overflow: hidden;
        margin: 25px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ========== کوین گیکو API ========== #
@st.cache_data(ttl=15)
def get_prices():
    coins = {
        'bitcoin': 'BTC/USDT',
        'ethereum': 'ETH/USDT',
        'binancecoin': 'BNB/USDT'
    }
    prices = {}
    for coin_id, pair in coins.items():
        try:
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd")
            prices[pair] = "{:,.2f}".format(response.json()[coin_id]['usd'])
        except:
            prices[pair] = "N/A"
    return prices

# ========== ٹریڈنگ ویو ویجٹ ========== #
def tradingview_chart():
    return """
    <div class="tv-container">
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <div id="tradingview_chart"></div>
        <script>
        new TradingView.widget({
            "autosize": true,
            "symbol": "BINANCE:BTCUSDT",
            "interval": "15",
            "timezone": "Asia/Karachi",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#1a1a1a",
            "enable_publishing": false,
            "hide_side_toolbar": false,
            "allow_symbol_change": true,
            "container_id": "tradingview_chart"
        });
        </script>
    </div>
    """

# ========== مین لیآؤٹ ========== #
# سائیڈبار
with st.sidebar:
    st.markdown("<h1 style='color: #00ff88 !important'>مینو</h1>", unsafe_allow_html=True)
    menu = st.radio("", ["ہوم", "لائیو چارٹ", "سگنلز", "اکاؤنٹ"])

# مرکزی علاقہ
if menu == "ہوم":
    st.markdown("<h1>پیشہ ور ٹریڈنگ پلیٹ فارم</h1>", unsafe_allow_html=True)
    
    # قیمتیں کارڈز
    prices = get_prices()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="price-card">
            <h3>🔴 BTC/USDT</h3>
            <h1 style='color: #00ff88'>${prices['BTC/USDT']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="price-card">
            <h3>🔵 ETH/USDT</h3>
            <h1 style='color: #00ff88'>${prices['ETH/USDT']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="price-card">
            <h3>🟢 BNB/USDT</h3>
            <h1 style='color: #00ff88'>${prices['BNB/USDT']}</h1>
        </div>
        """, unsafe_allow_html=True)

elif menu == "لائیو چارٹ":
    st.markdown("<h1>لائیو ٹریڈنگ چارٹ</h1>", unsafe_allow_html=True)
    st.markdown(tradingview_chart(), unsafe_allow_html=True)

elif menu == "سگنلز":
    st.markdown("<h1>AI ٹریڈنگ سگنلز</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔥 فوری خریداری", help="مضبوط خریداری کا سگنل")
        st.button("🛑 فوری فروخت", help="ہنگامی فروخت کا الارم")
    with col2:
        st.button("📈 طویل مدتی", help="طویل مدتی ہولڈ")
        st.button("⚠️ خطرے کا الارم", help="مارکیٹ میں اتار چڑھاؤ")
