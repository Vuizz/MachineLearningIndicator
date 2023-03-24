import os
import spacy
from newsapi import NewsApiClient

# Set your News API key
newsapi = NewsApiClient(api_key='<YOUR_API_KEY>')

# Define the date range
start_date = '2020-01-01'
end_date = '2021-09-30'

# Fetch news articles related to the cryptocurrency industry
articles = newsapi.get_everything(q='cryptocurrency', language='en', sort_by='relevancy', from_param=start_date, to=end_date, page_size=100)

# Load SpaCy's English language model
nlp = spacy.load('en_core_web_sm')

# Perform Named Entity Recognition (NER) on the fetched news articles
industry_entities = []

for article in articles['articles']:
    text = article['title'] + ' ' + article['description']
    doc = nlp(text)
    
    count = 0
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'GPE']:
            count += 1

    if count > 0:
        date = pd.to_datetime(article['publishedAt']).date()
        industry_entities.append((date, count))

# Convert the industry entity data into a DataFrame
industry_data = pd.DataFrame(industry_entities, columns=['Date', 'Count'])
industry_data = industry_data.groupby('Date').sum()

# Download historical data for Bitcoin
btc = yf.download('BTC-USD', start=start_date, end=end_date, progress=False)

# Use the 'Close' prices to calculate daily returns
btc_returns = btc['Close'].pct_change().dropna()

# Merge the industry data and Bitcoin returns into a single DataFrame
combined_data = pd.concat([btc_returns, industry_data], axis=1).dropna()
combined_data.columns = ['BTC', 'Industry Entities']

# Calculate the correlation between Bitcoin returns and industry entity counts
correlation = combined_data.corr()
print(correlation)
