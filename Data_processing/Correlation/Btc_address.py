import pandas as pd
import yfinance as yf
from blockchain import statistics

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch the number of unique Bitcoin addresses data
stats = statistics.get()
unique_addresses = stats.n_unique_addresses

# Convert the unique addresses data into a DataFrame
address_data = pd.DataFrame(unique_addresses, columns=['Date', 'Unique Addresses'])
address_data['Date'] = pd.to_datetime(address_data['Date'].dt.date)
address_data = address_data.set_index('Date')

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the unique address data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_returns, address_data], axis=1).dropna()
combined_data.columns = ['BTC', 'Unique Addresses']

# Calculate the correlation between Bitcoin returns and the number of unique addresses
correlation = combined_data.corr()
print(correlation)
