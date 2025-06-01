import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import time

# سب سے پہلے صفحے کی ترتیب
st.set_page_config(page_title="Urdu Trading AI", layout="wide")

# آٹو ریفریش ہر 60 سیکنڈ
st_autorefresh(interval=60 * 1000, key="datarefresh")

# CoinMarketCap API Key یہاں ڈالیں
CMC_API_KEY = "🔑YOUR_NEW_API_KEY_HERE"  # ← یہاں اپنی نئی Key لگائیں

# ---------------------------------------------
# فنکشن: لائیو ڈیٹا حاصل کریں
def get_crypto_data(symbol="BTC"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"symbol": symbol, "convert": "USD"}
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data["data"][symbol]["quote"]["USD"]
    except Exception as e:
        st.error(f"ڈیٹا حاصل نہیں ہوا: {e}")
        return None

# ---------------------------------------------
# فنکشن: سگنل تجزیہ
def get_signal(price_change_percent):
    if price_change_percent > 1.5:
        return "🟢 Buy", "green"
    elif price_change_percent < -1.5:
        return "🔴 Sell", "red"
    else:
        return "🟡 Neutral", "yellow"

# ---------------------------------------------
# فنکشن: بلنکنگ لائٹ HTML
def blinking_text(text, color):
    return f"""<marquee direction="left" scrollamount="5">
    <span style='color:{color}; font-size:26px; font-weight:bold;'>{text}</span></marquee>"""

# ---------------------------------------------
# UI سیکشن
st.title("💹 Urdu AI Trading Assistant with CMC Live Data")

coin = st.selectbox("🪙 کرپٹو سلیکٹ کریں:", ["BTC", "ETH", "BNB", "SOL", "ADA", "XRP", "DOGE"])

data = get_crypto_data(coin)

if data:
    st.metric(label="💵 Live Price", value=f"${data['price']:.2f}")
    st.metric(label="📉 1h % Change", value=f"{data['percent_change_1h']:.2f}%")
    st.metric(label="📈 24h % Change", value=f"{data['percent_change_24h']:.2f}%")

    # سگنل
    signal, color = get_signal(data['percent_change_1h'])
    st.markdown(blinking_text(f"{signal} Signal", color), unsafe_allow_html=True)

    # چارٹ پیٹرن سرخی
    st.subheader("📊 چارٹ پیٹرن کی پہچان (Demo Headers)")
    patterns = ["Head & Shoulders", "Double Top", "Double Bottom", "Triangle", "Flag", "Wedge", 
                "Cup & Handle", "Rounding Bottom", "Triple Top", "Triple Bottom",
                "Ascending Triangle", "Descending Triangle", "Symmetrical Triangle", "Rectangle", "Pennant"]
    cols = st.columns(5)
    for i, pattern in enumerate(patterns):
        with cols[i % 5]:
            st.info(f"📐 {pattern}")

    # 6 انڈیکیٹرز (ڈیجیٹل ڈسپلے)
    st.subheader("📟 Indicators")
    st.success("RSI: 53.2")
    st.success("MACD: Bullish")
    st.success("Stochastic: Neutral")
    st.success("Volume: High")
    st.success("MA Crossover: No")
    st.success("VWAP: Above")
else:
    st.warning("ڈیٹا دستیاب نہیں۔ براہ کرم API Key چیک کریں۔")
