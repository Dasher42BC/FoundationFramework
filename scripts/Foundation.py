# Foundation 03282002 module for Bridge Commander
# Written March 15, 2002 by Dasher42, all rights reserved.


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
soundList = Registry()
bridgeList = Registry()

pGameType = None
pCurrentMode = None

bTesting = 1

version = '20020525'


#########################################################
# Mode-related definitions

# The MutatorDef is a definition of a game mode, a collection of references to the active
# ships, projectiles, and other plugins that loaded into a game.
class MutatorDef:

	def __init__(self, name = None):
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
		self.bBase = 0				# One one base MutatorDef can be activated at a time.
		self.bEnabled = 0			#
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
		return 'GalaxyBridge'


# A gameplay mode for a stock BC setup
MutatorDef.Stock = MutatorDef('Stock Systems')
MutatorDef.Stock.bBase = 1

MutatorDef.StockSounds = MutatorDef(None)

# A gameplay mode for a stock BC setup
MutatorDef.StockShips = MutatorDef('Stock Ships')

# A generic add-on mode
MutatorDef.QuickBattle = MutatorDef('Extra Ships and Mods')
MutatorDef.QuickBattle.shipMenu = qbShipMenu
MutatorDef.QuickBattle.playerShipMenu = qbPlayerShipMenu


#########################################################
# A function to generate in-game structures using MutatorDefs
# Parameters:
# 	baseMode:  A MutatorDef that serves as the base for all other active modes to append to or revise
# 	dArgs:  A dictionary for forward argument compatibility
# Effects:  None
# Returns:  A MutatorDef set up starting with baseMode and with all other active non-base modes included
def BuildGameMode(baseMode = None, dArgs = {}):
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
		modes = [ MutatorDef.QuickBattle ]
		if dict and dict.has_key('modes'):
			modes = dict['modes']
		for mode in modes:
			self.AddToMutator(mode)

	def CheckForErrors(self):
		return None

	def AddToMutator(self, toMode):
		# print self.name, 'added to', toMode.name
		toMode.elements.append(self)


#########################################################
# Override-related definitions
class OverrideDef(MutatorElementDef):
	def __init__(self, name, sItem, sNewItem, dict = {}):
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
		pPreModule = __import__(string.join(pre[:-1], '.'))
		pPostModule = __import__(string.join(post[:-1], '.'))

		self.original = pPreModule.__dict__[pre[-1]]
		pPreModule.__dict__[pre[-1]] = pPostModule.__dict__[post[-1]]
		# print 'Activating %s overriding %s' % (self.sNewItem, self.sItem)

	def _SwapOutModules(self, pre, post):
		import string
		pPreModule = __import__(string.join(pre[:-1], '.'))

		pPreModule.__dict__[pre[-1]] = self.original
		self.original = None
		# print 'Deactivating %s restoring %s' % (self.sNewItem, self.sItem)

	def Activate(self):
		import string
		global bTesting

		if self.original:	return

		pre = string.split(self.sItem, '.')
		post = string.split(self.sNewItem, '.')

		if bTesting:
			self._SwapInModules(pre, post)
		else:
			try:
				self._SwapInModules(pre, post)
			except:
				pass

	def Deactivate(self):
		import string

		if not self.original:	return

		pre = string.split(self.sItem, '.')
		post = string.split(self.sNewItem, '.')

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
# Race-related definitions

class RaceDef:

	def __init__(self, name, abbrev, dict = {}):
		self.name = name
		self.num = raceList.Register(self, name)
		self.abbrev = abbrev
		self.ships = []
		self.weapons = []


#########################################################
# TGL-related definitions

class TGLDef(MutatorElementDef):

	def __init__(self, name, filePathName, dict = {}):
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

	def __init__(self, name, maximum, minimum = 0, dict = {}):
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

	def __init__(self, name, bridgeString, dict = {}):
		self.bridgeString = bridgeString
		self.num = bridgeList.Register(self, name)

		# This is a touch risky but I foresee no problem - Dasher42
		bridgeList._keyList[bridgeString] = self

		self.locations = None
		if dict.has_key('locations'):
			self.locations = dict['locations']
		MutatorElementDef.__init__(self, name, dict)

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
					raise SyntaxError, 'Foundation.BridgeDef.SetLocation: ' + locationName + ' ' + evalStr
			return 1
		except:
			pass
		return None


#########################################################
# Ship-related definitions
# These are intended to be base classes for objects instantiated in

class ShipDef(MutatorElementDef):

	def __init__(self, abbrev, species, dict = {}):
		self.abbrev = abbrev
		self.species = species
		self.race = None
		self.desc = ''
		self.hasTGLName = 0
		self.hasTGLDesc = 0
		self.menuGroup = None
		self.playerMenuGroup = None
		self.engineSound = None
		self.bridge = None
		self.era = 0

		self.__dict__.update(dict)
		if not self.__dict__.has_key('iconName'):	self.iconName = abbrev
		if not self.__dict__.has_key('name'):		self.name = abbrev
		if not self.__dict__.has_key('shipFile'):	self.shipFile = abbrev
		if not self.__dict__.has_key('shipPrefix'):	self.shipPrefix = 'ships.'

		if dict.has_key('race'):
			self.race = dict['race']
			self.race.ships.append(self)

		self.sAttackModule = None

		self.friendlyDetails = [self.abbrev, self.name, self.StrFriendlyDestroyed(), self.StrFriendlyAI(), 'Friendly']
		self.enemyDetails = [self.abbrev, self.name, self.StrEnemyDestroyed(), self.StrEnemyAI(), 'Enemy']

		self.num = shipList.Register(self, abbrev)
		if shipList._keyList.has_key(self.name):
			self.friendlyDetails[2] = shipList[self.name].friendlyDetails[2]
			self.enemyDetails[2] = shipList[self.name].enemyDetails[2]

		# This is quite deliberately commented out, as
		# MutatorElementDef.__init__(self, self.name, dict)

	def AddToMutator(self, toMode):
		toMode.elements.append(self)
		if self.menuGroup:
			self.RegisterQBShipMenu(self.menuGroup, toMode)
		if self.playerMenuGroup:
			self.RegisterQBPlayerShipMenu(self.playerMenuGroup, toMode)

	def GetIconNum(self):							return self.species
	def GetSpecies(self):							return self.species
	def GetAttackModule(self):						return 'NonFedAttack'
	def GetRace(self):								return self.race
	def StrFriendlyDestroyed(self):					return 'QBFriendlyGenericShipDestroyed'
	def StrEnemyDestroyed(self):					return 'QBEnemyGenericShipDestroyed'
	def StrFriendlyAI(self):						return 'QuickBattleFriendlyAI'
	def StrEnemyAI(self):							return 'QuickBattleAI'

	def MenuGroup(self):
		if self.menuGroup is not None:
			return self.menuGroup
		return 'Other Ships'

	def GetBridge(self):
		if self.bridge is not None:
			return self.bridge
		return 'GalaxyBridge'

	def EngineSound(self):
		if self.engineSound is not None:
			return self.engineSound
		return '%s Engines' % (self.race.name)

	def EngineSound(self):							return '%s Engines' % (self.race.name)


	def RegisterQBShipMenu(self, group = None, mode = MutatorDef.QuickBattle):
		if not self.menuGroup:
			self.menuGroup = group
		if not shipList._keyList.has_key(self.abbrev):
			# If this failed, we know that there was an ImportError exception caught in ShipDef.__init__ -Dasher
			return
		if not group:	group = self.MenuGroup()
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
			mode.shipMenu[group] = ([ self ], { self.name: self } )
		if mode.elements.count(self) == 0:
			mode.elements.append(self)

	def RegisterQBPlayerShipMenu(self, group = None, mode = MutatorDef.QuickBattle):
		if not self.playerMenuGroup:
			self.playerMenuGroup = group
		if not shipList._keyList.has_key(self.abbrev):
			# If this failed, we know that there was an ImportError exception caught in ShipDef.__init__ -Dasher
			return
		if not group:	group = self.MenuGroup()
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
			mode.playerShipMenu[group] = ([ self ], { self.name: self } )
		if mode.elements.count(self) == 0:
			mode.elements.append(self)



# Really, these are little more than namespaces for containing other things.
Federation = RaceDef('Federation', 'Fed')
Cardassian = RaceDef('Cardassian', 'Card')
Klingon = RaceDef('Klingon', 'Klingon')
Romulan = RaceDef('Romulan', 'Romulan')
Ferengi = RaceDef('Ferengi', 'Ferengi')
Kessok = RaceDef('Kessok', 'Kessok')
Dominion = RaceDef('Dominion', 'Dom')
Breen = RaceDef('Breen', 'Breen')
Borg = RaceDef('Borg', 'Borg')


class StarBaseDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Federation
		ShipDef.__init__(self, abbrev, species, dict)
	def StrFriendlyAI(self):
		return 'StarbaseFriendlyAI'
	def StrEnemyAI(self):
		return 'StarbaseAI'



class CardStarBaseDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Cardassian
		ShipDef.__init__(self, abbrev, species, dict)
	def StrFriendlyAI(self):
		return 'StarbaseFriendlyAI'
	def StrEnemyAI(self):
		return 'StarbaseAI'


class FedShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Federation
		ShipDef.__init__(self, abbrev, species, dict)
	def GetAttackModule(self):
		return 'FedAttack'


class GalaxyDef(FedShipDef):
	def __init__(self, abbrev, species, dict):
		FedShipDef.__init__(self, abbrev, species, dict)
	def StrFriendlyDestroyed(self):
		return 'QBFriendlyGalaxyDestroyed'
	def StrEnemyDestroyed(self):
		return 'QBEnemyGalaxyDestroyed'
	def GetBridge(self):
		return 'GalaxyBridge'

	def GetBridge(self):
		if self.bridge is not None:
			return self.bridge
		return 'GalaxyBridge'

class SovereignDef(FedShipDef):
	def __init__(self, abbrev, species, dict):
		FedShipDef.__init__(self, abbrev, species, dict)
	def StrFriendlyDestroyed(self):
		return 'QBFriendlySovereignDestroyed'
	def StrEnemyDestroyed(self):
		return 'QBEnemySovereignDestroyed'
	def GetBridge(self):
		return 'SovereignBridge'


class CardShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Cardassian
		ShipDef.__init__(self, abbrev, species, dict)


class RomulanShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Romulan
		ShipDef.__init__(self, abbrev, species, dict)


class KlingonShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Klingon
		ShipDef.__init__(self, abbrev, species, dict)


class KessokShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Kessok
		ShipDef.__init__(self, abbrev, species, dict)


class FerengiShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Ferengi
		ShipDef.__init__(self, abbrev, species, dict)


class DominionShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Dominion
		ShipDef.__init__(self, abbrev, species, dict)


class BorgShipDef(ShipDef):
	def __init__(self, abbrev, species, dict):
		dict['race'] = Borg
		ShipDef.__init__(self, abbrev, species, dict)


#########################################################
# Sound-related definitions

class SoundDef(MutatorElementDef):
	def __init__(self, file, name, volume = 1.0, dict = None):
		self.fileName = file
		self.name = name
		self.volume = volume
		self.num = soundList.Register(self, name)

		newDict = { 'modes': [ MutatorDef.StockSounds ] }
		if not dict:
			dict = {}
		dict.update(newDict)

		MutatorElementDef.__init__(self, name, dict)

	def AddToMutator(self, toMode):
		toMode.sounds[self.name] = self
		toMode.elements.append(self)


######################################################################################
# Used for testing in small modules.  Comment out import App, instantiate this as App.
class DummyApp:
	def __init__(self):
		self.seqIssued = {}
		self.counter = 0
	def __getattr__(self, name):
		if self.seqIssued.has_key(name):	return self.seqIssued[name]
		self.seqIssued[name] = self.counter
		self.counter = self.counter + 1
		return self.counter - 1

# import os

# def LoadMods(dir):
# 	files = os.listdir(dir)
# 	files.sort()

# 	for f in files:
# 		if f[0] != '_' and f[-3:] == '.py':
# 			mod = 'DynamicLoad.' + f[0:-3]
# 			print "Importing ", mod
# 			__import__(mod)

# LoadMods(os.path.join(os.getcwd(), 'Plugins'))

# import nt
# Check to make sure a file is there.  Returns 0/1 for false/true.
def VerifyFile(file):

	return 1

	try:					import file
	except ImportError:		return 0
	return 1


def LoadToOther(shipFile, name, species, shipPrefix):
	menuGroup = 'New Ships'
	replaces = None

	if shipList._keyList.has_key(shipFile):
		replaces = shipList[shipFile]
	elif shipList._keyList.has_key(name):
		replaces = shipList[name]

	if not replaces:
		thisShip = ShipDef(shipFile, species, { 'name': name, 'shipPrefix': shipPrefix } )
		thisShip.RegisterQBShipMenu(menuGroup)
		thisShip.RegisterQBPlayerShipMenu(menuGroup)


# Reserved scripts\Plugins\*.py files we don't want to load
reservedShips = {
	'__init__': None,
	'example': None
}


# Based off of Banbury's GetShipList() snippet. -Dasher
def LoadExtraShips(dir = 'scripts\\Custom\\Ships', hpdir = 'scripts\\Custom\\Ships\\Hardpoints', dReservedShips = reservedShips):
	import nt
	import string

	list = nt.listdir(dir)
	list.sort()

	shipDotPrefix = string.join(string.split(dir, '\\')[1:], '.') + '.'
	hpDotPrefix = string.join(string.split(hpdir, '\\')[1:], '.') + '.'

	for ship in list:
		s = string.split(ship, '.')
		if len(s) <= 1:
			continue
		# Indexing by -1 lets us be sure we're grabbing the extension. -Dasher42
		extension = s[-1]
		shipFile = string.join(s[:-1], '.')

		# We don't want to accidentally load the wrong ship.
		if (extension == 'pyc' or extension == 'py') and not dReservedShips.has_key(string.lower(shipFile)):
			if bTesting:
				pModule = __import__(shipDotPrefix + shipFile)
				if hasattr(pModule, 'GetShipStats'):
					stats = pModule.GetShipStats()
					LoadToOther(shipFile, stats['Name'], stats['Species'], shipDotPrefix)
			else:
				try:
					pModule = __import__(shipDotPrefix + shipFile)
					if hasattr(pModule, 'GetShipStats'):
						stats = pModule.GetShipStats()
						LoadToOther(shipFile, stats['Name'], stats['Species'], shipDotPrefix)
				except:
					continue



#########################################################
# Based off of Banbury's GetShipList() snippet.
# Parameters:
# 	dir:  A path to the subfolder of Bridge Commander to look for .py or .pyc files to autoload
# 	dExcludePlugins:  A dictionary whose keys are the filenames, less extensions, to avoid loading.
# Effects:  Imports all .py and .pyc files found in the folder that are not named in dExcludePlugins.
# Returns:  None

def LoadExtraPlugins(dir = 'scripts\\Custom\\Autoload', dExcludePlugins = {}):
	import nt
	import string

	list = nt.listdir(dir)
	list.sort()

	dotPrefix = string.join(string.split(dir, '\\')[1:], '.') + '.'
	bTesting = 1

	for plugin in list:
		s = string.split(plugin, '.')
		if len(s) <= 1:
			continue
		# Indexing by -1 lets us be sure we're grabbing the extension. -Dasher42
		extension = s[-1]
		fileName = string.join(s[:-1], '.')

		# We don't want to accidentally load the wrong ship.
		if (extension == 'pyc' or extension == 'py') and not dExcludePlugins.has_key(fileName):
			if bTesting:
				pModule = __import__(dotPrefix + fileName)
			else:
				try:
					pModule = __import__(dotPrefix + fileName)
				except:
					pass


def LoadConfig():
	global mutatorList
	pModule = __import__('Custom.FoundationConfig')

	for i in mutatorList._keyList.values():
		if pModule.lActiveMutators.count(i.name) != 0:
			i.Enable()
		else:
			i.Disable()


def SaveConfig():
	import nt
	global mutatorList

	pModule = __import__('Custom.FoundationConfig')
	pModule.lActiveMutators = []

	sOut = [ 'lActiveMutators = [' ]
	for i in mutatorList._keyList.values():
		if i.IsEnabled():
			pModule.lActiveMutators.append(i.name)
			sOut.append('\t"""%s""",' % (i.name))
	sOut.append(']')

	# print sOut

	file = nt.open('scripts\\Custom\\FoundationConfig.py', nt.O_WRONLY|nt.O_TRUNC|nt.O_CREAT)
	for i in sOut:
		nt.write(file, i + '\n')
	nt.close(file)


