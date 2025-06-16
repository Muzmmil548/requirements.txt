import streamlit as st
from streamlit_autorefresh import st_autorefresh
import requests

# ✅ Page Config (سب سے اوپر ہونا چاہیے)
st.set_page_config(page_title="📊 Urdu Scalping Binance Live", layout="wide")

# ✅ Auto-refresh ہر 30 سیکنڈ میں
st_autorefresh(interval=10 * 1000, key="refresh")

# ✅ Title
st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Top 50 Binance Coins)")
st.markdown("تمام indicators سمارٹ منی، آرڈر فلو اور Binance کے Live ڈیٹا پر مبنی ہیں۔")

# ✅ Get Top 50 Coins from Binance API
@st.cache_data(ttl=3600)
def get_top_50_symbols():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)
        data = response.json()
        filtered = []
        for d in data:
            symbol = d.get("symbol", "")
            volume = d.get("quoteVolume", "0")
            if symbol.endswith("USDT") and "BUSD" not in symbol:
                try:
                    volume_float = float(volume)
                    filtered.append((symbol, volume_float))
                except:
                    continue
        sorted_symbols = sorted(filtered, key=lambda x: x[1], reverse=True)
        top_symbols = [s[0] for s in sorted_symbols[:50]]
        return top_symbols if top_symbols else ["BTCUSDT"]
    except Exception as e:
        st.error(f"⛔ Binance سے symbols نہیں مل سکے: {e}")
        return ["BTCUSDT"]

# ✅ Dropdown میں 50 coins
symbols = get_top_50_symbols()
selected_symbol = st.selectbox("🔍 ٹاپ 50 کوائن منتخب کریں:", symbols, index=symbols.index("BTCUSDT") if "BTCUSDT" in symbols else 0)

# ✅ TradingView چارٹ
with st.expander("📺 Live TradingView Chart"):
    st.components.v1.iframe(
        f"https://s.tradingview.com/embed-widget/single-quote/?symbol=BINANCE:{selected_symbol}&locale=en",
        height=250, scrolling=False
    )

# ✅ Binance سے Live Price
def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url).json()
    return float(response['price'])

# ✅ Binance سے Order Book
def get_order_book(symbol):
    url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=5"
    response = requests.get(url).json()
    bid_vol = sum(float(bid[1]) for bid in response['bids'])
    ask_vol = sum(float(ask[1]) for ask in response['asks'])
    return bid_vol, ask_vol

# ✅ Recent Trades
def get_trades(symbol):
    url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit=50"
    response = requests.get(url).json()
    buyers = sum(1 for trade in response if trade['isBuyerMaker'] == False)
    sellers = sum(1 for trade in response if trade['isBuyerMaker'] == True)
    return buyers, sellers

# ✅ Effort Calculation
def calculate_effort(bid, ask):
    return round(abs(bid - ask) / max(bid + ask, 1) * 100, 2)

# ✅ Get All Live Data
try:
    price = get_price(selected_symbol)
    bid_volume, ask_volume = get_order_book(selected_symbol)
    buyers, sellers = get_trades(selected_symbol)
    effort = calculate_effort(bid_volume, ask_volume)
    dominancy = "Buyers" if buyers > sellers else "Sellers"
    demand_zone = "Yes" if bid_volume > ask_volume * 1.2 else "No"
    supply_zone = "Yes" if ask_volume > bid_volume * 1.2 else "No"

    # ✅ Display Indicators
    data = {
        "Price": price,
        "Bid Volume": bid_volume,
        "Ask Volume": ask_volume,
        "Buyers": buyers,
        "Sellers": sellers,
        "Effort %": effort,
        "Dominancy": dominancy,
        "Demand Zone": demand_zone,
        "Supply Zone": supply_zone
    }

    for label, value in data.items():
        color = "white"
        if label == "Price":
            color = "green"
        elif label in ["Bid Volume", "Buyers"] and value > 1000:
            color = "green"
        elif label in ["Ask Volume", "Sellers"] and value > 1000:
            color = "red"
        elif label == "Effort %" and value > 10:
            color = "orange"
        elif label == "Dominancy":
            color = "green" if value == "Buyers" else "red"
        elif label == "Demand Zone":
            color = "green" if value == "Yes" else "gray"
        elif label == "Supply Zone":
            color = "red" if value == "Yes" else "gray"

        st.markdown(f"""
            <div style='font-size:20px; background-color:#222; color:{color}; padding:10px; margin-bottom:5px;'>
            <b>{label}</b>: {value}</div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("🔴 Binance سے Live Data حاصل کرنے میں مسئلہ ہے: " + str(e))

st.success("✅ Live Binance Urdu Scalping Assistant مکمل چل رہا ہے۔ اگلا مرحلہ: AI Signal + Pattern Detection")
