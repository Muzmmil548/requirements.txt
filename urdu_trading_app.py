import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIG ---
st.set_page_config(page_title="اردو پرو ٹریڈنگ ایپ", layout="wide")

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: green;'>اردو پروفیشنل ٹریڈنگ ایپ</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- SIDEBAR: Exchange Toggle Buttons ---
st.sidebar.markdown("### ایکسچینج منتخب کریں:")
binance_on = st.sidebar.checkbox("Binance", value=True)
bybit_on = st.sidebar.checkbox("Bybit", value=False)
cme_on = st.sidebar.checkbox("CME", value=False)
bitget_on = st.sidebar.checkbox("Bitget", value=False)
kucoin_on = st.sidebar.checkbox("KuCoin", value=False)
mexc_on = st.sidebar.checkbox("MEXC", value=False)
okx_on = st.sidebar.checkbox("OKX", value=False)

# --- Timeframe Dropdown ---
timeframe = st.sidebar.selectbox("ٹائم فریم منتخب کریں", ["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"])

# --- TradingView Chart Function ---
def display_tradingview_chart(exchange, symbol, interval="1m"):
    st.markdown(f"""
    <div class="tradingview-widget-container">
        <div id="tradingview_{exchange}_{symbol}"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({
        "width": 800,
        "height": 600,
        "symbol": "{exchange}:{symbol}",
        "interval": "{interval}",
        "timezone": "Asia/Karachi",
        "theme": "light",
        "style": "1",
        "locale": "en",
        "toolbar_bg": "#f1f3f6",
        "hide_top_toolbar": true
        });
        </script>
    </div>
    """, unsafe_allow_html=True)

# --- Fetch Binance Data for Heatmap ---
def fetch_binance_heatmap_data():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df['symbol'] = df['symbol'].apply(lambda x: x if x.endswith('USDT') else None)
    df = df.dropna(subset=['symbol'])
    df['priceChangePercent'] = df['priceChangePercent'].astype(float)
    return df[['symbol', 'priceChangePercent']]

# --- Plot Market Heatmap ---
def plot_heatmap():
    data = fetch_binance_heatmap_data()
    data = data.set_index('symbol').sort_values('priceChangePercent', ascending=False)

    # Create heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(data[['priceChangePercent']].T, annot=True, cmap="RdYlGn", cbar=True, ax=ax)
    st.pyplot(fig)

# --- Display Exchange Charts ---
if binance_on:
    symbol = "BTCUSDT"
    st.markdown(f"### Binance - {symbol}")
    display_tradingview_chart("BINANCE", symbol, timeframe)

if bybit_on:
    symbol = "BTCUSDT"
    st.markdown(f"### Bybit - {symbol}")
    display_tradingview_chart("BYBIT", symbol, timeframe)

if cme_on:
    symbol = "BTCUSD"
    st.markdown(f"### CME - {symbol}")
    display_tradingview_chart("CME", symbol, timeframe)

if bitget_on:
    symbol = "BTCUSDT"
    st.markdown(f"### Bitget - {symbol}")
    display_tradingview_chart("BITGET", symbol, timeframe)

if kucoin_on:
    symbol = "BTC-USDT"
    st.markdown(f"### KuCoin - {symbol}")
    display_tradingview_chart("KUCOIN", symbol, timeframe)

if mexc_on:
    symbol = "BTC_USDT"
    st.markdown(f"### MEXC - {symbol}")
    display_tradingview_chart("MEXC", symbol, timeframe)

if okx_on:
    symbol = "BTC-USDT"
    st.markdown(f"### OKX - {symbol}")
    display_tradingview_chart("OKX", symbol, timeframe)

# --- Display Market Heatmap ---
st.subheader("Market Heatmap")
plot_heatmap()

# --- Placeholder for Depth of Market (DOM) ---
st.subheader("Depth of Market (DOM) Placeholder")
st.info("DOM فیچر جلد شامل کیا جائے گا۔")

# --- Auto Traffic Light System (Green/Yellow/Red) ---
def display_traffic_light(price_change_percentage):
    if price_change_percentage > 5:
        color = "green"
    elif -5 <= price_change_percentage <= 5:
        color = "yellow"
    else:
        color = "red"
    
    st.markdown(f"<h2 style='color: {color};'>Price Change: {price_change_percentage}%</h2>", unsafe_allow_html=True)

# --- Example: Display Traffic Light for Binance ---
if binance_on:
    data = fetch_binance_heatmap_data()
    display_traffic_light(data['priceChangePercent'].iloc[0])

# --- 6 Trading Indicators ---
st.subheader("6 Trading Indicators (Indicators like RSI, MACD, etc.)")
st.markdown("""
- **RSI (Relative Strength Index)**
- **MACD (Moving Average Convergence Divergence)**
- **SMA (Simple Moving Average)**
- **EMA (Exponential Moving Average)**
- **Bollinger Bands**
- **Stochastic Oscillator**
""")
