from vaderSentiment import SentimentIntensityAnalyzer
from Twarcfind import *
from pprint import pprint
import Utility

jsonfile = "testa0"

def posnegsentiment(jsonfile):
    
    data = Utility.readJsonFile(jsonfile)

    valuelist = {}
    analyzer = SentimentIntensityAnalyzer()
    for sentence in data:
        if "user" in sentence and "id" in sentence["user"]:
            newid = sentence["user"]["id"]
            if sentence["user"]["id"] not in valuelist:
                vs = analyzer.polarity_scores(sentence["text"])
                print(vs)
                valuelist[newid] =  [vs["pos"],vs["neg"]]
            else:
               valuelist[newid] += [vs["pos"],vs["neg"]]
    #print(valuelist)
    return valuelist

valuelist = posnegsentiment(jsonfile)
print(valuelist)
    
'''
class sentiments():
    def __init__(self):
        pass

    def posnegsentiment(self, jsonfile):
        
        data = ReadData(jsonfile)
        jsondoclist = data.readData()


        valuelist = {}
        analyzer = SentimentIntensityAnalyzer()
        for sentence in jsondoclist:
            if "user" in sentence and "id" in sentence["user"]:
                newid = sentence["user"]["id"]
                if sentence["user"]["id"] not in sentence["user"]:
                    vs = analyzer.polarity_scores(sentence["text"])
                    valuelist[newid] =  [vs["pos"],vs["neg"]]
                else:
                   valuelist[newid] += [vs["pos"],vs["neg"]]
        #print(valuelist)
        return valuelist
##def main():
##    a = sentiments()
##    a.posnegsentiment(jsonfile)
##main()
    #print("{:-<65} {}".format(sentence, str(vs)))
'''