# requirements.tx
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

# --- Dummy order book data generator ---
def get_order_book():
    prices = np.arange(99, 101, 0.02)
    bids = np.random.randint(1, 20, size=prices.shape)
    asks = np.random.randint(1, 20, size=prices.shape)
    df = pd.DataFrame({
        "price": prices,
        "bids": bids,
        "asks": asks
    })
    return df

# --- Order Book Heatmap (DOM) Section ---
order_book = get_order_book()
heatmap_data = np.vstack([order_book["bids"], order_book["asks"]])
fig_dom = go.Figure(
    data=go.Heatmap(
        z=heatmap_data,
        x=order_book["price"],
        y=["Bids", "Asks"],
        colorscale="Viridis",
        reversescale=True,
        colorbar=dict(title="Volume")
    )
)
fig_dom.update_layout(
    title="Order Book Heatmap (DOM)",
    xaxis_title="Price",
    yaxis_title="Side",
    margin=dict(t=50, b=20, l=20, r=20),
    height=300
)
st.plotly_chart(fig_dom, use_container_width=True)

# --- Main App Title ---
st.title("📈 Urdu Trading Assistant")

# --- Sidebar: Exchange toggles ---
st.sidebar.header("ایکسچینجز منتخب کریں")
exchanges = {
    "Binance": st.sidebar.checkbox("Binance", value=True),
    "Bybit":   st.sidebar.checkbox("Bybit",   value=True),
    "CME":     st.sidebar.checkbox("CME",     value=True),
    "Bitget":  st.sidebar.checkbox("Bitget",  value=True),
    "KuCoin":  st.sidebar.checkbox("KuCoin",  value=True),
    "MEXC":    st.sidebar.checkbox("MEXC",    value=True),
    "OKX":     st.sidebar.checkbox("OKX",     value=True),
}

# --- Live price chart (dummy) ---
def get_price_data():
    times = pd.date_range(end=pd.Timestamp.now(), periods=50, freq='T')
    prices = np.cumsum(np.random.randn(50)) + 100
    df = pd.DataFrame({"time": times, "price": prices})
    return df

df = get_price_data()
fig = go.Figure(go.Candlestick(
    x=df['time'], open=df['price'], high=df['price']+0.5,
    low=df['price']-0.5, close=df['price']))
fig.update_layout(margin=dict(t=40, b=20, l=20, r=20))
st.plotly_chart(fig, use_container_width=True)

# --- Indicators ---
ema20 = df['price'].ewm(span=20).mean().iloc[-1]
ema50 = df['price'].ewm(span=50).mean().iloc[-1]
diff = df['price'].diff()
rsi = 100 - (100/(1 + (diff.clip(lower=0).sum()/diff.clip(upper=0).abs().sum())))

st.markdown("### 🔧 انڈیکیٹرز")
col1, col2, col3 = st.columns(3)
col1.metric("EMA 20", f"{ema20:.2f}")
col2.metric("EMA 50", f"{ema50:.2f}")
col3.metric("RSI", f"{rsi:.2f}")

# --- Traffic light logic ---
signal = "Wait"
color  = "🟡"
if ema20 > ema50 and rsi < 70:
    signal, color = "Buy", "🟢"
elif ema20 < ema50 and rsi > 30:
    signal, color = "Sell", "🔴"

st.markdown(f"## Traffic Light: {color} **{signal}**")

# --- Exchange signals ---
st.markdown("### 🔀 ایکسچینج سگنلز")
for name, enabled in exchanges.items():
    if enabled:
        st.write(f"- **{name}**: {color} {signal}")
    else:
        st.write(f"- {name}: _Inactive_")

# --- Market Heatmap ---
def generate_heatmap_data():
    data = np.random.rand(10, 10)
    return pd.DataFrame(data, columns=[f"Col {i}" for i in range(10)])

st.subheader("Market Heatmap")
df_heat = generate_heatmap_data()
fig_heat = px.imshow(df_heat, text_auto=True, aspect="auto", color_continuous_scale="RdYlGn")
st.plotly_chart(fig_heat, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Urdu Trading Assistant – تمام حقوق محفوظ ہیں")
