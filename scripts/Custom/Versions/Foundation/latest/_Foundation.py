#########################################################
# Foundation Framework for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023, by Dasher42
# Credit for legacy snippets from MLeo, Banbury, and others noted where possible.
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

import App
import Foundation
import FoundationTriggers

# Thanks to MLeo for the first piece of a whole new diagnostic framework.
from bcdebug import debug

version = "20230603"


#########################################################
# Shared dictionaries - direct access of these is deprecated

qbShipMenu = {}
qbPlayerShipMenu = {}


#########################################################
# Shared registries

from Registry import Registry

mutatorList = Registry()

shipList = Registry()
systemList = Registry()
raceList = Registry()
factionList = raceList
soundList = Registry()
bridgeList = Registry()

pGameType = None
pCurrentMode = None
pCurrentBridge = None

bFoundationInitialized = 0
bTesting = 1

# NonSerializedObjects = ('mode', 'version', 'MotionBlurOverrider', 'mbOverrider')

_g_dExcludePlugins = {
    # These are legacy Foundation fixes and updates, superceded in Foundation 2023
    "000-Fixes20030217": 1,
    "000-Fixes20030221": 1,
    "000-Fixes20030305-FoundationTriggers": 1,
    "000-Fixes20030402-FoundationRedirect": 1,
    "000-Fixes20040627-ShipSubListV3Foundation": 1,
    "000-Fixes20040715": 1,
    "000-Fixes20230424-ShipSubListV4_7Foundation": 1,
    "000-Utilities-Debug-20040328": 1,
    "000-Utilities-FoundationMusic-20030410": 1,
    "000-Utilities-GetFileNames-20030402": 1,
    "000-Utilities-GetFolderNames-20040326": 1,
    "000-Utilities-MediaList": 1,
    "001-Addons-FoundationRedirect": 1,
    "002-DevUtil-CheckClicked": 1,
    "FixTorps": 1,
    "LoadRemoveNanoBridgeFixAnnex": 1,
    "LoadRemoveNanoFolderDefAnnex": 1,
}

# This stupidly simple setter put in place to keep people using the interface, not implementation.  Because, that's naughty.
def SetExcludePlugin(sImport):
    global _g_dExcludePlugins
    _g_dExcludePlugins[sImport] = 1

# For anywhere an empty object is needed
class Dummy:
    pass

class Flags:
    """A generic long bitvector.  Accessors maintain integrity of the >32 bit size."""

    def __init__(self, val=0):
        self._value = long(val)

    def __repr__(self):
        return str(self._value)

    def __long__(self):
        return self._value

    def __int__(self):
        return self._value

    def List(self, registry):
        out = []
        for i in range(0, len(registry)):
            if self[i]:
                out.append(registry[i])
        return string.join(out, ", ")

    def __iand__(self, other):
        return self._value & long(other)

    def __ixor__(self, other):
        return self._value ^ long(other)

    def __ior__(self, other):
        return self._value | long(other)

    def Toggle(self, num):
        if long(num) >= 1024:  # Manual limits imposed because extremely high precisions cause slowdown
            raise IndexError  # and could be a sign of buggy code.
        self._value = self._value ^ long(1 << long(num))

    def Set(self, num):
        if long(num) >= 1024:  # Manual limits imposed because extremely high precisions cause slowdown
            raise IndexError  # and could be a sign of buggy code.
        self._value = self._value | long(1 << long(num))

    def UnSet(self, num):
        if long(num) >= 1024:  # Manual limits imposed because extremely high precisions cause slowdown
            raise IndexError  # and could be a sign of buggy code.
        self._value = self._value & long(1 << long(num))

    def Clear(self):
        self_value = long(0)

    def __getitem__(self, i):
        return self._value & long(1 << long(i))

    # This is experimental
    def __setitem__(self, i, val):
        if val:
            self._value = self._value | long(1 << long(i))
        else:
            self._value = self._value & long(1 << long(i))
        return self._value



ERA_ENT = 1
ERA_PRETOS = 2
ERA_TOS = 4
ERA_TMP = 8
ERA_PRETNG = 16
ERA_TNG = 32
ERA_DS9 = 64
ERA_NEMESIS = 128
ERA_PIC = 256


def Initialize(bTestFlag=0):
    import Foundation
    global bTesting

    if not Foundation.bFoundationInitialized:
        import StaticDefs

        if bTestFlag != 0:
            bTesting = 1

        Foundation.LoadExtraShips()
        Foundation.LoadExtraPlugins()

# Music lists, potentially faction and era specific
class MusicDef:
    def __init__(self):
        self.dMain = {}  # Base songs/fanfares to use as music...
        self.dStates = {}

    def AddFolder(self, sFolder, sGroup):
        if not self.dStates.has_key(sGroup):
            self.dStates[sGroup] = []
        try:
            lFolder = nt.listdir(sFolder)
            for i in lFolder:
                sName = sFolder + "/" + i

                s = string.split(i, ".")
                name = string.join(s[:-1], ".")
                ext = string.lower(s[-1])
                if ext == "mp3":
                    self.dMain[sName] = name
                    self.dStates[sGroup].append(name)
        except:
            pass

    def Add(self, obj):
        # Update from the folder's __init__.py
        try:
            self.dMain.update(obj.dMain)
            self.dStates.update(obj.dStates)
        except:
            pass

        # Now add in from the subfolders
        try:
            for i in obj.lFolders:
                s = string.split(i, "/")
                self.AddFolder(i, s[-1])
        except:
            pass

    def BuildList(self):
        # PrintDict(self.dGroups)

        lStates = []  # Special music states which are collections of pieces of music, played in random order.
        lTrans = []
        lMain = []
        bBlanked = 0

        for i in self.dMain.keys():
            lMain.append(i, self.dMain[i])

        kPtr = None
        kMaxlen = 0
        for i in self.dStates.keys():
            k = self.dStates[i]
            if len(k) > kMaxlen:
                kMaxlen = len(k)
                kPtr = k

        for i in self.dStates.keys():
            k = self.dStates[i]
            if len(k) == 0:
                k = kPtr
            if len(k) == 1:
                # This is necessary; BC crashes if there's only one element in a state list.
                if not bBlanked:
                    lMain.append("Custom/Music/Blank.mp3", "Blank")
                    bBlanked = 1
                k.append("Blank")
            if i == "Transition":
                for j in k:
                    lTrans.append(j)
            else:
                lStates.append(i, k)

        return (lMain, lTrans, lStates)

    def ChangeMusic(self, pEngine):
        lStates = []  # Special music states which are collections of pieces of music, played in random order.
        lTrans = []
        lMain = []

        (lMain, lTrans, lStates) = self.BuildList()

        import DynamicMusic

        DynamicMusic.ChangeMusic(tuple(lMain), tuple(lTrans), tuple(lStates), pEngine)

    def Initialize(self, pGame, pEngine):
        lStates = []  # Special music states which are collections of pieces of music, played in random order.
        lTrans = []
        lMain = []

        (lMain, lTrans, lStates) = self.BuildList()

        import DynamicMusic

        DynamicMusic.Initialize(pGame, tuple(lMain), tuple(lTrans), tuple(lStates), pEngine)


MusicDef.default = MusicDef()
MusicDef.default.dMain = {
    "sfx/Music/EpisGen2.mp3": "Starting Ambient",
    "sfx/Music/Starbase12.mp3": "Starbase12 Ambient",
    "sfx/Music/Nebula 1.mp3": "Nebula Ambient",
    "sfx/Music/Failure-8d.mp3": "Lose",
    "sfx/Music/Success-12.mp3": "Win",
    "sfx/Music/Transition 13.mp3": "EnemyBlewUp",
    "sfx/Music/Transition 14.mp3": "PlayerBlewUp",
    "sfx/Music/Panic-9a.mp3": "Panic-9a",
    "sfx/Music/Panic-9b.mp3": "Panic-9b",
    "sfx/Music/Panic-9c.mp3": "Panic-9c",
    "sfx/Music/Panic-9d.mp3": "Panic-9d",
    "sfx/Music/Panic-9e.mp3": "Panic-9e",
    "sfx/Music/Panic-9f.mp3": "Panic-9f",
    "sfx/Music/Panic-9g.mp3": "Panic-9g",
    "sfx/Music/Neutral-10i.mp3": "Neutral-10i",
    "sfx/Music/Neutral-10b.mp3": "Neutral-10b",
    "sfx/Music/Neutral-10c.mp3": "Neutral-10c",
    "sfx/Music/Neutral-10d.mp3": "Neutral-10d",
    "sfx/Music/Neutral-10e.mp3": "Neutral-10e",
    "sfx/Music/Neutral-10f.mp3": "Neutral-10f",
    "sfx/Music/Neutral-10g.mp3": "Neutral-10g",
    "sfx/Music/Neutral-10h.mp3": "Neutral-10h",
    "sfx/Music/Neutral-10a.mp3": "Neutral-10a",
    "sfx/Music/Confident-11a.mp3": "Confident-11a",
    "sfx/Music/Confident-11b.mp3": "Confident-11b",
    "sfx/Music/Confident-11c.mp3": "Confident-11c",
    "sfx/Music/Confident-11d.mp3": "Confident-11d",
    "sfx/Music/Confident-11e.mp3": "Confident-11e",
    "sfx/Music/Confident-11f.mp3": "Confident-11f",
    "sfx/Music/Confident-11g.mp3": "Confident-11g",
}

MusicDef.default.dStates = {
    "Combat Confident": ("Confident-11a", "Confident-11b", "Confident-11c", "Confident-11d", "Confident-11e", "Confident-11f", "Confident-11g"),
    "Combat Neutral": ("Neutral-10i", "Neutral-10b", "Neutral-10c", "Neutral-10d", "Neutral-10e", "Neutral-10f", "Neutral-10g", "Neutral-10h", "Neutral-10a"),
    "Combat Panic": ("Panic-9a", "Panic-9b", "Panic-9c", "Panic-9d", "Panic-9e", "Panic-9f", "Panic-9g"),
}



#########################################################
# Mode-related definitions

# The MutatorDef is a definition of a game mode, a collection of references to the active
# ships, projectiles, and other plugins that loaded into a game.
class MutatorDef:
    def __init__(self, name=None):
        self.name = name
        self.elements = []

        # These things get registries because their species numbers are important.
        self.shipSpecies = Registry()
        self.projectileSpecies = Registry()
        self.bridgeList = Registry()
        self.startShipDef = None

        self.shipMenu = {}
        self.playerShipMenu = {}
        self.systems = {}
        self.sounds = {}
        self.tglFiles = {}
        self.bBase = 0  # One one base MutatorDef can be activated at a time.
        self.bEnabled = 0  #
        self.overrides = []
        self.tgls = []

        if self.name:
            mutatorList.Register(self, self.name)

    def Update(self, mode):
        # print 'Updating %s from %s; base flag %d, start %s' % (self.name, mode.name, mode.bBase, mode.startShipDef)
        if mode.startShipDef:
            self.startShipDef = mode.startShipDef

        for i in mode.elements:
            i.AddToMutator(self)

    def IsEnabled(self):
        return self.bEnabled

    # It would seem that these are so simplistic that you'd want to just leave them as direct
    # variable accesses, given Python's non-private nature, but polymorphic subclassing operates
    # on methods, not member data. -Dasher42
    def Enable(self):
        # print 'Enabling', self.name
        self.bEnabled = 1

        # Activate the code overrides
        for i in self.overrides:
            i.ImmediateActivate()

    def Disable(self):
        # print 'Disabling', self.name
        self.bEnabled = 0
        # We need to make a copy of the list prior to reversing it
        revList = self.overrides[:]
        revList.reverse()
        for i in revList:
            i.ImmediateDeactivate()

    def Activate(self):
        # Set pCurrentMode so that this can be found elsewhere easily
        global pCurrentMode
        pCurrentMode = self

        # Activate the code overrides
        for i in self.overrides:
            i.Activate()

    def Deactivate(self):
        global pCurrentMode
        pCurrentMode = None

        # We need to make a copy of the list prior to reversing it
        revList = self.overrides[:]
        revList.reverse()
        for i in revList:
            i.Deactivate()

    def LoadTGLs(self):
        for i in self.tgls:
            i.Load()

    def UnLoadTGLs(self):
        for i in self.tgls:
            i.Unload()

    def GetBridge(self):
        if self.startShipDef:
            return self.startShipDef.GetBridge()
        return "GalaxyBridge"

    def GetMusic(self):
        try:
            return self.music
        except:
            try:
                return self.faction.music
            except:
                return MusicDef.default


# A gameplay mode for a stock BC setup
MutatorDef.Stock = MutatorDef("Stock Systems")
MutatorDef.Stock.bBase = 1

MutatorDef.StockSounds = MutatorDef(None)

# A gameplay mode for a stock BC setup
MutatorDef.StockShips = MutatorDef("Stock Ships")

# A generic add-on mode
MutatorDef.QuickBattle = MutatorDef("Extra Ships and Mods")
MutatorDef.QuickBattle.shipMenu = qbShipMenu
MutatorDef.QuickBattle.playerShipMenu = qbPlayerShipMenu


#########################################################
# A function to generate in-game structures using MutatorDefs
# Parameters:
# 	baseMode:  A MutatorDef that serves as the base for all other active modes to append to or revise
# 	dArgs:  A dictionary for forward argument compatibility
# Effects:  None
# Returns:  A MutatorDef set up starting with baseMode and with all other active non-base modes included
def BuildGameMode(baseMode=None, dArgs={}):
    LoadConfig()

    gameMode = MutatorDef()
    gameMode.startShipDef = ShipDef.Galaxy

    # We have to have those sounds; overrides are fine, but taking them out?
    # for i in MutatorDef.Stock.sounds.values():
    # 	i.AddToMutator(gameMode)

    if baseMode:
        gameMode.Update(baseMode)

    count = 0
    for key in mutatorList._arrayList:
        mode = mutatorList._keyList[key]
        # print mode, mode.name, mode.bBase, mode.bEnabled
        if mode.IsEnabled():
            count = count + 1
            gameMode.Update(mode)

    if not count:
        gameMode.Update(MutatorDef.Stock)
        gameMode.Update(MutatorDef.StockShips)

    return gameMode


# A base class for other definitions that are included in modes.
class MutatorElementDef:
    def __init__(self, name, dict):
        self.name = name
        modes = [MutatorDef.QuickBattle]
        if dict and dict.has_key("modes"):
            modes = dict["modes"]
        for mode in modes:
            self.AddToMutator(mode)

    def CheckForErrors(self):
        return None

    def AddToMutator(self, toMode):
        toMode.elements.append(self)


#########################################################
# Override-related definitions
class OverrideDef(MutatorElementDef):
    def __init__(self, name, sItem, sNewItem, dict={}):
        self.sItem = sItem
        self.sNewItem = sNewItem
        self.original = None
        # print 'Creating override of %s with %s' % (self.sItem, self.sNewItem)
        MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        # print 'Adding override %s to mode %s' % (self.name, toMode.name)
        toMode.overrides.append(self)
        toMode.elements.append(self)

    def _SwapInModules(self, pre, post):
        import string

        pPreModule = __import__(string.join(pre[:-1], "."))
        pPostModule = __import__(string.join(post[:-1], "."))

        self.original = pPreModule.__dict__[pre[-1]]
        pPreModule.__dict__[pre[-1]] = pPostModule.__dict__[post[-1]]
        # print 'Activating %s overriding %s' % (self.sNewItem, self.sItem)

    def _SwapOutModules(self, pre, post):
        import string

        pPreModule = __import__(string.join(pre[:-1], "."))

        pPreModule.__dict__[pre[-1]] = self.original
        self.original = None
        # print 'Deactivating %s restoring %s' % (self.sNewItem, self.sItem)

    def Activate(self):
        import string

        global bTesting

        if self.original:
            return

        pre = string.split(self.sItem, ".")
        post = string.split(self.sNewItem, ".")

        if bTesting:
            self._SwapInModules(pre, post)
        else:
            try:
                self._SwapInModules(pre, post)
            except:
                pass

    def Deactivate(self):
        import string

        if not self.original:
            return

        pre = string.split(self.sItem, ".")
        post = string.split(self.sNewItem, ".")

        if bTesting:
            self._SwapOutModules(pre, post)
        else:
            try:
                self._SwapOutModules(pre, post)
            except:
                pass

    def ImmediateActivate(self):
        pass

    def ImmediateDeactivate(self):
        pass


#########################################################
# Faction-related definitions


class FactionDef:
    def __init__(self, name, abbrev, dict={}):
        self.name = name
        self.num = factionList.Register(self, name)
        self.abbrev = abbrev
        self.ships = []
        self.weapons = []
        self.music = MusicDef.default

RaceDef = FactionDef

#########################################################
# TGL-related definitions


class TGLDef(MutatorElementDef):
    def __init__(self, name, filePathName, dict={}):
        self.num = systemList.Register(self, name)
        self.filePathName = filePathName
        self.handle = None
        MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        toMode.tgls.append(self)
        toMode.elements.append(self)

    def Load(self):
        if not self.handle:
            import App

            self.handle = App.g_kLocalizationManager.Load(self.filePathName)

    def Unload(self):
        if self.handle:
            import App

            App.g_kLocalizationManager.Unload(self.handle)
            self.handle = None


#########################################################
# System-related definitions


class SystemDef(MutatorElementDef):
    def __init__(self, name, maximum, minimum=0, dict={}):
        self.maximum = maximum
        self.minimum = minimum
        self.num = systemList.Register(self, name)
        MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        toMode.systems[self.name] = self
        toMode.elements.append(self)


#########################################################
# Bridge-related definitions


class BridgeDef(MutatorElementDef):
    def __init__(self, name, bridgeString, dict={}):
        self.bridgeString = bridgeString
        self.num = Foundation.bridgeList.Register(self, name)

        # This is a touch risky but I foresee no problem - Dasher42
        Foundation.bridgeList._keyList[bridgeString] = self

        self.locations = None
        if dict.has_key("locations"):
            self.locations = dict["locations"]
            # print 'Updating locations', name, self, self.locations, dict.keys()
        Foundation.MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        toMode.bridgeList.Register(self, self.name)
        toMode.elements.append(self)

    def SetLocation(self, locationName, kAM, pSequence, pAnimNode):
        try:
            loc = self.locations[locationName]
            import App

            kAM.LoadAnimation(loc[0], loc[1])
            pSequence.AppendAction(App.TGAnimPosition_Create(pAnimNode, loc[1]))
            for i in range(2, len(loc)):
                try:
                    exec(loc[i])
                except SyntaxError:
                    pass  # raise SyntaxError, evalStr
            return 1
        except:
            pass
        return None


def BridgeSetLocation(locationName, kAM, pSequence, pAnimNode):
    if Foundation.pCurrentBridge:
        return Foundation.pCurrentBridge.SetLocation(locationName, kAM, pSequence, pAnimNode)
    return None


#########################################################
# Ship-related definitions
# These are intended to be base classes for objects instantiated in


class ShipDef(MutatorElementDef):
    def __init__(self, abbrev, species, dict={}):
        self.abbrev = abbrev
        self.species = species
        self.faction = None
        self.desc = ""
        self.hasTGLName = 0
        self.hasTGLDesc = 0
        self.menuGroup = None
        self.playerMenuGroup = None

        self.__dict__.update(dict)
        if not self.__dict__.has_key("iconName"):
            self.iconName = abbrev
        if not self.__dict__.has_key("name"):
            self.name = abbrev
        if not self.__dict__.has_key("shipFile"):
            self.shipFile = abbrev
        if not self.__dict__.has_key("shipPrefix"):
            self.shipPrefix = "ships."

        if dict.has_key("faction"):
            self.faction = dict["faction"]
            self.faction.ships.append(self)

        self.sAttackModule = None

        self.friendlyDetails = [self.abbrev, self.name, self.StrFriendlyDestroyed(), self.StrFriendlyAI(), "Friendly"]
        self.enemyDetails = [self.abbrev, self.name, self.StrEnemyDestroyed(), self.StrEnemyAI(), "Enemy"]

        self.num = shipList.Register(self, abbrev)
        if shipList._keyList.has_key(self.name):
            self.friendlyDetails[2] = shipList[self.name].friendlyDetails[2]
            self.enemyDetails[2] = shipList[self.name].enemyDetails[2]

        # This is quite deliberately commented out
        # MutatorElementDef.__init__(self, self.name, dict)

    def Activate(self):
        pModule = Foundation.FolderManager("ship", self.shipFile)
        pModule.__dict__[self.name] = self
        pModule.__dict__[self.abbrev] = self

    def AddToMutator(self, toMode):
        toMode.elements.append(self)
        if self.menuGroup:
            self.RegisterQBShipMenu(self.menuGroup, toMode)
        if self.playerMenuGroup:
            self.RegisterQBPlayerShipMenu(self.playerMenuGroup, toMode)

    def GetIconNum(self):
        return self.species

    def GetSpecies(self):
        return self.species

    def GetAttackModule(self):
        return "NonFedAttack"

    def GetRace(self):
        return self.faction

    def StrFriendlyDestroyed(self):
        return "QBFriendlyGenericShipDestroyed"

    def StrEnemyDestroyed(self):
        return "QBEnemyGenericShipDestroyed"

    def StrFriendlyAI(self):
        return "QuickBattleFriendlyAI"

    def StrEnemyAI(self):
        return "QuickBattleAI"

    def MenuGroup(self):
        return "Other Ships"

    def GetBridge(self):
        return "GalaxyBridge"

    def RegisterQBShipMenu(self, group=None, mode=MutatorDef.QuickBattle):
        if not self.menuGroup:
            self.menuGroup = group
        if not shipList._keyList.has_key(self.abbrev):
            # If this failed, we know that there was an ImportError exception caught in ShipDef.__init__ -Dasher
            return
        if not group:
            group = self.MenuGroup()
        if mode.shipMenu.has_key(group):
            if mode.shipMenu[group][1].has_key(self.name):
                previous = mode.shipMenu[group][1][self.name]
                # print previous.__dict__.items()
                # print self.__dict__.items()
                previous.shipFile = self.shipFile
                previous.iconName = self.iconName
                previous.species = self.species
                return
            mode.shipMenu[group][0].append(self)
            mode.shipMenu[group][1][self.name] = self
        else:
            mode.shipMenu[group] = ([self], {self.name: self})
        if mode.elements.count(self) == 0:
            mode.elements.append(self)

    def RegisterQBPlayerShipMenu(self, group=None, mode=MutatorDef.QuickBattle):
        if not self.playerMenuGroup:
            self.playerMenuGroup = group
        if not shipList._keyList.has_key(self.abbrev):
            # If this failed, we know that there was an ImportError exception caught in ShipDef.__init__ -Dasher
            return
        if not group:
            group = self.MenuGroup()
        if mode.playerShipMenu.has_key(group):
            if mode.playerShipMenu[group][1].has_key(self.name):
                previous = mode.playerShipMenu[group][1][self.name]
                previous.shipFile = self.shipFile
                previous.iconName = self.iconName
                previous.species = self.species
                return
            mode.playerShipMenu[group][1][self.name] = self
            mode.playerShipMenu[group][0].append(self)
        else:
            mode.playerShipMenu[group] = ([self], {self.name: self})
        if mode.elements.count(self) == 0:
            mode.elements.append(self)




Federation = FactionDef("Federation", "Fed")
Cardassian = FactionDef("Cardassian", "Card")
Klingon = FactionDef("Klingon", "Klingon")
Romulan = FactionDef("Romulan", "Romulan")
Ferengi = FactionDef("Ferengi", "Ferengi")
Kessok = FactionDef("Kessok", "Kessok")
Dominion = FactionDef("Dominion", "Dom")
Breen = FactionDef("Breen", "Breen")
Borg = FactionDef("Borg", "Borg")


class StarBaseDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Federation
        ShipDef.__init__(self, abbrev, species, dict)

    def StrFriendlyAI(self):
        return "StarbaseFriendlyAI"

    def StrEnemyAI(self):
        return "StarbaseAI"


class CardStarBaseDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Cardassian
        ShipDef.__init__(self, abbrev, species, dict)

    def StrFriendlyAI(self):
        return "StarbaseFriendlyAI"

    def StrEnemyAI(self):
        return "StarbaseAI"


class FedShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Federation
        ShipDef.__init__(self, abbrev, species, dict)

    def GetAttackModule(self):
        return "FedAttack"


class GalaxyDef(FedShipDef):
    def __init__(self, abbrev, species, dict):
        FedShipDef.__init__(self, abbrev, species, dict)

    def StrFriendlyDestroyed(self):
        return "QBFriendlyGalaxyDestroyed"

    def StrEnemyDestroyed(self):
        return "QBEnemyGalaxyDestroyed"


class SovereignDef(FedShipDef):
    def __init__(self, abbrev, species, dict):
        FedShipDef.__init__(self, abbrev, species, dict)

    def StrFriendlyDestroyed(self):
        return "QBFriendlySovereignDestroyed"

    def StrEnemyDestroyed(self):
        return "QBEnemySovereignDestroyed"

    def GetBridge(self):
        return "SovereignBridge"


class CardShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Cardassian
        ShipDef.__init__(self, abbrev, species, dict)


class RomulanShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Romulan
        ShipDef.__init__(self, abbrev, species, dict)


class KlingonShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Klingon
        ShipDef.__init__(self, abbrev, species, dict)


class KessokShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Kessok
        ShipDef.__init__(self, abbrev, species, dict)


class FerengiShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Ferengi
        ShipDef.__init__(self, abbrev, species, dict)


class DominionShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Dominion
        ShipDef.__init__(self, abbrev, species, dict)


class BorgShipDef(ShipDef):
    def __init__(self, abbrev, species, dict):
        dict["faction"] = Borg
        ShipDef.__init__(self, abbrev, species, dict)


#########################################################
# Sound-related definitions


class SoundDef(MutatorElementDef):
    def __init__(self, file, name, volume=1.0, dict=None):
        self.fileName = file
        self.name = name
        self.volume = volume
        self.num = soundList.Register(self, name)

        newDict = {"modes": [MutatorDef.StockSounds]}
        if not dict:
            dict = {}
        dict.update(newDict)

        MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        toMode.sounds[self.name] = self
        toMode.elements.append(self)


class ListenerDef:
    def __init__(self, funcs):
        debug(__name__ + ", __init__")
        self.funcs = funcs

    def __call__(self, pObject, pEvent):
        debug(__name__ + ", __call__")
        for i in self.funcs:
            i(pObject, pEvent)


class MaskListenerDef:
    def __init__(self, funcs):
        debug(__name__ + ", __init__")
        self.funcs = funcs

    def __call__(self, pObject, pEvent):
        debug(__name__ + ", __call__")
        pShip = App.ShipClass_Cast(pEvent.GetDestination())
        pTorp = App.Torpedo_Cast(pEvent.GetSource())
        pAttacker = App.ShipClass_Cast(pEvent.GetFiringObject())

        iAttackerMask = 0

        iShipMask = sList[pShip.GetName()]._pMask
        iTorpMask = pTorp.GetModuleName()
        if pAttacker:
            iAttackerMask = sList[pAttacker.GetName()]._pMask

        for i in self.funcs:
            if i.destMask and not iShipMask & i.destMask:
                continue
            if i.sourceMask and not iTorpMask & i.sourceMask:
                continue
            if i.fireMask and not iAttackerMask & i.fireMask:
                continue

            i(pObject, pEvent)


propertyList = Registry()


class PropertyDef:
    def __init__(self, name, triggers, dict={}):
        debug(__name__ + ", __init__")
        self.name = name
        self.triggers = triggers
        self.mask = long(1 << propertyList.Register(self, name))

    def Add(self, target):
        debug(__name__ + ", Add")
        if not target.__dict__.has_key("_pList"):
            target._pList = [self]
            target._pMask = self.mask
        else:
            target._pList.append(self)
            target._pMask = target._pMask | self.mask

    def Remove(self, target):
        debug(__name__ + ", Remove")
        target._pList.remove(self)
        target._pMask = target._pMask ^ self.mask


class RedirectMutatorDef(MutatorDef):
    def __init__(self, name=None):
        MutatorDef.__init__(self, name)

        self.folders = {
            "ship": ["ships."],
            "hp": ["ships.Hardpoints."],
        }

    def __call__(self, type, key):
        if self.folders.has_key(type):
            for i in self.folders[type]:
                try:
                    # print 'importing', type, i + key
                    mod = __import__(i + key)
                    # print mod
                    if mod is not None:
                        return mod
                except ImportError:
                    pass

        return None

    def Add(self, type, folder):
        if self.folders.has_key(type):
            self.folders[type].insert(0, folder)
        else:
            self.folders[type] = [folder]

    def Remove(self, type, folder):
        try:
            self.folders[type].remove(folder)
        except:
            pass


FolderManager = RedirectMutatorDef()



##########################################################
# The cat's out of the bag on this one already, as TriggerDefs have found
# their way into NanoFX.  They are an event listener encapsulated into a
# contained MutatorElement object, able to be created and shut down easily.
##########################################################

class TriggerDef(MutatorElementDef):
    def __init__(self, name, eventKey, dict={}):
        debug(__name__ + ", __init__")
        self.eventKey = eventKey
        self.count = 0
        key = name + str(eventKey)
        FoundationTriggers.__dict__[name + str(eventKey)] = self
        Foundation.MutatorElementDef.__init__(self, name, dict)

    def AddToMutator(self, toMode):
        debug(__name__ + ", AddToMutator")
        toMode.overrides.append(self)
        toMode.elements.append(self)

    def __call__(self, pObject, pEvent):
        # print pEvent.GetEventType(), pEvent.GetRefCount()
        debug(__name__ + ", __call__")
        pObject.CallNextHandler(pEvent)

    def ImmediateActivate(self):
        pass

    def ImmediateDeactivate(self):
        pass

    def Activate(self):
        import MissionLib
        debug(__name__ + ", Activate")
        debug(__name__ + ", Activate " + str(self.eventKey))
        debug(__name__ + ", Activate " + str(self.name + str(self.eventKey)))
        if not self.count:
            pGame = App.Game_GetCurrentGame()
            App.g_kEventManager.AddBroadcastPythonFuncHandler(self.eventKey, MissionLib.GetEpisode(), "FoundationTriggers." + self.name + str(self.eventKey))
        self.count = self.count + 1

    def Deactivate(self, force=0):  # Here is where we have a fix for the previous implementation
        if self.count:
            debug(__name__ + ", Deactivate")
            self.count = self.count - 1
            if force or not self.count:
                # print 'Shutting down listener for', self.name
                pGame = App.Game_GetCurrentGame()
                App.g_kEventManager.RemoveBroadcastHandler(self.eventKey, pGame, "FoundationTriggers." + self.name + str(self.eventKey))


Foundation.TriggerDef = TriggerDef

Foundation.TriggerDef.ET_FND_CREATE_SHIP = App.UtopiaModule_GetNextEventType()
Foundation.TriggerDef.ET_FND_CREATE_PLAYER_SHIP = App.UtopiaModule_GetNextEventType()


##########################################################
# This is a TriggerDef meant to only be active when needed.
# It is currently BROKEN, but when it is fixed, TimerDef and
# EventQueue will subclass from it instead of TriggerDef.
##########################################################
class DemandTriggerDef(TriggerDef):
    ##########################################################
    # The Start and Stop methods reimplement what was the domain of
    # TriggerDef's Activate and Deactivate, making a distinction
    # between what is available and what is automatically active.
    def Start(self):
        debug(__name__ + ", Start")
        TriggerDef.Activate(self)

    def Stop(self, force=0):
        debug(__name__ + ", Stop")
        TriggerDef.Deactivate(self, force)

    ##########################################################
    # MutatorElement functions.  These are overridden to prevent
    # automatic activation.
    def Activate(self):
        debug(__name__ + ", Activate")
        pass

    def Deactivate(self, soft=0):
        debug(__name__ + ", Deactivate")
        self.Stop(1)


##########################################################
# Here, we get into timers, which by their nature ought to be
# active only when needed, and be as efficient as possible in
# their implementation.
##########################################################
class TimerDef(DemandTriggerDef):
    def __init__(self, name, eventKey, tInterval, tDuration, dict={}):
        debug(__name__ + ", __init__")
        self.eventKey = eventKey
        self.count = 0
        self.idTimer = None
        self.tInterval = tInterval
        self.tDuration = tDuration
        key = name + str(eventKey)
        FoundationTriggers.__dict__[name + str(eventKey)] = self
        Foundation.MutatorElementDef.__init__(self, name, dict)

    def __call__(self, pObject, pEvent):
        debug(__name__ + ", __call__")
        pass

    def Start(self):
        # print 'Start:  self.__dict__', self.__dict__

        debug(__name__ + ", Start")
        if self.count == 0:
            # print 'Making a timer', self.__dict__

            sFunc = "FoundationTriggers." + self.name + str(self.eventKey)
            pTimer = MissionLib.CreateTimer(self.eventKey, sFunc, App.g_kUtopiaModule.GetGameTime(), self.tInterval, self.tDuration)
            self.idTimer = pTimer.GetObjID()

        # print 'Start:  self.__dict__', self.__dict__

        self.count = self.count + 1

    def Stop(self, force=0):
        debug(__name__ + ", Stop")
        if self.count:
            self.count = self.count - 1
            if (force or self.count == 0) and self.idTimer:
                # print 'Shutting down listener for', self.name
                App.g_kTimerManager.DeleteTimer(self.idTimer)
                self.idTimer = None
                self.count = 0
            DemandTriggerDef.Stop(self, force)

    def Activate(self):
        debug(__name__ + ", Activate")
        pass

    def Deactivate(self):
        debug(__name__ + ", Deactivate")
        self.Stop(1)


class EventQueueDef(TimerDef):
    def __init__(self, name, eventKey, tInterval, tDuration, dict={}):
        debug(__name__ + ", __init__")
        TimerDef.__init__(self, name, eventKey, tInterval, tDuration, dict={})
        self.dEvents = {}
        self.empty = 0

    def __call__(self, pObject, pEvent):
        # now = int(App.g_kUtopiaModule.GetGameTime())
        debug(__name__ + ", __call__")
        now = int(App.g_kUtopiaModule.GetGameTime() * 10) / 10.0

        # print now

        # Modify this part to include sub second times
        lMoments = self.dEvents.keys()
        lMoments.sort()

        if len(lMoments) > 0 and lMoments[0] <= now:
            while len(lMoments) > 0 and lMoments[0] <= now:
                iMoment = lMoments.pop(0)
                for i in self.dEvents[iMoment]:
                    next = i(iMoment)
                    if next:
                        i._when = next
                        self.Queue(i)
                    else:
                        i.Cancel(1)
                del self.dEvents[iMoment]
            self.empty = 0

        elif len(self.dEvents.keys()) == 0:
            self.empty = self.empty + 1

        if self.empty == 5:  # We've been empty for five pulses, let's stop now.
            self.empty = 0
            self.Stop()

    def Queue(self, oEvent):
        debug(__name__ + ", Queue")
        oEvent._queue = self
        when = int((App.g_kUtopiaModule.GetGameTime() + oEvent._when) * 10) / 10.0
        oEvent._when = when
        # print 'Queuing', oEvent, when

        try:
            self.dEvents[when].append(oEvent)
        except KeyError:
            self.dEvents[when] = [oEvent]

        if not self.idTimer:
            self.Start()

    def CancelQueued(self, oEvent=None):
        debug(__name__ + ", CancelQueued")
        if oEvent:
            if self.dEvents.has_key(oEvent._when):
                self.dEvents[oEvent._when].remove(oEvent)
        else:
            self.dEvents = {}
            self.Stop(1)



#########################################################
# System-related definitions


class FolderDef(OverrideDef):
    def __init__(self, type, folder, dict={}):
        OverrideDef.__init__(self, type + folder + "Folder", None, None, dict)
        self.type = type
        self.folder = folder

    def Activate(self):
        f = Foundation.FolderManager
        f.Add(self.type, self.folder)

    def Deactivate(self):
        Foundation.FolderManager.Remove(self.type, self.folder)


FolderDef("ship", "ships.", { 'modes': [ Foundation.MutatorDef.StockShips ] })
FolderDef("hp", "ships.Hardpoints.", { 'modes': [ Foundation.MutatorDef.StockShips ] })


# import nt
# Check to make sure a file is there.  Returns 0/1 for false/true.
def VerifyFile(file):
    return 1

    try:
        import file
    except ImportError:
        return 0
    return 1


def LoadToOther(shipFile, name, species, shipPrefix):
    menuGroup = "New Ships"
    replaces = None

    if shipList._keyList.has_key(shipFile):
        replaces = shipList[shipFile]
    elif shipList._keyList.has_key(name):
        replaces = shipList[name]

    if not replaces:
        thisShip = ShipDef(shipFile, species, {"name": name, "shipPrefix": shipPrefix})
        thisShip.RegisterQBShipMenu(menuGroup)
        thisShip.RegisterQBPlayerShipMenu(menuGroup)


# Reserved scripts\Plugins\*.py files we don't want to load
reservedShips = {"__init__": None, "example": None}


# Based off of Banbury's GetShipList() snippet. -Dasher
def LoadExtraShips(dir="scripts\\Custom\\Ships", hpdir="scripts\\Custom\\Ships\\Hardpoints", dReservedShips=reservedShips):
    import nt
    import string

    list = nt.listdir(dir)
    list.sort()

    shipDotPrefix = string.join(string.split(dir, "\\")[1:], ".") + "."
    hpDotPrefix = string.join(string.split(hpdir, "\\")[1:], ".") + "."

    for ship in list:
        s = string.split(ship, ".")
        if len(s) <= 1:
            continue
        # Indexing by -1 lets us be sure we're grabbing the extension. -Dasher42
        extension = s[-1]
        shipFile = string.join(s[:-1], ".")

        # We don't want to accidentally load the wrong ship.
        if (extension == "pyc" or extension == "py") and not dReservedShips.has_key(string.lower(shipFile)):
            if bTesting:
                pModule = __import__(shipDotPrefix + shipFile)
                if hasattr(pModule, "GetShipStats"):
                    stats = pModule.GetShipStats()
                    LoadToOther(shipFile, stats["Name"], stats["Species"], shipDotPrefix)
            else:
                try:
                    pModule = __import__(shipDotPrefix + shipFile)
                    if hasattr(pModule, "GetShipStats"):
                        stats = pModule.GetShipStats()
                        LoadToOther(shipFile, stats["Name"], stats["Species"], shipDotPrefix)
                except:
                    continue


#########################################################
# Based off of Banbury's GetShipList() snippet.
# Parameters:
# 	dir:  A path to the subfolder of Bridge Commander to look for .py or .pyc files to autoload
# 	dExcludePlugins:  A dictionary whose keys are the filenames, less extensions, to avoid loading.
# Effects:  Imports all .py and .pyc files found in the folder that are not named in dExcludePlugins.
# Returns:  None


def LoadExtraPlugins(dir="scripts\\Custom\\Autoload", dExcludePlugins=_g_dExcludePlugins):
    import nt
    import string

    list = nt.listdir(dir)
    list.sort()

    dotPrefix = string.join(string.split(dir, "\\")[1:], ".") + "."
    bTesting = 1

    for plugin in list:
        s = string.split(plugin, ".")
        if len(s) <= 1:
            continue
        # Indexing by -1 lets us be sure we're grabbing the extension. -Dasher42
        extension = s[-1]
        fileName = string.join(s[:-1], ".")

        # We don't want to accidentally load the wrong ship.
        if (extension == "pyc" or extension == "py"):
            if dExcludePlugins.has_key(fileName):
                debug(__name__ + ": Ignoring outdated plugin" + fileName)
                continue
            if bTesting:
                pModule = __import__(dotPrefix + fileName)
            else:
                try:
                    pModule = __import__(dotPrefix + fileName)
                except:
                    pass


#########################################################
# Loads the Foundation Config, with updates for explicitly deactivated mutators.
#########################################################
def LoadConfig():
    global mutatorList

    try:
        pModule = __import__("Custom.FoundationConfig")
    except:
        pModule = Dummy()
            
    if not pModule.__dict__.has_key('lActiveMutators'):
        pModule.lActiveMutators = []
    # 2023: we are now assuming all mutators active unless otherwise specified
    if not pModule.__dict__.has_key('lDeactivatedMutators'):
        pModule.lDeactivatedMutators = []

    for i in mutatorList._keyList.values():
        if pModule.lDeactivatedMutators.count(i.name) != 0:
            i.Disable()
        else:
            i.Enable()


#########################################################
# Saves Foundation Config, with updates for explicitly deactivated mutators.
#########################################################
def SaveConfig():
    global mutatorList
    import nt

    try:
        pModule = __import__("Custom.FoundationConfig")
    except:
        pModule = Dummy()
        
    pModule.lActiveMutators = []
    pModule.lDeactivatedMutators = []

    for i in mutatorList._keyList.values():
        if i.IsEnabled():
            pModule.lActiveMutators.append(i.name)
        else:
            pModule.lDeactivatedMutators.append(i.name)

    lOut = ["lActiveMutators = ["]
    for i in pModule.lActiveMutators:
        lOut.append('    "%s",' % i)
    lOut.append("]")

    lOut.append("lDeactivatedMutators = [")
    for i in pModule.lDeactivatedMutators:
        lOut.append('    "%s",' % i)
    lOut.append("]")

    file = nt.open("scripts\\Custom\\FoundationConfig.py", nt.O_WRONLY | nt.O_TRUNC | nt.O_CREAT)
    for i in lOut:
        nt.write(file, i + "\n")
    nt.close(file)


def ClearPYCs(dir):
    files = nt.listdir(dir)

    for f in files:
        if f[0] != "_" and f[-4:] == ".pyc":
            nt.unlink(dir + "\\" + f)


###############################################################################
## Get File Names with extension from path sFolderPath
## Based on snippets contributed by Banbury, thank you!
###############################################################################
def GetFileNames(sFolderPath, extension):
    import string

    sFileList = nt.listdir(sFolderPath)

    retList = []

    for i in sFileList:
        s = string.split(string.lower(i), ".")
        ext = s[-1]

        if extension == ext:
            retList.append(i)

    retList.sort()
    return retList


def IsDir(sFolder):
    return (nt.stat(sFolder)[0] & 0170000) == 0040000


###############################################################################
## Get Folder Names which match expression from path sFolderPath
## Based on snippets contributed by Banbury, thank you!
###############################################################################
def GetFolderNames(sFolderPath, matching=None):
    lsFiles = nt.listdir(sFolderPath)

    retList = []

    for i in lsFiles:
        if i == ".git":
            continue
        if not (nt.stat(sFolderPath + '//' + i)[0] & 0170000) == 0040000:
            continue
        if matching and string.find(string.lower(i), matching) == -1:
            continue
        retList.append(i)

    retList.sort()
    return retList


def GetShipScript(pPlayer):
    import string

    l = string.split(pPlayer.GetScript(), ".")
    return l[-1]
