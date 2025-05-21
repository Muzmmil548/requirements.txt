import streamlit as st
import requests
import time
import random

st.set_page_config(page_title="اردو ٹریڈنگ ایپ", layout="wide")
st.markdown("<h1 style='text-align: center;'>اردو ٹریڈنگ اسسٹنٹ</h1>", unsafe_allow_html=True)

# --------- CoinMarketCap API ---------
CMC_API_KEY = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
CMC_API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY,
}

# ----------- Manual Refresh Button -----------
if st.button("🔄 ڈیٹا ریفریش کریں"):
    st.cache_data.clear()
    time.sleep(0.5)
    st.rerun()

# ----------- TradingView Chart -----------
st.markdown("### لائیو مارکیٹ چارٹ (BTC/USDT)")
st.components.v1.html("""
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_0cd12&symbol=BINANCE:BTCUSDT&interval=5&theme=dark&style=1&locale=ur" 
    width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", height=400)

# ---------- Fetch Coins ----------
@st.cache_data(ttl=60)
def get_top_coins():
    params = {
        "start": "1",
        "limit": "10",
        "convert": "USD"
    }
    response = requests.get(CMC_API_URL, headers=headers, params=params)
    data = response.json()
    return data["data"]

coins = get_top_coins()

# --------- Helper Function to Simulate Signal ---------
def get_signal():
    signal = random.choice(["buy", "sell", "hold"])
    if signal == "buy":
        return "🟢 خریداری کا موقع", "green"
    elif signal == "sell":
        return "🔴 فروخت کا اشارہ", "red"
    else:
        return "🟡 انتظار کریں", "yellow"

# ----------- Display Coins -----------
for coin in coins:
    name = coin["name"]
    price = coin["quote"]["USD"]["price"]
    change = coin["quote"]["USD"]["percent_change_24h"]
    buyers = random.randint(100, 1000)
    sellers = random.randint(100, 1000)
    signal_text, color = get_signal()

    st.markdown(f"## {name}")
    st.write(f"قیمت: ${price:,.2f}")
    st.write(f"24 گھنٹے میں تبدیلی: {change:.2f}%")
    st.write(f"خریدار: {buyers} | فروخت کنندگان: {sellers}")
    st.markdown(
        f"<div style='font-size:24px; font-weight:bold; color:{color}; animation: blinker 1s linear infinite;'>{signal_text}</div>"
        "<style>@keyframes blinker {50% {opacity: 0;}}</style>", unsafe_allow_html=True
    )
    st.markdown("---")
