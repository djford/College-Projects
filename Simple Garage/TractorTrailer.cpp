/*
Daniel Ford
9/18/13
cpp file for class TractorTrailer that constructs the tractor trailer using an extension of Vehicle constuctor,
sets the weight of the load in the tractor trailer, and displays its total weight and number of wheels.
*/

#include "StdAfx.h"
#include "TractorTrailer.h"


TractorTrailer::TractorTrailer(){
	loadWeight = 0;

}//default constructor

TractorTrailer::TractorTrailer(string nameIn, double mpgIn, int weightIn, int wheelsIn) : Vehicle(nameIn, mpgIn, weightIn){
	wheels = wheelsIn;
	loadWeight = 0;
}//parameterized constructor shares some with Vehicle

int TractorTrailer::getWheelCount() const{
	return wheels;
}//gets the number of wheels on the tractor trailer

void TractorTrailer::setLoadWeight(int loadWeightIn){
	loadWeight = loadWeightIn;
}//sets the weight of the load in the tractor trailer


int TractorTrailer::getWeight() const{
	int totalWeight = Vehicle::getWeight() + loadWeight;
	return totalWeight;
}//gets the total weight of the tractor trailer by adding its weight with its load weight




