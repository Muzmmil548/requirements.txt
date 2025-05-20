import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="اردو پروفیشنل ٹریڈنگ اسسٹنٹ", layout="wide")

st.title("اردو پروفیشنل ٹریڈنگ اسسٹنٹ")
st.markdown("CoinGecko API کے ذریعے تازہ تجزیہ، AI سگنلز، اور چارٹ پیٹرن")

# Refresh Button
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()

# Select number of coins
option = st.selectbox("کتنے سکہ دیکھنا چاہتے ہیں؟", ["Top 10", "Top 50"])
per_page = 10 if option == "Top 10" else 50

# Get data
url = f"https://api.coingecko.com/api/v3/coins/markets"
params = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc',
    'per_page': per_page,
    'page': 1,
    'sparkline': 'true',
    'price_change_percentage': '1h,24h,7d'
}
response = requests.get(url, params=params)
data = response.json()

# Show one central TradingView chart
selected_coin = st.selectbox("کوائن چارٹ دیکھیں:", [coin['symbol'].upper() for coin in data])
st.components.v1.html(f"""
    <iframe src="https://www.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE%3A{selected_coin}USDT&interval=15&hidesidetoolbar=1&symboledit=1&saveimage=1&toolbarbg=F1F3F6&studies=[]&theme=dark&style=1&timezone=exchange" width="100%" height="500" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
""", height=500)

# Show analysis
for coin in data:
    st.subheader(f"{coin['name']} ({coin['symbol'].upper()})")

    # AI Signal
    p1h = coin.get('price_change_percentage_1h_in_currency', 0)
    p24h = coin.get('price_change_percentage_24h_in_currency', 0)
    if p1h > 1 and p24h > 3:
        signal = "🟢 خریدنے کا اشارہ"
    elif p1h < -1 and p24h < -3:
        signal = "🔴 فروخت کا اشارہ"
    else:
        signal = "🟡 انتظار کریں"

    st.markdown(f"**AI سگنل:** {signal}")

    # Pattern Detection (basic)
    try:
        spark = coin['sparkline_in_7d']['price']
        if len(spark) >= 10:
            if spark[0] < spark[5] and spark[5] > spark[-1] and spark[0] < spark[-1]:
                st.markdown("**پیٹرن ڈیٹیکٹ ہوا: Head & Shoulders**")
    except:
        pass

    st.markdown(f"""
    **قیمت:** ${coin['current_price']}  
    **1h تبدیلی:** {p1h:.2f}%  
    **24h تبدیلی:** {p24h:.2f}%  
    **7d تبدیلی:** {coin.get('price_change_percentage_7d_in_currency', 0):.2f}%
    """)
    st.markdown("---")
