# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:49:04 2017

@author: Destiny
"""

import Utility
import os

def getDepressionScore(answerList):
    aList = []
    for item in answerList:
        if item == 0 or item == 'Not at all' or item == 'Not difficult at all':
            aList.append(0)
        if item == 1 or item == 'Several days' or item == 'Somewhat difficult':
            aList.append(1)
        if item == 2 or item == 'More than half the days' or item == 'Very difficult':
            aList.append(2)
        if item == 3 or item == 'Nearly every day' or item == 'Extremely difficult':
            aList.append(3)
    if not ((aList[0] >= 2 or aList[1] >= 2) and aList[9] >= 1):
        return -1
    sum1 = 0
    sum2 = 0
    sum3 = 0
    count = 0
    for i in range(9):
        if aList[i] == 1:
            sum1 += 1
        elif aList[i] == 2:
            sum2 += 2
        elif aList[i] == 3:
            sum3 += 3
        elif aList[i] != 0:
            print("Wrong value")
        if i != 9 and aList[i] >= 2:
            count += 1
        elif aList[i] >= 1:
            count += 1
    if count < 5:
        return -1
    total = sum1 + sum2 + sum3
    return total
    
def getStringDescription(score=None, answerList=None):
    if answerList != None:
        score = getDepressionScore(answerList)
    if score == None:
        print("Error. No score or answerList provided.\n")
        return -1
    if score >= 20:
        return "Major depression, severe.\n"
    elif score >= 15:
        return "Major depression, moderately severe.\n"
    elif score >= 10:
        return "Minor depression++. Dysthymia*. Major depression, mild.\n"
    elif score >= 5:
        return "Minimal symptoms*.\n"
    else:
        return "No deperssion.\n"

def resultinfoToScore():
    resultfile = open('Data/MTurk/result_info.csv')
    result = resultfile.read().split('\n')[:-1]
    resultfile.close()
    newresult = result
    newresult[0] += ',score'
    for i in result[1:]:
        if i != '':
            score = getDepressionScore(i.split(',')[1:])
            newresult[result.index(i)] = i + ',' + str(score)
        else: 
            newresult[result.index(i)] = i
    if os.path.isfile('Data/MTurk/result_info.csv'):
        Utility.silentRemove('Data/MTurk/result_info.csv')
    newresultfile = open('Data/MTurk/result_info.csv','a')
    filestr = ''
    for i in newresult:
        filestr += i + '\n'
    newresultfile.write(filestr[:-1])
    newresultfile.close()

#resultinfoToScore()
