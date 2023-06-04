#########################################################
# Foundation Framework for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023 update by Dasher42
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

from bcdebug import debug

def UpdateNamespace(pSource, pTarget, bClearTargetFirst = 0, lSerializedObjects = None, lNonSerializedObjects = None):
    if lSerializedObjects and lNonSerializedObjects:
        debug("%s: Illogical use of lSerializedObjects %s and lNonSerializedObjects %s" % (__name__, lSerializedObjects, lNonSerializedObjects))
        raise FlagrantError

    if bClearTargetFirst:
        # TODO:  take all steps to re-initialize the module.
        pass

    pTarget.__dict__.update(pSource.__dict__)