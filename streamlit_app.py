import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go

# Sidebar
st.sidebar.title("تجزیاتی چیک لسٹ - اردو میں")
symbol = st.sidebar.text_input("سکرپٹ کا نام (جیسے: AAPL, BTC-USD, ES=F)", "AAPL")
start_date = st.sidebar.date_input("شروع کی تاریخ", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("آخری تاریخ", pd.to_datetime("today"))

# Data loading
@st.cache_data
def load_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    df.reset_index(inplace=True)
    return df

df = load_data(symbol, start_date, end_date)

# Indicators calculation
df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()
df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean() / df['Close'].pct_change().rolling(14).std()))
df['MA_10'] = df['Close'].rolling(window=10).mean()
df['MA_200'] = df['Close'].rolling(window=200).mean()

# Price Chart
st.subheader(f"{symbol} کا قیمت چارٹ")
fig = go.Figure()
fig.add_trace(go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'],
                             low=df['Low'], close=df['Close'], name='Candlestick'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_20'], line=dict(width=1), name='EMA 20'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA_50'], line=dict(width=1), name='EMA 50'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_10'], line=dict(width=1), name='MA 10'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['MA_200'], line=dict(width=1), name='MA 200'))
fig.update_layout(xaxis_rangeslider_visible=False)
st.plotly_chart(fig)

# RSI Indicator
st.subheader("RSI (Relative Strength Index)")
rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], line=dict(width=2), name='RSI'))
rsi_fig.update_layout(yaxis=dict(range=[0,100]))
st.plotly_chart(rsi_fig)

# Heatmap
st.subheader("مارکیٹ ہیٹ میپ")
heatmap_data = pd.DataFrame(np.random.rand(10, 5), columns=[f'Col {i+1}' for i in range(5)])
st.dataframe(heatmap_data.style.background_gradient(cmap='RdYlGn'), use_container_width=True)

# Urdu Indicator Summary
st.subheader("خلاصہ (Summary)")
st.markdown("""
- **EMA 20 اور EMA 50** کی کراسنگ سے رجحان کا اندازہ لگائیں  
- **RSI 70 سے اوپر** ہو تو اوورباؤٹ، **30 سے نیچے** ہو تو اوورسیل  
- **MA 200** لمبے وقت کا ٹرینڈ دکھاتا ہے  
- **Heatmap** سے اندازہ لگائیں کہ مجموعی مارکیٹ کا موڈ کیا ہے  
""")
