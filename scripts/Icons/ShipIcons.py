# ShipIcons.py
#
# Load Ship Icons for interface.
#
#

import App
import Foundation
import Registry

shipIconNames = {}
shipIconNums = {}
topSpecies = 0


class ShipIconDef:
    def __init__(self, name, dict={"x": 128, "y": 128}):
        global topSpecies, shipIcons
        self.name = name
        self.__dict__.update(dict)

        if not self.__dict__.has_key("file"):
            self.file = "Data/Icons/Ships/" + name + ".tga"

        if self.__dict__.has_key("species"):
            if self.species > topSpecies:
                topSpecies = self.species
        else:
            self.species = topSpecies + 1
            topSpecies = self.species

        shipIconNames[name] = self
        shipIconNums[self.species] = self


# Function to load LCARS icon group
def LoadShipIcons(ShipIcons=None):
    if ShipIcons is None:
        ShipIcons = App.g_kIconManager.CreateIconGroup("ShipIcons")
        # Add LCARS icon group to IconManager
        App.g_kIconManager.AddIconGroup(ShipIcons)

    # Glass for when no ship is selected
    TextureHandle = ShipIcons.LoadIconTexture("Data/Icons/Bridge/Background/ScreenBlock.tga")
    ShipIcons.SetIconLocation(App.SPECIES_UNKNOWN, TextureHandle, 0, 0, 8, 8)

    ShipIconDef("Galaxy", {"species": App.SPECIES_GALAXY})
    ShipIconDef("Sovereign", {"species": App.SPECIES_SOVEREIGN})
    ShipIconDef("Akira", {"species": App.SPECIES_AKIRA})
    ShipIconDef("Ambassador", {"species": App.SPECIES_AMBASSADOR})
    ShipIconDef("Nebula", {"species": App.SPECIES_NEBULA})
    ShipIconDef("FedShuttle", {"species": App.SPECIES_SHUTTLE})
    ShipIconDef("Transport", {"species": App.SPECIES_TRANSPORT})
    ShipIconDef("Freighter", {"species": App.SPECIES_FREIGHTER})
    ShipIconDef("Galor", {"species": App.SPECIES_GALOR})
    ShipIconDef("Keldon", {"species": App.SPECIES_KELDON})
    ShipIconDef("CardFreighter", {"species": App.SPECIES_CARDFREIGHTER})
    ShipIconDef("Hybrid", {"species": App.SPECIES_CARDHYBRID})
    ShipIconDef("Warbird", {"species": App.SPECIES_WARBIRD})
    ShipIconDef("BirdOfPrey", {"species": App.SPECIES_BIRD_OF_PREY})
    ShipIconDef("Vorcha", {"species": App.SPECIES_VORCHA})
    ShipIconDef("KessokHeavy", {"species": App.SPECIES_KESSOK_HEAVY})
    ShipIconDef("KessokLight", {"species": App.SPECIES_KESSOK_LIGHT})
    ShipIconDef("KessokMine", {"species": App.SPECIES_KESSOKMINE})
    ShipIconDef("Marauder", {"species": App.SPECIES_MARAUDER})
    ShipIconDef("FedStarbase", {"species": App.SPECIES_FED_STARBASE})
    ShipIconDef("FedOutpost", {"species": App.SPECIES_FED_OUTPOST})
    ShipIconDef("CardStarbase", {"species": App.SPECIES_CARD_STARBASE})
    ShipIconDef("CardOutpost", {"species": App.SPECIES_CARD_OUTPOST})
    ShipIconDef("CardStation", {"species": App.SPECIES_CARD_STATION})
    ShipIconDef("DryDock", {"species": App.SPECIES_DRYDOCK})
    ShipIconDef("SpaceFacility", {"species": App.SPECIES_SPACE_FACILITY})
    ShipIconDef("CommArray", {"species": App.SPECIES_COMMARRAY})
    ShipIconDef("CommLight", {"species": App.SPECIES_COMMLIGHT})
    ShipIconDef("Probe", {"species": App.SPECIES_PROBE})
    ShipIconDef("ProbeType2", {"species": App.SPECIES_PROBETYPE2})
    ShipIconDef("Asteroid", {"species": App.SPECIES_ASTEROID})
    ShipIconDef("Sunbuster", {"species": App.SPECIES_SUNBUSTER})
    ShipIconDef("LifeBoat", {"species": App.SPECIES_ESCAPEPOD})

    global topSpecies
    topSpecies = topSpecies + 100

    for shipDef in Foundation.shipList._keyList.values():
        if shipIconNames.has_key(shipDef.iconName):
            iconDef = shipIconNames[shipDef.iconName]
        else:
            iconDef = ShipIconDef(shipDef.iconName)
        shipDef.species = iconDef.species

    for i in shipIconNums.values():
        # print i.file, i.species, ' : ',
        TextureHandle = ShipIcons.LoadIconTexture(i.file)
        ShipIcons.SetIconLocation(i.species, TextureHandle, 0, 0, 128, 128)
