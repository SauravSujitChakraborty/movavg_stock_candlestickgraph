import pandas as pd
from yahooquery import Ticker
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuration
symbol = 'CBA.AX'
start_date = '2016-06-01'
end_date = '2017-06-01'

print(f"Downloading data for {symbol} using alternative engine...")

try:
    # 1. Using yahooquery to bypass the yfinance block
    t = Ticker(symbol, asynchronous=False)
    df = t.history(start=start_date, end=end_date)

    if df.empty or 'adjclose' not in df.columns:
        print("Still blocked by Yahoo. Please try again in 15 minutes.")
    else:
        # 2. Reformat data (yahooquery uses a MultiIndex by default)
        df = df.reset_index().set_index('date')
        
        # 3. Technical Calculations
        df['MA50'] = df['adjclose'].rolling(50).mean()
        df['MA200'] = df['adjclose'].rolling(200).mean()

        # 4. Visualization
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.1, subplot_titles=('Price', 'Volume'),
                            row_heights=[0.7, 0.3])

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df.index, open=df['open'], high=df['high'], 
            low=df['low'], close=df['adjclose'], name='OHLC'
        ), row=1, col=1)
        
        # Moving Averages
        fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], line=dict(color='gray'), name='MA50'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df['MA200'], line=dict(color='orange'), name='MA200'), row=1, col=1)

        # Volume
        fig.add_trace(go.Bar(x=df.index, y=df['volume'], marker_color='red', name='Volume'), row=2, col=1)

        fig.update_layout(height=800, template='plotly_white', xaxis_rangeslider_visible=False)

        print("Success! Opening chart...")
        fig.show()

except Exception as e:
    print(f"Connection Error: {e}")