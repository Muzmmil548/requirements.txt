import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests
import pandas as pd
import datetime
import plotly.graph_objs as go

# ✅ Page Config (یہ سب سے اوپر ہونا چاہیے)
st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

# ✅ Auto-refresh (ہر 30 سیکنڈ میں)
st_autorefresh(interval=10 * 1000, key="refresh")

# ✅ ہیڈر
st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators)")
st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

# ✅ Top 50 Symbols from Binance
@st.cache_data(ttl=600)
def get_top_50_symbols():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        data = response.json()
        usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:50]]
    except Exception as e:
        return []

symbols = get_top_50_symbols()

if not symbols:
    st.error("Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔")
    st.stop()

# ✅ Coin Selector
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

# ✅ TradingView Chart with Indicator View
with st.expander("📺 Live Indicator Chart (TradingView)"):
    st.components.v1.iframe(
        f"https://www.tradingview.com/chart/?symbol=BINANCE:{selected_symbol}",
        height=500, scrolling=True
    )

# ✅ Get Live Price
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url).json()['price'])

# ✅ Get Order Book
def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    data = requests.get(url).json()
    bid_vol = sum([float(x[1]) for x in data['bids']])
    ask_vol = sum([float(x[1]) for x in data['asks']])
    return bid_vol, ask_vol

# ✅ Get Recent Trades
def get_trades(symbol):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100"
    trades = requests.get(url).json()
    buyers = sum(1 for t in trades if not t['isBuyerMaker'])
    sellers = sum(1 for t in trades if t['isBuyerMaker'])
    return buyers, sellers

# ✅ AI Signal Logic
def ai_signal(bid, ask, buyers, sellers):
    effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    if dominancy == "Buyers" and effort < 10:
        return "🟢 Buy (Long)"
    elif dominancy == "Sellers" and effort < 10:
        return "🔴 Sell (Short)"
    else:
        return "🟡 Wait"

# ✅ Get All Data
try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    signal = ai_signal(bid_volume, ask_volume, buyers, sellers)
except:
    st.error("📡 Binance API سے ڈیٹا حاصل نہیں ہو سکا")
    st.stop()

# ✅ Display All Info
st.markdown("---")
st.subheader("📊 Real-Time Smart Money Metrics")

info = {
    "🟡 Price": f"${price:.2f}",
    "📥 Bid Volume": round(bid_volume, 2),
    "📤 Ask Volume": round(ask_volume, 2),
    "🟢 Buyers": buyers,
    "🔴 Sellers": sellers,
    "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers",
    "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2),
    "🤖 AI Signal": signal
}

for label, val in info.items():
    st.markdown(f"<div style='font-size:20px; background-color:#111; color:white; padding:8px; margin-bottom:5px;'> <b>{label}</b>: {val}</div>", unsafe_allow_html=True)

# ✅ Plotly Candlestick Chart
with st.expander("🕯️ 1 منٹ کا Candle Chart (Binance)"):
    end_time = int(datetime.datetime.now().timestamp() * 1000)
    start_time = end_time - (60 * 60 * 1000)  # پچھلے 1 گھنٹے کے candles

    url = f"https://api.binance.com/api/v3/klines?symbol={selected_symbol}&interval=1m&startTime={start_time}&endTime={end_time}&limit=60"
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'num_trades',
        'taker_buy_base_vol', 'taker_buy_quote_vol', 'ignore'
    ])
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    fig = go.Figure(data=[go.Candlestick(
        x=df['time'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name="Candles"
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ ایپ مکمل اور کامیابی سے چل رہی ہے۔")
