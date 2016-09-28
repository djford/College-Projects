#include "StdAfx.h"
#include "StringStack.h"
#include <string>
#include <iostream>
using namespace std;

StringStack::StringStack(void){
	myList = new StringLinkedList();
}

StringStack::StringStack(const StringStack& toCopy){
	myList = new StringLinkedList(*toCopy.myList);
}


StringStack::~StringStack(void){
	delete myList;
}

bool StringStack::isEmpty(){
	return myList->isEmpty();
}

void StringStack::push(string newString){
	myList->addAtHead(newString);
}

bool StringStack::pop(){
	return myList->removeHead();
}

string StringStack::peek(){
	return myList->getStringAtHead();
}
