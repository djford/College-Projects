// Linked List Project.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <string>
#include <iostream>

#include "StringLinkedList.h"
#include "StringStack.h"
#include "StringQueue.h"
#include "StringTooLongException.h"

void addAtTailAndPrint(StringLinkedList aList, string nameToAdd){
	aList.addAtTail(nameToAdd);
	cout << "In addAtTailAndPrint:" << aList.toString() << endl;
}

int _tmain(int argc, _TCHAR* argv[])
{
	try{
	StringLinkedList *myList = new StringLinkedList();
	/*
	StringStack myStack = StringStack();
	myStack.push("Bob");
	myStack.push("Alice");
	myStack.push("Jane");

	while (!myStack.isEmpty()){
		cout << myStack.peek() << endl;
		myStack.pop();
	}

	StringQueue myQ = StringQueue();
	myQ.enqueue("Bob");
	myQ.enqueue("Alice");
	myQ.enqueue("Jane");

	while(!myQ.isEmpty()){
		cout << myQ.peekFront() << endl;
		myQ.dequeue();
	}
	*/

	try{
		myList->getStringAtHead();
	}
	catch(logic_error e){
		cout << "Error in getStringAtHead()" << e.what() << endl;
	}


	try{
		myList->addAtHead("Trololololo");
	}
	catch (StringTooLongException e){
		cout << "Error:" << e.what() << endl;
		cout << e.getAllowedLength() << endl;
	}
	myList->addAtHead("Bob");
	myList->addAtHead("Bill");
	myList->addAtTail("Jane");
	myList->addAtTail("Bobobbobobob");

	cout << "My List:" << myList->toString() << endl;

	addAtTailAndPrint(*myList, "Sally");

	cout << "My List again:" << myList->toString() << endl;

	delete myList;
	myList = nullptr;
	}
	catch (exception e){
		cout << "Error in main" << e.what() << endl;
	}

	return 0;
}

