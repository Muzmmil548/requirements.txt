import streamlit as st import pandas as pd import numpy as np import random

st.set_page_config(page_title="📊 Urdu Scalping Assistant", layout="wide")

st.title("📈 اردو اسکیلپنگ اسسٹنٹ (Smart Money + Volume)") st.markdown("تمام indicators سمارٹ منی اور آرڈر فلو لاجک پر مبنی ہیں۔")

Sample data generator (replace with live data source later)

def get_mock_data(): data = { "Price Change": round(random.uniform(-0.5, 0.5), 3), "Bid Volume": random.randint(500, 2000), "Ask Volume": random.randint(500, 2000), "Buyers": random.randint(300, 1500), "Sellers": random.randint(300, 1500), "Effort": round(random.uniform(1.0, 5.0), 2), "Dominancy": random.choice(["Buyers", "Sellers"]), "Institutional Buying": random.choice(["Low", "Moderate", "High"]), "Institutional Selling": random.choice(["Low", "Moderate", "High"]), "Demand Zone": random.choice(["Yes", "No"]), "Supply Zone": random.choice(["Yes", "No"]) } return pd.DataFrame([data])

Fetch mock data

data = get_mock_data()

Display data in colored format

for column in data.columns: value = data[column][0] color = "white"

if column in ["Price Change"]:
    color = "green" if value > 0 else "red" if value < 0 else "gray"

if column in ["Bid Volume", "Buyers", "Institutional Buying"]:
    color = "green" if isinstance(value, int) and value > 1000 else "orange"

if column in ["Ask Volume", "Sellers", "Institutional Selling"]:
    color = "red" if isinstance(value, int) and value > 1000 else "orange"

if column == "Dominancy":
    color = "green" if value == "Buyers" else "red"

if column in ["Demand Zone"]:
    color = "green" if value == "Yes" else "gray"

if column in ["Supply Zone"]:
    color = "red" if value == "Yes" else "gray"

st.markdown(f"<div style='font-size:20px; background-color:#222; color:{color}; padding:10px; margin-bottom:5px;'>
    <b>{column}</b>: {value}</div>", unsafe_allow_html=True)

Note

st.info("📌 یہ صرف ڈیمو ورژن ہے، اصلی مارکیٹ ڈیٹا APIs سے جوڑنے کے بعد خودکار سگنلز بھی شامل ہوں گے۔")

