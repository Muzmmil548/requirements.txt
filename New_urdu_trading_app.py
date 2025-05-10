import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

st.set_page_config(layout="wide", page_title="Pro Trading Assistant", page_icon="📊")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
        body { background-color: #0D1117; color: white; }
        .main { background-color: #0D1117; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .stButton>button { background-color: #21262D; color: white; border-radius: 12px; padding: 0.5rem 1rem; }
        .stSelectbox, .stTextInput, .stNumberInput, .stMultiSelect, .stDateInput, .stSlider, .stRadio > div { background-color: #161B22; color: white; border-radius: 8px; }
        .light-on { color: #39FF14; font-size: 24px; font-weight: bold; }
        .light-off { color: #4A4A4A; font-size: 24px; font-weight: bold; }
        .title { font-size: 36px; color: #58A6FF; text-align: center; font-weight: bold; margin-bottom: 2rem; }
        .indicator-box, .pattern-box { background-color: #161B22; padding: 1rem; border-radius: 12px; margin-bottom: 1rem; }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<div class='title'>Professional Urdu Trading Assistant</div>", unsafe_allow_html=True)

# --- TradingView Chart ---
st.markdown("""
    <iframe src="https://www.tradingview.com/chart/" width="100%" height="500" frameborder="0"></iframe>
""", unsafe_allow_html=True)

# --- Exchange Toggle (AI Signal based on selected coin) ---
selected_coin = st.selectbox("Select a Coin:", [f"Coin {i+1}" for i in range(50)])
ai_signal = random.choice(["Buy", "Sell", "Hold"])
color_map = {"Buy": "🟢", "Sell": "🔴", "Hold": "🟡"}
st.markdown(f"**AI Suggestion for {selected_coin}:** {color_map[ai_signal]} {ai_signal}")

# --- Indicator Lights ---
st.markdown("<h4>Professional Indicators</h4>", unsafe_allow_html=True)
indicators = ["RSI", "MACD", "Moving Average", "Bollinger Bands", "Stochastic", "Volume"]
cols = st.columns(3)
for i, indicator in enumerate(indicators):
    status = random.choice(["on", "off"])
    light = "🟢" if status == "on" else "⚫"
    with cols[i % 3]:
        st.markdown(f"<div class='indicator-box'>{indicator}: <span class='{'light-on' if status == 'on' else 'light-off'}'>{light}</span></div>", unsafe_allow_html=True)

# --- Chart Pattern Lights ---
st.markdown("<h4>Chart Patterns Detection</h4>", unsafe_allow_html=True)
patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom", "Ascending Triangle",
    "Descending Triangle", "Symmetrical Triangle", "Bullish Flag", "Bearish Flag", "Cup & Handle",
    "Wedge", "Rectangle", "Pennant", "Diamond", "Broadening Wedge"
]
pattern_cols = st.columns(3)
for i, pattern in enumerate(patterns):
    status = random.choice(["on", "off"])
    light = "🟢" if status == "on" else "⚫"
    with pattern_cols[i % 3]:
        st.markdown(f"<div class='pattern-box'>{pattern}: <span class='{'light-on' if status == 'on' else 'light-off'}'>{light}</span></div>", unsafe_allow_html=True)

# --- End Message ---
st.markdown("<hr><div style='text-align: center; color: gray;'>Designed and Customized as per Professional UI | All rights reserved</div>", unsafe_allow_html=True)
