import pandas as pd
import yfinance as yf
import ccxt
import datetime

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Initialize the CCXT Binance API
binance = ccxt.binance()

# Fetch historical OHLCV data for Bitcoin
ohlcv_data = binance.fetch_ohlcv('BTC/USDT', timeframe='1D', since=binance.parse8601(start_date), limit=1000)

# Convert the OHLCV data into a DataFrame
ohlcv_df = pd.DataFrame(ohlcv_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
ohlcv_df['Date'] = pd.to_datetime(ohlcv_df['timestamp'], unit='ms').dt.date
ohlcv_df = ohlcv_df.set_index('Date')

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the trading volume data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_returns, ohlcv_df['volume']], axis=1).dropna()
combined_data.columns = ['BTC', 'Trading Volume']

# Calculate the correlation between Bitcoin returns and trading volume
correlation = combined_data.corr()
print(correlation)
