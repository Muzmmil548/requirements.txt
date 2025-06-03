import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# بیننس API کے بغیر ڈیمو ڈیٹا
def get_demo_data():
    date_rng = pd.date_range(end=datetime.today(), periods=100, freq='5min')
    prices = np.cumsum(np.random.randn(100) * 0.5) + 100
    data = pd.DataFrame({
        'timestamp': date_rng,
        'Open': prices - np.random.uniform(0.5, 1.5, 100),
        'High': prices + np.random.uniform(0.5, 1.5, 100),
        'Low': prices - np.random.uniform(1.5, 2.5, 100),
        'Close': prices,
        'Volume': np.random.randint(100, 1000, 100)
    })
    return data

# 2. ریاضیاتی فیچرز
def calculate_features(data):
    data['MA20'] = data['Close'].rolling(20).mean()
    data['MA50'] = data['Close'].rolling(50).mean()
    
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    data['RSI'] = 100 - (100 / (1 + gain/loss))
    
    data['Momentum'] = data['Close'].diff(5)
    
    return data.dropna()

# 3. AI ماڈل
def train_model(data):
    X = data[['MA20', 'RSI', 'Momentum']]
    y = (data['Close'].shift(-5) > data['Close']).astype(int)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

# 4. سگنل جنریٹر
def generate_signal(model, current_data):
    features = pd.DataFrame({
        'MA20': [current_data['MA20'].iloc[-1]],
        'RSI': [current_data['RSI'].iloc[-1]],
        'Momentum': [current_data['Momentum'].iloc[-1]]
    })
    proba = model.predict_proba(features)[0][1]
    
    if proba > 0.7 and current_data['Momentum'].iloc[-1] > 0:
        return 'BUY'
    elif proba < 0.3 and current_data['Momentum'].iloc[-1] < 0:
        return 'SELL'
    return 'HOLD'

# 5. ٹریڈنگ ویو چارٹ
def create_tradingview_chart(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data['timestamp'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['MA20'],
        line=dict(color='blue', width=1),
        name='MA 20'
    ))
    
    fig.add_trace(go.Scatter(
        x=data['timestamp'],
        y=data['MA50'],
        line=dict(color='orange', width=1),
        name='MA 50'
    ))
    
    fig.update_layout(
        title='ٹریڈنگ ویو چارٹ',
        xaxis_title='تاریخ',
        yaxis_title='قیمت',
        xaxis_rangeslider_visible=False,
        height=600
    )
    
    return fig

# 6. Streamlit ایپ
def main():
    st.title("AI اسکیلپنگ ٹریڈر - ڈیمو ورژن")
    
    # ڈیٹا لوڈ کریں
    data = get_demo_data()
    data = calculate_features(data)
    model = train_model(data)
    
    # ٹریڈنگ ویو چارٹ
    st.plotly_chart(create_tradingview_chart(data.tail(100)), use_container_width=True)
    
    # سگنل جنریٹر
    st.header("سگنل جنریٹر")
    current_price = st.number_input("موجودہ قیمت درج کریں", value=float(data['Close'].iloc[-1]))
    
    if st.button("سگنل جنریٹ کریں"):
        current_data = pd.DataFrame({
            'MA20': [data['MA20'].iloc[-1]],
            'RSI': [data['RSI'].iloc[-1]],
            'Momentum': [current_price - data['Close'].iloc[-2]]
        })
        
        signal = generate_signal(model, current_data)
        
        if signal == 'BUY':
            st.success(f"سگنل: {signal} 🟢")
            st.info(f"سٹاپ لاس: {current_price * 0.99:.2f}")
            st.info(f"ٹارگٹ: {current_price * 1.02:.2f}")
        elif signal == 'SELL':
            st.error(f"سگنل: {signal} 🔴")
            st.info(f"سٹاپ لاس: {current_price * 1.01:.2f}")
            st.info(f"ٹارگٹ: {current_price * 0.98:.2f}")
        else:
            st.warning(f"سگنل: {signal} 🟡")

if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    main()
