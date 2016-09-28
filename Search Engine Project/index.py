"""
Daniel Ford and Josh Chang

Sets up the different types of queries and tokenizes the query entries to be used in the search.
Also sets up the index to store information for each of the items.
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


class Index(object):

    def __init__(self):
       os.chdir("data")
       self.db = WebDB('cache.db')
       os.chdir("clean")
       self.positionalIndex = dict()
       for file in os.listdir('.'):
           f = codecs.open(file, "r", 'utf-8')
           position = 0
           temp = str(file).split('.')
           docID = int(temp[0])
           for token in f:
               position += 1
               if token not in self.positionalIndex:
                   self.positionalIndex[token] = dict()
               if docID not in self.positionalIndex[token]:
                   self.positionalIndex[token][docID] = list()
               self.positionalIndex[token][docID].append(position)
           f.close()


    def wrdtokenize(self,token):
        thing = word_tokenize(token)
        return thing[0]

    def singleSearch(self, query):
       spider = Spider()
       stemQuery = spider.stem([query])
       query = stemQuery[0]
       query = self.wrdtokenize((query))+'\r\n'
       resultFlag = 0
       counter = 0
       for token in self.positionalIndex:
           if token == query:
               resultFlag += 1
               for docID in self.positionalIndex[token]:
                   counter += 1
                   url = self.db.lookupCachedURL_byID(docID)[0]
                   title = self.db.lookupCachedURL_byID(docID)[2]
                   urlID = self.db.lookupCachedURL_byURL(url)
                   itemID = self.db.lookupItemID(urlID)
                   item = self.db.lookupItemNameType(itemID)[0]
                   itemType = self.db.lookupItemNameType(itemID)[1]
                   print(url)
                   print(title)
                   print(item)
                   print(itemType)
                   print(counter)
                   print("----------")
       if resultFlag == 0:
           print("No Results for : " + query)

    def orQuery(self, query):
       spider = Spider()
       querysplit = (query.split())
       query1 = querysplit[0]
       query2 = querysplit[1]
       stemQuery1 = spider.stem([query1])
       stemQuery2 = spider.stem([query2])
       query1 = stemQuery1[0]
       query2 = stemQuery2[0]
       query1 = self.wrdtokenize(query1)+'\r\n'
       query2 = self.wrdtokenize(query2)+'\r\n'
       foundList = []
       resultflag = 0
       counter = 0
       for token in self.positionalIndex:
           if token == query1:
               resultflag += 1
               for docID in self.positionalIndex[token]:
                   foundList.append(docID)

       for token in self.positionalIndex:
           if token == query2:
               resultflag += 1
               for docID in self.positionalIndex[token]:
                   if docID not in foundList:
                       foundList.append(docID)

       for docID in foundList:
           counter += 1
           url = self.db.lookupCachedURL_byID(docID)[0]
           title = self.db.lookupCachedURL_byID(docID)[2]
           urlID = self.db.lookupCachedURL_byURL(url)
           itemID = self.db.lookupItemID(urlID)
           item = self.db.lookupItemNameType(itemID)[0]
           itemType = self.db.lookupItemNameType(itemID)[1]
           print(url)
           print(title)
           print(item)
           print(itemType)
           print(counter)
           print("----------")
       if resultflag == 0:
           print("No Results for: " + query1 + 'or' + query2)
           return


    def andQuery(self, query):
       foundList1 = []
       foundList2 = []
       spider = Spider()
       querysplit = (query.split())
       query1 = querysplit[0]
       query2 = querysplit[1]
       stemQuery1 = spider.stem([query1])
       stemQuery2 = spider.stem([query2])
       query1 = stemQuery1[0]
       query2 = stemQuery2[0]
       query1 = self.wrdtokenize(query1)+'\r\n'
       query2 = self.wrdtokenize(query2)+'\r\n'
       counter = 0
       resultflag = 0
       for token in self.positionalIndex:
           if token == query1:
               resultflag += 1
               for docID in self.positionalIndex[token]:
                   foundList1.append(docID)


       for token in self.positionalIndex:
           if token == query2:
               resultflag += 1
               for docID in self.positionalIndex[token]:
                   foundList2.append(docID)


       for i in (set(foundList1).intersection(foundList2)):
                   counter += 1
                   url = self.db.lookupCachedURL_byID(i)[0]
                   title = self.db.lookupCachedURL_byID(i)[2]
                   urlID = self.db.lookupCachedURL_byURL(url)
                   itemID = self.db.lookupItemID(urlID)
                   item = self.db.lookupItemNameType(itemID)[0]
                   itemType = self.db.lookupItemNameType(itemID)[1]
                   print(url)
                   print(title)
                   print(item)
                   print(itemType)
                   print(counter)
                   print("----------")
       if resultflag == 0:
           print("No Results for: " + query1 + 'and' + " " + query2)
           return



    def phraseQuery(self, query):
        spider = Spider()
        phraseList = []
        querysplit = (query.split())
        query1 = querysplit[0]
        query2 = querysplit[1]
        stemQuery1 = spider.stem([query1])
        stemQuery2 = spider.stem([query2])
        query1 = stemQuery1[0]
        query2 = stemQuery2[0]
        query1 = self.wrdtokenize((query1))
        query2 = self.wrdtokenize((query2))
        idList1 = self.getIdFromQuery(query1)
        idList2 = self.getIdFromQuery(query2)
        counter = 0
        try:
            for x in idList1:
                for y in idList2:
                    if x==y:
                        file = codecs.open(str(y) + '.txt', "r", 'utf-8')
                        iterFile = iter(file)
                        for line in iterFile:
                            if line.strip() == query1:
                                try:
                                    nextLine = next(iterFile)
                                except StopIteration:
                                    break
                                if nextLine.strip() == query2:
                                    listCheck = self.db.lookupCachedURL_byID(int(x))
                                    if listCheck not in phraseList:
                                        phraseList.append(listCheck)
                                        break
                        file.close()
        except TypeError:
            print("0 results")
        for item in phraseList:
            if item != None:
                counter += 1
                print(item)
                print(counter)




    def nearQuery(self, query):
        spider = Spider()
        phraseList = []
        querysplit = (query.split())
        query1 = querysplit[0]
        query2 = querysplit[1]
        stemQuery1 = spider.stem([query1])
        stemQuery2 = spider.stem([query2])
        query1 = stemQuery1[0]
        query2 = stemQuery2[0]
        query1 = self.wrdtokenize((query1))
        query2 = self.wrdtokenize((query2))
        idList1 = self.getIdFromQuery(query1)
        idList2 = self.getIdFromQuery(query2)
        counter = 0
        try:
            for x in idList1:
                for y in idList2:
                    if x==y:
                        file = codecs.open(str(y) + '.txt', "r", 'utf-8')
                        iterFile = iter(file)
                        for line in iterFile:
                            if line.strip() == query1:
                                if line.strip() == query2 or line.strip() == query1:
                                    for x in range(0,5):
                                        try:
                                            nextLine = next(iterFile)
                                        except StopIteration:
                                            break
                                        if nextLine.strip() == query2 or nextLine.strip() == query1:
                                            listCheck = self.db.lookupCachedURL_byID(int(x))
                                            if listCheck not in phraseList:
                                                phraseList.append(listCheck)
                                                break
                        file.close()
        except TypeError:
            print("0 results")
        for item in phraseList:
            if item != None:
                counter += 1
                print(item)
                print(counter)


    def getIdFromQuery(self, query):
        for key, value in self.positionalIndex.items():
            if (query + '\r\n') == key:
                idList = []
                for k, v in value.items():
                   idList.append(k)
                return idList
        return None



def main():
   newIndex = Index()
   #os.chdir("..")
   #os.chdir("..")
   #with open("save.p", "wb") as outfile:
       #pickle.dump(newIndex, outfile)


   #with open("save.p", "rb") as infile:
       #index = pickle.load(infile)

   #os.chdir("data")
   #os.chdir("clean")





   choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))
   while 0 < choice < 7:

       if choice == 1:
           print("Single Query!")
           token = input('Enter a token: ')
           newIndex.singleSearch(token)
           choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))


       elif choice == 2:
           print("OR Query! 'ex. big or bad...'")
           token = input('Type in an OR query: ')
           newIndex.orQuery(token)
           choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))


       elif choice == 3:
           print("AND Query! 'ex. big and bad...'")
           token = input("Type in an AND query: ")
           newIndex.andQuery(token)
           choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))


       elif choice == 4:
           print("PHRASE Query! 'ex. rock star...'")
           token = input("Type in an PHRASE query: ")
           newIndex.phraseQuery(token)
           choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))


       elif choice == 5:
           print("NEAR Query! 'ex. rock star...'")
           token = input("Type in an PHRASE query: ")
           newIndex.nearQuery(token)
           choice = int(input("Please enter a number: \n (1)single \n (2)or \n (3)and \n (4)phrase \n (5)near  \n (6)Quit \n > "))

       elif choice == 6:
           exit(0)

   print("Invalid number")



main()




