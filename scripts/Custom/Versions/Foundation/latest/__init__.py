#########################################################
# Foundation Plugin System for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023 update by Dasher42
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

# In most versioned mods, the __init__.py of the latest version is intended
# to hold version numbers and dependency requirements. -Dasher42

# Other versioned mods should probably load their versioned dependencies here.

from bcdebug import debug

debug("Foundation 2023 initializing")

pFoundation = __import__("Foundation")
pNewFoundation = __import__("_Foundation")

pFoundation.__dict__.update(pNewFoundation.__dict__)