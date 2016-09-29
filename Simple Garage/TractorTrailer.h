/*
Daniel Ford
9/18/13
Header file for class TractorTrailer that states its variables and methods. Inherited from Vehicle class.
*/

#pragma once
#include "Vehicle.h"
class TractorTrailer : public Vehicle
{
private:
	int wheels;
	int loadWeight;
public:
	TractorTrailer();
	TractorTrailer(string, double, int, int);
	void setLoadWeight(int);
	int getWheelCount() const;
	int getWeight() const;
};

