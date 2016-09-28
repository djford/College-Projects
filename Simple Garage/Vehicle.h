/*
Daniel Ford
9/18/13
Header File for class Vehicle that states it's variables and methods.
*/
#pragma once
#include <string>
using namespace std;
class Vehicle
{
private:
	string name;
	double mpg;
	int weight;
public:
	Vehicle();
	Vehicle(string, double, int);
	bool isEmpty();
	bool isOwner(string) const;
    double getMpg() const;
    virtual int getWeight() const;
    virtual int getWheelCount() const=0;
};

