
import streamlit as st

st.set_page_config(page_title="Scalping Checklist (Urdu)", layout="centered")

st.title("اسکیلپنگ ٹریڈ چیک لسٹ (اردو)")

st.header("ٹریڈ لینے سے پہلے نیچے والے پوائنٹس چیک کریں:")

checklist = [
    "کیا قیمت EMA 20 کے اوپر ہے؟ (Buy کے لیے)",
    "کیا قیمت EMA 20 کے نیچے ہے؟ (Sell کے لیے)",
    "کیا RSI اووربوٹ یا اوورسیل لیول کے قریب ہے؟",
    "کیا MACD لائن سگنل لائن کو کراس کر رہی ہے؟",
    "کیا وولیوم میں اچانک اضافہ ہوا ہے؟",
    "کیا آرڈر فلو یا DOM میں بڑی بائنگ/سیلنگ دکھ رہی ہے؟",
    "کیا VWAP سے دوری ہو گئی ہے؟ ریورژن کا موقع؟",
    "کیا ٹائم آف ڈے صحیح ہے؟ (NY/LD اوپن)",
    "کیا آپ نے اسٹاپ لاس اور ٹارگٹ سیٹ کیا؟",
    "کیا خبر (News) کا وقت نہیں ہے؟"
]

score = 0

for item in checklist:
    if st.checkbox(item):
        score += 1

st.subheader(f"آپ کے پوائنٹس: {score} / {len(checklist)}")

if score >= 7:
    st.success("آپ کی تیاری اچھی ہے، ٹریڈ لینے کا موقع ہو سکتا ہے۔")
elif 4 <= score < 7:
    st.warning("کچھ پوائنٹس مسنگ ہیں، احتیاط سے فیصلہ کریں۔")
else:
    st.error("ٹریڈ مت لیں، زیادہ تر پوائنٹس میچ نہیں کر رہے۔")

st.markdown("---")
st.caption("یہ چیک لسٹ صرف لرننگ اور پریکٹس کے لیے ہے۔")
