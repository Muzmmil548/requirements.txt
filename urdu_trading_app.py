import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit.components.v1 import html

st.set_page_config(layout="wide")

st.title("Professional Trading Assistant App")

# Exchange toggle section
st.sidebar.header("Select Exchanges")
exchanges = {
    "Binance": st.sidebar.toggle("Binance"),
    "Bybit": st.sidebar.toggle("Bybit"),
    "CME": st.sidebar.toggle("CME"),
    "Bitget": st.sidebar.toggle("Bitget"),
    "KuCoin": st.sidebar.toggle("KuCoin"),
    "MEXC": st.sidebar.toggle("MEXC"),
    "OKX": st.sidebar.toggle("OKX")
}

# Sample price fetcher for Binance
@st.cache_data(ttl=60)
def fetch_binance_data(symbol="BTCUSDT", interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = pd.DataFrame(response.json(), columns=[
        'Time', 'Open', 'High', 'Low', 'Close', 'Volume',
        'CloseTime', 'QuoteAssetVolume', 'NumTrades', 'TakerBuyBaseVol',
        'TakerBuyQuoteVol', 'Ignore'
    ])
    data['Time'] = pd.to_datetime(data['Time'], unit='ms')
    data['Close'] = pd.to_numeric(data['Close'])
    return data[['Time', 'Close']]

# Indicator Calculation
def calculate_indicators(df):
    df['EMA'] = df['Close'].ewm(span=10).mean()
    delta = df['Close'].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean()
    df['Signal'] = df['MACD'].ewm(span=9).mean()
    df['BB_upper'] = df['Close'].rolling(20).mean() + 2 * df['Close'].rolling(20).std()
    df['BB_lower'] = df['Close'].rolling(20).mean() - 2 * df['Close'].rolling(20).std()
    df['VWAP'] = df['Close'].expanding().mean()
    return df

# Auto traffic light system
def get_traffic_signal(rsi):
    if rsi > 70:
        return "Red"
    elif rsi < 30:
        return "Green"
    else:
        return "Yellow"

# Main chart and analysis
if exchanges["Binance"]:
    st.subheader("Binance Live Chart with Indicators")
    df = fetch_binance_data()
    df = calculate_indicators(df)
    
    # Display chart
    fig, ax = plt.subplots()
    ax.plot(df['Time'], df['Close'], label='Price')
    ax.plot(df['Time'], df['EMA'], label='EMA')
    ax.fill_between(df['Time'], df['BB_upper'], df['BB_lower'], alpha=0.2, label='Bollinger Bands')
    ax.set_title("Price with Indicators")
    ax.legend()
    st.pyplot(fig)
    
    # Traffic signal
    signal = get_traffic_signal(df['RSI'].iloc[-1])
    st.success(f"Current Market Signal: {signal}")

# Market Heatmap placeholder
st.subheader("Market Heatmap")
heatmap_data = pd.DataFrame({
    'Token': ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'DOGE', 'ADA', 'AVAX', 'MATIC', 'DOT'],
    'Change': [2, -1, 0.5, -3, 4, 1.5, -0.2, 3, -1.2, 0.7]
})
heatmap_pivot = heatmap_data.pivot_table(values='Change', index='Token', aggfunc='sum')
fig, ax = plt.subplots()
sns.heatmap(heatmap_pivot, annot=True, cmap='RdYlGn', center=0, ax=ax)
st.pyplot(fig)

# DOM Placeholder
st.subheader("Depth of Market (DOM)")
st.info("Live DOM data feature will be available once supported APIs are integrated.")
