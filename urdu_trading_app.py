# Urdu Trading Assistant App with GPT-4-Turbo + HuggingFace fallback
import streamlit as st
import time
import requests

# Sidebar toggle for auto-refresh
auto_refresh = st.sidebar.toggle("آٹو ریفریش", value=True)
refresh_interval = 30  # seconds

# Set OpenAI and HuggingFace tokens (store in secrets)
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
HF_API_KEY = st.secrets.get("HF_API_KEY", "")

# Fallback AI function using HuggingFace
def ai_fallback_response(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0].get("generated_text", "کوئی جواب نہیں ملا")
    return "فالو بیک ناکام ہوا"

# OpenAI GPT-4-Turbo response
@st.cache_data(show_spinner=False)
def get_gpt4_response(prompt):
    try:
        from openai import OpenAI
        openai.api_key = OPENAI_API_KEY
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "آپ ایک ماہر ٹریڈنگ اسسٹنٹ ہیں جو اردو میں تجزیہ کرتے ہیں۔"},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return ai_fallback_response(prompt)

# Sidebar Tabs for AI Sections
st.sidebar.title("AI روبوٹ")
ai_mode = st.sidebar.radio("ایک آپشن منتخب کریں:", ("AI سگنل اسسٹنٹ", "فنڈامینٹل نیوز تجزیہ"))

st.title("پروفیشنل اردو ٹریڈنگ اسسٹنٹ")
st.markdown("---")

# Home Panel
st.header("لائیو مارکیٹ انڈیکیٹرز اور AI تجزیہ")
st.markdown("**براہ کرم ایک کوائن منتخب کریں اور AI اسسٹنٹ کے تجزیہ کا انتظار کریں۔**")

# Select Coin Dropdown
coins = ["BTC", "ETH", "BNB", "SOL", "XRP"]
selected_coin = st.selectbox("کوائن منتخب کریں:", coins)

# User trigger prompt
if ai_mode == "AI سگنل اسسٹنٹ":
    prompt = f"{selected_coin} کے لیے مختصر اسکیلپنگ سگنل دو، صرف بائے، سیل یا ویٹ میں جواب دو۔"
elif ai_mode == "فنڈامینٹل نیوز تجزیہ":
    prompt = f"{selected_coin} کے لیے حالیہ خبریں اور فنڈامینٹل انیلیسس فراہم کریں، اردو میں۔"
else:
    prompt = "کسی بھی کرپٹو کوائن کے بارے میں تجزیہ کریں۔"

if st.button("AI تجزیہ حاصل کریں"):
    with st.spinner("AI سے جواب حاصل کیا جا رہا ہے..."):
        ai_result = get_gpt4_response(prompt)
        st.success("تجزیہ مکمل")
        st.write(ai_result)

# TradingView Chart (Optional)
st.markdown("---")
st.markdown("### لائیو ٹریڈنگ ویو چارٹ")
selected_symbol = st.selectbox("چارٹ منتخب کریں:", ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"])
st.components.v1.html(f"""
    <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_b15b7&symbol={selected_symbol}&interval=1&theme=dark" 
    width="100%" height="500" frameborder="0"></iframe>
""", height=500)

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_interval)
    st.experimental_rerun()

st.markdown("---")
st.info("AI اسسٹنٹ خودکار تجزیہ دیتا ہے، فیصلہ سمجھداری سے کریں")
