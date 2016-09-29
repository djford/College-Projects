/*
Daniel Ford
9/18/13
Header file for class Car that states its variables and methods. Inherited from Vehicle class.
*/

#pragma once
#include "Vehicle.h"
#include <string>
using namespace std;
class Car : public Vehicle
{
private:
	int wheels;

public:
	Car();
	Car(string, double, int);
	int getWheelCount() const;
};

