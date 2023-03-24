import os
import quandl
import pandas as pd

# Set your Quandl API key
quandl.ApiConfig.api_key = '<YOUR_API_KEY>'

# Download historical data for Bitcoin and its hash rate
btc = quandl.get('BCHAIN/MKPRU', start_date='2020-01-01', end_date='2021-09-30')
btc_hash_rate = quandl.get('BCHAIN/HRATE', start_date='2020-01-01', end_date='2021-09-30')

# Use the 'Value' columns to calculate daily returns for both datasets
btc_returns = btc.pct_change().dropna()
btc_hash_rate_returns = btc_hash_rate.pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, btc_hash_rate_returns], axis=1)
combined_returns.columns = ['BTC', 'Hash Rate']

# Calculate the correlation between Bitcoin and its hash rate
correlation = combined_returns.corr()
print(correlation)
