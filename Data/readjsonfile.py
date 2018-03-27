#from twarc import Twarc
import json
import sys
import unicodedata as ud
import codecs
import time
import glob
import os

class ReadData():
    def __init__(self,dirfile):
        self.dirfile = dirfile
    def readData(self):

        file = open(self.dirfile,'r')
        userNameList = file.read().split('\n')


        for i in range(len(userNameList)):
            if userNameList[i][0] == '@':
                userNameList[i] = userNameList[i][1:]
    
        json_dic = {}
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        for username in userNameList:
            for filename in glob.glob(os.path.join("Training/", username+'.json')):
                with open(filename,"r") as f:
                    for parsed_json in load_json_multiple(f):
                        parsed_json["text"] =parsed_json["text"].translate(non_bmp_map)
                        if username not in json_dic:
                            json_dic[username] = [parsed_json["text"]]
                        else:
                            json_dic[username] += [parsed_json["text"]]
        return json_dic


def load_json_multiple(segments):
    chunk = ""
    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass
##        
##m = ReadData("Data/Depressed.txt")
##m.readData()

