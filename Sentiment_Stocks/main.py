from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

site = 'https://finviz.com/quote.ashx?t='
stocks = ['AMZN', 'GOOG', 'FB', 'NFLX', 'AAPL']

news_tables = {}

# Loops through each stock's webpage, acquiring the news table element
for stock in stocks:
    url = fiz_url + stock

    req = Request(url=url, headers={'user-agent': 'my-app'})
    response = urlopen(req)

    html = bs(response, features='html.parser')
    news_table = html.find(id='news-table')
    news_tables[stock] = news_table

parsed_data = []

# Loops through each row in table to get article time, date, and title
for stock, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([stock, date, time, title])

# Put data into Pandas DataFrame
df = pd.DataFrame(parsed_data, columns=['stock', 'date', 'time', 'title'])

# Trained sentiment analyzer
vader = SentimentIntensityAnalyzer()

f = lambda title: vader.polarity_scores(title)['compound']
# Apply polarity analysis on each title and adds new column "compound"
df['compound'] = df['title'].apply(f)
df['date'] = pd.to_datetime(df.date).dt.date  # convert date column from string to datetime format

# Set up DataFrame to average sentiment scores per stock per day
df = df.groupby(['stock', 'date']).mean()
df = df.unstack()
df = df.xs('compound', axis="columns").transpose()

# Visualize data
df.plot(
    kind='bar', 
    title='Sentiment Analysis of Stock Headlines',
    ylabel='Sentiment Score',
    xlabel='Date',
    figsize=(16,10))
plt.show()