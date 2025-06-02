# --- Chart Patterns (Improved Display with AI Signal) ---
st.markdown("---")
st.subheader("📊 چارٹ پیٹرن AI سگنلز:")

chart_patterns = [
    "Head & Shoulders", "Inverse H&S", "Double Top", "Double Bottom",
    "Symmetrical Triangle", "Ascending Triangle", "Descending Triangle",
    "Falling Wedge", "Rising Wedge", "Cup & Handle", "Bullish Flag",
    "Bearish Flag", "Rectangle", "Triple Top", "Triple Bottom"
]

def simulate_patterns():
    return {p: random.choice(["🟢 Buy", "🔴 Sell", "🟡 Hold", "❌ No Pattern"]) for p in chart_patterns}

patterns = simulate_patterns()

# 3 Columns layout for better visual alignment
cols = st.columns(3)
for i, (pattern, signal) in enumerate(patterns.items()):
    with cols[i % 3]:
        color = "green" if "🟢" in signal else "red" if "🔴" in signal else "orange" if "🟡" in signal else "gray"
        st.markdown(f"""
        <div style='border:2px solid {color}; border-radius:10px; padding:10px; margin:5px; background-color:#f9f9f9; font-size:16px'>
        <b>{pattern}</b><br>
        Signal: <span style='color:{color}; font-weight:bold;'>{signal}</span>
        </div>
        """, unsafe_allow_html=True)

# --- Confirmed Inverse H&S Alert (if active) ---
if patterns.get("Inverse H&S") == "🟢 Buy":
    confirmed = random.choice([True, False])
    if confirmed:
        ihs_alert = """
        <div style='background-color:#d0f0c0; padding:20px; border-radius:10px; font-size:18px; border:2px solid green'>
        <b>📈 Inverse Head & Shoulders کنفرم ہو چکا ہے!</b><br><br>
        🕒 Timeframe: Simulated 1H<br>
        📍 Neckline Breakout: ✅ Confirmed<br>
        🎯 Signal: <span style='color:green; font-weight:bold;'>Bullish Reversal</span><br>
        🔔 Action: Buying Zone Active
        </div>
        """
        st.markdown(ihs_alert, unsafe_allow_html=True)
