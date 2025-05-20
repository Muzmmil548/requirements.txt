import streamlit as st
import requests
import time

# CoinMarketCap API Key
API_KEY = '9fee371c-217b-49cd-988a-5c0829ae1ea8'

# App title
st.set_page_config(page_title="AI Urdu Trading Assistant", layout="wide")
st.title("AI اردو ٹریڈنگ اسسٹنٹ")

# Refresh Button
if st.button("ڈیٹا ریفریش کریں"):
    st.experimental_rerun()

# Auto Refresh every 30 seconds
st.markdown("""
    <meta http-equiv="refresh" content="30">
""", unsafe_allow_html=True)

# TradingView Chart (Single chart at top)
st.markdown("""
<iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_8cc0f&symbol=BINANCE:BTCUSDT&interval=1&symboledit=1&saveimage=1&toolbarbg=F1F3F6&studies=[]&theme=dark&style=1&timezone=Asia/Karachi&withdateranges=1&hide_side_toolbar=0&allow_symbol_change=1&details=1&hotlist=1&calendar=1&show_popup_button=1&locale=ur" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", unsafe_allow_html=True)

# CSS for blinking lights
st.markdown("""
<style>
.blink {
  animation: blinker 1s linear infinite;
  font-weight: bold;
}
@keyframes blinker {
  50% { opacity: 0; }
}
</style>
""", unsafe_allow_html=True)

# Get Top 10 Coins from CoinMarketCap
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
params = {
    'start': '1',
    'limit': '10',
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# Dummy signal function (replace with actual AI logic if needed)
def get_signal(price_change):
    if price_change > 2:
        return 'buy'
    elif price_change < -2:
        return 'sell'
    else:
        return 'hold'

# Display each coin with AI suggestion
for coin in data['data']:
    name = coin['name']
    symbol = coin['symbol']
    price = round(coin['quote']['USD']['price'], 4)
    change = round(coin['quote']['USD']['percent_change_24h'], 2)
    signal = get_signal(change)

    # Traffic Light Display
    if signal == 'buy':
        st.markdown(f"<span class='blink' style='color:green;'>🟢 {name} خریداری کا موقع ہے</span>", unsafe_allow_html=True)
    elif signal == 'sell':
        st.markdown(f"<span class='blink' style='color:red;'>🔴 {name} فروخت کا وقت ہے</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span class='blink' style='color:orange;'>🟡 {name} انتظار کریں</span>", unsafe_allow_html=True)

    # Coin Info Summary
    st.write(f"**{name} ({symbol})**")
    st.write(f"قیمت: ${price} |  24 گھنٹے تبدیلی: {change}%")
    st.markdown("---")
    
