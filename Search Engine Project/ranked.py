"""
Daniel Ford and Josh Chang

Sets up the index to be searched through using the web pages we scraped from the net.
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




        sortedValues = (sorted(scores.values()))
        docIDlist = []
        for i in range(5):
            for docID in scores:
                if sortedValues[(len(sortedValues) - 1 - i)] == scores[docID]:
                    docIDlist.append(docID)
        print("Top Five URLS: \n")
        counter = 0
        for docID in docIDlist:
            counter += 1
            url = (self.db.lookupCachedURL_byID(docID)[0])
            title = (self.db.lookupCachedURL_byID(docID)[2])
            print(str(counter) + ". " + url + "\n" + title + "\n" + str(sortedValues[len(sortedValues) - 1 - (counter - 1)]) +"\n")

        print("Top Five Items: \n")
        itemcounter = 0
        itemDict = dict()
        for docID in scores:
            itemID = self.db.lookupItemID(docID)
            item = self.db.lookupItemNameType(itemID)[0]
            if item not in itemDict:
                itemDict[item] = scores[docID]
            else:
                itemDict[item] += scores[docID]

        itemList = []
        sortedItems = sorted(itemDict.values())
        for i in range(5):
            for item in itemDict:
                if (sortedItems[(len(sortedItems) - 1 - i)]) == itemDict[item]:
                    itemList.append(item)
        for item in itemList:
            itemcounter += 1
            print(str(itemcounter) + ". " + item + "\n" + str(itemDict[item]) + "\n")










def main():
    rankedIndex = Ranked()
    #pickle.dump(rankedIndex.positionalIndex, open("save.p", "wb"))


    documentWeight = input("Enter a document weighting scheme(nnn, ltc): ")
    queryWeight = input("Enter a query weighting scheme(nnn, ltc): ")

    print("Loading Index...")

    if documentWeight == "nnn":
        rankedIndex.nnnDoc()
    if documentWeight == "ltc":
        rankedIndex.ltcDoc()



    query = input("Enter a query or QUIT to exit: ")
    while query != "QUIT":
        if queryWeight == "nnn":
            rankedIndex.Query(query, "nnn")
        if queryWeight == "ltc":
            rankedIndex.Query(query, "ltc")

        query = input("Enter a query or QUIT to exit: ")

main()