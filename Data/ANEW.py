"""
@author: Shengjue Yuan
"""


import math, re, string, requests, json
from datapreproccess import *
import io
import numpy as np
import nltk
from nltk.stem import PorterStemmer

class ANEW:

    def __init__(self,txt):
        with io.open("ANEW2010ALL.txt","r",encoding = "utf-8") as f:
            self.anewlexicon = f.read()
        self.txt = txt
        self.user =[]
        self.json ={}
        self.score = {}
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

        text = DataPreprocess(self.txt)
        text.set_data()
        text.Preprocess()
        text.singularize()
        self.jsondic = text.get_jsondic()
        self.user = text.get_user()

    def grade_act_dom_score(self):
        """
        calculating the dominance score and the activation score
        """

        for user in self.user:
            temptot = len(self.jsondic[user])
            totdom = 0
            totact = 0
            fracdom = 0
            fracact = 0
            for tweets in self.jsondic[user]:
                n = 0
                domscore = 0
                actscore = 0
                for word in tweets:
                    if word in self.anewlex_dict:
                        n+=1

                        domscore += float(self.anewlex_dict[word][1][1])
                        actscore += float(self.anewlex_dict[word][0][1])
                if n !=0:
                    domscore = domscore/n
                    actscore = actscore/n
                totdom +=domscore
                totact += actscore
            fracdom = float(totdom/temptot)
            fracact = float(totact/temptot)
            self.score[user] = [("dom",fracdom),("act",fracact)]
        print(self.score)
                

                        
def main():
    a = ANEW(txt = "Data/UnDepressed.txt")
    a.make_anewlex_dict()
    a.set_textanduser()
    a.grade_act_dom_score()
##    b = Depression(txt = "Data/UnDepressed.txt")
##    b.make_deplex_dict()
##    b.make_depalex_list()
##    b.set_textanduser()
##    b.grade_depression_score()

main()
