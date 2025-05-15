import streamlit as st
import streamlit.components.v1 as components
import time

# --- Page Config ---
st.set_page_config(page_title="Scalping App", layout="wide")

# --- CSS for Bottom Navigation Bar ---
st.markdown("""
    <style>
    .nav-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #111;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 100;
    }
    .nav-item {
        color: white;
        text-align: center;
        font-size: 14px;
        cursor: pointer;
    }
    .nav-item:hover {
        color: yellow;
    }
    .active {
        color: yellow;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State for Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

# --- Fake navbar using radio button ---
selected = st.radio("Menu", ["Home", "Chart Patterns", "AI Signals", "Top Coins", "Settings"],
                    index=["Home", "Chart Patterns", "AI Signals", "Top Coins", "Settings"].index(st.session_state.page),
                    horizontal=True, label_visibility="collapsed")

st.session_state.page = selected

# --- Live TradingView Chart (only shown in top pages) ---
def show_chart():
    st.markdown("### Live TradingView Chart")
    components.html("""
        <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_chart&symbol=BINANCE:BTCUSDT&interval=15&theme=dark&style=1&locale=en" 
        width="100%" height="400" frameborder="0"></iframe>
    """, height=400)

# --- Pages ---
if st.session_state.page == "Home":
    st.title("🏠 Home")
    show_chart()
    st.success("Welcome to the Urdu Trading App.")

elif st.session_state.page == "Chart Patterns":
    st.title("📈 Chart Patterns")
    show_chart()
    st.markdown("چارٹ پیٹرن خودکار تجزیہ")
    patterns = ["Head & Shoulders", "Double Top", "Triangle", "Cup & Handle"]
    for pattern in patterns:
        st.markdown(f"- {pattern}: <span class='blinking' style='color: green;'>● Detected</span>", unsafe_allow_html=True)

elif st.session_state.page == "AI Signals":
    st.title("🤖 AI Signals")
    show_chart()
    st.info("BTC: 🟢 Buy")
    st.warning("ETH: 🟡 Hold")
    st.error("SOL: 🔴 Sell")

elif st.session_state.page == "Top Coins":
    st.title("💰 Top 10 Coins")
    show_chart()
    coins = ["BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "DOT", "AVAX", "LINK"]
    selected = st.selectbox("کوائن منتخب کریں", coins)
    st.success(f"آپ نے منتخب کیا ہے: **{selected}**")

elif st.session_state.page == "Settings":
    st.title("⚙️ Settings")
    st.toggle("Dark Mode")
    st.toggle("Auto Refresh")

# --- Blinking Signal CSS ---
st.markdown("""
    <style>
    @keyframes blink {
        0% {opacity: 1;}
        50% {opacity: 0;}
        100% {opacity: 1;}
    }
    .blinking {
        animation: blink 1s infinite;
    }
    </style>
""", unsafe_allow_html=True)
