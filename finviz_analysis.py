# THIS PROJECT PREDICTS SENTIMENT BASED ON TOP HEADLINES

# PROJECT GOALS:
# USER CAN INPUT STOCK NAMES
# PROGRAM SCRAPES DATA FROM FIN NEWS WEBSITE
# PLOTS THE GENERAL SENTIMENT USING POLARITY SCORES

# IMPORT LIBRARIES
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

website_url = 'https://finviz.com/quote.ashx?t='

# INTERACTIVE CHOICE

print('DO YOU WANT TO CHOOSE YOUR TICKERS?')
user_input = input().upper()

if user_input == 'YES':
    ticker_input = input('ENTER VALID TICKERS SEPARATED BY COMMAS: ')
    tickers = [ticker.strip() for ticker in ticker_input.split(',')]
else:
    print('THIS PROGRAM WILL USE AMZN, GOOG, FB AS DEFAULTS')
    tickers = ['AMZN', 'GOOG', 'FB']

news_tables = {}

for ticker in tickers:
    url = website_url + ticker

    # OPEN URL + ACCESS HTML DATA
    headers = {'user-agent': 'my-app'}
    response = requests.get(url, headers=headers)

    html = BeautifulSoup(response.text, 'html.parser')

    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

parsed_data = []  # LIST OBJ, LIST OF LISTS

for ticker, news_table in news_tables.items():

    for row in news_table.findAll('tr'):

        title = row.a.get_text()
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[0]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])
vader = SentimentIntensityAnalyzer()


def f(title): return vader.polarity_scores(title)['compound']


df['compound_score'] = df['title'].apply(f)

# ORGANIZE DATES


def organize_dates(date_str):
    if date_str is not None:
        return pd.to_datetime(date_str).date()
    else:
        return df['date'].fillna(method='ffill')


df['date'] = df['date'].apply(organize_dates)

plt.figure(figsize=(10, 10))
mean_df = df.groupby(['ticker', 'date']).mean()  # OF COMPOUND COLUMN
mean_df = mean_df.unstack()
mean_df = mean_df.xs('compound', axis='columns').transpose()
mean_df.plot(kind='bar')

plt.show
