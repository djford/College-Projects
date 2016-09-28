#include "StdAfx.h"
#include "StringLinkedList.h"
#include <iostream>
#include "StringNode.h"
#include "StringTooLongException.h"

StringLinkedList::StringLinkedList(void){
	head = nullptr;
	maxStringLength = 7;
}

StringLinkedList::StringLinkedList(const StringLinkedList& toCopy){
	head = nullptr;
	maxStringLength = toCopy.maxStringLength;
	StringNode *nodeToCopy = toCopy.head;
	while (nodeToCopy != nullptr){
		addAtTail(nodeToCopy->getContents());
		nodeToCopy = nodeToCopy->getNext();
	}
}


StringLinkedList::~StringLinkedList(void){
	StringNode* current = head;
	//walk down list and call delete on each individual StringNode
	while(current != nullptr){
		StringNode* temp = current->getNext();
		delete current;
		current = temp;
	}
}

void StringLinkedList::addAtHead(string newString){
	if (newString.length() > maxStringLength){
		throw StringTooLongException(newString.length(), maxStringLength, "String to long in addAtHead()");
	}
	//create a node
	StringNode* newNode = new StringNode(newString);
	//point the newNode's next at the current value of head (the beginning of the current list)
	newNode->setNext(head);
	//point head at the newNode (the new beginning of the list)
	head = newNode;
}

void StringLinkedList::addAtTail(string newString){
	if (newString.length() > maxStringLength){
		throw invalid_argument("String to long in addAtTail()");
	}

	if (head == nullptr){
		addAtHead(newString);
	}
	else{
		//walk to end of list
		StringNode* current = head;
		while(current->getNext() != nullptr){
			current = current->getNext();
		}
		//create a new node and connect at end
		current->setNext(new StringNode(newString));
	}
}

string StringLinkedList::toString(){
	string ret = "";
	StringNode* current = head;
	//walk the list, add each element to the string, with commas in between
	while(current != nullptr){
		ret += current->getContents() + ", ";
		current = current->getNext();
	}
	return ret;
}

string StringLinkedList::toStringReverse(StringNode* current){ 
	//base case: empty list
	if(current == nullptr){
		return " ";
	}
	//recursive case
	else{
		string myString = current->getContents();
		string rest = toStringReverse(current->getNext());
		string newString = rest + myString;
		return newString;
	}
}

string StringLinkedList::toStringReverse(){
	return toStringReverse(head);
}

string StringLinkedList::getStringAtHead(){
	if (head != nullptr){
		return head->getContents();
	}
	else{
		throw logic_error("Operation on empty list in getStringAtHead()");
	}
}

bool StringLinkedList::removeHead(){
	if (head != nullptr){
		StringNode* temp = head;
		head = head->getNext();
		delete temp;
		return true;
	}
	else{
		return false;
	}
}

bool StringLinkedList::isEmpty(){
	if(head == nullptr){
		return true;
	}
	else{
		return false;
	}
}