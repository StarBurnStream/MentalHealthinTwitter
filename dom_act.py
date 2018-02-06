import requests
import json
import nltk
from nltk import word_tokenize
import re
from textblob import TextBlob
from textblob import Word
from os.path import isfile, join
import string
import io
import math, re, string, requests, json
import numpy as np

#nltk.download()
#download all packages


class DataPreprocess():
    def __init__(self,text):
        self.text = text
           
    def Preprocess(self):
        # get rid of url
        self.text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', self.text)

        # get rid of @user and hashtags
        self.text= self.text.split()
        temp = []
        for i in range(len(self.text)):
            if self.text[i][0] != '@' and self.text[i][0] != '#' and self.text[i][0] != "R":
                temp += [self.text[i]]
        self.text = temp

   
        #tokenize data and change them all to lower case
        sub_all = []
        for i in range(len(self.text)):
            if self.text[i][0] == "'":
                self.text[i-1] = self.text[i-1].join(self.text[i])
            tokens = word_tokenize(self.text[i].lower())
            tokens = [word.split("/") for word in tokens]
            tokens = ["".join(word) for lists in tokens for word in lists]
            tokens = [word for word in tokens if len(word)>0]
            sub_all += tokens
        self.text = sub_all


        #remove punctuations
        for i in range(len(self.text)):
            self.text[i] = "".join(c for c in self.text[i] if c not in string.punctuation)
        self.text = [s for s in self.text if s]

                
    def singularize(self):
        """
        convert the plurals to singulars and the verbs to the first person present.
        """
        temp = [TextBlob(word) for word in self.text]
        self.text = [list(word.words.singularize())[0] for word in temp]
        tempv = [Word(word) for word in self.text]
        self.text = [word.lemmatize("v") for word in tempv]
        
    def get_text(self):
        return self.text




class ANEW:

    def __init__(self,text):
        with io.open("ANEW2010ALL.txt","r",encoding = "utf-8") as f:
            self.anewlexicon = f.read()
        self.text = text
        self.dom = 0
        self.act = 0
        self.anewlex_dict = {}

       
    def make_anewlex_dict(self):
        """
        Convert depressed lexicon file to a dictionary
        """
        self.anewlexicon = self.anewlexicon.split("\n")
        self.anewlexicon = self.anewlexicon[1:]
        for line in self.anewlexicon:
            (Word,Wdnum,ValMn,ValSD,AroMn,AroSD,DomMn,DomSD) = line.split()
            if Word not in self.anewlex_dict:
                self.anewlex_dict[Word] = [("AroMn",AroMn),("DomMn",DomMn)]
            else:
                self.anewlex_dict[Word] = [("AroMn",AroMn),("DomMn",DomMn)]



    def get_act_dom_score(self):
        return self.score

    def set_textanduser(self):
        """
        set tokenized text from the jsonfile and get user list
        also get the combinedic
        """

        text = DataPreprocess(self.text)
        text.Preprocess()
        text.singularize()
        self.text = text.get_text()

    def grade_act_dom_score(self):
        """
        calculating the dominance score and the activation score
        """
        n = 0
        domscore = 0
        actscore = 0
        for word in self.text:
            if word in self.anewlex_dict:
                n+=1
                domscore += float(self.anewlex_dict[word][1][1])
                actscore += float(self.anewlex_dict[word][0][1])
        if n !=0:
            domscore = float(domscore/n)
            actscore = float(actscore/n)
        self.dom = domscore
        self.act = actscore
    def get_score(self):
        return self.dom, self.act


                        
def get_act_dom_score(tweet):
    a = ANEW(tweet["text"])
    a.make_anewlex_dict()
    a.set_textanduser()
    a.grade_act_dom_score()
    dom, act = a.get_score()
    return dom, act


##dom, act = get_act_dom_score("Data/UnDepressed to'day @ta http:haha went to trees chickens eggs goes")
##print(dom,act)
