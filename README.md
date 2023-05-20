# BCFoundationPlugins
The Foundation Plugin System for Bridge Commander, the Python framework that jumpstarted the BC modding scene

---

# HISTORY

Originally released March 2002, inheriting from the "Dynamic Tables"
prototype released February 23, 2002.  This is an update of a formal release
made as of March 20, 2002, rapid changes expected soon.

Written by Dasher42.  All content featuring revisions of Totally Games
content falls under the terms found in SDKLicense.txt.  All additional code
is LGPL: work based on it must include its own source code and abide by the
Totally Games license as well.

---

# WHY IT EXISTS

By default, Bridge Commander allows a great deal of moddability, but adding
new ships requires users to download the SDK and edit the .py files.  This
is a tedious process, and it is unfeasible to distribute, say, an edited
QuickBattle.py for every ship out there if you want multiple mods on a
single installation.

This is a system to allow easy integration of mods into Bridge Commander. 
It replaces the static indexes of Bridge Commander with dynamic structures,
thus providing the means for ship modders to easily distribute their ships
without overwriting any of the end user's files.

Specifically, the Foundation currently allows the following types of mods:

Ships
Systems
Sounds
Bridges
Folders for the players' additional music
Overrides of scripts without overwriting scripts
Event-driven signal/slot code additions


Overrides – A special Foundation concept, this allows you to replace an
object or module inside the Python interpreter with another without having
to overwrite any of the game's .py/.pyc files!  An example is the intercept
or planet-orbiting AI; this can now be replaced without overwriting stock
files.

Mutators – Another special Foundation concept; it contains any number of the
above mods within itself and allows the (de)activation of its contents from
a new section of the game configure screen.

---

# INSTALLATION

To install this, simply copy the files into the Bridge Commander installation - or a second copy of it, which I do *strongly* recommend. This can be done with a simple copy of the Bridge Commander folder. If you mess up, just rename your suspect scripts folder and copy the scripts folder from your original BC installation in!

This package can be used with single player and multiplayer game modes, but
can readily be used to 

As a result, you should have:


`{(Bridge Commander Folder)\scripts\bcdebug.py
(Bridge Commander Folder)\scripts\Custom\FoundationConfig.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Fixes20030402-FoundationRedirect.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Utilities-GetFileNames-20030402.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Utilities-FoundationMusic-20030410.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Fixes20030221.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Fixes20030305-FoundationTriggers.py
(Bridge Commander Folder)\scripts\Custom\Autoload\000-Fixes*ShipSubList*.py
(Bridge Commander Folder)\scripts\Custom\Autoload\__init__.py
(Bridge Commander Folder)\scripts\Custom\Autoload\FixTorps.py
(Bridge Commander Folder)\scripts\Custom\Ships\__init__.py
(Bridge Commander Folder)\scripts\Custom\__init__.py
(Bridge Commander Folder)\scripts\Icons\ShipIcons.py
(Bridge Commander Folder)\scripts\StaticDefs.py
(Bridge Commander Folder)\scripts\QuickBattle\QuickBattle.py
(Bridge Commander Folder)\scripts\Tactical\Interface\WeaponsDisplay.py
(Bridge Commander Folder)\scripts\Tactical\Interface\ShieldsDisplay.py
(Bridge Commander Folder)\scripts\Foundation.py
(Bridge Commander Folder)\scripts\FoundationMenu.py
(Bridge Commander Folder)\scripts\LoadBridge.py
(Bridge Commander Folder)\scripts\LoadTacticalSounds.py
(Bridge Commander Folder)\scripts\Fixes20030217.py
(Bridge Commander Folder)\scripts\FoundationTriggers.py
(Bridge Commander Folder)\scripts\MainMenu\mainmenu.py
(Bridge Commander Folder)\scripts\loadspacehelper.py
(Bridge Commander Folder)\scripts\Registry.py}`



...where (Bridge Commander Folder) is wherever the new copy of Bridge Commander is located. To help ensure that the installation is completed successfully, .pyc versions of the above .py files will be provided as well.

--- 

# USAGE

Installing a mod

Installing a properly-packaged mod into a Foundation-enabled Bridge Commander installation is a simple matter of copying it in, subfolders and all.

If the mod in question is an older-style mod that has a plugin file in scripts\Plugins, simply move that file to scripts\Custom\Autoload.

A “properly-packaged” mod will not overwrite pre-existing .py or .pyc files. Mods that overwrite your existing .py or .pyc files when first installed may well cause problems with your installation. If you're not sure that a mod is properly packaged, unzip it separately and copy it over top of your BC/Foundation installation, but refuse to overwrite files when prompted.

Some mods, usually those that are not a simple ship or sound, need to be activated from the game's configuration panel. When in the game you will want to go to the Configure -> Mutators section and enable them.

Packaging a ship

Got a ship you want to make plugin-ready? Here is a step-by-step guide to making a ship compliant with Foundation. When done you will have something that you can distribute and that the end user can integrate by simply copying it in.

Export the models. You should have the following:

The model and textures:

`{data\Models\Ships\NewShip\
data\Models\Ships\NewShip\NewShip.NIF (optionally NewShipMed.NIF and NewShipLow.NIF too)
data\Models\Ships\NewShip\High\(textures as .TGA's)
data\Models\Ships\NewShip\Medium\(textures as .TGA's)
data\Models\Ships\NewShip\Low\(textures as .TGA's)}`

The ship definition and hardpoints:

{scripts\Ships\NewShip.py
scripts\Ships\Hardpoints\newship.py}

Scripts\Ships\NewShip.py must have a properly set up GetShipStats() section for the ship to work. Some of these parameters are case- sensitive; be careful!

`{def GetShipStats():

KShipStats = {


"FilenameHigh": "data/Models/Ships/NewShip/NewShip.nif",
"FilenameMed": "data/Models/Ships/NewShip/NewShipMed.nif",
"FilenameLow": "data/Models/Ships/NewShip/NewShipLow.nif",
"Name": "NewShip", # <- These are
"HardpointFile": "newship", # <- important!
"Species": Multiplayer.SpeciesToShip.VORCHA

}
return kShipStats}`

You must make a scripts\Custom\Ships\NewShip.py file.  The simplest way to
do this is to copy the Example.py file in that folder to NewShip.py and edit
it by replacing “Example” with the name of your ship.  More editing may be
required; read the file's comments for details.  It is important that it
refer to the name of the scripts\Ships\NewShip.py file, and it is case-
sensitive.

Got an icon?  A 128x128 .TGA of your ship?  Put it in data\Icons\Ships.  If
its name is different from that of the ship, the Example.py file will show
you how to use it.

That's it!

Packaging a sound effect

You may include statements to load sound effects ship plugin files or indeed
any file you load along with the ship.  You can even use it to make drop-in
replacements for sound effects without replacing the stock sounds.  You need
only include a line like the following:

`{Foundation.SoundDef("sfx/Weapons/Klingon Torp.wav", "Klingon Plasma
Torpedo", 1.0)}`

The first argument in double quotes specifies the file, the second gives you
a name to refer to this sound by from inside the ship's hardpoints, and the
third is a volume adjuster, 1.0 being the normal level.

Packaging a system

Adding a new system is relatively easy.  You need only make a .py file in
scripts\Custom\Autoload named after the system you're adding.  Its contents
should look like this:

`{import Foundation

Foundation.SystemDef('New System', 3)}`

This will set things up for a new system with three planets.  Systems
without planets can get by with 0 planets; systems like Vesuvi which have
missing inner planets get defined in this manner:

`{import Foundation

Foundation.SystemDef('New System', 5, 2)}`

This will create a system with the inner two planets missing.

Packaging a TGL

This is fairly simple.  Look at the following example:

`{Foundation.TGLDef('FTB Ships', 'data/TGL/FTBShips.TGL')}`

The first argument is a simple name for the TGL, the second is the
path/filename to be used.  See QuickBattle.py if you want to see how this is
being loaded/unloaded.

Packaging an Override

This procedure is not for the novice, but it does allow the intermediate to
advanced Bridge Commander modder a way to replace the game's code without
overwriting it.  While it may not always work with some setups of GUI
events, cases where an object or module is all that need be replaced should
be doable.  This is a bleeding-edge feature that requires some knowledge of
Python to know how to package the replacements properly.  However, getting
the Foundation to play its part is simple, as seen in this example from the
author's Intercept AI plugin:

`{import Foundation

Foundation.OverrideDef('Intercept_Dasher', 'AI.PlainAI.Intercept.Intercept',
'AI.PlainAI.Intercept_Dasher.Intercept_Dasher' } )}`

The override is actually activated by calling the override's Activate()
function, i.e.  interceptoverride.Activate(), and deactivated by – you
guessed it – Deactivate(), which puts the overriden Python object back in
place.

Packaging a Mutator

This procedure is not for the novice either!  Any SoundDef, ShipDef,
SystemDef, or OverrideDef can have, as a final argument to its constructor,
a dictionary as an argument, which is surprisingly enough named “dict”. 
Here's a version of the example of an Override that packages two Overrides
inside a single Mutator.

`{import Foundation

mode = Foundation.MutatorDef('Acceleration Intercept')}`

`{Foundation.OverrideDef.Intercept_Dasher =
Foundation.OverrideDef('Intercept_Dasher', 'AI.PlainAI.Intercept.Intercept',
'AI.PlainAI.Intercept_Dasher.Intercept_Dasher', dict = { 'modes': [ mode ] }
) Foundation.OverrideDef.Orbit_Dasher =
Foundation.OverrideDef('Orbit_Dasher', 'AI.Player.OrbitPlanet.CreateAI',
'AI.Player.OrbitPlanet_Dasher.CreateAI', dict = { 'modes': [ mode ] } )}`

Note that mutators are loaded in the order that they are defined inside the
Python interpreter.  If you want detailed control of what mutator takes
precedence over another, I recommend the use of Nanobyte's Mod Packager,
version 3.0 or higher.  Currently, the Foundation's version of QuickBattle
builds a temporary mutator that copies all active mutators into a single
object to provide a “master control”.  See QuickBattle.py for details on the
useage of Foundation.BuildGameMode().

It is good form to call a Mutator's Activate() method when initializing a
game that uses it and the Deactivate() method when the game is being
terminated.  This essentially calls the related methods of all contained
overrides.

---

# PREVIOUS CHANGES


March 31, 2002 release:

A number of new features have been added:

A ship may be added to the game without a file in the scripts\Plugins
folder.  Thanks to a snippet from Banbury which I have adapted and
incorporated, you only need the conventional file in scripts\Ships and its
related hardpoint file for the ship to appear in the "Other Ships"
QuickBattle menus.

The structure of the scripts\Plugins folder has changed;
scripts\Plugins\Custom will be used for future versions of Nanobyte's GUI
tool and use Custom.py as a direct counterpart of the old Plugins.py.  Other
plugin files can be copied into scripts\Plugins where they will be loaded
automatically.  Regular plugins cannot override Custom plugins.

By default, ships now use ASCII strings for the QuickBattle menu buttons. 
See the above instructions.  This is meant to provide an acceptable minimum
level of functionality; TGL support is encouraged!  It will help the
non-English-speaking users.

Sounds can now be incorporated via plugins!


March 20, 2002 release 2:

The format for the plugins has changed.  I didn't want to do this, but the
change that's been made is the kind that means that we won't have to do this
again.  The new format is much more flexible and forward-compatible.  It's
best to get this over and done with at this early stage.

This mod's name has changed to better suit its idiom.  "Dynamic Tables" was
rather awkward, and hey, a better name always helps my propaganda efforts. 
;)

Finally, a bug has been fixed associated with some ships being set as the
player's ship when their ships\Script\ship.py filename didn't match their
abbreviation.

---

# TROUBLESHOOTING

Did you install this mod and then see Bridge Commander stop working?  Walk
through the following steps:

Is this about the '???' buttons?  They still work.  See the Bridge Commander
SDK's documentation about TGL files.  If this is your only problem, relax. 
We're working on it.  ;)

Did you unpack this into your copy of the Bridge Commander directory?  If
so, this file you're reading should appear there, above \data, \scripts,
\Screen Shots, everything.

Did you have any mods already installed that could be conflicting?  Try
renaming your scripts folder and copying in the scripts folder from under
the Setup folder on your Bridge Commander CD, and then installing a fresh
copy of the Foundation over top.

Did you install a plugin and then see the game stop working?  Try putting #
signs in front of its import statement in \scripts\Plugins\Custom\Custom.py,
or moving the .py and .pyc files out of \scripts\Plugins.

Did it work?  Maybe an import statement is incorrect.  Double-check to be
sure; these things are case-sensitive and must match the .py file's name. 
Also, make sure you have no leading spaces; a line that reads " import
NewShip.py" is trouble!  See step 8.

If the plugin still doesn't work, it or Foundation itself could have an
error, or maybe there's a conflict of some kind.  Getting work from separate
sources to cooperate nicely on a single install isn't as simple as it
sounds.

Make sure there are no .PY files in your Bridge Commander folder that
correspond to the ones included herein.  They could be compiled to .PYCs and
break this mod.  QuickBattles.py, loadspacehelper.py, ShipIcons.py,
ShieldDisplay.py, and WeaponsDisplay.py would be obvious offenders.

Did you install another mod after this one that overwrote Foundation? 
Regrettably, all other existing QuickBattle mods are incompatible with this
one as of now.  Work will go forward to make them into plugins as well.  If
you want this mod and them, make another fresh copy of Bridge Commander or
just get your hands dirty.

Failing all this, append " -TestMode" to your Bridge Commander icon's target
field, hit the back apostrophe in-game when it starts to have trouble, and
press enter.  Tell the experts what happened.

---

# NOTE TO DEVELOPERS

Goals and proper usage: This plugin project is meant to expand beyond ships
into an easy "glue layer" for Bridge Commander mods, providing a simple
installation process and an easy way to activate or deactivate mods.  As
such, please do not distribute modified versions of the existing .PY and
.PYC files in this mod indiscriminately, as you could break compatibility
with other mods that people *will* try to install and future versions of the
Foundation.  Until a better installation framework is available, the
recommended way to distribute the Foundation with your mod is to include it
in a nested ZIP file where the user has the option to install it or not. 
You should be able to do this without requiring any files to be overwritten.

MenuBuilders – the other feature: Contained within scripts\FoundationMenu
are classes that will let you easily create menus of Foundation-loaded ships
and systems.  They are the ShipMenuBuilderDef and SystemMenuBuilderDef, and
they may be loaded as follows:

{systemMenu = Foundation.SystemMenuBuilderDef(tglDatabase)}

The tglDatabase parameter is a table usually loaded through a
pMission.SetDatabase() call.  See the included QuickBattle.py – if you're
going to try this, I assume you understand the Python script!  ;)

(the sadly necessary) 

--- 

# LEGALESE AND DISCLAIMER:

This software is provided as-is, and the author makes no guarantee of the
performance of this software, its security, compatibility, safety, or
usefulness, and cannot be held liable for any consequence of this software's
use.

Permission is given to modify or distribute the included files as a
component of Bridge Commander under the terms of the Activision SDK license
(included as SDKLicense.txt) with the following provisions:

This README.md file and the accompanying LICENSE and shall be included in
any distribution, and credit given in any work which incorporates this
package's files,

Any inclusion of the non-Activision source code contained herein may only be
distributed with source code included per the terms of the Lesser GNU Public
License (LGPL) as of v2.1, and where this does not violate the terms of the
Activision SDK license.  Any redistributions which include them, import
them, revise them, or build on them must include their own Python
source, including a .py file for every included .pyc, sufficient to have a
complete Python layer when added to Activision assets.

Binary assets included with any redistribution of the Foundation Plugin
System shall be construed as New Game Materials per the Activision SDK
license.

All rights are reserved by the author(s).

In short, use it, respect its open source nature, if you distribute changes
to it or with it, make them open and give the following people credit:

Dasher42, the original author of the Foundation Plugin System,

Laurelin, who discovered significant portions of the Totally Games code of
interest to these modifications,

MLeoDaalder who did much to update and maintain Foundation extensions over
the years,

Evan Light AKA Sleight42,

Banbury, who contributed code snippets that were adapted into this release
of the Foundation.

Special thanks also go out to Nanobyte and DigitalFiend whose work is making
the Foundation more accessible for the end users.


That's all, have fun!

