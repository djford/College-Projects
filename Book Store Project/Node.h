#pragma once
#include<string>
#include "Customer.h"
using namespace std;
class Node{
private:
	string contents1;
	string contents2;
	Node* next;
public:
	Node(Customer contentsIn, Node* nextIn);
	~Node(void);
	string getContents();
	void setContents(Customer contentsIn);
	Node* getNext();
	void setNext(Node* nextIn);
};

