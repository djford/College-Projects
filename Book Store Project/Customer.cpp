#include "StdAfx.h"
#include "Customer.h"


Customer::Customer(string nameIn, string desiredTitleIn){
	name = nameIn;
	desiredTitle = desiredTitleIn;
}


Customer::~Customer(void){
}

string Customer::getName(){
	return name;
}

string Customer::getDesiredTitle(){
	return desiredTitle;
}
