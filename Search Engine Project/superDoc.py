"""
Daniel Ford and Josh Chang

Sets up the index for our superDoc project which is the same as the normal project but with significantly
more items to collect and search for.
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
           #temp = self.db.superDoc((i+1))[0]
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

        for itemID in range(1,self.numDocs+1):
            scores[itemID] = random.random() * 0.000000001

        for stemQuery in termFreq:
            if stemQuery in self.positionalIndex:
                for itemID in self.positionalIndex[stemQuery]:
                    scores[itemID] += self.positionalIndex[stemQuery][itemID][0] * termFreq[stemQuery]




        sortedValues = (sorted(scores.values()))
        itemIDlist = []
        for i in range(5):
            for itemID in scores:
                if sortedValues[(len(sortedValues) - 1 - i)] == scores[itemID]:
                    itemIDlist.append(itemID)

        print("Top Five Items: \n")
        counter = 0
        for itemID in itemIDlist:
            counter += 1
            item = (self.db.lookupItemNameType(itemID)[0])
            print(str(counter) + ". " + item + "\n" + str(sortedValues[len(sortedValues) - 1 - (counter - 1)]) +"\n")



def main():
   superIndex = superDoc()
   #pickle.dump(superIndex.positionalIndex, open("saveSuper.p", "wb"))
   itemWeight = input("Enter a document weighting scheme(nnn, ltc): ")
   queryWeight = input("Enter a query weighting scheme(nnn, ltc): ")

   print("Loading Index...")

   if itemWeight == "nnn":
      superIndex.nnnDoc()
   if itemWeight == "ltc":
      superIndex.ltcDoc()



   query = input("Enter a query or QUIT to exit: ")
   while query != "QUIT":
      if queryWeight == "nnn":
          superIndex.Query(query, "nnn")
      if queryWeight == "ltc":
          superIndex.Query(query, "ltc")

      query = input("Enter a query or QUIT to exit: ")

main()
