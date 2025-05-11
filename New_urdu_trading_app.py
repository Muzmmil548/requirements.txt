import streamlit as st
import pandas as pd
class TradingViewApp:
    def __init__(self):
        self.exchanges = {
            'Binance': False,
            'Bybit': False,
            'CME': False,
            'Bitget': False,
            'KuCoin': False,
            'MEXC': False,
            'OKX': False
        }
        self.data = None

    def toggle_exchange(self, exchange):
        if exchange in self.exchanges:
            self.exchanges[exchange] = not self.exchanges[exchange]

    def fetch_live_data(self, exchange):
        # Placeholder for fetching live data from the exchange API
        # This should be replaced with actual API calls
        return pd.DataFrame()

    def calculate_indicators(self):
        if self.data is not None:
            self.data['EMA_20'] = self.data['Close'].ewm(span=20, adjust=False).mean()
            self.data['RSI'] = self.calculate_rsi(self.data['Close'])
            self.data['MACD'] = self.calculate_macd(self.data['Close'])
            self.data['Volume_Spike'] = self.data['Volume'].rolling(window=20).mean()
            self.data['VWAP'] = self.calculate_vwap(self.data)
            self.data['Order_Imbalance'] = self.calculate_order_imbalance()

    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(self, series):
        exp1 = series.ewm(span=12, adjust=False).mean()
        exp2 = series.ewm(span=26, adjust=False).mean()
        return exp1 - exp2

    def calculate_vwap(self, df):
        return (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()

    def calculate_order_imbalance(self):
        # Placeholder for order imbalance calculation
        return np.random.rand(len(self.data))

    def generate_signals(self):
        self.data['Signal'] = 'Neutral'
        conditions = [
            (self.data['EMA_20'] > self.data['Close']) & (self.data['RSI'] < 30),
            (self.data['EMA_20'] < self.data['Close']) & (self.data['RSI'] > 70)
        ]
        choices = ['Buy', 'Sell']
        self.data['Signal'] = np.select(conditions, choices, default='Neutral')

    def display_signals(self):
        color_map = {'Buy': 'green', 'Sell': 'red', 'Neutral': 'yellow'}
        self.data['Color'] = self.data['Signal'].map(color_map)
        plt.scatter(self.data.index, self.data['Close'], c=self.data['Color'])
        plt.title('Trading Signals')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.show()

    def run(self):
        for exchange, active in self.exchanges.items():
            if active:
                self.data = self.fetch_live_data(exchange)
                self.calculate_indicators()
                self.generate_signals()
                self.display_signals()

app = TradingViewApp()
app.toggle_exchange('Binance')
app.run()
        
