/*
Daniel Ford
10/3/13
cpp for class Garage that creates and array of pointers and uses them in conjunction with owner names and vehicle locations
to add, remove, get number of vehicles, total weight, avg mpg, and total number of wheels of vehicles that are being pointed at.
Vehicles can also be created from strings and files and the garage can double its size when a vehicle is being added to a full
garage.
*/

#include "StdAfx.h"
#include "Garage.h"
#include "Vehicle.h"
#include "Car.h"
#include "TractorTrailer.h"
#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
using namespace std;


Garage::Garage(){
	size = 0;
	parkingSpotsPtrArray = new Vehicle*[size];
	for (int x=0; x< size; x++){
		parkingSpotsPtrArray[x] = nullptr;
	}
	
}//default constuctor

Garage::Garage(int sizeIn){
    size = sizeIn;
	parkingSpotsPtrArray = new Vehicle*[size];
	for (int x=0; x< size; x++){
		parkingSpotsPtrArray[x] = nullptr;
	}
	
}//parameterized constructor with a specific size to set the number of spots in the garage


bool Garage::addVehicle(Vehicle* newVehicle){
	for (int x=0; x<size; x++){
		if (parkingSpotsPtrArray[x] == nullptr){
			parkingSpotsPtrArray[x] = newVehicle;
			return true;
		}
	}
	return false;

}//adds a vehicle to the garage if the pointer is pointing to an empty spot

bool Garage::addVehicleFromString(string line){
	int carsParked = 0;
	for (int x=0; x< size; x++){
		if (parkingSpotsPtrArray[x] != nullptr){
			carsParked = carsParked + 1;
		}
	}

	if (carsParked == size){
		doubleCapacity();
	}

	stringstream splitter(line); 

	string vehicleType;
	if (getline(splitter, vehicleType, ',')){
		if (vehicleType == "Car"){
			string name;
			if(getline(splitter, name, ',')){
				string mpgStr;
				if(getline(splitter, mpgStr, ',')){
					double mpg = stod(mpgStr);
					string weightStr;
					if(getline(splitter, weightStr, ',')){
						int weight = stoi(weightStr);
						Vehicle* newCar = new Car(name, mpg, weight);
						addVehicle(newCar);
						return true;
					}
				}
			}

		}
		else if (vehicleType == "TractorTrailer"){
			string name;
			if(getline(splitter, name, ',')){
				string mpgStr;
				if(getline(splitter, mpgStr, ',')){
					double mpg = stod(mpgStr);
					string weightStr;
					if(getline(splitter, weightStr, ',')){
						int weight = stoi(weightStr);
						string wheelsStr;
						if(getline(splitter, wheelsStr, ',')){
							int wheels = stoi(wheelsStr);
							Vehicle* newTractorTrailer = new TractorTrailer(name, mpg, weight, wheels);
							addVehicle(newTractorTrailer);
							return true;
						}
					}
				}
			}
		}
	
	}

	cerr << "Creation failed for string: "<< line << endl;
	return false;

}//takes a vehicle string and breaks it up into pieces first determining the sub class and then using each piece to be the values of the vehicle
//parameters and then sends the newly created vehicle to the addVehicle method to be added to the garage and also calls the doubleCapacity method
//after checking if all the current number of spots in the garage are full

bool Garage::addVehiclesFromFile(string filename){
	ifstream infile(filename);
	if (infile.is_open()){
		string next;
		while(getline(infile, next)){
			addVehicleFromString(next);
		}
		return true;
	}
	return false;
}//takes the vehicle strings from a file and sends them to the addVehicleFromString method to be split up and formed into a vehicle

void Garage::doubleCapacity(){
	newSize = size * 2;
	newParkingSpotsPtrArray = new Vehicle*[size * 2];

	for (int x=0; x < size; x++){
		newParkingSpotsPtrArray[x] = parkingSpotsPtrArray[x];
	}

	for (int x=size; x < newSize; x++){
		newParkingSpotsPtrArray[x] = nullptr;
	}

	for (int x=0; x < size; x++){
		parkingSpotsPtrArray[x] = nullptr;
	}

   delete [] parkingSpotsPtrArray;
	parkingSpotsPtrArray = newParkingSpotsPtrArray;
	
	
	size = size * 2;
}//doubles the size of the old array by creating a new array of double the original size and copies the addresses contained in the old array to 
//the new one and then sets the old array to point at the same addresses as the new

int Garage::getLocationByOwner(string name){
	for (int x=0; x<size; x++){
		if(parkingSpotsPtrArray[x] != nullptr){
			if(parkingSpotsPtrArray[x]->isOwner(name) == true){
				return x;
			}
		}
	}
	return -1;
}//uses the owners name to find the spot of a vehicle unless the owner does not own a vehicle in the garage

bool Garage::removeVehicle(int spot){
		if (parkingSpotsPtrArray[spot] < 0){
			if (parkingSpotsPtrArray[spot] != nullptr){
				parkingSpotsPtrArray[spot] = nullptr;
				return true;
			}
		}
		
		cout << "Error: tried to remove from invalid spot: " << spot << endl;
		return false;
		

}//uses the spot in the garage to remove the vehicle from that spot and set the pointer to point at an empty spot

 int Garage::getVehicleCount() const{
	int count = 0;
	for (int x=0; x<size; x++){
		if (parkingSpotsPtrArray[x] != nullptr){
			count = count + 1;
		}
	}
	return count;
}//gets the number of vehicles currently being pointed at in the garage

 int Garage::getTotalWeight() const{
	int totalWeight = 0;
	for (int x=0; x<size; x++){
		if (parkingSpotsPtrArray[x] != nullptr){
			totalWeight = totalWeight + parkingSpotsPtrArray[x] ->getWeight();
		}
	}
	return totalWeight;
}//gets the weight of all vehicles being pointed at in the garage and adds them up to be displayed

 double Garage::getAvgMpg() const{
	double totalMpg = 0.0;
	double avgMpg = 0.0;
	for (int x = 0; x<size; x++){
		if (parkingSpotsPtrArray[x] != nullptr){
			totalMpg = totalMpg + (parkingSpotsPtrArray[x])->getMpg();
		}
	}
	avgMpg = totalMpg/getVehicleCount();
	return avgMpg;
}//gets the mpg of all vehicles being pointed at in the garage and adds them up and divides by the number 
//of vehicles in the garage in order to display the average mpg of all vehicles

 int Garage::getTotalWheelCount() const{
	int totalWheelCount = 0;
	for (int x=0; x<size; x++){
		if (parkingSpotsPtrArray[x] != nullptr){
			totalWheelCount = totalWheelCount + (parkingSpotsPtrArray[x])->getWheelCount();
		}
	}
	return totalWheelCount;
}//gets the total number of wheels of all vehicles being pointed at in the garage

bool Garage::removeVehicleByOwner(string name){
	for (int x=0; x<size; x++){
		if(parkingSpotsPtrArray[x] != nullptr){
			if(parkingSpotsPtrArray[x]->isOwner(name) == true){
				parkingSpotsPtrArray[x] = nullptr;
				return true;
			}
		}
	}
	cout << "Error : tried to remove unknown owner: " << name << endl;
	return false;
	
		
	
}// uses the name of the owner to remove the vehicle from the spot the owners vehicle is being pointed at and 
 // sets that pointer to point at an empty spot 


Garage::~Garage(){
	for (int x=0; x< size; x++){
		parkingSpotsPtrArray[x] = nullptr;
	}
	delete [] parkingSpotsPtrArray;
}//releases the memory in the array and deletes the array