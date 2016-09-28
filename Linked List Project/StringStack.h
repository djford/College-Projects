#pragma once
#include <string>
#include <iostream>
#include "StringLinkedList.h"
using namespace std;
class StringStack{
private:
	StringLinkedList *myList;
public:
	StringStack(void);
	StringStack(const StringStack&);
	~StringStack(void);
	bool isEmpty();
	void push(string);
	bool pop();
	string peek();
};

