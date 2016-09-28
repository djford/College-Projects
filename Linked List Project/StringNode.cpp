#include "StdAfx.h"
#include "StringNode.h"
#include <iostream>

StringNode::StringNode(string contentsIn, StringNode* nextIn){
	contents = contentsIn;
	next = nextIn;
}


StringNode::~StringNode(void){

}

string StringNode::getContents(){
	return contents;
}

void StringNode::setContents(string contentsIn){
	contents = contentsIn;
}

StringNode* StringNode::getNext(){
	return next;
}

void StringNode::setNext(StringNode* nextIn){
	next = nextIn;
}

