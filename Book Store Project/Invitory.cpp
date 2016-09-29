#include "StdAfx.h"
#include "Invitory.h"
#include "InvitoryItem.h"
#include <iostream>
#include <fstream>


Invitory::Invitory(void){
}


Invitory::~Invitory(void){
}

Invitory::Invitory(int sizeIn){
	size = sizeIn;
	invitoryList = new InvitoryItem*[size];

	for (int x=0; x< size; x++){
		invitoryList[x] = nullptr;
	}
}

bool Invitory::addTitle(string bookTitle){
	int temp;
	InvitoryItem* book = new InvitoryItem;
	if(invitoryList[0] != nullptr){
		for (int x=0; x< size; x++){
			if(invitoryList[x]->getTitle() == bookTitle){
				cout << "Title: " << invitoryList[x]->getTitle() << ", haveValue: " << invitoryList[x]->getHaveValue() << ", wantValue: " << invitoryList[x]->getWantValue() << endl;
			}
		}
	}
	for (int x=0; x< size; x++){
		if(invitoryList[x] == nullptr){
			book->setTitle(bookTitle);
			cout << "How many copies of this book do you want?" << endl;
			cin >> temp;
			book->setWantValue(temp);
			invitoryList[x] = book;
			return true;
		}
	}
}

bool Invitory::modifyWant(){
	int temp;
	string bookTitle;
	bool flag = false;
	cout << "What book do you want to modify the want value for: ";
	cin >> bookTitle;
	if(invitoryList[0] == nullptr){
		cout << "There are no books in the inventory at this time" << endl;
		return flag;
	}

	for (int x=0; x< size; x++){
		if (invitoryList[x]->getTitle() == bookTitle){
			cout << "Current want value: " << invitoryList[x]->getWantValue() << endl;
			cout << "What is your new desired want value?: ";
			cin  >> temp;
			invitoryList[x]->setWantValue(temp);
			flag = true;
		}
	}

	if (flag == false){
		cout << "Book not found in inventory";
	}

	return flag;
}

bool Invitory::orderBooks(){
	int index = 0;
	if (invitoryList[0] == nullptr){
		cout << "No books are in the inventory" << endl;
		return false;
	}
	ofstream outfile = ofstream("order.txt");
	while(invitoryList[index] != nullptr){
		if (invitoryList[index]->getWantValue() > invitoryList[index]->getHaveValue()){
			outfile <<"Ordered: " << invitoryList[index]->getTitle() << ": " << invitoryList[index]->getWantValue();
			invitoryList[index]->setHaveValue(invitoryList[index]->getWantValue());
			invitoryList[index]->setWantValue(0);
		}
		index++;
	}
	return true;
}

	