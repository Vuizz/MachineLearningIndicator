import yfinance as yf
import pandas as pd

# Download historical data for Bitcoin and S&P 500
btc = yf.download('BTC-USD', start='2020-01-01', end='2021-09-30', progress=False)
sp500 = yf.download('^GSPC', start='2020-01-01', end='2021-09-30', progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()
sp500_returns = sp500['Close'].pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, sp500_returns], axis=1)
combined_returns.columns = ['BTC', 'S&P500']

# Calculate the correlation between Bitcoin and S&P 500 returns
correlation = combined_returns.corr()
print(correlation)
