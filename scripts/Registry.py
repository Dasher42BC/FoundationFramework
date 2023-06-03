# Registry classes; these are considered ordered dictionaries in modern Python
# First written November 2001, updated June 2023
# By Dasher42, all rights reserved under the Lesser GNU Public License v2.1


# Registry is an ordered dictionary meant to get items either by integers as array offsets, or strings as dictionary keys
class Registry:
    def __init__(self):
        self._keyList = {}
        self._arrayList = []

    def Register(self, obj, name):
        if self._keyList.has_key(name):
            self._keyList[name] = obj
            for i in range(0, len(self._arrayList)):
                if self._arrayList[i] == name:
                    return i  # Return offset of current placement

        self._keyList[name] = obj
        self._arrayList.append(name)
        return len(self._arrayList) - 1  # Return array size as it was before

    def Remove(self, what):
        self.__delitem__(what)

    def GetName(self, i):
        if self._keyList.has_key(i):
            return self._keyList[i]
        return None

    def List(self, col=1):
        i = 0
        end = len(self._arrayList)
        width = 80 / col
        retval = ""
        for key in self._arrayList:
            if i != end and i % col == 0:
                retval = retval + "\r"
            i = i + 1
            retval = retval + ("%s%s" % (key, (" " * (width - len(key)))))
        return retval

    def ListNumbered(self, col=1, width=80):
        i = 0
        end = len(self._arrayList)
        # width /= (col + 4)
        width = (width / col) - col
        retval = ""
        for key in self._arrayList:
            i = i + 1
            retval = retval + ("%3d) %s%s" % (i, key, (" " * (width - len(key)))))
            if i != end and i % col == 0:
                retval = retval + "\r"
        return retval

    def __len__(self):
        return len(self._arrayList)

    def __repr__(self):
        return self.List()

    def __getitem__(self, i):
        try:
            idx = int(i)
        except ValueError:
            return self._keyList[i]
        return self._keyList[self._arrayList[idx]]

    def __iter__(self):
        return self._arrayList.iteritems()

    def has_key(self, key):
        return self._keyList.has_key(key)

    def __cmp__(self, dict):
        return cmp(self._keyList, dict)

    def __setitem__(self, key, item):
        if not self._keyList.has_key(key):
            self._arrayList.append(key)
        self._keyList[key] = item

    def __delitem__(self, key):
        if self._keyList.has_key(what):
            self._arrayList.remove(what)
            del self._keyList[what]

    def clear(self):
        self._keyList.clear()
        self._arrayList.clear()

    def copy(self):
        import copy
        return copy.copy(self)

    def keys(self):
        return self._keyList.keys()

    def items(self):
        return self._keyList.items()

    def values(self):
        return self._keyList.values()

    def has_key(self, key):
        return self._keyList.has_key(key)

    def update(self, dict):
        for k, v in dict.items():
            self._keyList[k] = v

    def get(self, key, failobj=None):
        return self._keyList.get(key, failobj)


class IntHashRegistry(Registry):
    def __init__(self):
        Registry.__init__(self)
        self._hashList = {}

    def Register(self, obj, name):
        Registry.Register(self, obj, name)
        self._hashList[int(obj)] = obj

    def Remove(self, what):
        if self._hashList.has_key(what):
            Registry.Remove(self, self._hashList[what.__repr__()])
            del self._hashList[what]
        else:
            del self._hashList[self._keyList[what]]
            Registry.Remove(self, what)

    def __getitem__(self, i):
        try:
            idx = hash(i)
        except ValueError:
            return self._keyList[i]
        if self._hashList.has_key(idx):
            return self._hashList[idx]
        return None
