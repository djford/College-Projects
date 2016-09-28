#include "StdAfx.h"
#include "StringQueue.h"
#include <string>
#include <iostream>
using namespace std;

StringQueue::StringQueue(void){
	myList = new StringLinkedList();
}


StringQueue::~StringQueue(void){
	delete myList;
}

bool StringQueue::isEmpty(){
	return myList->isEmpty();
}

void StringQueue::enqueue(string myString){
	 myList->addAtTail(myString);
}

bool StringQueue::dequeue(){
	return myList->removeHead();
}

string StringQueue::peekFront(){
	return myList->getStringAtHead();
}
