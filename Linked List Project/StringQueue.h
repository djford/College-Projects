#pragma once
#include <string>
#include <iostream>
#include "StringLinkedList.h"
using namespace std;
class StringQueue{
private:
	StringLinkedList* myList;
public:
	StringQueue(void);
	~StringQueue(void);
	bool isEmpty();
	void enqueue(string);
	bool dequeue();
	string peekFront();
};

