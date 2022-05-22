#include<vector>
#include<array>
#include<fstream>

struct atomic_pos
{
	std::string elm = "";
	std::array<double, 3> pos = { 0,0,0 };
	//std::array<bool, 3> moveable = { 1,1,1 };
};
class pw_o
{
private:
	std::ifstream ifs;
	int ibrav = 0;
	double alat = 0;
	std::array<double, 9> cell_para = { 0,0,0,0,0,0,0,0,0 };
	std::vector<atomic_pos> atomic_poss;
	std::array<double, 6> celldm = { 0,0,0,0,0,0 };
	enum kw
	{

		//cell_para = 0xc,
		//atomic_pos = 0xa
	};
	double vecNorm(double v1, double v2, double v3);
	void getcelldm();
	void printcelldm();
public:
	pw_o();
	void in_pw_o(std::string path);
};