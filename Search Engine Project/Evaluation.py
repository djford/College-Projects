"""
Daniel Ford and Josh Chang

Evaluates, scores, and outputs results for various metrics of queries while searching though the web page index and
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

class Ranked(object):
    def __init__(self):
       self.positionalIndex = pickle.load(open("save.p", "rb"))
       os.chdir("data")
       self.numDocs = 782
       self.db = WebDB('cache.db')
       #os.chdir("clean")
       #self.positionalIndex = dict()
       #for file in os.listdir('.'):
           #f = codecs.open(file, "r", 'utf-8')
           #position = 0
           #dWeight = 0
           #temp = str(file).split('.')
           #docID = int(temp[0])
           #for token in f:
               #position += 1
               #if token not in self.positionalIndex:
                   #self.positionalIndex[token] = dict()
               #if docID not in self.positionalIndex[token]:
                   #self.positionalIndex[token][docID] = list()
               #self.positionalIndex[token][docID].append(position)
           #f.close()
       #for token in self.positionalIndex:
           #for docID in self.positionalIndex[token]:
               #self.positionalIndex[token][docID].insert(0, dWeight)

    def wrdtokenize(self,token):
        thing = word_tokenize(token)
        return thing[0]


    def nnnDoc(self):
        for token in self.positionalIndex:
            for docID in self.positionalIndex[token]:
                rawTermFreq = len(self.positionalIndex[token][docID])-1
                self.positionalIndex[token][docID][0] = rawTermFreq




    def ltcDoc(self):
        for token in self.positionalIndex:
            #docFreq = len(self.positionalIndex[token])
            invDocFreq = math.log10(self.numDocs/len(self.positionalIndex[token])) #calculates inverse document frequency
            for docID in self.positionalIndex[token]:
                termFreq = 1 + math.log10(len(self.positionalIndex[token][docID])-1) #calculates term frequency
                weight = invDocFreq * termFreq #calculates weight before normalization
                self.positionalIndex[token][docID][0] = weight #puts weight in the initial spot in the positional list
        docLen = dict()#dummy dictionary that holds the weights of each doc
        for token in self.positionalIndex:
            for docID in self.positionalIndex[token]:
                docLen[docID] = self.positionalIndex[token][docID][0]
        for token in self.positionalIndex:
            for docID in self.positionalIndex[token]:
                docLen[docID] += math.pow(self.positionalIndex[token][docID][0], 2)#squares the weight of each doc and adds them into the dummy dictionary
        for token in self.positionalIndex:
            for docID in self.positionalIndex[token]:
                self.positionalIndex[token][docID][0] = self.positionalIndex[token][docID][0]/math.sqrt(docLen[docID])#takes the current weight in each document and divides it by the square root of the value in the dummy dictionary






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

        for docID in range(1,self.numDocs):
            scores[docID] = random.random() * 0.000000001

        for stemQuery in termFreq:
            if stemQuery in self.positionalIndex:
                for docID in self.positionalIndex[stemQuery]:
                    scores[docID] += self.positionalIndex[stemQuery][docID][0] * termFreq[stemQuery]



        itemDict = dict()
        for docID in scores:
            itemID = self.db.lookupItemID(docID)[0]
            #item = self.db.lookupItemNameType(itemID)[0]
            if itemID not in itemDict:
                itemDict[itemID] = scores[docID]
            else:
                itemDict[itemID] += scores[docID]

        itemList = []
        sortedItems = sorted(itemDict.values())

        for i in range(len(sortedItems)):
            for itemID in itemDict:
                if (sortedItems[(len(sortedItems) - 1 - i)]) == itemDict[itemID]:
                    itemList.append(itemID)

        return(itemList)


    def relevant(self, itemList, qNum):
        relevantList = []
        for i in range(len(itemList)):
            if (itemList[i]) == qNum:
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
    rankedIndex = Ranked()

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
            qNum = 1
            for item in rawList:
                query = item
                itemList = rankedIndex.Query(query, todo[1])
                relList = rankedIndex.relevant(itemList, qNum)
                qNum += 1
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