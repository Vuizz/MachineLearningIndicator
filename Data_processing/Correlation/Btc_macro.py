import yfinance as yf
import pandas as pd

# Download historical data for Bitcoin and the US Dollar Index
btc = yf.download('BTC-USD', start='2020-01-01', end='2021-09-30', progress=False)
dxy = yf.download('DX-Y.NYB', start='2020-01-01', end='2021-09-30', progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()
dxy_returns = dxy['Close'].pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, dxy_returns], axis=1)
combined_returns.columns = ['BTC', 'DXY']

# Calculate the correlation between Bitcoin and the US Dollar Index
correlation = combined_returns.corr()
print(correlation)
