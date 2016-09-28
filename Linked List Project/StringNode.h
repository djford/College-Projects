#pragma once
#include <string>
using namespace std;
class StringNode{
private:
	string contents;
	StringNode* next;
public:
	StringNode(string contentsIn, StringNode* nextIn = nullptr);
	~StringNode(void);
	string getContents();
	void setContents(string contentsIn);
	StringNode* getNext();
	void setNext(StringNode* nextIn);
};

