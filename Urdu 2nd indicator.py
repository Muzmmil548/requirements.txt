import streamlit as st from streamlit_autorefresh import st_autorefresh import requests import pandas as pd import datetime

✅ Page Config (یہ سب سے اوپر ہونا چاہیے)

st.set_page_config(page_title="📊 Urdu Scalping AI Assistant", layout="wide")

✅ Auto-refresh (ہر 30 سیکنڈ میں)

st_autorefresh(interval=30 * 1000, key="refresh")

✅ ہیڈر

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (AI Signals + Dual Timeframes)") st.markdown("تمام Indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

✅ Timeframe Selector

timeframe = st.radio("⏱️ Scalping Timeframe:", ["1m", "5m"], index=1)

✅ Top 50 Symbols from Binance

@st.cache_data(ttl=600) def get_top_50_symbols(): try: url = "https://api.binance.com/api/v3/ticker/24hr" response = requests.get(url, timeout=10) data = response.json() usdt_pairs = [d for d in data if d['symbol'].endswith('USDT') and not d['symbol'].endswith('BUSD')] sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True) return [pair['symbol'] for pair in sorted_pairs[:50]] except: return []

symbols = get_top_50_symbols() if not symbols: st.error("📡 Symbols لوڈ نہیں ہو سکے، Binance API سے مسئلہ ہو سکتا ہے۔") st.stop()

selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=0)

✅ TradingView Chart with Indicator View

with st.expander("📺 Live Indicator Chart (TradingView)"): st.components.v1.iframe( f"https://s.tradingview.com/embed-widget/advanced-chart/?symbol=BINANCE:{selected_symbol}&interval={timeframe}&theme=dark", height=500, scrolling=True )

✅ Get Live Price

def get_price(symbol): url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}" return float(requests.get(url).json()['price'])

✅ Get Order Book

def get_order_book(symbol): url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5" data = requests.get(url).json() bid_vol = sum([float(x[1]) for x in data['bids']]) ask_vol = sum([float(x[1]) for x in data['asks']]) return bid_vol, ask_vol

✅ Get Recent Trades

def get_trades(symbol): url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=100" trades = requests.get(url).json() buyers = sum(1 for t in trades if not t['isBuyerMaker']) sellers = sum(1 for t in trades if t['isBuyerMaker']) return buyers, sellers

✅ AI Signal Logic

def ai_signal(bid, ask, buyers, sellers): effort = round(abs(bid - ask) / max(bid + ask, 1) * 100, 2) dominancy = "Buyers" if buyers > sellers else "Sellers" if dominancy == "Buyers" and effort < 10: return "🟢 Buy" elif dominancy == "Sellers" and effort < 10: return "🔴 Sell" else: return "🟡 Wait"

✅ Get All Data

try: price = get_price(selected_symbol) bid_volume, ask_volume = get_order_book(selected_symbol) buyers, sellers = get_trades(selected_symbol) signal = ai_signal(bid_volume, ask_volume, buyers, sellers) except: st.error("📡 Binance API سے ڈیٹا حاصل نہیں ہو سکا") st.stop()

✅ Display All Info

st.markdown("---") st.subheader("📊 Real-Time Smart Money Metrics")

info = { "🟡 Price": f"${price:.2f}", "📥 Bid Volume": round(bid_volume, 2), "📤 Ask Volume": round(ask_volume, 2), "🟢 Buyers": buyers, "🔴 Sellers": sellers, "🎯 Dominancy": "Buyers" if buyers > sellers else "Sellers", "⚖️ Effort %": round(abs(bid_volume - ask_volume) / max(bid_volume + ask_volume, 1) * 100, 2), "🤖 AI Signal": signal }

for label, val in info.items(): icon = "" if "AI Signal" in label: if "Buy" in val: icon = "<span style='color:lime;'>🟢</span>" elif "Sell" in val: icon = "<span style='color:red;'>🔴</span>" else: icon = "<span style='color:yellow;'>🟡</span>" st.markdown(f""" <div style='font-size:20px; background-color:#111; color:white; padding:8px; margin-bottom:5px;'> <b>{label}</b>: {val} {icon}</div> """, unsafe_allow_html=True)

st.success(f"✅ سب کچھ Live چل رہا ہے - Timeframe: {timeframe}")

