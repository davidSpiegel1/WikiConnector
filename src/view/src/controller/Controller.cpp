#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <cstring> // Include for strcpy function
#include <cstdlib>
#include "Controller.h"
using namespace std;

 Controller::Controller(){

	connector = "Wiki";

}

string Controller::getConnector(){

	return connector;

}

void Controller::changeConnector(string con){

	connector = con;
}

void Controller::Query (string query){


	const char* strLiteral = query.c_str(); // Convert std::string to const char*
     if (this->connector == "Wiki"){
    	
	// Create a character array to hold the concatenated command
    	char command[query.length() + sizeof("cd ..; cd model; python3 WikiSource.py ")];

    	// Copy the initial command into the concatenated command
    	strcpy(command, "cd ..; cd model; python3 WikiSource.py ");

    	// Concatenate the query to the command
    	strcat(command, strLiteral);

	int result = system(command);

     }else if (this->connector == "WorldBank"){

	char command[query.length()+sizeof("cd ..; cd model; python3 WorldBankSource.py")];

	strcpy(command,"cd ..; cd model; python3 WorldBankSource.py ");

	strcat(command,strLiteral);

	int result = system(command);

     }else if (this->connector == "AppleMusic"){

	char command[query.length()+sizeof("cd ..; cd model; python3 AppleMusic.py ")];

	strcpy(command,"cd ..; cd model; python3 AppleMusic.py ");

	strcat(command,strLiteral);

	int result = system(command);

     }

    
    	// Use the concatenated command with the system function
   	//int result = system(command);
	
	// Going to try and move the file into the correct drectory
	int result2 = system("cd ..; cd model; cp test.csv ../view");





}

