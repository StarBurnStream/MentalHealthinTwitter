# -*- coding: utf-8 -*-
"""
Created on Thu May 25 14:03:48 2017

@author: Destiny
"""
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from tweepy.models import Status
from tweepy.api import API
import time
import argparse
import string
import config
import json

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth)

f = open("Data/pastWeek2.json","a")

for tweet in tweepy.Cursor(api.search,q="sad",count=100,\
                           lang="en",\
                           since="2017-05-10").items():
    try:
        f.write(str(tweet.__repr__)+'\n\n')
        print(tweet.created_at)
    except BaseException as e:
        print("Error on_data: %s" % str(e))
f.close()