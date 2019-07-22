#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import csv
import json
import pprint
from collections import Counter

# load Twitter API credentials

pp = pprint.PrettyPrinter(indent=4)

with open('credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']

def retrieve_tweets():

        tweets = []
	hashtags = []

# Twitter allows access to only 3240 tweets via this method


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	for tweet in tweepy.Cursor(api.search, geocode="52.340413,4.917447,6km").items(100):
		tweets.append(tweet._json)
	
	for tweet in tweets:
		if (len(tweet['entities']['hashtags']) > 0):
			for hashtag in tweet['entities']['hashtags']:
				hashtags.append(hashtag['text'])

	pp.pprint(Counter(hashtags))

retrieve_tweets()
