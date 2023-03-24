import os
import spacy
import pandas as pd
import yfinance as yf
from newsapi import NewsApiClient

# Set your News API key
newsapi = NewsApiClient(api_key='<YOUR_API_KEY>')

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch news articles related to Bitcoin
articles = newsapi.get_everything(q='Bitcoin', language='en', sort_by='relevancy', from_param=start_date, to=end_date, page_size=100)

# Load SpaCy's English language model
nlp = spacy.load('en_core_web_sm')

# Perform Named Entity Recognition (NER) on the fetched news articles
regulatory_entities = []

for article in articles['articles']:
    text = article['title'] + ' ' + article['description']
    doc = nlp(text)

    count = 0
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'LAW', 'GPE']:
            count += 1

    if count > 0:
        date = pd.to_datetime(article['publishedAt']).date()
        regulatory_entities.append((date, count))

# Convert the regulatory entity data into a DataFrame
regulatory_data = pd.DataFrame(regulatory_entities, columns=['Date', 'Count'])
regulatory_data = regulatory_data.groupby('Date').sum()

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the regulatory data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_returns, regulatory_data], axis=1).dropna()
combined_data.columns = ['BTC', 'Regulatory Entities']

# Calculate the correlation between Bitcoin returns and regulatory entity counts
correlation = combined_data.corr()
print(correlation)
