import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("پروفیشنل اردو ٹریڈنگ اسسٹنٹ")

# Sidebar Options
st.sidebar.header("تجزیہ اختیارات")
top_n = st.sidebar.selectbox("سرفہرست سکے منتخب کریں", [10, 50], index=0)
pattern_detect = st.sidebar.checkbox("پیٹرن ڈیٹیکشن آن کریں؟", value=True)

# Function to fetch top coins
def fetch_top_coins(n=10):
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
        "sparkline": True,
        "price_change_percentage": "1h,24h,7d"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to detect simple pattern (placeholder)
def detect_pattern(prices):
    if len(prices) < 7:
        return ""
    mid = len(prices) // 2
    if prices[0] < prices[mid] and prices[-1] < prices[mid]:
        return "Head & Shoulders"
    return ""

# AI signal function (basic version)
def ai_signal(coin):
    change_1h = coin.get("price_change_percentage_1h_in_currency", 0)
    change_24h = coin.get("price_change_percentage_24h_in_currency", 0)
    change_7d = coin.get("price_change_percentage_7d_in_currency", 0)

    if change_1h > 1 and change_24h > 3:
        return "🟢 خریدنے کا اشارہ"
    elif change_1h < -1 and change_24h < -3:
        return "🔴 فروخت کا اشارہ"
    else:
        return "🟡 انتظار کریں"

# Main execution
coins = fetch_top_coins(top_n)

if not coins:
    st.error("ڈیٹا حاصل نہیں ہو سکا۔ براہ کرم بعد میں کوشش کریں۔")
else:
    for coin in coins:
        with st.container():
            col1, col2 = st.columns([1, 3])

            with col1:
                st.image(coin["image"], width=50)
                st.subheader(f'{coin["name"]} ({coin["symbol"].upper()})')
                st.metric("قیمت", f"${coin['current_price']}")
                st.write(ai_signal(coin))

            with col2:
                sparkline = coin.get("sparkline_in_7d", {}).get("price", [])
                if sparkline:
                    df = pd.DataFrame(sparkline, columns=["Price"])
                    st.line_chart(df)
                else:
                    st.info("سپارکلائن دستیاب نہیں۔")

                if pattern_detect and sparkline:
                    pattern = detect_pattern(sparkline)
                    if pattern:
                        st.success(f"پیٹرن ڈیٹیکٹ ہوا: {pattern}")
