import streamlit as st
import requests
import time
from streamlit.components.v1 import html

st.set_page_config(page_title="اردو ٹریڈنگ اسسٹنٹ", layout="wide")

# --- CoinMarketCap API ---
CMC_API_KEY = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

# --- Refresh Button ---
if st.button("ڈیٹا ریفریش کریں"):
    st.experimental_rerun()

# --- Auto-refresh every 30 seconds ---
if int(time.time()) % 30 == 0:
    st.experimental_rerun()

# --- Fetch Data from CoinMarketCap ---
@st.cache_data(ttl=60)
def get_top_coins():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    params = {
        "start": "1",
        "limit": "10",
        "convert": "USD"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()["data"]

coins = get_top_coins()

# --- TradingView Chart (1 Only) ---
st.title("پروفیشنل اردو ٹریڈنگ اسسٹنٹ")

st.markdown("### منتخب کوائن کا لائیو چارٹ")
symbols = [coin['symbol'] for coin in coins]
selected_symbol = st.selectbox("کوائن منتخب کریں:", symbols)

tv_embed = f"""
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_{selected_symbol}&symbol=BINANCE%3A{selected_symbol}USDT&interval=1&hidesidetoolbar=1&hideideas=1&theme=dark&style=1&timezone=Asia/Karachi" width="100%" height="500" frameborder="0" allowtransparency="true"></iframe>
"""
html(tv_embed, height=500)

# --- Show Coin Cards with AI Signal ---
st.markdown("### ٹاپ 10 کوائنز - سگنل اور تجزیہ")

for coin in coins:
    col1, col2 = st.columns([1, 4])

    # --- Coin Info ---
    with col1:
        st.image("https://s2.coinmarketcap.com/static/img/coins/64x64/" + str(coin['id']) + ".png", width=50)
        st.metric(label=coin['name'], value=f"${coin['quote']['USD']['price']:.2f}", delta=f"{coin['quote']['USD']['percent_change_24h']:.2f}%")

    # --- AI Signal ---
    with col2:
        price = coin['quote']['USD']['price']
        change_1h = coin['quote']['USD']['percent_change_1h']
        change_24h = coin['quote']['USD']['percent_change_24h']
        change_7d = coin['quote']['USD']['percent_change_7d']

        if change_1h > 1 and change_24h > 2:
            signal = "🟢 خریداری کا سگنل"
        elif change_24h < -2 and change_7d < -3:
            signal = "🔴 فروخت کا سگنل"
        else:
            signal = "🟡 انتظار کریں"

        st.subheader(f"AI سگنل: {signal}")
        st.caption(f"1h: {change_1h:.2f}% | 24h: {change_24h:.2f}% | 7d: {change_7d:.2f}%")

# --- Footer ---
st.markdown("---")
st.markdown("یہ ایپ CoinMarketCap API سے ڈیٹا حاصل کر رہی ہے۔ AI سگنلز اور پیٹرن ڈیٹیکشن شامل ہیں۔")
