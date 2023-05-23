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
* BUFFERING: int = 1 ............ Buffer ans write one line. <0:full; 0:off, 1:line; 2:os_default; >2:byte_size. https://docs.python.org/2/library/functions.html#open
* FORCE_FLUSH: bool = True ...... False: Don't flush the file after every write (if buffering is set)
* LOG_LEVEL: int = 5 ........... `[0..5]` (FATAL, ERROR, WARN, INFO, DEBUG or ALWAYS)
* GROUPS: set = {} .............. {}=All. Specify individual case-sensitive groups to log, e.g. {'Zone', 'Utils'}

The file is based on the Python dict() datatype. Use 'True' or 'False' as this is not JSON.