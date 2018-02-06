# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q apple -d data
# 
# It will produce the list of tweets for the query "apple" 
# in the file data/stream_apple.json

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

NUM_TWEET = 3
KEYWORD = 'sad'
#LOCATION = [[-76.89,40.95,-76.87,40.97],'Lewisburg'] # Lewisburg
#LOCATION = [[-6.38,49.87,1.77,55.81],'UK'] # UK
LOCATION = [[-124.87,27.5,-66.72,48.8], 'USA'] # USA

class CustomStreamListener(tweepy.StreamListener):

    def __init__(self,api = None,keyword = None, numTweet = 10, location = None):
        self.api = api
        self.keyword = keyword
        self.numTweet = numTweet
        self.location = location[1]
        self.count = 0
        self.outfile = "Data/stream_%s_%s_%d.json" % (self.keyword,self.location,self.numTweet)
        
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        status = Status.parse(self.api, data)
        try:
            if self.keyword in status.text:
                with open(self.outfile, 'a') as f:
                    f.write(raw_data)
                    print(raw_data)
                    self.count += 1
                    return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        if self.count >= self.numTweet:
            return False
        return True

    def on_error(self, status):
        print(status)
        return True
        

twitter_stream = Stream(auth, CustomStreamListener(api,KEYWORD,NUM_TWEET,LOCATION))
twitter_stream.filter(locations=LOCATION[0])
