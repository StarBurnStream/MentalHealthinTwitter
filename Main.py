# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 22:37:43 2017

@author: Junjie Jiang
"""

import json
from User import User
from twarc import Twarc
import config
import botometer
import time
import attributesWithoutLIWC
import Utility
import SVM
import os
import get_results
import depressionScoreCalculator

def main2(directory):
    #geocodeDict = Utility.deserialize('ColoradoCountySeatGeocode.json')
    regionDict = Utility.deserialize('Data/RegionDict.json')
    Utility.silentRemove('Data/regionNonRobotUser.txt')
    file = open('Data/regionNonRobotUser.txt','a')
    file.close()
    for region in regionDict:
        #file = open('Data/regionNonRobotUser.txt','w')
        fileNameStr = 'Data/' + directory + '/' + region
        #coordinate = regionDict[region].split(',')[:-1]
        userList = []
        try:
            print("Try to read file: " + fileNameStr)
            tmpData = Utility.readJsonFile(fileNameStr)
            userList = updateActiveUserList(tmpData,userList)
            print("Finish processing file: " + fileNameStr)
        except:
            break
        if not os.path.exists('Data/' + directory + '/' + region + '/Users/'):
            os.makedirs('Data/'+ directory + '/' + region + '/Users/')
        print("Storing unprocessed user list.")
        storeUserList(userList, 'Data/' + directory + '/' + region + '/Users/Unselected.txt')
        print("Calculating robot indices for " + str(len(userList)) + " users...")
        robotDict = Utility.deserialize('Data/robotDict.json')
        nonRobotDict = Utility.deserialize('Data/nonRobotDict.json')
        userList = calculateRobotIndex(robotDict,nonRobotDict,userList)
        print("User list robot index calculated. Writing into file...")
        storeUserList(userList, 'Data/' + directory + '/' + region + '/Users/UnselectedWithRobotIndex.txt')
        topNUsers = makeSelectedUserList(userList)
        with open('Data/regionNonRobotUser.txt','a') as f:
            f.write(region + ' ' + str(len(topNUsers)) + '\n')
        #file.close()
        
        '''
        print("Gaining" + " users' tweets... Writing into file...")
        topNUsers = getUserTweets(topNUsers)
        print("Users selected. Writing into file...")
        storeUserList(topNUsers, 'Data/' + directory + '/' + region + '/Users/Selected.txt')
        print("Here are the information for top " + str(numUsers) + " users:")
        for user in topNUsers:
            print(user.screenName, user.id, user.tweetCountInSample, user.volume, user.robotIndex )
        print("Serializing userList...")
        Utility.serialize(userList,'Data/' + directory + '/' + region + '/Users/userList')
        print("Serializing topNUserList...")
        Utility.serialize(topNUsers,'Data/' + directory + '/' + region + '/Users/topNUserList')
        #topNUsers = Utility.deserialize('Data/Users/topNUserList')
        SVM.main(topNUsers, directory, region)
        '''
    #file.close()
    
def calculateRobotIndex(robotDict,nonRobotDict,userList):
    trial = 3
    count = 0
    for user in userList:
        #user.robotIndex = checkRobot(user.screenName)['scores']['english']
        trys = -1
        while trys < trial:
            try:
                robotDict, nonRobotDict, result = Utility.checkRobot(robotDict, nonRobotDict, user.screenName)
                user.robotIndex = result['scores']['english']
                print("Succeeded")
                break
            except Exception as e:
                trys += 1
                try:
                    if e.__dict__['response'].status_code == 429:
                        print("Rate limit exceeded. Sleep 30 seconds..." + ' ' + user.screenName + " " + user.id)
                        trys = -1
                        time.sleep(30)
                    elif trys == 0 and str(e)[:3] == '502':
                        print("502 Server Error. Sleep 10 seconds..." + ' ' + user.screenName + " " + user.id)
                        time.sleep(10)
                    elif trys > 0 and str(e)[:3] == '502':
                        print("502 Server Error. Sleep 60 seconds..." + ' ' + user.screenName + " " + user.id)
                        time.sleep(60)
                    else:
                        print("Error: " + str(e) + ' ' + user.screenName + " " + user.id)
                except Exception as e1:
                    print("Error: " + str(e) + ' ' + user.screenName + " " + user.id)
                    #time.sleep(1)
                if trys == trial:
                    user.robotIndex = 1.0
                    print("Failed")
                    robotDict[user.screenName] = {}
                    robotDict[user.screenName]['scores'] = {}
                    robotDict[user.screenName]['scores']['english'] = 1.0
                    Utility.silentRemove('Data/robotDict.json')
                    Utility.serialize(robotDict, 'Data/robotDict.json')
        count += 1 
        print(str(count) + "/" + str(len(userList)) + ' Robot Index: ' + str(user.robotIndex))
    return userList

def storeUserList(userList,filename):
    Utility.silentRemove(filename)
    outfile = open(filename, "a")
    for user in userList:
        outfile.write(user.screenName + ' ' + user.id + ' ' + str(user.robotIndex) + '\n')
    outfile.close
        
def makeSelectedUserList(userList):
    userList = sorted(userList, key = User.getTweetCountInSample, reverse = True)
    indexList = []
    for user in userList:
        if user.robotIndex > 0.45:
            indexList.append(userList.index(user))
    userList = [ userList[i] for i in range(len(userList)) if i not in indexList ]
    return userList

def updateActiveUserList(data,userList):
    for tweet in data:
        userID = str(tweet["user"]["id"])
        user = Utility.userInUserList(userID, userList)
        if user == False:
            user = User(screenName=tweet["user"]["screen_name"],ID=userID)
            userList.append(user)
        user.tweetCountInSample += 1
    return userList
    
def getUserTweets(userList):
    t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
    indexList = []
    for user in userList:
        fileStr = ''
        for tweet in t.timeline(user_id=user.id):
            fileStr += json.dumps(tweet)+"\n"
        if fileStr != '':
            outfile = open("Data/Users/" + user.id + ".json","a")
            outfile.write(fileStr)
            outfile.close()
        else:
            indexList.append(userList.index(user))
    userList = [ userList[i] for i in range(len(userList)) if i not in indexList ]
    return userList
    
def main():
    get_results.get_results()
    twarcWork.acceptListToTrainingData()
    twarcWork.listToPredictingData()
    depressionScoreCalculator.resultinfoToScore()
    SVM.main()
