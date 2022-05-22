#include"pw_o.h"
#include<iostream>
#include<array>
#include<cmath>
#include<string>
#include<fstream>

pw_o::pw_o(){}
double pw_o::vecNorm(double v1, double v2, double v3)
{
	return sqrt(v1 * v1 + v2 * v2 + v3 * v3);
}
void pw_o::getcelldm()
{
	switch (ibrav)
	{
	case 1:
		celldm[0] = cell_para[0] * alat;
		break;
	case 4:
		celldm[0] = vecNorm(cell_para[0], cell_para[1], cell_para[2]);
		celldm[2] = cell_para[8] / celldm[0];
		celldm[0] *= alat;
		break;
	case 5:
		celldm[0] = vecNorm(cell_para[0], cell_para[1], cell_para[2]);
		celldm[3] = (cell_para[0] * cell_para[3] + cell_para[1] * cell_para[4] + cell_para[2] * cell_para[5]) / celldm[0] / sqrt(cell_para[3] * cell_para[3] + cell_para[4] * cell_para[4] + cell_para[5] * cell_para[5]);
		celldm[0] *= alat;
		break;
	case 6:
		celldm[0] = cell_para[0] * alat;
		celldm[2] = cell_para[8] / cell_para[0];
		break;
	case 8:
		celldm[0] = cell_para[0] * alat;
		celldm[1] = cell_para[4] / cell_para[0];
		celldm[2] = cell_para[8] / cell_para[0];
		break;
	case 12:
		celldm[0] = vecNorm(cell_para[0], cell_para[1], cell_para[2]);
		celldm[1] = vecNorm(cell_para[3], cell_para[4], cell_para[5]);
		celldm[2] = cell_para[8] / celldm[0];
		celldm[3] = (cell_para[0] * cell_para[3] + cell_para[1] * cell_para[4] + cell_para[2] * cell_para[5]) / celldm[0] / celldm[1];
		celldm[1] /= celldm[0];
		celldm[0] *= alat;
		break;
	}
}
void pw_o::printcelldm()
{
	switch (ibrav)
	{
	case 1:
		printf("celldm(1)=%.8f", celldm[0]);
		break;
	case 4:
		// as same as 6
	case 6:
		printf("celldm(1)=%.8f, celldm(3)=%.8f", celldm[0], celldm[2]);
		break;
	case 5:
		printf("celldm(1)=%.8f, celldm(4)=%.8f", celldm[0], celldm[3]);
		break;
	case 8:
		printf("celldm(1)=%.8f, celldm(2)=%.8f, celldm(3)=%.8f", celldm[0], celldm[1], celldm[2]);
		break;
	case 12:
		printf("celldm(1)=%.8f, celldm(2)=%.8f, celldm(3)=%.8f, celldm(4)=%.8f", celldm[0], celldm[1], celldm[2], celldm[3]);
		break;
	}
	printf(",\n\n");
}
void pw_o::in_pw_o(std::string path)
{
	int step = 1;
	std::string data;
	ifs.open(path);
	getline(ifs, data);
	std::cout << data << std::endl;
	while (getline(ifs, data))
	{
		if (data.substr(0, 12) == "     bravais")
		{
			ibrav = std::stoi(data.substr(32));
			printf("ibrav = %d\n", ibrav);
			break;
		}
	}
	while (getline(ifs, data))
	{
		if (data.substr(0, 25) == "     number of atoms/cell")
		{
			atomic_poss.resize(std::stoi(data.substr(32)));
			break;
		}
	}
	printf("\n\033[7mstep 0\033[0m\n\n");
	while (getline(ifs, data))
	{
		if (data.substr(0, 24) == "     the Fermi energy is")
		{
			printf("Ef             eV          %s\n", data.substr(25, 11).c_str());
		}
		else if (data.substr(0, 18) == "     Total force =")
		{
			printf("Total force    Ry/au       %s\n", data.substr(19, 17).c_str());
		}
		else if (data.substr(0, 38) == "          total   stress  (Ry/bohr**3)")
		{
			printf("P              kpar    %s\n", data.substr(70, 14).c_str());
			printf("\n\033[7mstep %d\033[0m\n\n", step++);
		}
		else if (data == "Begin final coordinates")
		{
			printf("\n\033[7mFinal structure\033[0m\n");
		}
		else if (data.substr(0, 15) == "CELL_PARAMETERS")
		{
			alat = stof(data.substr(23, 11));
			for (size_t i = 0; i < 9; i++)
			{
				ifs >> cell_para[i];
			}
			getcelldm();
			printcelldm();
		}
		else if (data.substr(0, 16) == "ATOMIC_POSITIONS")
		{
			for (size_t i = 0; i < atomic_poss.size(); i++)
			{
				//ifs >> atomic_poss[i].elm;
				//ifs >> atomic_poss[i].pos[0];
				//ifs >> atomic_poss[i].pos[1];
				//ifs >> atomic_poss[i].pos[2];
				//printf("%-3s          %13.10f       %13.10f       %13.10f", atomic_poss[i].elm.c_str(), atomic_poss[i].pos[0], atomic_poss[i].pos[1], atomic_poss[i].pos[2]);
				getline(ifs, data);
				printf("%s\n", data.c_str());
			}
			printf("\n");
		}
	}
	ifs.close();
}
