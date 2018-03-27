# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 09:56:51 2017

@author: Destiny
"""

'''
import dom_act
import Utility

file = Utility.readJsonFile('Data/Top50Colorado/13523182')
for tweet in file:
    dom, act = dom_act.get_act_dom_score(tweet)
    print(dom, act)

'''

'''
import Utility

vectorList = Utility.deserialize('Data/VectorList.json')
file = open('vectors.txt','a')
for vector in vectorList:
    file.write(str(vector) + '\n')
file.close
'''

'''
import Utility
import Main

countyDict = Utility.deserialize('ColoradoCountySeatGeocode.json')
file = open('CountyUsersIncludingLargeCities.txt','a')
#exceptionList = ['Denver','El Paso', 'Boulder', 'Broomfield', 'Pueblo', 'Arapahoe', 'Larimer']
for county in countyDict:
    #if county not in exceptionList:
    filename = 'Data/Colorado/' + county 
    data = Utility.readJsonFile(filename)
    userList = []
    userList = Main.updateActiveUserList(data, userList)
    file.write(county + '\t' + str(len(userList)) + '\n')
    print(county + '\t' + str(len(userList)))
file.close()
'''
import config
from twarc import Twarc
import Utility
import datetime

afile = open('Data/ColoradoRegion/NorthernFrontRange/Users/UnselectedWithRobotIndex.txt','r')
text = afile.read()
text = text.split('\n')
#print(text)
usernameList = []
count = 0
for line in text:
	linetext = line.split(' ')
	#print(linetext)
	if float(linetext[2]) <= 0.45:
		usernameList.append(linetext[0])
		count += 1
		if count >= 100:
			break
#print(usernameList, len(usernameList))
successcount = 0
usercount = 0
t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
for user in usernameList:
	print('Analyzing ' + user + ' data...')
	usercount += 1
	try:
		count = 0
		for tweet in t.timeline(screen_name=user):
			if count == 0:
				firstDate = Utility.dateStrToDate(tweet["created_at"])
				lastDate = firstDate - datetime.timedelta(14)
				count += 1
			currentDate = Utility.dateStrToDate(tweet["created_at"])
			if currentDate > lastDate:
				successcount += 1
				print("success")
				break
	except:
		usercount -= 1
		continue
print("success count in " + str(usercount) + " trials: " + str(successcount))
