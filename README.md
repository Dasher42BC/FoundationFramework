# FoundationPluginsForBC

This is the Foundation Framework for Bridge Commander, the Python framework that jumpstarted the game's modding scene. It is, by design, a forward-compatible, flexible, extensible core to allow modular Python script additions to Bridge Commander, to allow content from many creators to seamlessly play together.

The Foundation is:

- A forward-looking, object-oriented flexible core framework for game assets. The Foundation overwrites standard Bridge Commander scripts where necessary so you don't have to, and defines ways for well-written mods from different authors to co-exist without conflict.
- A means to automatically load plugins and updates, and a way for new content to supercede the old.
- Function libraries and object-oriented classes which allow for reliably added and modded content. Anything the game's Python layer can do, the Foundation offers several approaches adding to or replacing the game's content with new mods. If needed, they can even be activated and de-activated in-game if packaged as mutators.

The Foundation Framework has remained the shared framework behind nearly all non-trivial Bridge Commander mods since 2002 because it allows both beginner-friendly and content-specific ways to add ships, sounds, and media, and because for more technically skilled coders, it offers a core library that allows standard ways to add Python code capable of anything the game engine allows.

The content supported includes but not limited to:

- Ships with a high degree of customization, special characteristics, technologies, and even animations.
- Star systems, some vast compared to those included with the original.
- Sound/visual Effects.
- Bridges and custom game settings.
- Folders for addition music or other specialized games assets .
- Event-driven signal/slot code events, by packaging Bridge Commander's own frameworks in an extensible way.
- Overrides – A special Foundation concept, these are a kind of reversible code injection. They allow you to reversibly, controllably replace an object or module inside the Python interpreter with another without having to overwrite any of the game's .py/.pyc files.
- Mutators – Another special Foundation concept; it contains any number of the above mods within itself and allows the (de)activation of its contents from a new section of the game configure screen.

While the Foundation cannot guarantee that third-party code using it will behave well, and all Bridge Commander Python code has security and anti-cheat restrictions, the frameowrk provides options to mod developers to use well-tested code that will let them focus on their unique features without conflict with other work.

It is based on an open source, "stone soup" approach. As the rights to Star Trek and Bridge Commander are clearly reserved and in the hands of respected parties, this shared framework designed and licensed for open collaboration of fans and volunteer content creators.

# HISTORY

The original Foundation Plugin System was written by Dasher42.

It was based on a "Dynamic Tables" prototype released February 23, 2002, within days of the original game's release date, and became an official modding framework in March 2002 when Totally Games released the Bridge Commander SDK. The Foundation became the de-facto basis for all non-trivial mods to Bridge Commander, because it uses an object-oriented core and a forward-compatible design philosophy that allows plugins to make deep changes to its function.

Literally decades later, the framework is still in service, and is now being actively developed to allow modern software development methods on this old, yet surprisingly flexible game. While many amazing mods have been created based on this framework, there remains a great deal of potential.

# ROADMAP

Soon to come in Foundation 2023:

- A new official launcher and cross-platform mod manager, explicitly supporting Windows and Linux+Wine installations, git-driven snapshots and updates, and more.
- New pre-flight checks for mods and modpacks, allowing test-driven development without tedious playtesting, and thus more stable mod releases.
- A new versioned updates framework, ensuring that the latest version of key components are always retained even when people use outdated installers.
- Simultaneous support for stable single-player campaign and multiplayer modes, while allowing highly moddable local quickbattle and additional campaigns.

All content featuring revisions of Totally Games content falls under the terms found in SDKLicense.txt. All additional code is LGPL: work based on it must include its own source code and abide by the Totally Games license as well.

---

# INSTALLATION

To install this, simply copy the files into the Bridge Commander installation - or a second copy of it, which I do _strongly_ recommend. This can be done with a simple copy of the Bridge Commander folder. If you mess up, just rename your suspect scripts folder and copy the scripts folder from your original BC installation in!

This package can be used with single player and multiplayer game modes, but
can readily be used to

As a result, you should have:

```
scripts\bcdebug.py
scripts\Custom\FoundationConfig.py
scripts\Custom\Autoload\000-Fixes20030402-FoundationRedirect.py
scripts\Custom\Autoload\000-Utilities-GetFileNames-20030402.py
scripts\Custom\Autoload\000-Utilities-FoundationMusic-20030410.py
scripts\Custom\Autoload\000-Fixes20030221.py
scripts\Custom\Autoload\000-Fixes20030305-FoundationTriggers.py
scripts\Custom\Autoload\000-Fixes*ShipSubList*.py
scripts\Custom\Autoload\__init__.py
scripts\Custom\Autoload\FixTorps.py
scripts\Custom\Ships\__init__.py
scripts\Custom\__init__.py
scripts\Icons\ShipIcons.py
scripts\StaticDefs.py
scripts\QuickBattle\QuickBattle.py
scripts\Tactical\Interface\WeaponsDisplay.py
scripts\Tactical\Interface\ShieldsDisplay.py
scripts\Foundation.py
scripts\FoundationMenu.py
scripts\LoadBridge.py
scripts\LoadTacticalSounds.py
scripts\Fixes20030217.py
scripts\FoundationTriggers.py
scripts\MainMenu\mainmenu.py
scripts\loadspacehelper.py
scripts\Registry.py
```

...copied to wherever the new copy of Bridge Commander is located. To help ensure that the installation is completed successfully, .pyc versions of the above .py files will be provided as well.

---

# USAGE

## Installing a mod

Installing a properly-packaged mod into a Foundation-enabled Bridge Commander installation is a simple matter of copying it in, subfolders and all.

If the mod in question is an older-style mod that has a plugin file in scripts\Plugins, simply move that file to scripts\Custom\Autoload.

A “properly-packaged” mod will not overwrite pre-existing .py or .pyc files. Mods that overwrite your existing .py or .pyc files when first installed may well cause problems with your installation. If you're not sure that a mod is properly packaged, unzip it separately and copy it over top of your BC/Foundation installation, but refuse to overwrite files when prompted.

Some mods, usually those that are not a simple ship or sound, need to be activated from the game's configuration panel. When in the game you will want to go to the Configure -> Mutators section and enable them.

The simplest mods to package with the Foundation are ships, sound effects, and systems, and they will be demonstrated here. See the wiki for details on more complex plugin types for code, special technologies, and mutators.

---

## Packaging a ship

Got a ship you want to make plugin-ready? Here is a step-by-step guide to making a ship compliant with Foundation. When done you will have something that you can distribute and that the end user can integrate by simply copying it in.

Export the models. You should have the following:

The model and textures:

```
data\Models\Ships\NewShip\
data\Models\Ships\NewShip\NewShip.NIF (optionally NewShipMed.NIF and NewShipLow.NIF too)
data\Models\Ships\NewShip\High\(textures as .TGA's)
data\Models\Ships\NewShip\Medium\(textures as .TGA's)
data\Models\Ships\NewShip\Low\(textures as .TGA's)
```

The ship definition and hardpoints:

```
scripts\Ships\NewShip.py
scripts\Ships\Hardpoints\newship.py
```

Scripts\Ships\NewShip.py must have a properly set up GetShipStats() section for the ship to work. Some of these parameters are case- sensitive; be careful!

```
def GetShipStats():

KShipStats = {


"FilenameHigh": "data/Models/Ships/NewShip/NewShip.nif",
"FilenameMed": "data/Models/Ships/NewShip/NewShipMed.nif",
"FilenameLow": "data/Models/Ships/NewShip/NewShipLow.nif",
"Name": "NewShip", # <- These are
"HardpointFile": "newship", # <- important!
"Species": Multiplayer.SpeciesToShip.VORCHA

}
return kShipStats
```

You must make a scripts\Custom\Ships\NewShip.py file. The simplest way to
do this is to copy the Example.py file in that folder to NewShip.py and edit
it by replacing “Example” with the name of your ship. More editing may be
required; read the file's comments for details. It is important that it
refer to the name of the scripts\Ships\NewShip.py file, and it is case-
sensitive.

Got an icon? A 128x128 .TGA of your ship? Put it in data\Icons\Ships. If
its name is different from that of the ship, the Example.py file will show
you how to use it.

That's it!

---

## Packaging a sound effect

You may include statements to load sound effects ship plugin files or indeed
any file you load along with the ship. You can even use it to make drop-in
replacements for sound effects without replacing the stock sounds. You need
only include a line like the following:

```
Foundation.SoundDef("sfx/Weapons/Klingon Torp.wav", "Klingon Plasma
Torpedo", 1.0)
```

The first argument in double quotes specifies the file, the second gives you
a name to refer to this sound by from inside the ship's hardpoints, and the
third is a volume adjuster, 1.0 being the normal level.

---

## Packaging a system

Adding a new system is relatively easy. You need only make a .py file in
scripts\Custom\Autoload named after the system you're adding. Its contents
should look like this:

```
import Foundation

Foundation.SystemDef('New System', 3)
```

This will set things up for a new system with three planets. Systems
without planets can get by with 0 planets; systems like Vesuvi which have
missing inner planets get defined in this manner:

```
import Foundation

Foundation.SystemDef('New System', 5, 2)
```

This will create a system with the inner two planets missing.

---

## Packaging a TGL

This is fairly simple. Look at the following example:

```
Foundation.TGLDef('FTB Ships', 'data/TGL/FTBShips.TGL')
```

The first argument is a simple name for the TGL, the second is the
path/filename to be used. See QuickBattle.py if you want to see how this is
being loaded/unloaded.

---

## Packaging an Override

This is experts-only! However it does allow the intermediate to
advanced Bridge Commander modder with an understanding of Python a way to replace parts of the game's code without overwriting it. While it may not always work with some setups of GUI
events, cases where an object or module is all that need be replaced should
be doable. This is a bleeding-edge feature that requires some knowledge of
Python to know how to package the replacements properly. However, getting
the Foundation to play its part is simple, as seen in this example from the
author's Intercept AI plugin:

```
import Foundation

Foundation.OverrideDef('Intercept_Dasher', 'AI.PlainAI.Intercept.Intercept',
'AI.PlainAI.Intercept_Dasher.Intercept_Dasher' } )
```

The override is actually activated by calling the override's Activate()
function, i.e. interceptoverride.Activate(), and deactivated by – you
guessed it – Deactivate(), which puts the overriden Python object back in
place.

---

## Packaging a Mutator

This procedure is not for the novice either! Any SoundDef, ShipDef, SystemDef, or OverrideDef can have, as a final argument to its constructor, a dictionary as an argument, which is surprisingly enough named “dict”. Here's a version of the example of an Override that packages two Overrides inside a single Mutator.

```
import Foundation

mode = Foundation.MutatorDef('Acceleration Intercept')

Foundation.OverrideDef.Intercept_Dasher = Foundation.OverrideDef(
'Intercept_Dasher',
'AI.PlainAI.Intercept.Intercept',
'AI.PlainAI.Intercept_Dasher.Intercept_Dasher',
dict = { 'modes': [ mode ] })

Foundation.OverrideDef.Orbit_Dasher = Foundation.OverrideDef(
'Orbit_Dasher',
'AI.Player.OrbitPlanet.CreateAI',
'AI.Player.OrbitPlanet_Dasher.CreateAI',
dict = { 'modes': [ mode ] } )
```

Note that mutators are loaded in the order that they are defined inside the Python interpreter. If you want detailed control of what mutator takes precedence over another, I recommend the use of Nanobyte's Mod Packager, version 3.0 or higher. Currently, the Foundation's version of QuickBattle builds a temporary mutator that copies all active mutators into a single object to provide a “master control”. See QuickBattle.py for details on the useage of Foundation.BuildGameMode().

It is good form to call a Mutator's Activate() method when initializing a game that uses it and the Deactivate() method when the game is being terminated. This essentially calls the related methods of all contained overrides.

---

# TROUBLESHOOTING

Did you install this mod and then see Bridge Commander stop working? Walk through the following steps:

Is this about the '???' buttons? They still work. See the Bridge Commander SDK's documentation about TGL files to get them displaying correctly.

Did you unpack this into your copy of the Bridge Commander directory? If so, this file you're reading should appear there, above \data, \scripts, \Screen Shots, everything.

Did you have any mods already installed that could be conflicting? Try renaming your scripts folder and copying in the scripts folder from under the Setup folder on your Bridge Commander CD, and then installing a fresh copy of the Foundation over top.

Did you install a plugin and then see the game stop working? Try moving any files related to it in scripts\Custom\Autoload to a backup location outside of the Bridge Commander install.

Did you install another mod after this one that overwrote Foundation? Reinstall the Foundation. All mods that depend on Foundation should add their extensions using Foundation classes without overwriting the Foundation itself, and any mods that do not adhere to this practice need to be updated to play well with others.

Failing all this, append " -TestMode" to your Bridge Commander icon's target field, hit the back apostrophe in-game when it starts to have trouble, and press enter. Tell the experts what happened.

---

# NOTE TO DEVELOPERS

Goals and proper usage: This plugin project is meant to expand beyond ships into an easy "glue layer" for Bridge Commander mods, providing a simple installation process and an easy way to activate or deactivate mods. As such, please do not distribute modified versions of the existing .PY and .PYC files in this mod indiscriminately, as you could break compatibility with other mods that people _will_ try to install and future versions of the Foundation. Until a better installation framework is available, the recommended way to distribute the Foundation with your mod is to include it in a nested ZIP file where the user has the option to install it or not. You should be able to do this without requiring any files to be overwritten.

MenuBuilders – the other feature: Contained within scripts\FoundationMenu are classes that will let you easily create menus of Foundation-loaded ships and systems. They are the ShipMenuBuilderDef and SystemMenuBuilderDef, and they may be loaded as follows:

```
systemMenu = Foundation.SystemMenuBuilderDef(tglDatabase)
```

The tglDatabase parameter is a table usually loaded through a pMission.SetDatabase() call. See the included QuickBattle.py – if you're going to try this, I assume you understand Python!

---

# LEGALESE AND DISCLAIMER:

This software is provided as-is, and the author makes no guarantee of the performance of this software, its security, compatibility, safety, or usefulness, and cannot be held liable for any consequence of this software's use.

Permission is given to modify or distribute the included files as a component of Bridge Commander under the terms of the Totally Games SDK license (included as SDKLicense.txt) with the following provisions:

This README.md file, the SDKLicense.txt, and LICENSE file shall be included in any distribution, and credit given in any work which incorporates this package's files,

Any inclusion of the non-Totally Games source code contained herein may only be distributed with source code included per the terms of the Lesser GNU Public License (LGPL) as of v2.1 and the terms of Totally Games' SDKLicense.txt . Any redistributions which include these Python assets, imports them, revises them, or builds on them must include their own Python source, including a .py file for every included .pyc, sufficient to have a complete Python layer when added to Totally Games assets and Foundation libraries. This ensures the maintainability and fairness of the Foundation ecosystem to all participants.

Binary and non-Python assets (i.e. NIFs, TGAs, WAVs, MP3s) included with any redistribution of the Foundation Framework shall be construed as New Game Materials per the Totally Games SDK license. As they are not code, they are not contiguous with the LGPL Python code contained herein.

All rights are reserved by the author(s).

All trademarks, rights, prohibitions against unauthorized monetization expressed in Totally Games' licenses and CBS/Paramount's policies towards the Star Trek franchise apply.

Modders, coders, and content creators are encouraged to use the Foundation Framework with respect for its open source license and nature and the participatory benefits it brings them. If you distribute changes to it or with it, make them open per the Totally Games and LGPL licenses and give the following people credit:

Dasher42, the original author of the Foundation Framework,

Laurelin, who discovered significant portions of the Totally Games code of interest to these modifications,

MLeoDaalder who did much to update and maintain Foundation extensions over the years,

And also Sleight42, Sneaker98, and Banbury whose feedback and snippets contributed to the Foundation and its popular add-ons.

Special thanks also go out to Nanobyte and DigitalFiend whose work is making the Foundation more accessible for the end users.

That's all, have fun!
