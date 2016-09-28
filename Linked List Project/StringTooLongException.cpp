#include "StdAfx.h"
#include "StringTooLongException.h"


StringTooLongException::StringTooLongException(int attemptedLengthIn, int allowedLengthIn, const string& message)
	:invalid_argument(message){
		attemptedLength = attemptedLengthIn;
		allowedLength = allowedLengthIn;

}


StringTooLongException::~StringTooLongException(void){
}

int StringTooLongException::getAttemptedLength(){
	return attemptedLength;
}

int StringTooLongException::getAllowedLength(){
	return allowedLength;
}