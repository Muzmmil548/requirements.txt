import streamlit as st import requests import pandas as pd import matplotlib.pyplot as plt from streamlit.components.v1 import html import datetime

--- CONFIG ---

st.set_page_config(page_title="اردو پرو ٹریڈنگ ایپ", layout="wide")

--- HEADER ---

st.markdown("<h1 style='text-align: center; color: green;'>اردو پروفیشنل ٹریڈنگ ایپ</h1>", unsafe_allow_html=True) st.markdown("---")

--- SIDEBAR: Exchange & Feature Toggles ---

st.sidebar.markdown("### ایکسچینج منتخب کریں:") binance_on = st.sidebar.checkbox("Binance", value=True) bybit_on   = st.sidebar.checkbox("Bybit",   value=False) cme_on     = st.sidebar.checkbox("CME",     value=False) bitget_on  = st.sidebar.checkbox("Bitget",  value=False) kucoin_on  = st.sidebar.checkbox("KuCoin",  value=False) mexc_on    = st.sidebar.checkbox("MEXC",    value=False) okx_on     = st.sidebar.checkbox("OKX",     value=False)

--- Timeframe Dropdown ---

timeframe = st.sidebar.selectbox("ٹائم فریم منتخب کریں", ["1m","5m","15m","1h","4h","1d","1w","1M"] )

--- FUNCTIONS: Data Fetch & Indicators ---

Binance API Fetch

def fetch_binance(symbol, interval): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100" data = requests.get(url).json() df = pd.DataFrame(data, columns=["Open time","Open","High","Low","Close","Volume","Close time","QAV","NT","TBAV","TBQV","Ignore"]) df["Close"] = df["Close"].astype(float) return df

Bybit API Fetch

def fetch_bybit(symbol, interval): url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&limit=100" data = requests.get(url).json()["result"] df = pd.DataFrame(data) df["close"] = df["close"].astype(float) df.rename(columns={"close":"Close"}, inplace=True) return df

Indicator Calculation

def calculate_indicators(df): df['EMA'] = df['Close'].ewm(span=10).mean() df['RSI'] = (df['Close'].diff().apply(lambda x: x if x>0 else 0).rolling(14).mean())/ (df['Close'].diff().abs().rolling(14).mean())100 df['MACD'] = df['Close'].ewm(span=12).mean() - df['Close'].ewm(span=26).mean() df['Signal'] = df['MACD'].ewm(span=9).mean() df['BB_upper'] = df['Close'].rolling(20).mean()+2df['Close'].rolling(20).std() df['BB_lower'] = df['Close'].rolling(20).mean()-2*df['Close'].rolling(20).std() df['VWAP'] = df['Close']  # simplified return df

Traffic Light based on indicators

def traffic_light(row): if row['MACD']>row['Signal'] and row['RSI']>50: return '🟢 Green' elif abs(row['MACD']-row['Signal'])<0.5: return '🟡 Yellow' else: return '🔴 Red'

--- TradingView Chart Embed ---

def display_tradingview(exchange, symbol): html(f""" <iframe src="https://s.tradingview.com/widgetembed/?symbol={exchange}:{symbol}&interval={timeframe}&theme=light" width="100%" height="400"></iframe> """, height=400)

--- Market Heatmap ---

def plot_heatmap(): data = requests.get("https://api.binance.com/api/v3/ticker/24hr").json() df = pd.DataFrame(data) df = df[df['symbol'].str.endswith('USDT')] df['pct'] = df['priceChangePercent'].astype(float) top = df.nlargest(20, 'pct') symbols = top['symbol']; vals = top['pct'] fig, ax = plt.subplots(figsize=(12,2)) im = ax.imshow([vals], aspect='auto', cmap='RdYlGn') ax.set_yticks([]); ax.set_xticks(range(len(symbols))) ax.set_xticklabels(symbols, rotation=45, fontsize=8) fig.colorbar(im, orientation='horizontal', pad=0.2) st.pyplot(fig)

--- DOM Fetch & Display ---

def fetch_dom(exchange, symbol): if exchange=='Binance': data=requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10").json() else: data={'bids':[], 'asks':[]}  # extend per exchange bids=pd.DataFrame(data['bids'], columns=['Price','Qty']).astype(float) asks=pd.DataFrame(data['asks'], columns=['Price','Qty']).astype(float) return bids, asks

def display_dom(exchange, symbol): bids, asks=fetch_dom(exchange, symbol) st.markdown(f"{exchange} DOM - {symbol}") c1,c2=st.columns(2) with c1: st.table(bids) with c2: st.table(asks)

--- MAIN LAYOUT ---

symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT"]

Charts & Indicators per exchange

if binance_on: st.subheader("Binance") display_tradingview('BINANCE', symbols[0]) for sym in symbols: df = fetch_binance(sym, timeframe) df = calculate_indicators(df) signal=traffic_light(df.iloc[-1]) st.markdown(f"{sym} Signal: {signal}") if bybit_on: st.subheader("Bybit") display_tradingview('BYBIT', symbols[0]) for sym in symbols: df = fetch_bybit(sym, timeframe) df = calculate_indicators(df) signal=traffic_light(df.iloc[-1]) st.markdown(f"{sym} Signal: {signal}")

Placeholders

if cme_on: st.info("CME live data & indicators soon") if bitget_on: st.info("Bitget live data & indicators soon") if kucoin_on: st.info("KuCoin live data & indicators soon") if mexc_on: st.info("MEXC live data & indicators soon") if okx_on: st.info("OKX live data & indicators soon")

Market Heatmap

st.subheader("Market Heatmap") plot_heatmap()

Traffic Light for top mover

pct = requests.get("https://api.binance.com/api/v3/ticker/24hr").json()



