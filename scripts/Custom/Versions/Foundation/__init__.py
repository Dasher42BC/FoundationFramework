# TODO:  Write code to pick the latest directory for import

import nt
import ntpath
import string

loadPath = "scripts\\Custom\\Versions\\Foundation"

lDirs = []
for i in nt.listdir(loadPath):
    if (nt.stat("%s\\%s" % (loadPath, i))[0] & 0170000) == 0040000:
        lDirs.append(i)

lDirs.sort()

if len(lDirs) == 0:
    raise FlagrantError
else:
    print "Foundation 2023 loading, version", lDirs[-1]
    pModule = __import__(lDirs[-1])

