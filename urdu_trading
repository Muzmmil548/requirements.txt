# urdu_trading_ai_chart_app.py
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from streamlit.components.v1 import iframe

# ---------------- Chart Pattern Detection ----------------
def detect_all_patterns(df):
    patterns = []
    close = df['close'].values

    def check_double_top():
        if len(close) < 10:
            return False
        return close[-1] < close[-3] and abs(close[-3] - close[-6]) < 0.5

    def check_double_bottom():
        if len(close) < 10:
            return False
        return close[-1] > close[-3] and abs(close[-3] - close[-6]) < 0.5

    def check_head_and_shoulders():
        if len(close) < 7:
            return False
        return close[-4] > close[-5] and close[-4] > close[-3] and close[-2] < close[-3]

    def check_triple_top():
        if len(close) < 15:
            return False
        return abs(close[-3] - close[-6]) < 0.5 and abs(close[-3] - close[-9]) < 0.5

    def check_ascending_triangle():
        if len(close) < 6:
            return False
        return close[-1] > close[-2] and close[-2] > close[-3] and close[-4] > close[-5]

    if check_double_top():
        patterns.append("Double Top")
    if check_double_bottom():
        patterns.append("Double Bottom")
    if check_head_and_shoulders():
        patterns.append("Head & Shoulders")
    if check_triple_top():
        patterns.append("Triple Top")
    if check_ascending_triangle():
        patterns.append("Ascending Triangle")

    return patterns

# ---------------- Market Sentiment Based on Patterns ----------------
def analyze_sentiment(patterns):
    sentiment = {"Buy": 0, "Sell": 0, "Neutral": 0}
    for p in patterns:
        if p in ["Double Bottom", "Ascending Triangle"]:
            sentiment["Buy"] += 1
        elif p in ["Double Top", "Head & Shoulders", "Triple Top"]:
            sentiment["Sell"] += 1
        else:
            sentiment["Neutral"] += 1
    return sentiment

# ---------------- Binance OHLCV Fetch ----------------
def fetch_ohlcv(symbol="BTCUSDT", interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Binance سے ڈیٹا حاصل نہیں ہو سکا")
        return pd.DataFrame()
    
    data = response.json()
    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close']].astype(float)
    return df

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="📊 Urdu AI Chart App", layout="wide")
st.title("📊 اردو اے آئی چارٹ اسسٹنٹ")
st.markdown("✅ ٹائم فریم: **1H**, **4H**, **1D** | ⚠️ Scalping (1m/5m) Supported نہیں ہے")

# --- Inputs ---
symbol = st.selectbox("🪙 کرپٹو کوائن منتخب کریں:", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"])
interval = st.selectbox("⏱️ ٹائم فریم منتخب کریں:", ["1h", "4h", "1d"])

# --- Fetch Data & Chart ---
df = fetch_ohlcv(symbol, interval)
if not df.empty:
    st.subheader("📉 لائیو ٹریڈنگ ویو چارٹ:")
    iframe(f"https://s.tradingview.com/widgetembed/?symbol=BINANCE:{symbol}&interval={interval.upper()}&theme=dark", height=500)

    st.subheader("🧠 پیٹرن ڈیٹیکشن:")
    detected = detect_all_patterns(df)

    if detected:
        st.success("✅ مندرجہ ذیل پیٹرن ملے ہیں:")
        for p in detected:
            st.markdown(f"🔍 **{p}** pattern")
    else:
        st.warning("😕 اس وقت کوئی پیٹرن نہیں ملا۔")

    # --- Sentiment Analysis ---
    sentiment = analyze_sentiment(detected)
    st.subheader("📊 مارکیٹ سینٹیمنٹ:")
    st.markdown(f"🟢 **Buy Signals:** {sentiment['Buy']}")
    st.markdown(f"🔴 **Sell Signals:** {sentiment['Sell']}")
    st.markdown(f"🟡 **Neutral:** {sentiment['Neutral']}")

    # --- Light Blinking Indicator ---
    st.subheader("🚦 سگنل لائٹ:")
    if sentiment["Buy"] > sentiment["Sell"]:
        st.markdown("🟢 **BUY ZONE**")
    elif sentiment["Sell"] > sentiment["Buy"]:
        st.markdown("🔴 **SELL ZONE**")
    else:
        st.markdown("🟡 **NEUTRAL ZONE**")
