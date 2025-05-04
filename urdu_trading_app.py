import streamlit as st import requests import pandas as pd import matplotlib.pyplot as plt from streamlit.components.v1 import html

--- CONFIG ---

st.set_page_config(page_title="اردو پرو ٹریڈنگ ایپ", layout="wide")

--- HEADER ---

st.markdown("<h1 style='text-align: center; color: green;'>اردو پروفیشنل ٹریڈنگ ایپ</h1>", unsafe_allow_html=True) st.markdown("---")

--- SIDEBAR: Exchange & DOM Toggles ---

st.sidebar.markdown("### ایکسچینج منتخب کریں:") binance_on = st.sidebar.checkbox("Binance", value=True) bybit_on = st.sidebar.checkbox("Bybit", value=False) cme_on = st.sidebar.checkbox("CME", value=False) bitget_on = st.sidebar.checkbox("Bitget", value=False) kucoin_on = st.sidebar.checkbox("KuCoin", value=False) mexc_on = st.sidebar.checkbox("MEXC", value=False) okx_on = st.sidebar.checkbox("OKX", value=False)

st.sidebar.markdown("### DOM سیٹنگز:") dom_binance = st.sidebar.checkbox("Binance DOM", value=True) dom_bybit = st.sidebar.checkbox("Bybit DOM", value=False)

--- Timeframe ---

timeframe = st.sidebar.selectbox("ٹائم فریم منتخب کریں", ["1m", "5m", "15m", "1h", "4h", "1d", "1w", "1M"])

--- Data Fetch Functions ---

def fetch_binance(symbol, interval): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100" data = requests.get(url).json() df = pd.DataFrame(data, columns=["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "QAV", "Trades", "TBAV", "TBQV", "Ignore"]) df["Close"] = df["Close"].astype(float) df["Volume"] = df["Volume"].astype(float) return df

def fetch_bybit(symbol, interval): url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&limit=100" resp = requests.get(url).json().get("result", []) df = pd.DataFrame(resp) if "close" in df.columns: df.rename(columns={"close": "Close"}, inplace=True) df["Close"] = df["Close"].astype(float) df["volume"] = df.get("volume", df.get("Volume", pd.Series(0))).astype(float) return df

--- Indicator Calculation ---

def calculate_indicators(df): # EMA df["EMA"] = df["Close"].ewm(span=10).mean() # RSI delta = df["Close"].diff() gain = delta.where(delta > 0, 0) loss = -delta.where(delta < 0, 0) avg_gain = gain.rolling(14).mean() avg_loss = loss.rolling(14).mean() rs = avg_gain / avg_loss df["RSI"] = 100 - (100 / (1 + rs)) # MACD df["MACD"] = df["Close"].ewm(span=12).mean() - df["Close"].ewm(span=26).mean() df["Signal_Line"] = df["MACD"].ewm(span=9).mean() # Bollinger Bands rolling_mean = df["Close"].rolling(20).mean() rolling_std = df["Close"].rolling(20).std() df["BB_upper"] = rolling_mean + 2 * rolling_std df["BB_lower"] = rolling_mean - 2 * rolling_std # VWAP df["VWAP"] = (df["Close"] * df["Volume"]).cumsum() / df["Volume"].cumsum() return df

--- Traffic Light ---

def traffic_light(row): if row["MACD"] > row["Signal_Line"] and row["RSI"] > 50: return "🟢 Green" elif abs(row["MACD"] - row["Signal_Line"]) < 0.5: return "🟡 Yellow" else: return "🔴 Red"

--- TradingView Embed ---

def display_tradingview(exchange, symbol): html(f""" <iframe src="https://s.tradingview.com/widgetembed/?symbol={exchange}:{symbol}&interval={timeframe}&theme=light" 
width="100%" height="400" frameborder="0"></iframe> """, height=400)

--- Heatmap ---

def plot_heatmap(): data = requests.get("https://api.binance.com/api/v3/ticker/24hr").json() df = pd.DataFrame(data) df = df[df["symbol"].str.endswith("USDT")].copy() df["pct"] = df["priceChangePercent"].astype(float) top = df.nlargest(20, "pct") symbols = top["symbol"].tolist() vals = top["pct"].tolist() fig, ax = plt.subplots(figsize=(12, 2)) im = ax.imshow([vals], aspect='auto', cmap='RdYlGn') ax.set_yticks([]) ax.set_xticks(range(len(symbols))) ax.set_xticklabels(symbols, rotation=45, fontsize=8) fig.colorbar(im, orientation='horizontal', pad=0.2) st.pyplot(fig)

--- DOM ---

def fetch_dom(exchange, symbol): if exchange == "Binance": data = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10").json() bids = pd.DataFrame(data["bids"], columns=["Price", "Qty"]).astype(float) asks = pd.DataFrame(data["asks"], columns=["Price", "Qty"]).astype(float) elif exchange == "Bybit": resp = requests.get(f"https://api.bybit.com/v2/public/orderBook/L2?symbol={symbol}&limit=10").json().get("result", []) df = pd.DataFrame(resp) bids = df[df["side"] == "Buy"][ ["price", "size"] ].rename(columns={"price":"Price","size":"Qty"}).astype(float) asks = df[df["side"] == "Sell"][ ["price", "size"] ].rename(columns={"price":"Price","size":"Qty"}).astype(float) else: bids = pd.DataFrame() asks = pd.DataFrame() return bids, asks

def display_dom(exchange, symbol): st.subheader(f"{exchange} DOM - {symbol}") bids, asks = fetch_dom(exchange, symbol) col1, col2 = st.columns(2) with col1: st.markdown("Bids (خریدار)") st.table(bids) with col2: st.markdown("Asks (فروخت کنندہ)") st.table(asks)

--- MAIN ---

exchanges = { 'Binance': binance_on, 'Bybit': bybit_on, 'CME': cme_on, 'Bitget': bitget_on, 'KuCoin': kucoin_on, 'MEXC': mexc_on, 'OKX': okx_on } symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]

for exch, flag in exchanges.items(): if flag: st.subheader(exch) display_tradingview(exch.upper(), symbols[0]) if exch in ["Binance", "Bybit"]: for sym in symbols: df = fetch_binance(sym, timeframe) if exch == "Binance" else fetch_bybit(sym, timeframe) df = calculate_indicators(df) sig = traffic_light(df.iloc[-1]) st.markdown(f"{sym} Signal: {sig}") else: st.info(f"{exch} live data & indicators جلد شامل کیے جائیں گے۔") # DOM if exch == "Binance" and dom_binance: display_dom(exch, symbols[0]) if exch == "Bybit" and dom_bybit: display_dom(exch, symbols[0])

Market Heatmap & Top Mover Traffic Light

st.subheader("Market Heatmap") plot_heatmap()

Top Mover

top_pct = pd.read_json("https://api.binance.com/api/v3/ticker/24hr").loc[0, "priceChangePercent"].astype(float) clr = 'green' if top_pct > 0 else 'red' st.markdown(f"<h2 style='color:{clr};'>Top Mover: {top_pct:.2f}%</h2>", unsafe_allow_html=True)

End of Script

