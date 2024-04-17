#include <iostream>
#include <string>
using namespace std;
#pragma once

class Controller
{
public:
Controller();
void changeConnector(string query);
void Query(string query);
string getConnector();
private:
std::string connector;
};
