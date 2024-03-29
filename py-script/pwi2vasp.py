#! /usr/bin/env python3
import sys
for i in range(1, len(sys.argv)):
    pwiPath = sys.argv[i]
    print(pwiPath, end="")
    pwiFile = open(pwiPath, "r")
    inLine = pwiFile.readline().replace("\n", "").replace("\r", "")
    mode = -1 # 0 &Others, 1 &SYSTEM, 2 CELL_PARA, 3 ATOM_POS, -1 uncertain
    nl_SYSTEM = {}
    ntyp = 0
    cellPara = []
    atomPos = {}
    alat = 0.0
    while inLine:
        line = inLine
        if mode == -1:
            if line == "&SYSTEM":
                mode = 1
            elif line[0] == "&":
                mode = 0
            else:
                card = line.split()
                if card[0] == "CELL_PARAMETERS":
                    mode = 2
                    cardoption = card[1].strip("()\{\}")
                    if cardoption == "bohr":
                        alat = 0.5292
                    elif cardoption == "angstrom":
                        alat = 1.0
                elif card[0] == "ATOMIC_POSITIONS":
                    mode = 3
        elif mode == 0:
            if line == "/":
                mode = -1
        elif mode == 1:
            line = line.split("!")[0].replace(" ", "")
            if line == "/":
                mode = -1
            else:
                line = line.replace(" ", "").strip(",")
                keyVList = line.split(",")
                for kV in keyVList:
                    k_v = kV.split("=")
                    nl_SYSTEM.update({k_v[0]: k_v[1]})
        elif mode == 2:
            cellPara.append(list(map(float, line.split())))
            inLine = pwiFile.readline().replace("\n", "").replace("\r", "")
            cellPara.append(list(map(float, inLine.split())))
            inLine = pwiFile.readline().replace("\n", "").replace("\r", "")
            cellPara.append(list(map(float, inLine.split())))
            cellPara = [[x*alat for x in v] for v in cellPara]
            mode = -1
        elif mode == 3:
            for n in range(int(nl_SYSTEM["nat"])):
                atom_pos = line.split()[0:4]
                if atom_pos[0] in atomPos:
                    atomPos[atom_pos[0]].append([float(atom_pos[1]), float(atom_pos[2]), float(atom_pos[3])])
                else:
                    atomPos.update({atom_pos[0]:[[float(atom_pos[1]), float(atom_pos[2]), float(atom_pos[3])]]})
                inLine = pwiFile.readline()
                line = inLine
            mode = -1
        inLine = pwiFile.readline().replace("\n", "").replace("\r", "")
    pwiFile.close()
    if int(nl_SYSTEM["ibrav"]):
        print(": ibrav!=0 is not implemented")
        continue
    vaspOut = open(pwiPath+".vasp", "w")
    vaspOut.write("Generated by mview pwi2vasp\n1.0\n")
    vaspOut.write("%16.12f %16.12f %16.12f\n%16.12f %16.12f %16.12f\n%16.12f %16.12f %16.12f\n" % (cellPara[0][0], cellPara[0][1], cellPara[0][2], cellPara[1][0], cellPara[1][1], cellPara[1][2], cellPara[2][0], cellPara[2][1], cellPara[2][2]))
    atomN = []
    for elem in atomPos:
        atomN.append(len(atomPos[elem]))
        vaspOut.write("%5s" % (elem))
    vaspOut.write("\n")
    for n in atomN:
        vaspOut.write("%5d" % (n))
    vaspOut.write("\nDirect\n")
    for elem in atomPos:
        for pos in atomPos[elem]:
            vaspOut.write("%15.10f%15.10f%15.10f\n" % (pos[0], pos[1], pos[2]))
    vaspOut.close()
    print(" -> "+pwiPath+".vasp")
