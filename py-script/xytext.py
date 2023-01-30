import sys
import matplotlib.pyplot as plt
labelType = sys.argv[1]
skipLine = int(sys.argv[2])
for i in range(3, len(sys.argv)):
    path = sys.argv[i]
    rFile = open(path, "r")
    X = []
    Y = []
    inXY = ["", ""]
    for j in range(skipLine):
        rFile.readline()
    inLine = rFile.readline()
    inXY = inLine.replace(",", " ").split()
    while inLine:
        if len(inXY)>1:
            X.append(float(inXY[0]))
            Y.append(float(inXY[1]))
        inLine = rFile.readline()
        inXY = inLine.replace(",", " ").split()
    rFile.close()
    plt.plot(X, Y, label = path)
if(labelType == "raman"):
    plt.xlabel("Raman Shift (cm$^{-1}$)")
    plt.ylabel("Intensity (a.u.)")
elif(labelType == "xrd"):
    plt.xlabel("$2\\theta\\ (\degree)$")
    plt.ylabel("Intensity (a.u.)")
elif(labelType == "xps"):
    plt.xlabel("Binding Energy (eV)")
    plt.ylabel("Intensity (a.u.)")
    plt.gca().invert_xaxis()
elif(labelType == "xy"):
    plt.xlabel("x")
    plt.ylabel("y")
plt.title(labelType)
plt.legend()
plt.grid()
plt.show()
