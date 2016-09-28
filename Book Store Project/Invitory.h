#pragma once
#include<string>
#include"InvitoryItem.h"
using namespace std;
class Invitory{
private:
	int size;
	InvitoryItem** invitoryList;
public:
	Invitory(void);
	~Invitory(void);
	Invitory(int);
	string listInvitory();
	bool sellTitle(string);
	bool modifyWant();
	bool orderBooks();
	bool addTitle(string);
	bool saveInvitory();
};

