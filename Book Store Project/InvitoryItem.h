#pragma once
#include <string>
using namespace std;
class InvitoryItem{
private:
	string title;
	int haveValue;
	int wantValue;
public:
	InvitoryItem();
	~InvitoryItem(void);
	string getTitle();
	void setTitle(string
		);
	int getHaveValue();
	void setHaveValue(int);
	int getWantValue();
	void setWantValue(int);
};

