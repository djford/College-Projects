"""
Daniel Ford and Josh Chang

Evaluates, scores, and outputs results for various metrics of queries while searching though our superDoc index and
database.
"""

import os
from WebDB import WebDB
import codecs
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from bs4 import BeautifulSoup
from spider import *
import pickle
import math
import random
from random import shuffle

class superDoc(object):
   def __init__(self):
      self.positionalIndex = pickle.load(open("saveSuper.p", "rb"))
      #rawList = []
      os.chdir("data")
      #os.chdir("item")
      #for file in os.listdir('.'):
           #f = open(file, "r")
           #listItems = f.readlines()
           #for item in listItems:
               #if '\n' in listItems:
                   #listItems.remove('\n')
               #rawList.append(item.rstrip('\n'))
      #os.chdir("..")
      self.numDocs = 40
      self.db = WebDB('cache.db')
      #docIDtoSUPER = []
      #for i in range(782): #<--------DO NOT hard code this value, change soon!!!!!
           #temp = self.db.rankedIndex((i+1))[0]
           #docIDtoSUPER.append(temp)
      #print(docIDtoSUPER)



      #os.chdir("clean")
      #self.positionalIndex = dict()
      #for file in os.listdir('.'):
          #f = codecs.open(file, "r", 'utf-8')
          #position = 0
          #dWeight = 0
          #temp = str(file).split('.')
          #docID = int(temp[0])
          #itemID = docIDtoSUPER[docID-1]
          #for token in f:
              #position += 1
              #if token not in self.positionalIndex:
                  #self.positionalIndex[token] = dict()
              #if itemID not in self.positionalIndex[token]:
                  #self.positionalIndex[token][itemID] = list()
              #self.positionalIndex[token][itemID].append(position)

          #f.close()
      #for token in self.positionalIndex:
          #for itemID in self.positionalIndex[token]:
              #self.positionalIndex[token][itemID].insert(0, dWeight)




   def wrdtokenize(self,token):
       thing = word_tokenize(token)
       return thing[0]

   def nnnDoc(self):
        for token in self.positionalIndex:
            for itemID in self.positionalIndex[token]:
                rawTermFreq = len(self.positionalIndex[token][itemID])-1
                self.positionalIndex[token][itemID][0] = rawTermFreq

   def ltcDoc(self):
        for token in self.positionalIndex:
            #docFreq = len(self.positionalIndex[token])
            invDocFreq = math.log10(self.numDocs/len(self.positionalIndex[token])) #calculates inverse document frequency
            for itemID in self.positionalIndex[token]:
                termFreq = 1 + math.log10(len(self.positionalIndex[token][itemID])-1) #calculates term frequency
                weight = invDocFreq * termFreq #calculates weight before normalization
                self.positionalIndex[token][itemID][0] = weight #puts weight in the initial spot in the positional list
        docLen = dict()#dummy dictionary that holds the weights of each doc
        for token in self.positionalIndex:
            for itemID in self.positionalIndex[token]:
                docLen[itemID] = self.positionalIndex[token][itemID][0]
        for token in self.positionalIndex:
            for itemID in self.positionalIndex[token]:
                docLen[itemID] += math.pow(self.positionalIndex[token][itemID][0], 2)#squares the weight of each doc and adds them into the dummy dictionary
        for token in self.positionalIndex:
            for itemID in self.positionalIndex[token]:
                self.positionalIndex[token][itemID][0] = self.positionalIndex[token][itemID][0]/math.sqrt(docLen[itemID])#takes the current weight in each document and divides it by the square root of the value in the dummy dictionary

   def Query(self, query, qStr):
        query = query.lower()
        spider = Spider()
        termFreq = dict()
        querySplit = query.split()
        stemmed = spider.stem(querySplit)
        for stemQuery in stemmed:
            stemQuery = self.wrdtokenize(stemQuery)+'\r\n'
            if stemQuery not in termFreq:
                termFreq[stemQuery] = 1
            else:
                termFreq[stemQuery] += 1
        if qStr == "ltc":
            for stemQuery in termFreq:
                 termFreq[stemQuery] = 1 + math.log10(termFreq[stemQuery])

            for stemQuery in termFreq:
                for token in self.positionalIndex:
                    if stemQuery == token:
                        invDocFreq = math.log10(self.numDocs/len(self.positionalIndex[token]))
                        weight = termFreq[stemQuery]*invDocFreq
                        termFreq[stemQuery] = weight
            qLen2 = 0
            for stemQuery in termFreq:
                qLen2 += math.pow(termFreq[stemQuery], 2)
            for stemQuery in termFreq:
                termFreq[stemQuery] = termFreq[stemQuery]/(math.sqrt(qLen2))

        scores = dict()

        for itemID in range(self.numDocs):
            scores[itemID + 1] = random.random() * 0.000000001

        for stemQuery in termFreq:
            if stemQuery in self.positionalIndex:
                for itemID in self.positionalIndex[stemQuery]:
                    scores[itemID] += self.positionalIndex[stemQuery][itemID][0] * termFreq[stemQuery]

        sortedScores = sorted(scores.values())
        sortedScores.reverse()


        itemIDList = []
        for i in range(len(sortedScores)):
            for itemID in scores:
                if scores[itemID] == sortedScores[i]:
                    if itemID not in itemIDList:
                        itemIDList.append(itemID)
        return itemIDList


   def relevant(self, itemIDList, qNum):
        relevantList = []
        for i in range(len(itemIDList)):
            if (itemIDList[i]) == qNum:
                relevantList.append(1)
            else:
                relevantList.append(0)


        return relevantList

   def calcP_at_N(self, relevantList, n = 1):
        numer = 0
        denom = 0
        for i in range(n):
            denom += 1
            if(relevantList[i] == 1):
                numer += 1

        result = numer/denom
        return result

   def calcP_at_R(self, relevantList):
        R = 0
        numer = 0
        denom = 0
        for i in range(len(relevantList)):
            if(relevantList[i] == 1):
                R += 1

        for i in range (R):
            denom += 1
            if(relevantList[i] == 1):
                numer += 1

        result = numer/denom
        return result

   def MAP(self, relevantList):
        numer = 0
        denom = 0
        total = 0
        for i in range(len(relevantList)):
            denom += 1
            if(relevantList[i] == 1):
                numer += 1
                total += (numer/denom)

        result = total/numer
        return result

   def AUC(self, relevantList):
        sum1 = 0
        sum0 = 0
        total = 0
        for i in range(len(relevantList)):
            if(relevantList[i] == 1):
                sum1 += 1
            if(relevantList[i] == 0):
                sum0 += 1
                total += sum1

        result = (total/sum1)/sum0
        return result

def main():
    rankedIndex = superDoc()

    rawList = []
    os.chdir("item")
    for file in os.listdir('.'):
        f = open(file, "r")
        listItems = f.readlines()
        for item in listItems:
            if '\n' in listItems:
                listItems.remove('\n')
            rawList.append(item.rstrip('\n'))
    os.chdir("..")
    print(rawList)

    instanceList = ["nnn.nnn", "ltc.nnn", "nnn.ltc", "ltc.ltc", "ran.dom"]
    for instance in instanceList:
        todo = instance.split(".")
        indexing = todo[0]
        if indexing == "nnn":
            rankedIndex.nnnDoc()
            Pat1 = 0
            PatR = 0
            PAP = 0
            PAUC = 0
            qNum = 0
            for item in rawList:
                query = item
                qNum += 1
                itemIDList = rankedIndex.Query(query, todo[1])
                relList = rankedIndex.relevant(itemIDList, qNum)
                Pat1 += rankedIndex.calcP_at_N(relList)
                PatR += rankedIndex.calcP_at_R(relList)
                PAP += rankedIndex.MAP(relList)
                PAUC += rankedIndex.AUC(relList)
            print(todo[0]+"."+ todo[1])
            print("P@1: " + str(Pat1/qNum))
            print("P@R: " + str(PatR/qNum))
            print("PAP: " + str(PAP/qNum))
            print("PAUC: " + str(PAUC/qNum))

        elif indexing == "ltc":
            rankedIndex.ltcDoc()
            Pat1 = 0
            PatR = 0
            PAP = 0
            PAUC = 0
            qNum = 0
            for item in rawList:
                query = item
                qNum += 1
                relList = rankedIndex.relevant(rankedIndex.Query(query, todo[1]), qNum)
                Pat1 += rankedIndex.calcP_at_N(relList)
                PatR += rankedIndex.calcP_at_R(relList)
                PAP += rankedIndex.MAP(relList)
                PAUC += rankedIndex.AUC(relList)
            print(todo[0]+"."+ todo[1])
            print("P@1: " + str(Pat1/qNum))
            print("P@R: " + str(PatR/qNum))
            print("PAP: " + str(PAP/qNum))
            print("PAUC: " + str(PAUC/qNum))

        elif indexing == "ran":
            rankedIndex.ltcDoc()
            Pat1 = 0
            PatR = 0
            PAP = 0
            PAUC = 0
            qNum = 0
            for item in rawList:
                query = item
                qNum += 1
                relList = rankedIndex.relevant(rankedIndex.Query(query, todo[1]), qNum)
                shuffle(relList)
                Pat1 += rankedIndex.calcP_at_N(relList)
                PatR += rankedIndex.calcP_at_R(relList)
                PAP += rankedIndex.MAP(relList)
                PAUC += rankedIndex.AUC(relList)
            print("RANDOM")
            print("P@1: " + str(Pat1/qNum))
            print("P@R: " + str(PatR/qNum))
            print("PAP: " + str(PAP/qNum))
            print("PAUC: " + str(PAUC/qNum))

main()
