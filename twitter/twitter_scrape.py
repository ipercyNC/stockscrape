import datetime
import os
import sys
import scipy
import numpy
import matplotlib.pyplot as plt
import pandas
from pandas.plotting import scatter_matrix
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import LogisticRegression
import snscrape.modules.twitter as sntwitter
import csv
import pandas as pd
import itertools
import json
import snscrape.modules.twitter as sntwitter
keyword = 'gme'
maxTweets = 3000
#tweets = {}
tdf = None
counts = {}

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown Type")

def scrape_tweets(start_date, end_date, output_file):
    tweets = {}
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + ' since:{start_date} until:{end_date} lang:en'
                                                        .format(start_date=start_date, end_date=end_date)).get_items()):
            # if i > maxTweets :
            #     break
            username = tweet.username
            text = tweet.content
            pubdate = tweet.date
            permalink = tweet.url
            tweets[tweet.id]= {
                "permalink":permalink,
                "pubdate":pubdate,
                "text":text,
                "username":username
            }
    with open(output_file, "w") as f:
        f.write(json.dumps(tweets, default=datetime_handler))


def tweet_count(json_path, json_files):
    for f in json_files:
        filename = os.path.splitext(f)[0]
        with open(os.path.join(json_path, f), "r") as read_file:
            data = json.load(read_file)
            counts[filename] = len(data.keys())


if __name__ == '__main__':
    #scrape_tweets('2020-01-01', '2020-01-31', 'jan2020.json')
    # scrape_tweets('2020-02-01', '2020-02-29', 'feb2020.json')
    # scrape_tweets('2020-03-01', '2020-03-31', 'mar2020.json')
    # scrape_tweets('2020-04-01', '2020-04-30', 'apr2020.json')
    # scrape_tweets('2020-05-01', '2020-05-31', 'may2020.json')
    # scrape_tweets('2020-06-01', '2020-06-30', 'jun2020.json')
    # scrape_tweets('2020-07-01', '2020-07-31', 'jul2020.json')
    # scrape_tweets('2020-08-01', '2020-08-31', 'aug2020.json')
    # scrape_tweets('2020-09-01', '2020-09-30', 'sep2020.json')
    # scrape_tweets('2020-10-01', '2020-10-31', 'oct2020.json')
    # scrape_tweets('2020-11-01', '2020-11-30', 'nov2020.json')
    # scrape_tweets('2020-12-01', '2020-12-31', 'dec2020.json')
    #scrape_tweets('2021-01-01', '2021-01-31', 'jan2021.json')
    #scrape_tweets('2021-02-01', '2021-02-28', 'feb2021.json')
    #scrape_tweets('2021-03-01', '2021-03-09', 'mar2021.json')
    json_path = os.path.join(os.getcwd(), 'json_files')
    tweet_count(json_path, ['jan2020.json', 'feb2020.json', 'mar2020.json', 'apr2020.json', 'may2020.json',
                 'jun2020.json', 'jul2020.json', 'aug2020.json', 'sep2020.json', 'oct2020.json',
                'nov2020.json', 'dec2020.json', 'jan2021.json', 'feb2021.json', 'mar2021.json'])
    print(counts)


