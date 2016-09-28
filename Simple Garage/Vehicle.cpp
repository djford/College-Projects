/*
Daniel Ford
9/18/13
cpp file for Vehicle class that constucts the vehicle and displays its properties owner, weight, and mpg.
*/
#include "StdAfx.h"
#include "Vehicle.h"
#include <string>
using namespace std;

static const string EMPTY = "emptySpot";
Vehicle::Vehicle(){
	name = EMPTY;
	mpg = 0.0;
	weight = 0;
}//default constructor which represents an empty spot

Vehicle::Vehicle(string nameIn, double mpgIn, int weightIn){
	name = nameIn;
	mpg = mpgIn;
	weight = weightIn;
}//paramatized constructor

bool Vehicle::isEmpty(){
	if (name == EMPTY){
		return true;
	}
	else{
		return false;
   }
}//tells the user if the vehicle is represented as an empty spot



bool Vehicle::isOwner(string ownerName) const{
	if (ownerName == name){
		return true;
	}
	else{
		return false;
	}
}//checks if a person owns a vehicle


 double Vehicle::getMpg() const{
	return mpg;
}//gives the mpg of a vehicle

 int Vehicle::getWeight() const{
	return weight;
}//gives the weight of a vehicle

 

