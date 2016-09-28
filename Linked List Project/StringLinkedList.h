#pragma once
#include <string>
#include "StringNode.h"
#include<exception>
class StringLinkedList{
private:
	//pointer to the start of the list (nullptr if list is empty)
	StringNode *head;
	int maxStringLength;
	string toStringReverse(StringNode* current);
public:
	StringLinkedList(void);
	StringLinkedList(const StringLinkedList&);
	~StringLinkedList(void);
	// add a string element to the head (start) of list
	void addAtHead(string newString);
	// add a string element to the tail (end) of list
	void addAtTail(string newString);
	//return a string representing all elements
	string toString();
	//returns the string at the head node of the list
	//throws: logic_error if list is empty
	string getStringAtHead();
	bool removeHead();
	bool isEmpty();
	string toStringReverse();
};

