import pandas as pd
import numpy as np
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
from ta.volume import OnBalanceVolumeIndicator
from ta.others import CumulativeReturnIndicator
import requests

# Set API endpoint and parameters
url = 'https://api.coincap.io/v2/assets/bitcoin/history'
params = {
    'interval': 'd1',
    'start': '1367107200000',  # Bitcoin historical data available from April 28, 2013
    'end': '1616505600000',  # March 23, 2021
}

# Get data from API
response = requests.get(url, params=params).json()
data = response['data']

# Convert data to Pandas DataFrame and set index to timestamp
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('timestamp', inplace=True)

# Clean data and fill missing values
df.drop(['time', 'symbol'], axis=1, inplace=True)
df['priceUsd'].replace('None', np.nan, inplace=True)
df['priceUsd'].fillna(method='ffill', inplace=True)
df = df.astype(float)

# Calculate technical indicators
bb = BollingerBands(close=df['priceUsd'], window=20, window_dev=2)
df['bb_upperband'], df['bb_middleband'], df['bb_lowerband'] = bb.bollinger_hband(), bb.bollinger_mavg(), bb.bollinger_lband()

rsi = RSIIndicator(close=df['priceUsd'], window=14)
df['rsi'] = rsi.rsi()

ema = EMAIndicator(close=df['priceUsd'], window=50)
df['ema'] = ema.ema_indicator()

obv = OnBalanceVolumeIndicator(close=df['priceUsd'], volume=df['volume'])
df['obv'] = obv.on_balance_volume()

cri = CumulativeReturnIndicator(close=df['priceUsd'])
df['cri'] = cri.cumulative_return()

# Add more complex datapoints
df['daily_return'] = df['priceUsd'].pct_change()
df['volatility'] = (df['priceUsd'].rolling(20).std() / df['priceUsd'].rolling(20).mean()) * 100
df['returns_3days'] = df['priceUsd'].pct_change(periods=3)
df['returns_7days'] = df['priceUsd'].pct_change(periods=7)

# Normalize and scale data
cols_to_normalize = ['priceUsd', 'bb_upperband', 'bb_middleband', 'bb_lowerband', 'rsi', 'ema', 'obv', 'cri',
                     'daily_return', 'volatility', 'returns_3days', 'returns_7days']
df[cols_to_normalize] = (df[cols_to_normalize] - df[cols_to_normalize].mean()) / df[cols_to_normalize].std()

# Remove first row containing NaN values
df = df.iloc[1:]

# Save data to CSV file
df.to_csv('bitcoin_data.csv')
