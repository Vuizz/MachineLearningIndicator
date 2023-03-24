import yfinance as yf
import pandas as pd

# Download historical data for Bitcoin and SPDR Gold Shares ETF (GLD)
btc = yf.download('BTC-USD', start='2020-01-01', end='2021-09-30', progress=False)
gld = yf.download('GLD', start='2020-01-01', end='2021-09-30', progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()
gld_returns = gld['Close'].pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, gld_returns], axis=1)
combined_returns.columns = ['BTC', 'Gold']

# Calculate the correlation between Bitcoin and gold returns
correlation = combined_returns.corr()
print(correlation)
