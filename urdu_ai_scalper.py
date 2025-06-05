import streamlit as st  
from streamlit_autorefresh import st_autorefresh  
import pandas as pd  
import random  
import requests  
import numpy as np
from datetime import datetime  
from streamlit.components.v1 import iframe  
  
# --- AI Mini Logic Function ---
def ai_mini_decision_logic(prices, indicators):
    """
    🧠 Mini AI logic for trading decision making using Calculus, Probability & Algebra.
    
    Inputs:
    - prices: list or array of recent closing prices
    - indicators: dict of indicator values like RSI, MACD, EMA etc

    Returns:
    - final_decision (str): 🟢 / 🟡 / 🔴
    - urdu_message (str): اردو میں مشورہ
    """
    # --- Calculus: Trend Detection via Derivative (slope)
    slope = np.polyfit(range(len(prices[-5:])), prices[-5:], 1)[0]  # recent trend slope
    
    # --- Algebra: Weighted Score from indicators
    weights = {
        'RSI': 0.3,
        'MACD': 0.3,
        'EMA_Cross': 0.4
    }
    # Normalize RSI around 50, so RSI close to 50 means neutral
    rsi_score = (100 - abs(indicators.get('RSI', 50) - 50)) / 50  
    macd_score = indicators.get('MACD', 0)  # assume +1 or -1 for bullish/bearish
    ema_cross_score = indicators.get('EMA_Cross', 0)  # 1 or -1
    
    score = (rsi_score * weights['RSI'] +
             macd_score * weights['MACD'] +
             ema_cross_score * weights['EMA_Cross'])
    
    # --- Probability: confidence % estimate
    confidence = min(100, max(0, 50 + (score * 20) + (slope * 10)))

    # --- Urdu Signal Decision
    if confidence > 70:
        return "🟢", f"اعتماد: {confidence:.1f}% - مارکیٹ مثبت لگ رہی ہے، خریداری کا موقع"
    elif confidence < 40:
        return "🔴", f"اعتماد: {confidence:.1f}% - مارکیٹ کمزور ہے، فروخت یا انتظار بہتر ہے"
    else:
        return "🟡", f"اعتماد: {confidence:.1f}% - مارکیٹ غیر یقینی ہے، محتاط رہیں یا انتظار کریں"


# ================= Main Streamlit App =================

# ✅ Page Config  
st.set_page_config(layout="wide")  
st_autorefresh(interval=60 * 1000, key="datarefresh")  
st.title("📊 اردو ٹریڈنگ اسسٹنٹ (AI چارٹ اور سگنلز کے ساتھ)")  
  
# ✅ Coin Selection  
symbols = ["BTC", "ETH", "BNB", "SOL", "XRP"]  
selected_symbol = st.selectbox("کوائن منتخب کریں:", symbols)  
  
# ✅ Timeframe Selection  
timeframes = {"1m": "1", "5m": "5", "15m": "15", "1h": "60", "4h": "240", "1d": "D"}  
selected_tf = st.selectbox("⏱️ ٹائم فریم منتخب کریں:", options=list(timeframes.keys()), index=3)  
  
# ✅ TradingView Chart with timeframe  
tv_url = f"https://www.tradingview.com/widgetembed/?symbol=BINANCE:{selected_symbol}USDT&interval={timeframes[selected_tf]}&hidesidetoolbar=1&theme=dark"  
st.subheader(f"📈 لائیو چارٹ: {selected_symbol}USDT ({selected_tf})")  
iframe(tv_url, height=500)  
  
# ✅ Price Fetch  
api_key = "9fee371c-217b-49cd-988a-5c0829ae1ea8"  
url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={selected_symbol}&convert=USD"  
headers = {"X-CMC_PRO_API_KEY": api_key}  
response = requests.get(url, headers=headers)  
price = response.json()["data"][selected_symbol]["quote"]["USD"]["price"]  
price = round(price, 2)  
  
st.markdown("---")  
st.subheader("💰 موجودہ قیمت اور تجزیہ")  
  
# ✅ TP/SL Box  
tp = price * 1.03  
sl = price * 0.97  
tp_sl_box = f"""  
<div style='background-color:#f9f9f9; padding:15px; border-radius:10px; border:1px solid #ccc; font-size:18px'>  
<b>🎯 ٹیک پرافٹ (TP):</b> <span style='color:green;'>${tp:.2f}</span> <br>  
<b>⛔ اسٹاپ لاس (SL):</b> <span style='color:red;'>${sl:.2f}</span>  
</div>  
"""  
st.markdown(tp_sl_box, unsafe_allow_html=True)  
  
# ---------------- AI Mini Logic Usage -------------------

# For demo purpose, we simulate some indicator values  
# In your real app, replace this with actual indicator calculations  
indicators = {
    "RSI": random.uniform(30, 70),       # RSI between 30-70  
    "MACD": random.choice([-1, 1]),      # Bullish or Bearish  
    "EMA_Cross": random.choice([-1, 1])  # Bullish or Bearish cross  
}

# Simulate price history for slope calculation (last 10 prices with small random changes)
prices = [price + random.uniform(-1, 1) for _ in range(10)]

ai_signal, ai_message = ai_mini_decision_logic(prices, indicators)

st.markdown("---")  
st.subheader("🤖 AI Mini Logic ٹریڈ سگنل:")  

def blinking_html(text, color):  
    return f"""  
    <div style='animation: blinker 1s linear infinite; color:{color}; font-size:24px; font-weight:bold;'>  
        {text}  
    </div>  
    <style>  
    @keyframes blinker {{ 50% {{ opacity: 0; }} }}  
    </style>  
    """  

color_map = {"🟢": "green", "🟡": "orange", "🔴": "red"}  
st.markdown(blinking_html(f"📍 سگنل: {ai_signal} - {ai_message}", color_map[ai_signal]), unsafe_allow_html=True)  
  
# ================= Original Code Continues ===================

# ✅ Market Sentiment  
buyers = random.randint(40, 70)  
sellers = 100 - buyers  
neutral = random.randint(0, 10)  
sentiment_box = f"""  
<div style='background-color:#eaf4ff; padding:15px; border-radius:10px; border:1px solid #b3d4fc; font-size:18px'>  
<h4>🤖 AI مارکیٹ سینٹیمنٹ</h4>  
🟢 <b>خریدار:</b> {buyers}%<br>  
🔴 <b>فروخت کنندہ:</b> {sellers}%<br>  
⚪ <b>نیوٹرل:</b> {neutral}%  
</div>  
"""  
st.markdown(sentiment_box, unsafe_allow_html=True)  
  
# ✅ AI Signal  
signal = "🟢 Buy" if buyers > sellers else "🔴 Sell" if sellers > buyers else "🟡 Hold"  
color = "green" if signal == "🟢 Buy" else "red" if signal == "🔴 Sell" else "orange"  
  
st.markdown("### 📢 AI ٹریڈ سگنل:")  
st.markdown(blinking_html(f"📍 سگنل: {signal}", color), unsafe_allow_html=True)  
  
# ✅ Chart Patterns  
chart_patterns = [  
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",  
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",  
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",  
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"  
]  
  
# ✅ Pattern Valid Timeframes  
pattern_timeframes = {  
    "Head & Shoulders": ["1h", "4h", "1d"],  
    "Inverse H&S": ["1h", "4h", "1d"],  
    "Double Top": ["1h", "4h"],  
    "Double Bottom": ["1h", "4h"],  
    "Symmetrical Triangle": ["1h", "4h"],  
    "Ascending Triangle": ["1h", "4h"],  
    "Descending Triangle": ["1h", "4h"],  
    "Falling Wedge": ["1h", "4h", "1d"],  
    "Rising Wedge": ["1h", "4h", "1d"],  
    "Cup & Handle": ["4h", "1d"],  
    "Bullish Flag": ["1h", "4h"],  
    "Bearish Flag": ["1h", "4h"],  
    "Rectangle": ["1h", "4h"],  
    "Triple Top": ["1h", "4h"],  
    "Triple Bottom": ["1h", "4h"]  
}  
  
# ✅ Pattern Simulation with TF Check  
def simulate_patterns_with_tf(selected_tf):  
    results = {}  
    for pattern in chart_patterns:  
        allowed_tfs = pattern_timeframes.get(pattern, [])  
        if selected_tf in allowed_tfs:  
            results[pattern] = random.choice(["🟢", "🔴", "🟡"])  
        else:  
            results[pattern] = "❌"  
    return results  
  
# ✅ Display Patterns  
st.markdown("---")  
st.subheader("📊 چارٹ پیٹرن ڈیٹیکشن:")  
patterns = simulate_patterns_with_tf(selected_tf)  
for pattern, signal in patterns.items():  
    st.markdown(f"{pattern}: {signal}")  
  
# ✅ Footer  
st.markdown("---")  
st.caption("Developed by Urdu Trading AI | Auto Refreshed | Powered by Streamlit")
