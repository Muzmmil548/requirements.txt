import streamlit as st
import pandas as pd
import time
import threading
import asyncio
import os
from utils.exchange_connectors import (
    BinanceConnector, BybitConnector, BitgetConnector, 
    KuCoinConnector, MexcConnector, OkxConnector, CmeConnector
)
from utils.data_processor import DataProcessor
from components.chart import display_chart
from components.orderbook import display_orderbook
from components.signals import display_signals, display_traffic_light
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.selected_exchange = "Binance"
    st.session_state.selected_symbol = "BTCUSDT"
    st.session_state.exchange_data = {}
    st.session_state.active_exchanges = {
        "Binance": True,
        "Bybit": False,
        "CME": False,
        "Bitget": False,
        "KuCoin": False,
        "MEXC": False,
        "OKX": False
    }
    st.session_state.update_interval = 2  # seconds
    st.session_state.timeframe = "1m"  # default timeframe
    st.session_state.stop_thread = False
    st.session_state.thread = None
    st.session_state.data_processor = DataProcessor()

# Main app title
st.title("Crypto Trading Dashboard")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    
    # Symbol selection
    symbols = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "XRPUSDT"]
    selected_symbol = st.selectbox("Select Trading Pair", symbols, index=symbols.index(st.session_state.selected_symbol))
    
    if selected_symbol != st.session_state.selected_symbol:
        st.session_state.selected_symbol = selected_symbol
        st.rerun()
    
    # Timeframe selection
    timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
    selected_timeframe = st.selectbox("Select Timeframe", timeframes, index=timeframes.index(st.session_state.timeframe))
    
    if selected_timeframe != st.session_state.timeframe:
        st.session_state.timeframe = selected_timeframe
        st.rerun()
    
    # Exchange selection
    st.subheader("Exchanges")
    
    # Create toggle switches for each exchange
    exchanges = list(st.session_state.active_exchanges.keys())
    for exchange in exchanges:
        is_active = st.toggle(f"{exchange}", value=st.session_state.active_exchanges[exchange], key=f"toggle_{exchange}")
        
        # Update active state
        if is_active != st.session_state.active_exchanges[exchange]:
            st.session_state.active_exchanges[exchange] = is_active
            if is_active and st.session_state.selected_exchange != exchange:
                st.session_state.selected_exchange = exchange
                st.rerun()
    
    # Select which active exchange to display
    active_exchanges = [ex for ex in exchanges if st.session_state.active_exchanges[ex]]
    if active_exchanges:
        selected_exchange = st.selectbox("Display Exchange", active_exchanges, index=active_exchanges.index(st.session_state.selected_exchange) if st.session_state.selected_exchange in active_exchanges else 0)
        if selected_exchange != st.session_state.selected_exchange:
            st.session_state.selected_exchange = selected_exchange
            st.rerun()
    else:
        st.warning("Please enable at least one exchange")

# Function to initialize exchange connectors
def initialize_connectors():
    connectors = {}
    
    # Initialize connectors for enabled exchanges
    if st.session_state.active_exchanges["Binance"]:
        connectors["Binance"] = BinanceConnector()
    
    if st.session_state.active_exchanges["Bybit"]:
        connectors["Bybit"] = BybitConnector()
    
    if st.session_state.active_exchanges["CME"]:
        connectors["CME"] = CmeConnector()
    
    if st.session_state.active_exchanges["Bitget"]:
        connectors["Bitget"] = BitgetConnector()
    
    if st.session_state.active_exchanges["KuCoin"]:
        connectors["KuCoin"] = KuCoinConnector()
    
    if st.session_state.active_exchanges["MEXC"]:
        connectors["MEXC"] = MexcConnector()
    
    if st.session_state.active_exchanges["OKX"]:
        connectors["OKX"] = OkxConnector()
    
    return connectors

# Function to update data in background
async def update_data_async(connectors, symbol, timeframe, stop_event):
    while not stop_event.is_set():
        try:
            for exchange_name, connector in connectors.items():
                # Fetch klines (candlestick data)
                klines = await connector.get_klines(symbol, timeframe, limit=100)
                
                # Fetch orderbook
                orderbook = await connector.get_orderbook(symbol)
                
                # Fetch recent trades
                trades = await connector.get_trades(symbol, limit=50)
                
                # Update session state with new data
                if exchange_name not in st.session_state.exchange_data:
                    st.session_state.exchange_data[exchange_name] = {}
                
                st.session_state.exchange_data[exchange_name].update({
                    'klines': klines,
                    'orderbook': orderbook,
                    'trades': trades,
                    'last_update': time.time()
                })
                
                # Calculate indicators
                if klines is not None and len(klines) > 0:
                    indicators = st.session_state.data_processor.calculate_indicators(klines)
                    st.session_state.exchange_data[exchange_name]['indicators'] = indicators
                
                # Small delay between exchanges to avoid API rate limits
                await asyncio.sleep(0.5)
            
            # Wait for the update interval
            await asyncio.sleep(st.session_state.update_interval)
        
        except Exception as e:
            logger.error(f"Error updating data: {e}")
            await asyncio.sleep(5)  # Wait a bit longer if there's an error

def update_data_thread():
    connectors = initialize_connectors()
    stop_event = threading.Event()
    
    async def run_updates():
        await update_data_async(
            connectors,
            st.session_state.selected_symbol,
            st.session_state.timeframe,
            stop_event
        )
    
    # Run the async loop in the thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(run_updates())
    finally:
        loop.close()
    
    st.session_state.stop_thread = False

# Start or restart the update thread when needed
if not st.session_state.initialized or st.session_state.stop_thread:
    # Stop existing thread if it's running
    if st.session_state.thread is not None and st.session_state.thread.is_alive():
        st.session_state.stop_thread = True
        st.session_state.thread.join(timeout=5)
    
    # Start a new thread
    st.session_state.stop_thread = False
    st.session_state.thread = threading.Thread(target=update_data_thread)
    st.session_state.thread.daemon = True
    st.session_state.thread.start()
    st.session_state.initialized = True

# Main dashboard layout
col1, col2 = st.columns([7, 3])

with col1:
    # Price Chart
    st.subheader(f"{st.session_state.selected_symbol} Chart ({st.session_state.selected_exchange})")
    
    chart_placeholder = st.empty()
    
    # Check if we have data for the selected exchange
    if (st.session_state.selected_exchange in st.session_state.exchange_data and 
        'klines' in st.session_state.exchange_data[st.session_state.selected_exchange]):
        
        klines_data = st.session_state.exchange_data[st.session_state.selected_exchange]['klines']
        indicators_data = st.session_state.exchange_data[st.session_state.selected_exchange].get('indicators', {})
        
        with chart_placeholder.container():
            display_chart(klines_data, indicators_data, st.session_state.selected_symbol)
    else:
        chart_placeholder.info(f"Waiting for {st.session_state.selected_exchange} data...")

with col2:
    # Order Book / DOM
    st.subheader("Order Book (DOM)")
    orderbook_placeholder = st.empty()
    
    if (st.session_state.selected_exchange in st.session_state.exchange_data and 
        'orderbook' in st.session_state.exchange_data[st.session_state.selected_exchange]):
        
        orderbook_data = st.session_state.exchange_data[st.session_state.selected_exchange]['orderbook']
        
        with orderbook_placeholder.container():
            display_orderbook(orderbook_data)
    else:
        orderbook_placeholder.info("Waiting for orderbook data...")
    
    # Trading Signals
    st.subheader("Trading Signals")
    signals_placeholder = st.empty()
    
    if (st.session_state.selected_exchange in st.session_state.exchange_data and 
        'indicators' in st.session_state.exchange_data[st.session_state.selected_exchange]):
        
        indicators = st.session_state.exchange_data[st.session_state.selected_exchange]['indicators']
        
        with signals_placeholder.container():
            display_signals(indicators)
            
            # Traffic Light System
            st.subheader("Signal Summary")
            display_traffic_light(indicators)
    else:
        signals_placeholder.info("Calculating signals...")

# Footer
st.markdown("---")
st.caption("Cryptocurrency Trading Dashboard - Real-time data and signals")

# On app close, stop the background thread
import atexit

def cleanup():
    if hasattr(st.session_state, 'stop_thread'):
        st.session_state.stop_thread = True
    if hasattr(st.session_state, 'thread') and st.session_state.thread is not None:
        st.session_state.thread.join(timeout=1)

atexit.register(cleanup)
