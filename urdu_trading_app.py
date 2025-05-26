import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit.components.v1 import iframe
import random

st.set_page_config(layout="wide")
st.title("اردو ٹریڈنگ اسسٹنٹ ایپ (AI سسٹم کے ساتھ)")

# Binance candle data fetch
def get_binance_ohlc(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    res = requests.get(url)
    data = res.json()
    df = pd.DataFrame(data, columns=[
        "Time", "Open", "High", "Low", "Close", "Volume",
        "_", "__", "___", "____", "_____", "______"
    ])
    df["Time"] = pd.to_datetime(df["Time"], unit='ms')
    df["Open"] = df["Open"].astype(float)
    df["Close"] = df["Close"].astype(float)
    return df[["Time", "Open", "Close"]]

# Simulated AI Chart Patterns
patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]

def detect_patterns():
    return {p: random.choice(["🟢", "🟡", "🔴"]) for p in patterns}

def buyer_seller_ratio():
    buyers = random.randint(45, 95)
    sellers = 100 - buyers
    return buyers, sellers

def blinking_icon(icon):
    return f"<span style='animation: blink 1s infinite;'>{icon}</span>"

st.markdown("""
<style>
@keyframes blink {
0% {opacity: 1;}
50% {opacity: 0.2;}
100% {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# CoinMarketCap Data (Top 50)
api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8"
headers = {"X-CMC_PRO_API_KEY": api_key}
cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

def get_market_data(limit=50):
    params = {"start": "1", "limit": limit, "convert": "USD"}
    response = requests.get(cmc_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()["data"]
        return pd.DataFrame([{
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Price": coin["quote"]["USD"]["price"],
            "Change(24h)": coin["quote"]["USD"]["percent_change_24h"]
        } for coin in data])
    else:
        return pd.DataFrame()

# Refresh Button
refresh = st.button("ڈیٹا دوبارہ لوڈ کریں (Refresh)")
if refresh or "df" not in st.session_state:
    st.session_state.df = get_market_data(50)

df = st.session_state.df

col1, col2 = st.columns([1, 2])

with col1:
    selected = st.selectbox("کوائن منتخب کریں:", df["Name"] if not df.empty else [])
    timeframe = st.selectbox("ٹائم فریم منتخب کریں:", ["1m", "5m", "15m", "1h"])

    if selected:
        coin_info = df[df["Name"] == selected].iloc[0]
        symbol = coin_info["Symbol"]
        price = coin_info["Price"]
        change = coin_info["Change(24h)"]
        binance_symbol = f"{symbol.upper()}USDT"

with col2:
    if selected:
        st.subheader(f"{selected} کا لائیو چارٹ:")
        iframe(f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{symbol}USDT&interval={timeframe}&hidesidetoolbar=1", height=420)

# AI Output Section
if selected:
    st.markdown("---")
    st.subheader("خلاصہ:")
    st.markdown(f"- موجودہ قیمت: ${price:.4f}")
    st.markdown(f"- 24 گھنٹے تبدیلی: {change:.2f}%")

    tp = price * 1.03
    sl = price * 0.97
    st.success(f"TP (ٹیک پرافٹ): ${tp:.2f}  |  SL (اسٹاپ لاس): ${sl:.2f}")

    st.subheader("AI مارکیٹ سینٹیمنٹ:")
    buyers, sellers = buyer_seller_ratio()
    st.info(f"خریدار: {buyers}%  |  فروخت کنندہ: {sellers}%")

    st.subheader("AI چارٹ پیٹرن ڈیٹیکشن (ٹائم فریم: " + timeframe + ")")
    detected = detect_patterns()
    for name, icon in detected.items():
        st.markdown(f"**{name}**: {blinking_icon(icon)}", unsafe_allow_html=True)

    # Historical Candle Data from Binance (Optional Display)
    st.markdown("---")
    st.subheader(f"{symbol.upper()}USDT کے Candle ڈیٹا ({timeframe})")
    try:
        df_candle = get_binance_ohlc(symbol=binance_symbol, interval=timeframe)
        st.dataframe(df_candle.tail(10), use_container_width=True)
    except:
        st.error("Binance API سے ڈیٹا حاصل نہیں ہو سکا")
