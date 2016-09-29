/*
Daniel Ford
9/18/13
Header file for class Garage that states its variables and methods.
*/
#pragma once
#include <string>
using namespace std;
#include "Vehicle.h"
class Garage
{
private:
	
	
    int size;
	int newSize;
	Vehicle **parkingSpotsPtrArray;
	Vehicle **newParkingSpotsPtrArray;
	bool addVehicle(Vehicle*);
	void doubleCapacity();

	bool empty;
public:
	Garage(void); 
	Garage(int);
	~Garage();
	int getLocationByOwner(string);
	bool addVehicleFromString(string);
	bool addVehiclesFromFile(string);
	bool removeVehicle(int);
    int getVehicleCount() const;
	int getTotalWeight() const;
	double getAvgMpg() const;
	int getTotalWheelCount() const;
	bool removeVehicleByOwner(string);
};
// Vehicle *myCar = new Vehicle(); delete myCar; myCar = nullptr;
