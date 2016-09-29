// GarageProject.cpp : Defines the entry point for the console application.
#include "stdafx.h"
#include "Vehicle.h"
#include "Car.h"
#include "TractorTrailer.h"
#include "Garage.h"
#include <iostream>
using namespace std;

//prints the information about a garage
void printGarageInfo(const Garage& g){
	cout << "Total cars:" << g.getVehicleCount() << ", Total Weight: " << g.getTotalWeight()  
		<< ", Total Wheel Count: " << g.getTotalWheelCount() << ", Average MPG: " << g.getAvgMpg()  << endl;
}

//main method to test the functionality of the Garage and Vehicle classes
int _tmain(int argc, _TCHAR* argv[]){
	
	//start with only 2 spaces
	Garage g = Garage(2);

	//add 4 vehicles, which causes array size to grow
	g.addVehicleFromString("Car,Bob,20.5,2000");
	g.addVehicleFromString("Car,Bill,40.5,3000");
	g.addVehicleFromString("TractorTrailer,Alice,10,12000,18");
	printGarageInfo(g);

	//remove Bill's car, and test that other removes don't cause problems
	g.removeVehicleByOwner("Bill");
	g.removeVehicleByOwner("Rick");
	g.removeVehicle(-1);
	g.removeVehicle(20);
	printGarageInfo(g);
	
	//add another vehicle, should bring total back to 4
	g.addVehicleFromString("TractorTrailer,Susie,7,14000,32");
	printGarageInfo(g);

	//add all vehicle from the file
	g.addVehiclesFromFile("GarageSave.txt");
	printGarageInfo(g);
	
	//remove several vehicles added from file
	g.removeVehicleByOwner("Terry");
	g.removeVehicleByOwner("Jess");
	printGarageInfo(g);

	return 0;
}