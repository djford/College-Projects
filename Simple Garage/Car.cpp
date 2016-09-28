/*
Daniel Ford
9/18/13
cpp file for Car class that constructs the car as and extension of vehilce constructor and displays the number of wheels.
*/

#include "StdAfx.h"
#include "Car.h"


Car::Car(){
	wheels = 4;
}//default constructor


Car::Car(string nameIn, double mpgIn, int weightIn) : Vehicle(nameIn, mpgIn, weightIn){
	wheels = 4;
}//parameterized constructor shares with Vehicle

int Car::getWheelCount() const{
	int wheels = 4;
	return wheels;
}//gets the number of wheels on the car


