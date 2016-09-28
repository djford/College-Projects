#pragma once
#include <exception>
#include <string>
using namespace std;
class StringTooLongException : public invalid_argument{
private:
	int attemptedLength;
	int allowedLength;
public:
	StringTooLongException(int attemptedLengthIn, int allowedLengthIn, const string& message);
	~StringTooLongException(void);
	int getAttemptedLength();
	int getAllowedLength();
};

