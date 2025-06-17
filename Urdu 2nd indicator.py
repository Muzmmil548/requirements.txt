import streamlit as st from streamlit_autorefresh import st_autorefresh import requests import pandas as pd import plotly.graph_objs as go

Set Page Config

st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide") st_autorefresh(interval=10 * 1000, key="refresh")

Header

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Indicators + Institutional Zones)") st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو، Demand/Supply Zones، اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

Get Top 50 Binance USDT Pairs

@st.cache_data(ttl=600) def get_top_50_symbols(): try: url = "https://api.binance.com/api/v3/ticker/24hr" response = requests.get(url, timeout=10) data = response.json() usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')] sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True) return [pair['symbol'] for pair in sorted_pairs[:50]] except Exception as e: st.error(f"⛔ Symbols Error: {e}") return []

symbols = get_top_50_symbols() if not symbols: st.stop()

selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols)

Live Chart Embed (TradingView)

with st.expander("📺 Live Indicator Chart"): st.components.v1.iframe(f"https://www.tradingview.com/chart/?symbol=BINANCE:{selected_symbol}", height=500)

Get Live Price

price_url = f"https://api.binance.com/api/v3/ticker/price?symbol={selected_symbol}" price = float(requests.get(price_url).json()['price'])

Get Order Book

depth = requests.get(f"https://api.binance.com/api/v3/depth?symbol={selected_symbol}&limit=5").json() bid_vol = sum([float(x[1]) for x in depth['bids']]) ask_vol = sum([float(x[1]) for x in depth['asks']])

Get Trades

trades_url = f"https://api.binance.com/api/v3/trades?symbol={selected_symbol}&limit=100" trades = requests.get(trades_url).json() buyers = sum(1 for t in trades if not t['isBuyerMaker']) sellers = sum(1 for t in trades if t['isBuyerMaker'])

AI Signal Logic

def ai_signal(bid, ask, buyers, sellers): effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2) dominancy = "Buyers" if buyers > sellers else "Sellers" if dominancy == "Buyers" and effort < 10: return "🟢 Buy (Long)" elif dominancy == "Sellers" and effort < 10: return "🔴 Sell (Short)" else: return "🟡 Wait" signal = ai_signal(bid_vol, ask_vol, buyers, sellers)

Institutional Activity

threshold = 10000 large_buys = sum(1 for t in trades if not t['isBuyerMaker'] and float(t['qty']) * price > threshold) large_sells = sum(1 for t in trades if t['isBuyerMaker'] and float(t['qty']) * price > threshold) if large_buys > large_sells and large_buys > 5: institutional = "🟢 Institutional Buying" elif large_sells > large_buys and large_sells > 5: institutional = "🔴 Institutional Selling" else: institutional = "🟡 No Strong Signal"

Display Data

st.subheader("📊 Smart Metrics") st.markdown(f"""

💰 Price: ${price:.2f}

📥 Bid Volume: {bid_vol:.2f}

📤 Ask Volume: {ask_vol:.2f}

🟢 Buyers: {buyers} | 🔴 Sellers: {sellers}

🎯 Effort %: {abs(bid_vol - ask_vol) / max(bid_vol + ask_vol, 1) * 100:.2f}%

⚖️ Dominancy: {'Buyers' if buyers > sellers else 'Sellers'}

🤖 AI Signal: {signal}

🧠 Institutional Activity: {institutional}
""")


Demand & Supply Zones

@st.cache_data(ttl=300) def get_ohlcv(symbol): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=100" raw = requests.get(url).json() df = pd.DataFrame(raw, columns=['time', 'open', 'high', 'low', 'close', 'volume','x','x','x','x','x']) df['close'] = df['close'].astype(float) df['time'] = pd.to_datetime(df['time'], unit='ms') return df[['time', 'close']]

def detect_zones(df): demand = [] supply = [] prices = df['close'].tolist() for i in range(5, len(prices) - 5): if prices[i] < min(prices[i-5:i]) and prices[i] < min(prices[i+1:i+6]): demand.append((df['time'].iloc[i], prices[i])) if prices[i] > max(prices[i-5:i]) and prices[i] > max(prices[i+1:i+6]): supply.append((df['time'].iloc[i], prices[i])) return demand, supply

ohlcv = get_ohlcv(selected_symbol) demand, supply = detect_zones(ohlcv)

fig = go.Figure() fig.add_trace(go.Scatter(x=ohlcv['time'], y=ohlcv['close'], name='Price')) for d in demand: fig.add_trace(go.Scatter(x=[d[0]], y=[d[1]], mode='markers+text', name='Demand', marker=dict(color='green', size=10))) for s in supply: fig.add_trace(go.Scatter(x=[s[0]], y=[s[1]], mode='markers+text', name='Supply', marker=dict(color='red', size=10))) st.plotly_chart(fig, use_container_width=True)

st.success("✅ مکمل AI اسسٹنٹ، انسٹی ٹیوشن سگنل اور زونز کام کر رہے ہیں")

