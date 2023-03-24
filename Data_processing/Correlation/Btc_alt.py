import os
import cryptocompare
import pandas as pd
from datetime import datetime

# Set your CryptoCompare API key
cryptocompare.cryptocompare._set_api_key_parameter('<YOUR_API_KEY>')

# Define a function to fetch historical price data for a given cryptocurrency
def get_crypto_data(crypto, currency='USD', start_date='2020-01-01', end_date='2021-09-30'):
    start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
    end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
    data = cryptocompare.get_historical_price_day(crypto, currency=currency, toTs=end_timestamp, limit=2000)
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

# Fetch historical price data for Bitcoin and an altcoin (e.g., Ethereum)
btc = get_crypto_data('BTC')
eth = get_crypto_data('ETH')

# Use the 'close' prices to calculate daily returns
btc_returns = btc['close'].pct_change().dropna()
eth_returns = eth['close'].pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, eth_returns], axis=1)
combined_returns.columns = ['BTC', 'ETH']

# Calculate the correlation between Bitcoin and Ethereum returns
correlation = combined_returns.corr()
print(correlation)
