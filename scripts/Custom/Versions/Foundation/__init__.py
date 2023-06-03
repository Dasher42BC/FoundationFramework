#########################################################
# Foundation Plugin System for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023 update by Dasher42
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

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

