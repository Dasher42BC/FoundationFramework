#########################################################
# Foundation Framework for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023 update by Dasher42
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

# In most versioned mods, the __init__.py of the latest version is intended
# to hold version numbers and dependency requirements. -Dasher42

from bcdebug import debug
from Custom.Versions.VersionUtils import UpdateNamespace

debug("Foundation 2023 initializing")

pTarget = __import__("Foundation")
pSource = __import__("_Foundation")

UpdateNamespace(pSource, pTarget)
