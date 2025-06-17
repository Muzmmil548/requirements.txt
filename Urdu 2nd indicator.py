import streamlit as st from streamlit_autorefresh import st_autorefresh import requests import pandas as pd

✅ Page Config

st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

✅ Auto-refresh (ہر 10 سیکنڈ میں)

st_autorefresh(interval=10 * 1000, key="refresh")

✅ Header

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Spot/Futures)") st.markdown("سمارٹ منی، آرڈر فلو، اور Binance کے Live ڈیٹا پر مبنی سگنلز")

✅ Spot API Symbols

@st.cache_data(ttl=600) def get_spot_symbols(): try: url = "https://api.binance.com/api/v3/ticker/24hr" response = requests.get(url, timeout=10) data = response.json() usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')] sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True) return [pair['symbol'] for pair in sorted_pairs[:50]] except Exception as e: st.error(f"⛔ Spot Symbols Error: {e}") return []

✅ Futures API Symbols

@st.cache_data(ttl=600) def get_futures_symbols(): try: url = "https://fapi.binance.com/fapi/v1/ticker/24hr" response = requests.get(url, timeout=10) data = response.json() usdt_pairs = [d for d in data if d['symbol'].endswith('USDT')] sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True) return [pair['symbol'] for pair in sorted_pairs[:50]] except Exception as e: st.error(f"⛔ Futures Symbols Error: {e}") return []

✅ Market Selector

market = st.radio("📊 مارکیٹ منتخب کریں:", ["Spot", "Futures"], horizontal=True)

✅ Load Symbols Accordingly

if market == "Spot": symbols = get_spot_symbols() else: symbols = get_futures_symbols()

if not symbols: st.error("📡 Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔") st.stop()

✅ Coin Selector

selected_symbol = st.selectbox(f"🔍 {market} ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

✅ Show TradingView Chart

with st.expander("📺 Live Indicator Chart (TradingView)"): market_prefix = "BINANCE" if market == "Spot" else "BINANCE" st.components.v1.iframe( f"https://www.tradingview.com/chart/?symbol={market_prefix}:{selected_symbol}", height=500, scrolling=True )

✅ Get Price

@st.cache_data(ttl=30) def get_price(symbol, is_futures): if is_futures: url = f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}" else: url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}" return float(requests.get(url).json()['price'])

✅ Get Order Book

def get_order_book(symbol, is_futures): url = f"https://{'fapi' if is_futures else 'api'}.binance.com/{'fapi/v1' if is_futures else 'api/v3'}/depth?symbol={symbol}&limit=5" data = requests.get(url).json() bid_vol = sum([float(x[1]) for x in data['bids']]) ask_vol = sum([float(x[1]) for x in data['asks']]) return bid_vol, ask_vol

✅ Get Recent Trades

def get_trades(symbol, is_futures): url = f"https://{'fapi' if is_futures else 'api'}.binance.com/{'fapi/v1' if is_futures else 'api/v3'}/trades?symbol={symbol}&limit=100" trades = requests.get(url).json() buyers = sum(1 for t in trades if not t['isBuyerMaker']) sellers = sum(1 for t in trades if t['isBuyerMaker']) return buyers, sellers

✅ AI Signal Logic

def ai_signal(bid, ask, buyers, sellers): effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2) dominancy = "Buyers" if buyers > sellers else "Sellers" if dominancy == "Buyers" and effort < 10: return "🟢 Buy (Long)" elif dominancy == "Sellers" and effort < 10: return "🔴 Sell (Short)" else: return "🟡 Wait"

✅ Collect Data

try: is_futures = (market == "Futures") price = get_price(selected_symbol, is_futures) bid_volume, ask_volume = get_order_book(selected_symbol, is_futures) buyers, sellers = get_trades(selected_symbol, is_futures) signal = ai_signal(bid_volume, ask_volume, buyers, sellers) except: st.error("⚠️ Binance API ڈیٹا حاصل نہ کر سکا") st.stop()

✅ Display Real-Time Info

st.markdown("---") st.subheader("📊 Smart Money + AI Signal")

info = { "🟡 Price": f"${price:.2f}", "📥 Bid Volume": round(bid_volume, 2), "📤 Ask Volume": round(ask_volume, 2), "🟢 Buyers": buyers, "🔴 Sellers": sellers, "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers", "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2), "🤖 AI Signal": signal }

for label, val in info.items(): st.markdown(f"<div style='font-size:20px; background-color:#111; color:white; padding:8px; margin-bottom:5px;'> <b>{label}</b>: {val}</div>", unsafe_allow_html=True)

st.success("✅ مکمل AI اسکیلپنگ سگنلز Live ہیں۔")

