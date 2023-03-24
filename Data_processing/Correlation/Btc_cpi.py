import pandas as pd
import yfinance as yf
from fredapi import Fred

# Set your FRED API key
fred = Fred(api_key='<YOUR_API_KEY>')

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch US CPI data
cpi_data = fred.get_series('CPIAUCSL', start_date, end_date, frequency='m')
cpi_data = cpi_data.pct_change().dropna()

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate monthly returns
btc_monthly = btc['Close'].resample('M').last().pct_change().dropna()

# Merge the CPI data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_monthly, cpi_data], axis=1).dropna()
combined_data.columns = ['BTC', 'CPI']

# Calculate the correlation between Bitcoin returns and CPI
correlation = combined_data.corr()
print(correlation)


# First, you'll need to sign up for an API key on the FRED website 
# (https://fred.stlouisfed.org/).
