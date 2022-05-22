import sys
pathNum = len(sys.argv)
for i in range(1, pathNum):
    path = sys.argv[i]
    rFile = open(path, "r")
    print(path + ":")
    print(rFile.read())
    rFile.close()