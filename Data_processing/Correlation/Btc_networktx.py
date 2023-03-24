import pandas as pd
import yfinance as yf
from blockchain import statistics

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch Bitcoin transaction volume data
stats = statistics.get()
transaction_volume = stats.trade_volume_btc

# Convert the transaction volume data into a DataFrame
transaction_data = pd.DataFrame(transaction_volume, columns=['Date', 'Volume'])
transaction_data['Date'] = pd.to_datetime(transaction_data['Date'].dt.date)
transaction_data = transaction_data.set_index('Date')

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the transaction volume data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_returns, transaction_data], axis=1).dropna()
combined_data.columns = ['BTC', 'Transaction Volume']

# Calculate the correlation between Bitcoin returns and transaction volume
correlation = combined_data.corr()
print(correlation)
