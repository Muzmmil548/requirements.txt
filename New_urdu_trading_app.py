# streamlit_app.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ========== Page Configuration ========== #
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Custom Styling ========== #
st.markdown("""
<style>
    /* Main container */
    .main {background: #f5f6fa}
    
    /* Header styling */
    h1 {color: #2c3e50; border-bottom: 2px solid #3498db}
    
    /* Buttons */
    .stButton>button {
        background: #3498db !important;
        border-radius: 8px;
        padding: 10px 24px;
    }
    
    /* Columns spacing */
    .stColumn {padding: 15px}
    
    /* Live chart box */
    .chart-box {
        border: 1px solid #dfe6e9;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ========== Live Data Generator ========== #
def generate_live_data():
    now = datetime.now()
    return pd.DataFrame({
        'timestamp': [now - timedelta(seconds=i) for i in range(100)],
        'price': np.random.normal(100, 2, 100).cumsum()
    })

# ========== Chart Components ========== #
def create_candlestick():
    df = generate_live_data()
    fig = go.Figure(go.Candlestick(
        x=df['timestamp'],
        open=df['price'].shift(1),
        high=df['price'] + 1.5,
        low=df['price'] - 1.5,
        close=df['price']
    ))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# ========== Main App ========== #
def main():
    # Sidebar Navigation
    with st.sidebar:
        st.header("TRADING SUITE")
        menu = st.radio("", ["Live Dashboard", "AI Signals", "Market Scanner"])
    
    # Live Dashboard (Main Page)
    if menu == "Live Dashboard":
        # Header
        st.header("CRYPTO SCALPING CHECKLIST", anchor=False)
        
        # Top Section (3 Columns)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Top Assets")
            st.write("""
            - BTC/USDT  
            - ETH/USDT  
            - BNB/USDT  
            - XRP/USDT  
            """)
        
        with col2:
            st.subheader("AI Signals")
            st.write("""
            🟢 STRONG BUY: BTC  
            🔴 SELL ALERT: ETH  
            🟡 HOLD: BNB  
            """)
        
        with col3:
            st.subheader("Patterns")
            st.write("""
            - Head & Shoulders  
            - Double Top  
            - Triangle  
            - Wedge  
            """)
        
        # Live Chart Section
        st.subheader("Live Price Action")
        with st.container():
            st.plotly_chart(create_candlestick(), use_container_width=True)
    
    # Other Pages
    elif menu == "AI Signals":
        st.header("AI Trading Signals")
        # Add AI components here
    
    elif menu == "Market Scanner":
        st.header("Market Scanner")
        # Add scanner components here

if __name__ == "__main__":
    main()
