"""
@author: Junjie Jiang
"""

import sklearn
from sklearn.svm import SVC
from sklearn import datasets
import numpy as np
import config
import Utility
from User import User
from twarc import Twarc
import json
import attributesWithoutLIWC
import attributesWithLIWC
import os
import dom_act
import twarcWork

def main():
    print("Training SVM...")
    clf = trainSVM()
    print("Predicting...")
    prediction = predictUserList(clf)
    print(prediction)

def matchInformation():
    wList = Utility.readCsv("Data/MTurk/worker_info.csv")[:-1]
    rList = Utility.readCsv("Data/MTurk/result_info.csv")[:-1]
    idList = [ x[3] for x in wList ][1:]
    scoreList =  [ y[11] for y in rList ][1:]
    return idList, scoreList

def trainSVM():
    idList, scoreList = matchInformation()
    vectorList = []
    targetList = []
    if os.path.exists('Data/Training/TrainingUserList.json'):
        userDict = Utility.deserialize('Data/Training/TrainingUserList.json')
    else:
        userDict = {}
    k = 0
    for userid in idList:
        k += 1
        print( str(k) + 'th user being analyzed...')
        if userid not in userDict:
            newUser, data = attributesWithoutLIWC.updateEngagements(userid,train=True)
            attributesWithoutLIWC.updateUserFollowers(newUser)
            attributesWithoutLIWC.updateUserFriends(newUser)
            pa = 0.0
            na = 0.0
            dom = 0.0
            act = 0.0
            for tweet in data:
                compound = attributesWithLIWC.getCompound(tweet)
                dom, act = dom_act.get_act_dom_score(tweet)
                if compound > 0:
                    pa += 1
                if compound < 0:
                    na += 1
            pa /= len(data)
            na /= len(data)
            dom /= len(data)
            act /= len(data)
            vector = [newUser.volume, newUser.retweets, newUser.reply, newUser.questions, newUser.links,
                      newUser.numFollowers, newUser.numFollowees, pa, na, dom, act]
            userDict[userid] = vector
        else:
            vector = userDict[userid]
        vectorList.append(vector)
        targetList.append(scoreList[idList.index(userid)])
        targetList = ['24','12','-1','-1','16','-1']  # Trial
    print(vectorList)
    print(targetList)
    Utility.silentRemove('Data/Training/TrainingUserList.json')
    Utility.silentRemove('Data/Training/VectorList.json')
    Utility.silentRemove('Data/Training/targetList.json')
    Utility.serialize(userDict, 'Data/Training/TrainingUserList.json')
    Utility.serialize(vectorList, 'Data/Training/VectorList.json')
    Utility.serialize(targetList, 'Data/Training/targetList.json')
    clf = sklearn.svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    clf.fit(vectorList, targetList) 
    return clf
    
def predictUserList(clf):
    idfile = open('Data/MTurk/rejectList.csv','r')
    userList = idfile.read().split('\n')[:-1]
    userList = ['14835269','898264108914667520','225761199','532688309'] # Trial
    if os.path.exists('Data/Predicting/PredictionDict.json'):
        predictionDict = Utility.deserialize('Data/Predicting/PredictionDict.json')
    else:
        predictionDict = {}
    prediction = {}
    k = 0
    for userid in userList:
        k += 1
        print( str(k) + 'th user being analyzed...')
        if userid not in predictionDict:
            user, data = attributesWithoutLIWC.updateEngagements(userid)
            attributesWithoutLIWC.updateUserFollowers(user)
            attributesWithoutLIWC.updateUserFriends(user)
            pa = 0.0
            na = 0.0
            for tweet in data:
                compound = attributesWithLIWC.getCompound(tweet)
                dom, act = dom_act.get_act_dom_score(tweet)
                if compound > 0:
                    pa += 1
                if compound < 0:
                    na += 1
            pa /= len(data)
            na /= len(data)
            dom /= len(data)
            act /= len(data)
            vector = [user.volume, user.retweets, user.reply, user.questions, user.links,
                      user.numFollowers, user.numFollowees, pa, na, dom, act]
            prediction[userid] = int(list(clf.predict([vector]))[0])
            predictionDict[userid] = prediction[userid]
        else:
            prediction[userid] = predictionDict[userid]
    Utility.silentRemove('Data/Predicting/Prediction.json')
    Utility.silentRemove('Data/Predicting/PredictionDict.json')
    Utility.serialize(prediction, 'Data/Predicting/Prediction.json')
    Utility.serialize(predictionDict, 'Data/Predicting/PredictionDict.json')
    return prediction




def getTrainingData():
    t = Twarc(config.consumer_key, config.consumer_secret, config.access_token, config.access_secret)
    file = open("Data/Depressed.txt",'r')
    depressed = file.read().split('\n')
    file.close()
    indexList = []
    for userName in depressed:
        RI = Utility.checkRobot(userName)['scores']['english']
        if RI >= 0.45:
            indexList.append(depressed.index(userName))
        else:
            tmpName = userName
            if userName[0] == '@':
                userName = userName[1:]
            if not os.path.exists('Data/Training/' + userName + '.json'):
                try:
                    fileStr = ''
                    for tweet in t.timeline(screen_name=userName):
                        fileStr += json.dumps(tweet)+"\n"
                    if fileStr == '':
                        Utility.silentRemove("Data/Training/" + userName + ".json")
                        indexList.append(depressed.index(tmpName))
                    else:
                        outfile = open("Data/Training/" + userName + ".json","a")
                        outfile.write(fileStr)
                        outfile.close
                except Exception as e:
                    Utility.silentRemove("Data/Training/" + userName + ".json")
    depressed = [ depressed[i] for i in range(len(depressed)) if i not in indexList ]
    file = open("Data/Depressed.txt",'w')
    for i in depressed:
        if depressed.index(i) != (len(depressed) - 1):
            file.write(i + '\n')
        else:
            file.write(i)
    file.close()
    file = open("Data/UnDepressed.txt",'r')
    undepressed = file.read().split('\n')
    file.close
    indexList = []
    for userName in undepressed:
        RI = Utility.checkRobot(userName)['scores']['english']
        if RI >= 0.45:
            indexList.append(undepressed.index(userName))
        else:
            tmpName = userName
            if userName[0] == '@':
                userName = userName[1:]
            if not os.path.exists('Data/Training/' + userName + '.json'):
                outfile = open("Data/Training/" + userName + ".json","a")
                try:
                    count = 0
                    for tweet in t.timeline(screen_name=userName):
                        outfile.write(json.dumps(tweet)+"\n")
                        count += 1 
                    outfile.close
                    if count == 0:
                        Utility.silentRemove("Data/Training/" + userName + ".json")
                        indexList.append(undepressed.index(tmpName))
                except:
                    outfile.close
                    Utility.silentRemove("Data/Training/" + userName + ".json")
    undepressed = [ undepressed[i] for i in range(len(undepressed)) if i not in indexList ] 
    file = open("Data/UnDepressed.txt",'w')
    for i in undepressed:
        if undepressed.index(i) != (len(undepressed) - 1):
            file.write(i + '\n')
        else:
            file.write(i)
    file.close
    
def trainSVM2():
    file = open("Data/Depressed.txt",'r')
    userNameList = file.read().split('\n')
    file.close
    vectorList = []
    targetList = []
    if os.path.exists('Data/TrainingUserList.json'):
        userDict = Utility.deserialize('Data/TrainingUserList.json')
    else:
        userDict = {}
    for userName in userNameList:
        if (userName != None) and (userName != ''):
            if userName[0] == '@':
                userName = userName[1:]
            if userName not in userDict:
                newUser, data = attributesWithoutLIWC.updateEngagements(userName,train=True)
                attributesWithoutLIWC.updateUserFollowers(newUser)
                attributesWithoutLIWC.updateUserFriends(newUser)
                pa = 0.0
                na = 0.0
                dom = 0.0
                act = 0.0
                for tweet in data:
                    compound = attributesWithLIWC.getCompound(tweet)
                    dom, act = dom_act.get_act_dom_score(tweet)
                    if compound > 0:
                        pa += 1
                    if compound < 0:
                        na += 1
                pa /= len(data)
                na /= len(data)
                dom /= len(data)
                act /= len(data)
                vector = [newUser.volume, newUser.retweets, newUser.reply, newUser.questions, newUser.links,
                          newUser.numFollowers, newUser.numFollowees, pa, na, dom, act]
                userDict[userName] = vector
            else:
                vector = userDict[userName]
            print(vector)
            vectorList.append(vector)
            targetList.append(1)
    file = open("Data/UnDepressed.txt",'r')
    userNameList = file.read().split('\n')
    file.close
    for userName in userNameList:
        if userName[0] == '@':
            userName = userName[1:]
        if userName not in userDict:
            newUser, data = attributesWithoutLIWC.updateEngagements(userName,train=True)
            attributesWithoutLIWC.updateUserFollowers(newUser)
            attributesWithoutLIWC.updateUserFriends(newUser)
            pa = 0.0
            na = 0.0
            for tweet in data:
                compound = attributesWithLIWC.getCompound(tweet)
                dom, act = dom_act.get_act_dom_score(tweet)
                if compound > 0:
                    pa += 1
                if compound < 0:
                    na += 1
            pa /= len(data)
            na /= len(data)
            dom /= len(data)
            act /= len(data)
            vector = [newUser.volume, newUser.retweets, newUser.reply, newUser.questions, newUser.links,
                      newUser.numFollowers, newUser.numFollowees, pa, na, dom, act]
            userDict[userName] = vector
        else:
            vector = userDict[userName]
        print(vector)
        vectorList.append(vector)
        targetList.append(0)
    Utility.silentRemove('Data/TrainingUserList.json')
    Utility.silentRemove('Data/VectorList.json')
    Utility.silentRemove('Data/targetList.json')
    Utility.serialize(userDict, 'Data/TrainingUserList.json')
    Utility.serialize(vectorList, 'Data/VectorList.json')
    Utility.serialize(targetList, 'Data/targetList.json')
    clf = sklearn.svm.SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    clf.fit(vectorList, targetList) 
    return clf
    
def predictUserList2(clf, userList, directory, county):
    if os.path.exists('Data/PredictionDict.json'):
        predictionDict = Utility.deserialize('Data/PredictionDict.json')
    else:
        predictionDict = {}
    prediction = {}
    for user in userList:
        if user.screenName not in predictionDict:
            data = attributesWithoutLIWC.updateEngagements(user)
            attributesWithoutLIWC.updateUserFollowers(user)
            attributesWithoutLIWC.updateUserFriends(user)
            pa = 0.0
            na = 0.0
            for tweet in data:
                compound = attributesWithLIWC.getCompound(tweet)
                dom, act = dom_act.get_act_dom_score(tweet)
                if compound > 0:
                    pa += 1
                if compound < 0:
                    na += 1
            pa /= len(data)
            na /= len(data)
            dom /= len(data)
            act /= len(data)
            vector = [user.volume, user.retweets, user.reply, user.questions, user.links,
                      user.numFollowers, user.numFollowees, pa, na, dom, act]
            prediction[user.screenName] = list(clf.predict([vector]))
            predictionDict[user.screenName] = prediction[user.screenName]
        else:
            prediction[user.screenName] = predictionDict[user.screenName]
    Utility.silentRemove('Data/' + directory + '/' + county + '/Prediction.json')
    Utility.silentRemove('Data/PredictionDict.json')
    Utility.serialize(prediction, 'Data/' + directory + '/' + county + '/Prediction.json')
    Utility.serialize(predictionDict, 'Data/PredictionDict.json')
    return prediction

'''
user1 = User(screenName='lightofsorrow', ID='823323480682680320')
user2 = User(screenName='rachaelxss', ID='939604578')
user3 = User(screenName='tonyheath2011', ID='248816806')
user4 = User(screenName='mommawedel', ID='47293791')
userList = [user1, user2, user3, user4]
main(userList)
'''
main()

