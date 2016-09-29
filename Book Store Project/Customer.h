#pragma once
#include<string>
using namespace std;
class Customer{
private:
	string name;
	string desiredTitle;
public:
	Customer(string, string);
	~Customer(void);
	string getName();
	string getDesiredTitle();
};

