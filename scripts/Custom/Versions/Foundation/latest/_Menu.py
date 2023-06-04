#########################################################
# Foundation Framework for Bridge Commander
# Written June 3, 2023 as part of Foundation 2023 update by Dasher42
# ShipListSubMenu Addition V4 by MLeoDaalder merged; thank you MLeo!
# All rights reserved under the Lesser GNU Public License v2.1
#########################################################

import App
import Foundation

ListType = type([])
StringType = type("a")
DictType = type({})


class TreeNode:
    def __init__(self, name, oShip=None, prefab=None, priority=None):
        self.name = name
        self.oShip = oShip
        self.prefab = prefab
        self.children = {}
        self.bMVAM = 0
        self.bShip = 0
        self.priority = priority


class TextButtonFactory:
    def __init__(self, tglDatabase):
        self.isTGL = 0
        self.text = None
        self.tglDatabase = tglDatabase

    def __call__(self, text):
        if self.tglDatabase.HasString(text):
            self.text = self.tglDatabase.GetString(text)
            self.isTGL = 1
            return self.text
        else:
            self.text = text
            self.isTGL = 0
            return text

    def MakeSubMenu(self):
        if self.isTGL:
            return App.STCharacterMenu_CreateW(self.text)
        elif self.text is not None:
            return App.STCharacterMenu_Create(self.text)
        else:
            return App.STCharacterMenu_Create("?!?")

    def MakeIntButton(self, eType, iSubType, uiHandler, fWidth=0.0, fHeight=0.0):
        pEvent = App.TGIntEvent_Create()
        pEvent.SetEventType(eType)
        pEvent.SetDestination(uiHandler)
        pEvent.SetInt(iSubType)

        if self.isTGL:
            if fWidth == 0.0:
                return App.STButton_CreateW(self.text, pEvent)
            return App.STRoundedButton_CreateW(self.text, pEvent, fWidth, fHeight)
        elif self.text is not None:
            if fWidth == 0.0:
                return App.STButton_Create(self.text, pEvent)
            return App.STRoundedButton_Create(self.text, pEvent, fWidth, fHeight)
        else:
            if fWidth == 0.0:
                return App.STButton_Create("?!?", pEvent)
            return App.STRoundedButton_Create("?!?", pEvent, fWidth, fHeight)

    def MakeStringButton(self, eType, sSubType, uiHandler, fWidth=0.0, fHeight=0.0):
        pEvent = App.TGStringEvent_Create()
        pEvent.SetEventType(eType)
        pEvent.SetDestination(uiHandler)
        pEvent.SetString(sSubType)

        if self.isTGL:
            return App.STButton_CreateW(self.text, pEvent)
        elif self.text is not None:
            return App.STButton_Create(self.text, pEvent)
        else:
            return App.STButton_Create("?!?", pEvent)

    def MakeYesNoButton(self, eType, sString, uiHandler, iState, fWidth=0.0, fHeight=0.0):
        pEvent = App.TGStringEvent_Create()
        pEvent.SetEventType(eType)
        pEvent.SetDestination(uiHandler)

        if self.isTGL:
            pMenuButton = App.STButton_CreateW(self.text, pEvent, fWidth, fHeight)
        elif self.text is not None:
            pMenuButton = App.STButton_Create(self.text, pEvent, fWidth, fHeight)
        else:
            pMenuButton = App.STButton_Create("?!?", pEvent, fWidth, fHeight)

        pEvent.SetString(sString)
        pEvent.SetSource(pMenuButton)

        pMenuButton.SetChoosable(1)
        pMenuButton.SetAutoChoose(1)
        if iState:
            pMenuButton.SetChosen(1)
        else:
            pMenuButton.SetChosen(0)

        return pMenuButton


class MenuBuilderDef:
    def __init__(self, tglDatabase):
        self.tglDatabase = tglDatabase
        self.textButton = TextButtonFactory(tglDatabase)

    def __call__(self, menu):
        pass


class MenuTreeNode:
    def __init__(self, name, oShip=None, prefab=None, priority=None):
        self.name = name
        self.oShip = oShip
        self.prefab = prefab
        self.children = {}
        self.bMVAM = 0
        self.bShip = 0
        self.priority = priority


class ShipMenuBuilderDef(MenuBuilderDef):
    def __init__(self, tglDatabase):
        MenuBuilderDef.__init__(self, tglDatabase)

    def __call__(self, raceShipList, menu, buttonType, uiHandler, fWidth=0.0, fHeight=0.0):
        foundShips = {}
        for race in raceShipList.keys():
            for ship in raceShipList[race][0]:
                foundShips[race] = 1
                break

        raceList = foundShips.keys()
        raceList.sort()

        oRoot = MenuTreeNode("Root", prefab=menu)
        for race in raceList:
            self.textButton(race)
            pRaceButton = self.textButton.MakeSubMenu()
            oRace = MenuTreeNode(race, prefab=pRaceButton)
            oRoot.children[race] = oRace

            shipList = raceShipList[race][1].keys()
            shipList.sort()

            for key in shipList:
                ship = raceShipList[race][1][key]
                self.textButton(ship.name)

                if ship.__dict__.get("Do not display", 0):
                    continue

                if hasattr(ship, "SubMenu") and type(ship.SubMenu) != ListType:
                    ship.SubMenu = [ship.SubMenu]
                if hasattr(ship, "SubSubMenu") and type(ship.SubSubMenu) != ListType:
                    ship.SubSubMenu = [ship.SubSubMenu]
                if not hasattr(ship, "Priority"):
                    ship.Priority = None

                oWork = oRace

                for name in ship.__dict__.get("SubMenu", []) + ship.__dict__.get("SubSubMenu", []):
                    oMenu = oWork.children.get(name + "_m", None)
                    if not oMenu:
                        oMenu = MenuTreeNode(name, prefab=App.STCharacterMenu_Create(name))
                        oWork.children[name + "_m"] = oMenu
                        if ship.Priority:
                            oMenu.priority = ship.Priority
                    oWork = oMenu
                bCreated = 0
                if HasMVAM():
                    oWork, bCreated = DoMVAMMenus(oWork, ship, buttonType, uiHandler, self, raceShipList, fWidth, fHeight)
                if not bCreated:
                    appended = ""
                    while oWork.children.has_key(ship.name + appended):
                        appended = appended + " "
                    oWork.children[ship.name + appended] = MenuTreeNode(ship.name, oShip=ship)
                    oWork.children[ship.name + appended].bShip = 1
                    if ship.Priority:
                        oWork.children[ship.name + appended].priority = ship.Priority

        BuildMenu(oRoot, self, buttonType, uiHandler, fWidth, fHeight)


class BridgeMenuBuilderDef(MenuBuilderDef):
    def __init__(self, tglDatabase):
        MenuBuilderDef.__init__(self, tglDatabase)

    def __call__(self, bridges, menu, buttonType, uiHandler):
        bridgeList = bridges._arrayList
        bridgeList.sort()

        for pBridge in bridgeList:
            i = bridges[pBridge]
            self.textButton(pBridge)
            menu.AddChild(self.textButton.MakeIntButton(buttonType, i.num, uiHandler))


class SystemMenuBuilderDef(MenuBuilderDef):
    def __init__(self, tglDatabase):
        MenuBuilderDef.__init__(self, tglDatabase)

    def BuildSubMenu(self, buttonString, minPlanets, numPlanets, buttonType, uiHandler):
        self.textButton(buttonString)
        pMenu = self.textButton.MakeSubMenu()
        for iIndex in range(minPlanets, numPlanets):
            planetString = buttonString + " " + str(iIndex + 1)
            self.textButton(planetString)
            pMenu.AddChild(self.textButton.MakeStringButton(buttonType, buttonString + str(iIndex + 1), uiHandler))

        pMenu.ForceUpdate(0)

        return pMenu

    def __call__(self, systems, menu, buttonType, uiHandler):
        systemList = systems.keys()
        systemList.sort()

        self.textButton("DeepSpace")
        menu.AddChild(self.textButton.MakeStringButton(buttonType, "DeepSpace", uiHandler))

        for sSystem in systemList:
            if sSystem == "DeepSpace":
                continue
            i = systems[sSystem]
            if i.maximum > 1:
                menu.AddChild(self.BuildSubMenu(i.name, i.minimum, i.maximum, buttonType, uiHandler))
            else:
                if i.maximum == 1:
                    self.textButton(sSystem)
                    menu.AddChild(self.textButton.MakeStringButton(buttonType, i.name + "1", uiHandler))
                else:
                    self.textButton(sSystem)
                    menu.AddChild(self.textButton.MakeStringButton(buttonType, i.name, uiHandler))


def BuildMenu(oMenu, self, buttonType, uiHandler, fWidth, fHeight, b=0):
    items = oMenu.children.items()
    items.sort()
    sortShips = {}
    newItems = {}
    for s, ship in items:
        newItems[s] = ship
        if hasattr(ship, "priority"):
            if ship.priority:
                sortShips[s] = ship.priority
            else:
                sortShips[s] = None
        else:
            sortShips[s] = None
    priorityDict = {}
    priorityShips = []
    nonPriorityShips = []
    for k, v in sortShips.items():
        if v:
            if not v in priorityDict.keys():
                priorityDict[v] = [k]
            else:
                l = priorityDict[v]
                l.append(k)
                l.sort()
        else:
            nonPriorityShips.append(k)
    nonPriorityShips.sort()
    priorityList = priorityDict.keys()
    priorityList.sort()
    if priorityList:
        for key in priorityList:
            for s in priorityDict[key]:
                priorityShips.append(s)

    merged = priorityShips + nonPriorityShips
    for item in merged:
        object = newItems[item]
        self.textButton(object.name)

        if object.bShip or (object.bMVAM and not len(object.children)):
            if not object.prefab:
                object.prefab = self.textButton.MakeIntButton(buttonType, object.oShip.num, uiHandler, fWidth, fHeight)
        else:
            if len(object.children):
                if not object.prefab:
                    object.prefab = self.textButton.MakeSubMenu()
                if object.name == "Human (Tau'ri) Ships":
                    BuildMenu(object, self, buttonType, uiHandler, fWidth, fHeight, 1)
                else:
                    BuildMenu(object, self, buttonType, uiHandler, fWidth, fHeight)

                if object.bMVAM:
                    object.prefab.SetTwoClicks()
                    pEvent = App.TGIntEvent_Create()
                    pEvent.SetEventType(buttonType)
                    pEvent.SetDestination(uiHandler)
                    pEvent.SetSource(object.prefab)
                    pEvent.SetInt(object.oShip.num)
                    object.prefab.SetActivationEvent(pEvent)

        oMenu.prefab.AddChild(object.prefab)


bHasMVAM = -1


def HasMVAM():
    global bHasMVAM
    if bHasMVAM != -1:
        return bHasMVAM
    try:
        import Custom.Autoload.Mvam
    except:
        bHasMVAM = 0
    else:
        bHasMVAM = 1
    return bHasMVAM


def DoMVAMMenus(oWork, ship, buttonType, uiHandler, self, raceShipList, fWidth, fHeight):
    if not ship.__dict__.get("bMvamMenu", 1):
        return oWork, 0

    import nt
    import string

    List = nt.listdir("scripts\\Custom\\Autoload\\Mvam\\")
    Mod = None
    for i in List:
        PosModName = string.split(i, ".")
        if len(PosModName) > 1 and PosModName[0] != "__init__":
            try:
                PosMod = __import__("Custom.Autoload.Mvam." + PosModName[0])
                if PosMod and PosMod.__dict__.has_key("MvamShips"):
                    if ship.shipFile in PosMod.MvamShips:
                        Mod = PosMod
                        break
            except:
                continue

    if not Mod:
        return oWork, 0

    shipB = None
    foundShips = {}
    for race in raceShipList.keys():
        for dummyShip in raceShipList[race][0]:
            foundShips[race] = 1
            break

    raceList = foundShips.keys()
    raceList.sort()

    for race in raceList:
        shipB = findShip(Mod.MvamShips[0], raceShipList[race][1])
        if shipB:
            break
    if not shipB:
        return oWork, 0

    if not shipB.__dict__.get("bMvamMenu", 1):
        return oWork, 0

    oTemp = oWork.children.get(shipB.name, None)
    if not oTemp:
        oTemp = TreeNode(shipB.name, oShip=shipB)
        oTemp.bMVAM = 1
        oWork.children[shipB.name] = oTemp
    oWork = oTemp
    return oWork, ship.shipFile == shipB.shipFile


def findShip(shipFile, raceShipList):
    shipList = raceShipList.keys()
    shipList.sort()
    for key in shipList:
        ship = raceShipList[key]
        if ship.shipFile == shipFile:
            return ship
