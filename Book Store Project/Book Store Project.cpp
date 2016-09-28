// Book Store Project.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
/*
#include "Invitory.h"
#include "WaitList.h"
*/
#include <string>
#include <iostream>
#include "InvitoryItem.h"
#include "Invitory.h"
#include "Customer.h"
#include "WaitList.h"
using namespace std;

int _tmain(int argc, _TCHAR* argv[]){
	string keyCommand;
	Invitory invitoryList(2);
	cout << "Welcome to the Book Store Interface. Please enter a key command to begin. Use the H command to display all command options." << endl;
	cin >> keyCommand;
	while (keyCommand != "Q"){
	if(keyCommand == "H"){
		cout << "H: Display all possible key commands" << endl;
		cout << "I: Display information for a specified title" << endl << "A: Add a book to the inventory and display information for a tittle that already exists in the inventory" << endl;
		cout << "M: Modify the amount of want for a specific title" << endl << "O: Order books to bring the number of books of a specific title equal to the number of wanted books of that title" << endl;
		cout << "D: Recieve delivered books, update number of books in the inventory, and sell books to customers in the wait list that wanted those books" << endl;
		cout << "R: Have books being returned added to the inventory" << endl << "S: Sell a book to a customer unless the book is not in stock in which case add the customer to the wait list" << endl;
		cout << "Q: Save the inventory and wait list and end the program" << endl;
		keyCommand = " ";
		cout << "Type another command to continue" << endl;
		cin >> keyCommand;
	}

	else if(keyCommand == "I"){

	}

	else if(keyCommand == "A"){
		string bookTitle;
		InvitoryItem tempBook;
		cout << "What is the title of the book?" << endl;
		cin >> bookTitle;
		invitoryList.addTitle(bookTitle);
		keyCommand = " ";
		cout << "Type another command to continue" << endl;
		cin >> keyCommand;
	}

	else if(keyCommand == "M"){
		invitoryList.modifyWant();
		keyCommand = " ";
		cout << "Type another command to continue" << endl;
		cin >> keyCommand;
	}

	else if(keyCommand == "O"){
		invitoryList.orderBooks();
		keyCommand = " ";
		cout << "Type another command to continue" << endl;
		cin >> keyCommand;
	}

	else if(keyCommand == "D"){

	}

	else if(keyCommand == "R"){

	}

	else if(keyCommand == "S"){

	}

	else if(keyCommand == "Q"){

	}
	}
	
	return 0;
}

