#  Vanilla Logs

Mod to enable the TS4 vanilla logs on startup. Based on https://modthesims.info/d/606667/sims-log-enabler.html by scumbumbo.

### Cheat commands
While running these commands are available (to be entered in the cheat console):
* logs.enable .... Enable logging, the log is always appended. Restarting TS4 clears the log.
* logs.disable ... Disable logging and close all open log files.
* logs.flush ..... Write buffered logs to disk.
* logs.level n ... Change the log level to n=[0..5] (FATAL, ERROR, WARN, INFO, DEBUG or ALWAYS)

All console changes are temporarily. They are not persisted in the configuration file.

### Configuration file
On startup, it will create a configuration file with these options:
* ENABLE_LOGGING: bool = True ... Write the vanilla logs when starting TS4
* BUFFERING: int = 1 ............ Buffer and write one line. <0:default; 0:unbuffered; 1:line; 2:os_default; >2:byte_size. https://docs.python.org/2/library/functions.html#open
* FORCE_FLUSH: bool = True ...... False: Don't flush the file after every write (if buffering is set)
* LOG_LEVEL: int = 5 ........... `[0..5]` (FATAL, ERROR, WARN, INFO, DEBUG or ALWAYS)
* GROUPS: set = {} .............. {}=All. Specify individual case-sensitive groups to log, e.g. {'Zone', 'Utils'}

The file is based on the Python dict() datatype. Use 'True' or 'False' as this is not JSON.


# Addendum

## Game compatibility
This mod has been tested with `The Sims 4` 1.108.329, S4CL 3.5, TS4Lib 0.3.20 (2024-05).
It is expected to be compatible with many upcoming releases of TS4, S4CL and TS4Lib.

## Dependencies
Download the ZIP file, not the sources.
* [This Mod](../../releases/latest)
* [TS4-Library](https://github.com/Oops19/TS4-Library/releases/latest)
* [S4CL](https://github.com/ColonolNutty/Sims4CommunityLibrary/releases/latest)
* [The Sims 4](https://www.ea.com/games/the-sims/the-sims-4)

If not installed download and install TS4 and these mods.
All are available for free.

## Installation
* Locate the localized `The Sims 4` folder which contains the `Mods` folder.
* Extract the ZIP file into this `The Sims 4` folder.
* It will create the directories/files `Mods/_o19_/$mod_name.ts4script`, `Mods/_o19_/$mod_name.package`, `mod_data/$mod_name/*` and/or `mod_documentation/$mod_name/*`
* `mod_logs/$mod_name.txt` will be created as soon as data is logged.

### Manual Installation
If you don't want to extract the ZIP file into `The Sims 4` folder you might want to read this. 
* The files in `ZIP-File/mod_data` are usually required and should be extracted to `The Sims 4/mod_data`.
* The files in `ZIP-File/mod_documentation` are for you to read it. They are not needed to use this mod.
* The `Mods/_o19_/*.ts4script` files can be stored in a random folder within `Mods` or directly in `Mods`. I highly recommend to store it in `_o19_` so you know who created it.

## Usage Tracking / Privacy
This mod does not send any data to tracking servers. The code is open source, not obfuscated, and can be reviewed.

Some log entries in the log file ('mod_logs' folder) may contain the local username, especially if files are not found (WARN, ERROR).

## External Links
[Sources](https://github.com/Oops19/)
[Support](https://discord.gg/d8X9aQ3jbm)
[Donations](https://www.patreon.com/o19)

## Copyright and License
* © 2024 [Oops19](https://github.com/Oops19)
* License for '.package' files: [Electronic Arts TOS for UGC](https://tos.ea.com/legalapp/WEBTERMS/US/en/PC/)  
* License for other media unless specified differently: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) unless the Electronic Arts TOS for UGC overrides it.
This allows you to use this mod and re-use the code even if you don't own The Sims 4.
Have fun extending this mod and/or integrating it with your mods.

Oops19 / o19 is not endorsed by or affiliated with Electronic Arts or its licensors.
Game content and materials copyright Electronic Arts Inc. and its licensors. 
Trademarks are the property of their respective owners.

### TOS
* Please don't put it behind a paywall.
* Please don't create mods which break with every TS4 update.
* For simple tuning modifications use [Patch-XML](https://github.com/Oops19/TS4-PatchXML) 
* or [LiveXML](https://github.com/Oops19/TS4-LiveXML).
* To check the XML structure of custom tunings use [VanillaLogs](https://github.com/Oops19/TS4-VanillaLogs).
