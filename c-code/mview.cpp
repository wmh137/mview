#include<cstdlib>
#include<iostream>
#include<string>
#include<fstream>
#include<map>
#include<time.h>

struct typeConf
{
    std::string bashStr;
    int argc;
    int argcMax;
};

int main(int argc, char const *argv[])
{
    timespec beginT, endT;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &beginT);
    std::string MVIEWPATH(getenv("MVIEWPATH"));
    if(MVIEWPATH.empty())
    {
        // env error
        std::cout<<"error: MVIEWPATH not found\n";
        return 0;
    }
    std::map<std::string, typeConf> confMap;
    typeConf inTypeConf;
    std::ifstream inFile;
    std::string inTypeName, inTypeArgcStr;
    // read mview.conf
    inFile.open(MVIEWPATH + "/mview.conf");
    while(!inFile.eof())
    {
        getline(inFile, inTypeName);
        getline(inFile, inTypeConf.bashStr, ',');
        getline(inFile, inTypeArgcStr, ',');
        inTypeConf.argc = std::stoi(inTypeArgcStr);
        getline(inFile, inTypeArgcStr);
        inTypeConf.argcMax = std::stoi(inTypeArgcStr);
        confMap[inTypeName] = inTypeConf;
    }
    inFile.close();
    std::map<std::string, typeConf>::const_iterator confIter;
    if(argc == 1)
    {
        // no input, show avail type
        // std::cout<<"error: no input\n";
        for(confIter = confMap.cbegin(); confIter != confMap.cend(); confIter++)
        {
            std::cout<<""<<confIter->first<<"\n\t"<<confIter->second.bashStr<<"\n";
        }
        return 0;
    }
    std::string typeName = argv[1];
    confIter = confMap.find(typeName);
    if(confIter == confMap.end())
    {
        // undefined type
        std::cout<<"error: undefined type \""<<typeName<<"\"\n";
        return 0;
    }
    if(argc < 2 + confIter->second.argc || argc > 2 + confIter->second.argcMax)
    {
        // too few or too many args for specific type
        std::cout<<"error: type \""<<typeName<<"\" need more than "<<confIter->second.argc<<" and less than "<<confIter->second.argcMax<<" arguments\n";
        return 0;
    }
    std::string bash = confIter->second.bashStr;
    bash.pop_back();
    bash.erase(0, 1);
    for(int i = 2; i < argc; i++)
    {
        bash.append(" ");
        bash.append(argv[i]);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &endT);
    long sec = endT.tv_sec - beginT.tv_sec, nsec = endT.tv_nsec - beginT.tv_nsec;
    if(nsec < 0)
    {
        sec -= 1;
        nsec += 1e9;
    }
    std::cout<<"mview react in "<<sec<<"s";
    if(nsec <= 5e3)
    {
        std::cout<<nsec<<"ns\n";
    }
    else if(nsec < 5e6)
    {
        std::cout<<nsec / 1e3<<"us\n";
    }
    else
    {
        std::cout<<nsec / 1e6<<"ns\n";
    }
    //cout<<bash<<endl;
    if(system(bash.c_str()) == -1)
    {
        std::cout<<"error: wrong input\n";
    }
    return 0;
}
