import requests
import json
import nltk
from nltk import word_tokenize
from readjsonfile import *
import re
from nltk.stem import PorterStemmer
from textblob import TextBlob
from textblob import Word
from os.path import isfile, join
import string
#nltk.download()
#download all packages


class DataPreprocess():
    def __init__(self,dirfile):
        self.dirfile = dirfile
        self.jsondic = {}
        self.user = []
        
    def set_data(self):
        ''' get twitter text data from json file,tokenize them and make annotations.'''
        data = ReadData(self.dirfile)
        json_dic = data.readData()
        self.jsondic = json_dic
        # a list for twitter texts, each twitter text is an element in the list.
        self.user = list(json_dic.keys())

       
    def get_user(self):
        return self.user

    def get_jsondic(self):
        return self.jsondic
            
    def Preprocess(self):
        # get rid of url
        for j in self.user:
            for i in range(len(self.jsondic[j])):
                self.jsondic[j][i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', self.jsondic[j][i])

        # get rid of @user and hashtags
        for j in self.user:
            for i in range(len(self.jsondic[j])):
                self.jsondic[j][i] = self.jsondic[j][i].split()
                temp = []
                
                for k in range(len(self.jsondic[j][i])):
                    if self.jsondic[j][i][k][0] != '@' and self.jsondic[j][i][k][0] != '#' and self.jsondic[j][i][k][0] != "R":
                        temp += [self.jsondic[j][i][k]]
                self.jsondic[j][i] = temp
   
        #tokenize data and change them all to lower case
        for j in self.user:
            for i in range(len(self.jsondic[j])):
                sub_all = []
                for k in range(len(self.jsondic[j][i])):
                    if self.jsondic[j][i][k][0] == "'":
                        self.jsondic[j][i][k-1] = self.jsondic[j][i][k-1].join(self.jsondic[j][i][k])
                    tokens = word_tokenize(self.jsondic[j][i][k].lower())
                    sub_all += tokens
                self.jsondic[j][i] = sub_all

        
        #remove punctuations       
        for j in self.user:
            for i in range(len(self.jsondic[j])):
                for k in range(len(self.jsondic[j][i])):
                    self.jsondic[j][i][k] = "".join(c for c in self.jsondic[j][i][k] if c not in string.punctuation)
                self.jsondic[j][i] = [s for s in self.jsondic[j][i] if s]
        
                
    def singularize(self):
        """
        convert the plurals to singulars and the verbs to the first person present.
        """
        for j in self.user:
            for i in range(len(self.jsondic[j])):
                temp = [TextBlob(word) for word in self.jsondic[j][i]]
                self.jsondic[j][i] = [list(word.words.singularize())[0] for word in temp]
                tempv = [Word(word) for word in self.jsondic[j][i]]
                self.jsondic[j][i] = [word.lemmatize("v") for word in tempv]

                    
    def convert_to_stem(self):
        stemmer = PorterStemmer()
        #convert to stem word      
        for user in self.user:
            for i in range(len(self.jsondic[user])):
                for j in range(len(self.jsondic[user][i])):
                    self.jsondic[user][i][j] = stemmer.stem(self.jsondic[user][i][j])
        
##def main():
##    a = DataPreprocess("Data/UnDepressed.txt")
##    a.set_data()
##    a.Preprocess()
##    a.singularize()
##                    
##main()
