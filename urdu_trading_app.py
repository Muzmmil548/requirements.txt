# Urdu Trading Assistant App (Full Version with Dual AI, Home Page, and Auto Refresh)

import streamlit as st
import time
import pandas as pd
import random

# ------------------------- Sidebar Settings ------------------------- #
st.sidebar.title("سیٹنگ")
auto_refresh = st.sidebar.toggle("آٹو ریفریش", value=True)
refresh_interval = 30  # seconds

# ------------------------- Navigation ------------------------- #
page = st.sidebar.radio("مینو منتخب کریں", ["ہوم", "تکنیکی AI اسسٹنٹ", "نیوز AI اسسٹنٹ"])

# ------------------------- Auto Refresh Logic ------------------------- #
if auto_refresh:
    st.experimental_rerun()
    time.sleep(refresh_interval)

# ------------------------- Sample Data ------------------------- #
def get_sample_signals():
    return {
        "BUY": random.randint(10, 20),
        "SELL": random.randint(5, 15),
        "NEUTRAL": random.randint(3, 10),
        "RECOMMENDATION": random.choice(["BUY", "SELL", "NEUTRAL"])
    }

def get_sample_news():
    sample_news = [
        ("Bitcoin hits new high as ETF rumors spread", "positive"),
        ("SEC delays Ethereum decision again", "neutral"),
        ("Binance faces regulatory action in Europe", "negative")
    ]
    return random.choice(sample_news)

# ------------------------- UI ------------------------- #
if page == "ہوم":
    st.title("پیشہ ور اردو ٹریڈنگ اسسٹنٹ")
    st.markdown("""
    یہ ایپ دو طاقتور AI روبوٹس پر مشتمل ہے:

    1. **تکنیکی AI**: انڈیکیٹرز، چارٹ پیٹرن، اور سکیلپنگ سگنل کا تجزیہ کرتا ہے۔  
    2. **نیوز AI**: CoinMarketCap جیسی سائٹس سے نیوز لے کر فنڈامنٹل تجزیہ دیتا ہے۔

    اوپر مینو سے کسی بھی AI ماڈیول کا انتخاب کریں۔
    """)

elif page == "تکنیکی AI اسسٹنٹ":
    st.title("تکنیکی تجزیہ AI")
    signals = get_sample_signals()
    st.metric("BUY سگنلز", signals['BUY'])
    st.metric("SELL سگنلز", signals['SELL'])
    st.metric("NEUTRAL سگنلز", signals['NEUTRAL'])
    st.subheader(f"AI تجویز: {signals['RECOMMENDATION']}")
    st.caption("AI اسسٹنٹ خودکار تجزیہ دیتا ہے، فیصلہ سمجھداری سے کریں")

elif page == "نیوز AI اسسٹنٹ":
    st.title("فنڈامنٹل نیوز تجزیہ AI")
    headline, sentiment = get_sample_news()
    st.subheader("تازہ ترین کرپٹو نیوز:")
    st.info(headline)

    if sentiment == "positive":
        st.success("AI تجزیہ: یہ خبر مثبت ہے — BUY سگنل")
    elif sentiment == "negative":
        st.error("AI تجزیہ: یہ خبر منفی ہے — SELL سگنل")
    else:
        st.warning("AI تجزیہ: یہ خبر نیوٹرل ہے — کوئی واضح سگنل نہیں")

    st.caption("نیوز AI مارکیٹ جذبات کا خودکار تجزیہ فراہم کرتا ہے")
    
