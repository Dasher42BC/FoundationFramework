# Foundation Framework for Bridge Commander

# This project is defunct.

The widespread violation of this software's license has made the sound maintenance of its ecosystem impossible.  This software has from the beginning been distributed under the terms of the LGPL license, v2.1 being current at the time of its writing.  Any inclusion of any of this project's files while omitting the readme, the license information or reference to it, or all source code - included or available - necessary for a complete build is violating the license, as well as disrupting the conditions needed for coders to correctly integrate and debug diverse work.  Without this, or literacy in why LGPL software is *not* freeware, this software is getting misused in ways that impact the entire ecosystem.

Auto-loading third-party Python plugins, while being expected functionality, has aslo proven to be this project's undoing.  Giving full privilege to all code and patches is not a model that can produce reliable code.  Projects like the Foundation can either:

* Make it a walled garden, restricting third-party modding, or
* Rely on savvy users to restrict its automatic loading, or
* Ensure that hotfixes are retired and real fixes are merged, rather than sticking around for decades and becoming explicit dependencies.  

There is no substitute for code review, and it takes non-trivial skill on the part of the modpack authors to ensure quality builds.  Please respect their work.  Any addition of third-party code, re-addition of Autoloads, or usage of code not compliant with the LGPL or Totally Games licenses is completely unsupported and discouraged by this project.  This software is as-is, and any risks or bugs are taken by those who make, distribute, or use them.

---

This is the Foundation Framework for Bridge Commander, the plug-in manager, library, and toolkit that jumpstarted the game's modding scene in March 2002, and has been its integration layer. It is a forward-compatible, flexible, extensible core to allow modular additions to Bridge Commander's Python layer, to allow content from many creators to seamlessly play together compatibly.  These can be beginner-friendly and content-specific ways to add ships, sounds, and media, or self-contained and reversible patching and injection methods for savvy Python coders.

It is based on an open source, "stone soup" approach. As the rights to Star Trek and Bridge Commander are clearly reserved and in the hands of respected parties, this shared framework designed and licensed for open collaboration of fans and volunteer content creators.

The Foundation is:

- A forward-looking, object-oriented flexible core framework for game assets. The Foundation overwrites standard Bridge Commander scripts where necessary so you don't have to, and defines ways for well-written mods from different authors to co-exist without conflict.
- A means to automatically load new plugins and updates, and manage updates so new content supercede the old.
- Function libraries, class libraries, and toolkits which allow for reliably added and modded content. Anything the game's Python layer can do, the Foundation offers several approaches adding to or replacing the game's content with new mods. If needed, they can even be activated and de-activated in-game if packaged as mutators.

The plugin types range from content-specific, stable, and novice-friendly to powerful experts-only tools for programmers:

- Ships with a high degree of customization, special characteristics, technologies, and even animations.
- Star systems, some vast compared to those included with the original.
- Sound/visual effects.
- Bridges and their effects.
- Custom game settings.
- Folder overlays for optional, additional music or other specialized games assets.
- Event-driven signal/slot code events, by packaging Bridge Commander's own frameworks in an extensible way.
- Overrides – A special Foundation concept, these are a kind of reversible code injection. They allow you to reversibly, controllably replace an object or module inside the Python interpreter with another without having to overwrite any of the game's .py/.pyc files.
- Mutators – Another special Foundation concept; it contains any number of the above mods within itself and allows the (de)activation of its contents from a new section of the game configure screen.

While the Foundation cannot guarantee that third-party code using it will behave well, and all Bridge Commander Python code has security and anti-cheat restrictions, the frameworkk provides well-tested code to mod developers that will let them focus on their unique features without conflict with other work.

# HISTORY

The original Foundation Plugin System was written by Dasher42.

Its first prototype, "Dynamic Tables", was released February 23, 2002, just days after the original game's release date.  The Foundation became an official plug-in framework in March 2002 when Totally Games released the Bridge Commander SDK, and code integration layer by May 2002.  This made it the de-facto basis for all non-trivial mods to Bridge Commander, because it uses an object-oriented core and a forward-compatible design philosophy that allows plugins to make deep changes to its function.

Literally decades later, the framework is still in service, and is now being actively developed to allow modern software development methods on this old, yet surprisingly flexible game. While many amazing mods have been created based on this framework, there remains a great deal of potential.

# ROADMAP

Soon to come in Foundation 2023:

- A consolidated, clean, maintainable core codebase integrated from the many updates by the original author and many contributors, once again unified and maintainable.
- A new framework for updates, "Versions", ensuring that the latest version of Foundation and other key components are always retained even when people use outdated installers.
- A new official launcher and cross-platform mod manager, explicitly supporting Windows and Linux+Wine installations, git-driven snapshots and updates, and more.
- New pre-flight checks for mods and modpacks, allowing test-driven development without tedious playtesting, and thus more stable mod releases.
- Simultaneous support for stable single-player campaign and multiplayer modes, while allowing the moddable sandbox people expect of Bridge Commander and Foundation.

All content featuring revisions of Totally Games content falls under the terms found in SDKLicense.txt. All additional code is LGPL: work based on it must include its own source code and abide by the Totally Games license as well.

---

# INSTALLATION

To install this, simply copy the files into the Bridge Commander installation - or a second copy of it, which I do _strongly_ recommend. This can be done with a simple copy of the Bridge Commander folder. If you mess up, just rename your suspect scripts folder and copy the scripts folder from your original BC installation in.

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

This README.md file, the SDKLicense.txt, and LICENSE file shall be included in any distribution, and credit given in any work which incorporates, modifies, extends, or alters the running of this package's files.

The Foundation's own files are provided under the terms of the Lesser GNU Public License 2.1.  This helpful guide will help you to understand it, and how it complements the licensing of the stock and SDK files for Bridge Commander: https://www.tldrlegal.com/license/gnu-lesser-general-public-license-v2-1-lgpl-2-1

Any inclusion of the non-Totally Games source code contained herein may only be distributed with complete source code of the Foundation and all .py files of the codebase built with it, included per the terms of the Lesser GNU Public License (LGPL) as of v2.1 and the terms of Totally Games' SDKLicense.txt. Any redistributions which include these Python assets, imports them, revises them, or builds on them must include their own Python source, including a .py file for every included .pyc, sufficient to have a complete Python layer when added to Totally Games assets and Foundation libraries. This ensures the maintainability and fairness of the Foundation ecosystem to all participants.

A documented link to the Bridge Commander SDK 1.1 such as https://www.moddb.com/games/star-trek-bridge-commander/downloads/star-trek-bridge-commander-sdk-v11 for any unmodified stock .py files is a good way to uphold both the Foundation's LGPL license and the Totally Games/Activision license simultaneously.  Modified files must be included, always.

Binary and non-Python assets (i.e. NIFs, TGAs, WAVs, MP3s) included with any redistribution of the Foundation Framework shall be construed exclusively as "New Game Materials" per the Totally Games SDK license. As they are not code, they are not contiguous with the LGPL Python code contained herein.

All rights are reserved by the author(s).

All trademarks, rights, prohibitions against unauthorized monetization expressed in Totally Games' licenses and CBS/Paramount's policies towards the Star Trek franchise apply.  Any solicitation of funds for the distribution of Foundation or Foundation-based content is explicitly forbidden.

Modders, coders, and content creators are encouraged to use the Foundation Framework with respect for its open source license and nature and the participatory benefits it brings them. If you distribute changes to it or with it, make them open per the Totally Games and LGPL licenses and give the following people credit:


### Credits

Original author and lead maintainer

* Dasher42, the original author of the Foundation Framework, who developed the core Foundation libraries with forward-compatibility in mind, and actively co-developed mods and standards needed for them with the community,

The first-generation Foundation Framework contributors whose powerhouse work made Foundation better and made its early mod scene so exciting.

* Laurelin, who discovered significant locations in the Totally Games code where the Foundation replaced mod-resistant code with flexible data structures, and without whom the release of prototypes within days of the game's original release and the first official Foundation within days of the SDK release would not have been possible so soon,
* Banbury, whose snippets contributed to the Foundation's easy of use with copied-in files,
* Sleight42, whose launcher framework proved how small ships and add-on ship functionality can work,
* Nano, whose feedback while designing the first GUI tools to help users publish content from Foundation was valuable, and whose NanoFX pushed the limits of what was considered possible,
* Apollo, who helped inspire the Foundation's maturation into a full-blown code framework, capable of updating even itself through plug-ins
* MLeoDaalder who did much to update and maintain Foundation extensions over the years, becoming the acting lead for years, and contributed invaluable debugging and utility code,
* Sneaker98, whose MVAM framework is a modding of triumph, both for separable ship sections and for animations,
* Defiant, whose work starting the famed Kobayashi Maru modpack led to snippets that are valuable to such large-scale integrations

The innovative and persistent Bridge Commander community who kept pieces of modding history that could easily have been lost forever, and inspired a return to active, freshly-inspired Foundation development in 2023:

* Blackrook32, whose work on detailed subsystem management helps push the sense of what's possible and helps drive Foundation's core support,
* JimmyB76, Bridge Commander's biggest cheerleader, who held the community's common square,
* Mario, who took on next-generation tools development and inspired innovative new ways to mock Appc for testing purposes, and suggested useful WrapperDefs which greatly expand our options for debugging without disturbing regular users, and whose work on DS9FX drove ideas of what Foundation could better support,
* Tethys, who brought internet multiplayer back into service, and who helped multiplayer-ready stable mplayer/ script directories work in parallel with the usual moddable scripts/,
* VonFrank42, whose tested minimalism helped pinpoint the best practices yet discovered, and how they should integrate to revive Single Player and Multiplayer in full.

Thanks also go out to those who kept Bridge Commander and Foundation exciting, whoever was at the helm of Foundation, including:

Pneumonic81, Raven Night, Mark, Lost Jedi, 

That's all, have fun!
