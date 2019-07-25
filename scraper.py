#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import csv
import json
import pprint
import MySQLdb
import io
import re
import time
from datetime import datetime
from time import mktime 
from datetime import timedelta

# load Twitter API credentials

pp = pprint.PrettyPrinter(indent=4)

with open('credentials.json') as cred_data:
	info = json.load(cred_data)
	consumer_key = info['CONSUMER_KEY']
	consumer_secret = info['CONSUMER_SECRET']
	access_key = info['ACCESS_KEY']
	access_secret = info['ACCESS_SECRET']
	
	parameters= {}
	parameters['hostname'] = info['HOSTNAME']
	parameters['database'] = info['DATABASE']
	parameters['user'] = info['USER']
	parameters['password'] = info['PASSWORD']

def retrieve_hashtags():

	tweets = []
	hashtags = []

# Twitter allows access to only 3240 tweets via this method

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)
	startSearchDate = datetime.now() - timedelta(hours=72) 

	for tweet in tweepy.Cursor(api.search, geocode="52.340413,4.917447,6km").items(3240):
		tweets.append(tweet._json)
	
	for tweet in tweets:
		tweet_id = tweet['id_str']
		if (len(tweet['entities']['hashtags']) > 0):
			for hashtag in tweet['entities']['hashtags']:
				hashtag_id = str(hashtag['indices'][0]) + str(hashtag['indices'][1])
				combined_id = tweet_id + hashtag_id
				combined_id = combined_id[-10:]
				hashtag_text = hashtag['text']
				created_at_object = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
				created_at = created_at_object.strftime("%Y-%m-%d %H:%M:%S")
				if created_at_object > startSearchDate:
					hashtags.append({'createdat': created_at, 'combinedid': combined_id, 'hashtagtext': hashtag_text})
	return hashtags

def form_sql_query(hashtags):
	query = "INSERT IGNORE INTO hashtagdata (combinedid,hashtag,time) VALUES "
	for hashtag in hashtags:
		query = query + "(%s,'%s','%s')," % (hashtag['combinedid'],hashtag['hashtagtext'],hashtag['createdat'])
	query = query[:-1] + ";"
	return query

def execute_sql_query(query, parameters):
	connection = MySQLdb.connect(host= parameters['hostname'],
				  user= parameters['user'],
				  passwd= parameters['password'],
				  db= parameters['database'])
	cursor = connection.cursor()
	connection.set_character_set('utf8mb4')
	#cursor.execute('SET NAMES utf8mb4;')
	#cursor.execute('SET CHARACTER SET utf8mb4;')
	#cursor.execute('SET character_set_connection=utf8mb4;')
	#connection.commit()
	try:
		cursor.execute(query)
		print("affected rows = {}".format(cursor.rowcount))
		connection.commit()
	except MySQLdb.Error, e:
		try:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			return None
		except IndexError:
			print "MySQL Error: %s" % str(e)
			return None
	except TypeError, e:
		print(e)
		return None
	except ValueError, e:
		print(e)
		return None
	finally:
		cursor.close()
		connection.close()

def main():
	hashtags = retrieve_hashtags()
	execute_sql_query(form_sql_query(hashtags), parameters)
	
main()
