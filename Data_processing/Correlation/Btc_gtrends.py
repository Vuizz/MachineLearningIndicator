import pandas as pd
import yfinance as yf
from pytrends.request import TrendReq

# Set up the pytrends connection
pytrends = TrendReq(hl='en-US', tz=360)

# Define the search keyword and date range
keyword = 'Bitcoin'
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch historical Google Trends data
timeframe = f'{start_date} {end_date}'
pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
google_trends_data = pytrends.interest_over_time().drop(columns='isPartial')

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Resample Google Trends data to match the frequency of Bitcoin price data
google_trends_data_daily = google_trends_data.resample('D').interpolate()
google_trends_data_daily_returns = google_trends_data_daily.pct_change().dropna()

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the two return series into a single DataFrame
combined_returns = pd.concat([btc_returns, google_trends_data_daily_returns], axis=1).dropna()
combined_returns.columns = ['BTC', 'Google Trends']

# Calculate the correlation between Bitcoin and Google Trends data
correlation = combined_returns.corr()
print(correlation)
