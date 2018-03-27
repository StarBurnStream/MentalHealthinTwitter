from twarc import Twarc
import config
import json
import sys
import unicodedata as ud
import codecs
import time

t = Twarc(config.consumer_key, config.consumer_secret,config.access_token, config.access_secret)
outfile = open("sad_Newyork_10.json","a")

Location = '40.7484,-73.9857,1mi' #Newyork
maxid = 865200000000000000
sinceid = 859000000000000000



count = 10
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
for tweet in t.search("sad",geocode=Location,max_id = maxid, since_id = sinceid):
    if count >0:
        tweet["text"] = tweet["text"].translate(non_bmp_map)
#        print(tweet["text"])
        print(tweet["created_at"])
        outfile.write(json.dumps(tweet)+"\n\n")
        count -=1
    else:
        break
#print(count)
outfile.close
