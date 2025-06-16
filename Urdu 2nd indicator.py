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
        data = requests.get("https://data-api.binance.vision/api/v3/ticker/24hr", timeout=10).json()
        filtered = [(d['symbol'], float(d.get('quoteVolume', 0))) for d in data
                    if d.get('symbol','').endswith('USDT') and 'BUSD' not in d.get('symbol','')]
        top = sorted(filtered, key=lambda x: x[1], reverse=True)[:50]
        return [s[0] for s in top] or ["BTCUSDT"]
    except Exception as e:
        st.error("Symbols لوڈ نہیں ہو سکے: " + str(e))
        return ["BTCUSDT"]

symbols = get_top_50_symbols()
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols,
                               index=symbols.index("BTCUSDT") if "BTCUSDT" in symbols else 0)

with st.expander("📺 Live TradingView Chart"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/single-quote/?symbol=BINANCE:{selected_symbol}&locale=en",
        height=250, scrolling=False)

def get_price(sym):
    return float(requests.get(f"https://data-api.binance.vision/api/v3/ticker/price?symbol={sym}",
                              timeout=5).json()['price'])

def get_order_book(sym):
    ob = requests.get(f"https://data-api.binance.vision/api/v3/depth?symbol={sym}&limit=5",
                      timeout=5).json()
    return sum(float(b[1]) for b in ob['bids']), sum(float(a[1]) for a in ob['asks'])

def get_trades(sym):
    tr = requests.get(f"https://data-api.binance.vision/api/v3/trades?symbol={sym}&limit=50",
                      timeout=5).json()
    return sum(not t['isBuyerMaker'] for t in tr), sum(t['isBuyerMaker'] for t in tr)

def calc_effort(b, a):
    return round(abs(b - a) / max(b + a, 1) * 100, 2)

try:
    p = get_price(selected_symbol)
    bv, av = get_order_book(selected_symbol)
    b, s = get_trades(selected_symbol)
    effort = calc_effort(bv, av)
    dom = "Buyers" if b > s else "Sellers"
    dz = "Yes" if bv > av * 1.2 else "No"
    sz = "Yes" if av > bv * 1.2 else "No"
except Exception as e:
    st.error("Binance سے ڈیٹا نہیں آیا: " + str(e))
    p = bv = av = b = s = effort = dom = dz = sz = "Error"

info = {"Price": p, "Bid Volume": bv, "Ask Volume": av,
        "Buyers": b, "Sellers": s, "Effort %": effort,
        "Dominancy": dom, "Demand Zone": dz, "Supply Zone": sz}

for lbl, val in info.items():
    col = "white"
    if val == "Error": col = "red"
    elif lbl == "Dominancy": col = "green" if val == "Buyers" else "red"
    elif lbl == "Effort %" and isinstance(val, (int, float)) and val > 10: col = "orange"
    st.markdown(f"<div style='background:#222;color:{col};padding:8px;border-radius:8px;margin:3px 0'>"
                f"<b>{lbl}:</b> {val}</div>", unsafe_allow_html=True)

st.success("✅ Live Urdu Scalping App – Binance Live Data آج صحیح آرہا ہے۔")
