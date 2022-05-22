#include<iostream>
#include"pw_o.h"

int main(int argc, char** argv)
{
	if (argc < 2) return 0;
	pw_o pw_O;
	pw_O.in_pw_o(std::string(argv[1]));
	return 0;
}