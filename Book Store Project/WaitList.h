#pragma once
#include<string>
#include"Node.h"
using namespace std;
class WaitList{
private:
	Node* head;
public:
	WaitList(void);
	~WaitList(void);
	void addCustomer();
	bool removeCustomer();
	string printWaitLine();
};

