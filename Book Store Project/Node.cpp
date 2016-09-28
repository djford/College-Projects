#include "StdAfx.h"
#include "Node.h"


Node::Node(Customer contentsIn, Node* nextIn){
	contents1 = contentsIn.getName();
	contents2 = contentsIn.getDesiredTitle();
	next = nextIn;
}


Node::~Node(void){
}

string Node::getContents(){
	return contents1 + "," + contents2;
}

void Node::setContents(Customer contentsIn){
	contents1 = contentsIn.getName();
	contents2 = contentsIn.getDesiredTitle();
}

Node* Node::getNext(){
	return next;
}

void Node::setNext(Node* nextIn){
	next = nextIn;
}

	



