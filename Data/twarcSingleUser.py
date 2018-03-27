# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:35:34 2017

@author: Destiny
"""
import datetime
from twarc import Twarc
import config
import json
import Utility
import pytz

t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
#endDate = Utility.dateStrToDate("Mon Feb 26 00:00:00 +0000 2018") + datetime.timedelta(1)
#beginDate = Utility.dateStrToDate("Mon Feb 26 00:00:00 +0000 2018")
localtz = 'America/New_York'
lastDate = Utility.dateStrToDate("Tue Mar 06 00:00:00 +0000 2018") + datetime.timedelta(1)
firstDate = Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017")
firstDate = firstDate.replace(tzinfo=localtz)
lastDate = lastDate.replace(tzinfo=localtz)
for tweet in t.timeline(screen_name='realDonaldTrump'):
#for tweet in t.filter(locations="-109.04891967773438,41.000422564349186,-102.04925537109375,36.997726914787634"):
    currentDate = Utility.getNewYorkTime(tweet["created_at"])
    #print(lastDate,currentDate,currentDate - Utility.dateStrToDate("Sun Oct 01 00:00:00 +0000 2017") <= datetime.timedelta(0))
    if (currentDate - firstDate) <= datetime.timedelta(0):
        try:
            outfile.close()
        except:
            pass
        break
    if str(lastDate)[:10] != str(currentDate)[:10]:
        try:
            outfile.close()
            outfile = open("Data/Trump/Trumpjson/"+str(currentDate)[:10]+".json","a")
        except:
            outfile = open("Data/Trump/Trumpjson/"+str(currentDate)[:10]+".json","a")
    lastDate = currentDate
    outfile.write(json.dumps(tweet) + '\n')


beginDate = Utility.dateStrToDate("Tue Mar 06 00:00:00 +0000 2018") + datetime.timedelta(1)
beginDate = lastDate.replace(tzinfo=localtz)
while beginDate - fisrtDate >= datetime.timedelta(0):
    print(beginDate)
    try:
        #print('0')
        data = Utility.readJsonFile("Data/Trump/Trumpjson/"+str(beginDate)[:10])
        #print('1')
        textfile = open("Data/Trump/Trumptxt/"+str(beginDate)[:10]+".txt","a")
        #print('2')
        for line in data:
            txt = line["text"]
            if "https:" in txt:
                txt = txt[:txt.index("https:")]
            textfile.write(txt + "\n")
        textfile.close()
    except:
        pass
    beginDate -= datetime.timedelta(1)

