#include "StdAfx.h"
#include "InvitoryItem.h"


InvitoryItem::InvitoryItem(){
	title = " ";
	haveValue = 0;
	wantValue = 0;
}


InvitoryItem::~InvitoryItem(void){
}

string InvitoryItem::getTitle(){
	return title;
}

void InvitoryItem::setTitle(string titleIn){
	title = titleIn;
}


int InvitoryItem::getHaveValue(){
	return haveValue;
}

void InvitoryItem::setHaveValue(int haveValueIn){
	haveValue = haveValue + haveValueIn;
}


int InvitoryItem::getWantValue(){
	return wantValue;
}

void InvitoryItem::setWantValue(int wantValueIn){
	wantValue = wantValue + wantValueIn;
}



