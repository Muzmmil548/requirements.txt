import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client

class TradingViewApp:
    def __init__(self):
        self.data = None
        self.api_key = 'your_api_key'  # یہاں اپنی Binance API key ڈالیں
        self.api_secret = 'your_api_secret'  # یہاں اپنی Binance Secret key ڈالیں

    def fetch_live_data(self):
        client = Client(self.api_key, self.api_secret)
        klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE)
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['close'] = data['close'].astype(float)
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['volume'] = data['volume'].astype(float)
        self.data = data[['close', 'high', 'low', 'volume']]

    def calculate_indicators(self):
        if self.data is not None:
            self.data['EMA_20'] = self.data['close'].ewm(span=20, adjust=False).mean()
            self.data['RSI'] = self.calculate_rsi(self.data['close'])

    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self):
        self.data['Signal'] = 'Neutral'
        conditions = [
            (self.data['EMA_20'] > self.data['close']) & (self.data['RSI'] < 30),
            (self.data['EMA_20'] < self.data['close']) & (self.data['RSI'] > 70)
        ]
        choices = ['Buy', 'Sell']
        self.data['Signal'] = np.select(conditions, choices, default='Neutral')

    def display_signals(self):
        color_map = {'Buy': 'green', 'Sell': 'red', 'Neutral': 'yellow'}
        self.data['Color'] = self.data['Signal'].map(color_map)
        plt.scatter(self.data.index, self.data['close'], c=self.data['Color'])
        plt.title('Trading Signals')
        plt.xlabel('Time')
        plt.ylabel('Price')
        st.pyplot(plt)  # Streamlit میں گراف دکھانے کے لیے

    def run(self):
        self.fetch_live_data()
        self.calculate_indicators()
        self.generate_signals()
        self.display_signals()

# ایپلیکیشن چلائیں
app = TradingViewApp()
app.run()
