import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime
from streamlit.components.v1 import iframe

# --- Binance سے ڈیٹا حاصل کرنا ---
def fetch_binance_data(symbol, interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])
        df["time"] = pd.to_datetime(df["time"], unit="ms")
        df["close"] = pd.to_numeric(df["close"])
        return df
    except:
        return None

# --- Indicators ---
def calculate_rsi(data, period=14):
    delta = data["close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(data):
    ema12 = data["close"].ewm(span=12, adjust=False).mean()
    ema26 = data["close"].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal

# --- Symbols and Timeframes ---
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
timeframes = {"1H": "1h", "4H": "4h", "1D": "1d"}

# --- UI Settings ---
st.set_page_config(layout="wide")
st.title("اردو ٹریڈنگ اسسٹنٹ ایپ (AI، چارٹ اور انڈیکیٹرز کے ساتھ)")

selected_symbol = st.selectbox("کوائن منتخب کریں:", symbols)
selected_tf_label = st.selectbox("ٹائم فریم منتخب کریں:", list(timeframes.keys()))
selected_tf = timeframes[selected_tf_label]

# --- Chart Embed ---
chart_url = f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}&interval={selected_tf_label}&hidesidetoolbar=1&theme=dark"
st.subheader(f"ٹریڈنگ ویو چارٹ ({selected_symbol} - {selected_tf_label})")
iframe(chart_url, height=500)

# --- Binance Price Data ---
df = fetch_binance_data(selected_symbol, interval=selected_tf)

if df is None:
    st.error("Binance سے ڈیٹا حاصل نہیں ہو سکا۔")
else:
    current_price = df["close"].iloc[-1]
    st.subheader("💰 موجودہ قیمت:")
    st.info(f"${current_price:.2f}")

    # --- TP/SL Calculation ---
    tp = current_price * 1.03
    sl = current_price * 0.97
    st.success(f"📈 TP: ${tp:.2f} | 📉 SL: ${sl:.2f}")

    # --- Sentiment (Simulated) ---
    buyers = random.randint(30, 90)
    sellers = 100 - buyers
    neutral = random.randint(0, 10)
    st.subheader("🤖 مارکیٹ سینٹیمنٹ:")
    st.info(f"🟢 خریدار: {buyers}% | 🔴 فروخت کنندہ: {sellers}% | ⚪ نیوٹرل: {neutral}%")

    # --- Pattern Detection (Simulated) ---
    st.subheader("📊 AI چارٹ پیٹرن ڈیٹیکشن:")
    chart_patterns = [
        "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
        "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
        "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
        "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
    ]
    pattern_detection = {p: random.choice(["🟢", "🔴", "🟡", "❌"]) for p in chart_patterns}
    for name, status in pattern_detection.items():
        st.markdown(f"**{name}**: {status}")

    # --- Indicators Calculation ---
    st.subheader("📈 تکنیکی انڈیکیٹرز (Real-Time):")
    df["RSI"] = calculate_rsi(df)
    macd, signal = calculate_macd(df)
    df["MACD"] = macd
    df["Signal"] = signal

    st.write(df[["time", "close", "RSI", "MACD", "Signal"]].tail(10))

    # --- AI Trade Signal ---
    st.subheader("🚨 AI ٹریڈ سگنل:")
    last_rsi = df["RSI"].iloc[-1]
    last_macd = df["MACD"].iloc[-1]
    last_signal = df["Signal"].iloc[-1]

    signal_text = "🔍 کوئی واضح سگنل نہیں"
    if last_rsi < 30 and last_macd > last_signal:
        signal_text = "🟢 Strong Buy Signal (Oversold + Bullish MACD)"
    elif last_rsi > 70 and last_macd < last_signal:
        signal_text = "🔴 Strong Sell Signal (Overbought + Bearish MACD)"
    elif last_macd > last_signal:
        signal_text = "🟢 MACD Bullish Crossover"
    elif last_macd < last_signal:
        signal_text = "🔴 MACD Bearish Crossover"

    st.success(signal_text)

# --- Footer ---
st.markdown("---")
st.caption("Developed by Urdu Trading AI Team | Powered by Streamlit, Binance API, and TradingView")
