import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests

st.set_page_config(page_title="📊 Urdu Scalping Binance Live", layout="wide")
st_autorefresh(interval=10 * 1000, key="refresh")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Top 50 Binance Coins)")
st.markdown("Smart Money + Order Flow با‑Binance Live ڈیٹا۔")

@st.cache_data(ttl=3600)
def get_top_50_symbols():
    try:
        data = requests.get("https://data.binance.com/api/v3/ticker/24hr", timeout=10).json()
        filtered = [(d['symbol'], float(d['quoteVolume'] or 0)) for d in data 
                    if d.get('symbol','').endswith('USDT') and 'BUSD' not in d.get('symbol','')]
        sorted_symbols = sorted(filtered, key=lambda x: x[1], reverse=True)
        return [s[0] for s in sorted_symbols[:50]] or ["BTCUSDT"]
    except Exception as e:
        st.error("Symbols لوڈ نہیں ہو سکے، Error: " + str(e))
        return ["BTCUSDT"]

symbols = get_top_50_symbols()
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=symbols.index("BTCUSDT") if "BTCUSDT" in symbols else 0)

with st.expander("📺 Live TradingView Chart"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/single-quote/?symbol=BINANCE:{selected_symbol}&locale=en",
        height=250, scrolling=False
    )

def get_price(symbol):
    url = f"https://data.binance.com/api/v3/ticker/price?symbol={symbol}"
    return float(requests.get(url, timeout=5).json()['price'])

def get_order_book(symbol):
    url = f"https://data.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    ob = requests.get(url, timeout=5).json()
    return sum(float(bid[1]) for bid in ob['bids']), sum(float(ask[1]) for ask in ob['asks'])

def get_trades(symbol):
    url = f"https://data.binance.com/api/v3/trades?symbol={symbol}&limit=50"
    trades = requests.get(url, timeout=5).json()
    return sum(not t['isBuyerMaker'] for t in trades), sum(t['isBuyerMaker'] for t in trades)

def calculate_effort(bid, ask):
    return round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)

# Live Data Fetch
try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    effort = calculate_effort(bid_volume, ask_volume)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    demand_zone = "Yes" if bid_volume > ask_volume * 1.2 else "No"
    supply_zone = "Yes" if ask_volume > bid_volume * 1.2 else "No"
except Exception as e:
    st.error("Binance data حاصل نہیں ہوا: " + str(e))
    price = bid_volume = ask_volume = buyers = sellers = effort = "N/A"
    dominancy = demand_zone = supply_zone = "Error"

data = {"Price": price, "Bid Volume": bid_volume, "Ask Volume": ask_volume, 
        "Buyers": buyers, "Sellers": sellers, "Effort %": effort, 
        "Dominancy": dominancy, "Demand Zone": demand_zone, "Supply Zone": supply_zone}

for label, value in data.items():
    color = "white"
    if label == "Price" and isinstance(value, (float,int)): color = "green"
    elif label in ["Bid Volume","Buyers"] and isinstance(value, (float,int)) and value>1000: color="green"
    elif label in ["Ask Volume","Sellers"] and isinstance(value,(float,int)) and value>1000: color="red"
    elif label=="Effort %" and isinstance(value,(float,int)) and value>10: color="orange"
    elif label=="Dominancy": color="green" if value=="Buyers" else "red"
    st.markdown(f"<div style='background:#222;color:{color};padding:8px;border-radius:8px;margin:3px 0'><b>{label}:</b> {value}</div>", unsafe_allow_html=True)

st.success("✅ Live Urdu Scalping App—اب Binance Live Data چل رہا ہے۔")
