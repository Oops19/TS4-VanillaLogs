"""
Sims Log Enabler
  by Scumbumbo@MTS
  Jan 31, 2018

Console commands:
  * logs.enable [append]      Enable logging, by default files are overwritten when reopened
  * logs.disable              Disable logging and close all open log files

v2 - Feb 3, 2018
  - Added options for INCLUDE_TIMESTAMPS and INCLUDE_OWNER_INFO
  - Rewrote the code for including some information to reduce possible issues with string.format()

######################################################################

v3 - o19 modifications:
    + Rename mod to 'VanillaLogs'
    + Stripped down the config options to simplify log file creation.
    + Using a dict() based configuration file to configure the remaining options.
    + File location moved to mod_logs and mod_data
    + Write one merged log file with all information instead of n³ log files
    + Removed duplicate logging code
    + Removed most of the global variables
    + Added 'logs.flush' command to flush the logs
    + Added 'logs.level n' command to change the log level
    + Added 'GROUPS' to configuration options to log only relevant groups

Default settings:
    * ENABLE_LOGGING: bool = True  # Write the vanilla logs when starting TS4
    * BUFFERING: int = 1           # Buffer ans write one line. <0:full; 0:off, 1:line; 2:os_default; >2:byte_size. https://docs.python.org/2/library/functions.html#open
    * FORCE_FLUSH: bool = True     # False: Don't flush the file after every write (if buffering is set)
    * LOG_LEVEL: int = 5           # [0..5] (FATAL, ERROR, WARN, INFO, DEBUG or ALWAYS)
    * GROUPS: set = {}             # {}=All. Specify individual case-sensitive groups to log, e.g. {'Zone', 'Utils'}

Console commands:
    * logs.enable    Enable logging, the log is always appended. Restarting TS4 clears the log.
    * logs.disable   Disable logging and close all open log files.
    * logs.flush     Write buffered logs to disk.
    * logs.level n   Change the log level to n=[0..5] (FATAL, ERROR, WARN, INFO, DEBUG or ALWAYS)
    All console changes are temporarily. They are not persisted in the configuration file.

Licensed and licensable according to the EA UGC TOS.

######################################################################
"""


import ast
import os.path
import sys
from datetime import datetime
from typing import Set

import sims.sim_info_base_wrapper
import sims.sim_info_mixin
import sims4.commands
import sims4.log
import sims4.reload
from sims4.gsi.archive import set_all_archivers_enabled
from ts4lib.utils.singleton import Singleton
from vanilla_logs.log_level import LogLevel


with sims4.reload.protected(globals()):
    _log_level = LogLevel.ALWAYS
    _groups = {}


class VanillaLogs(object, metaclass=Singleton):
    iso_data_format = '%Y-%m-%dT%H:%M:%S.%f'
    mod_name = 'vanilla_logs'
    log_name = 'VanillaLogs'
    default_enable_logging = True
    default_buffering = 1
    default_force_flush = True
    default_log_level = LogLevel.ALWAYS
    default_groups: Set = {}
    default_configuration = {
        'ENABLE_LOGGING': default_enable_logging,
        'LOG_LEVEL': default_log_level,
        'BUFFERING': default_buffering,
        'FORCE_FLUSH': default_force_flush,
        'GROUPS': default_groups,
    }

    def __init__(self):

        __ts4_folder = os.path.dirname(os.path.abspath(__file__)).partition(f"{os.sep}Mods{os.sep}")[0]
        if not os.path.exists(__ts4_folder):
            __ts4_folder = '.'
        __data_folder = os.path.join(__ts4_folder, f'mod_data/{VanillaLogs.mod_name}')
        __logs_folder = os.path.join(__ts4_folder, 'mod_logs')

        os.makedirs(__data_folder, exist_ok=True)
        os.makedirs(__logs_folder, exist_ok=True)

        config_file = os.path.join(__data_folder, f'{VanillaLogs.mod_name}.txt')
        self._log_file = os.path.join(__logs_folder, f'{VanillaLogs.log_name}.txt')

        # noinspection PyBroadException
        try:
            with open(config_file, 'rt', encoding='UTF-8') as fp:
                configuration = ast.literal_eval(fp.read())
                self.configuration = {**VanillaLogs.default_configuration, **configuration}
        except:
            self.configuration = VanillaLogs.default_configuration
            with open(config_file, 'wt', encoding='UTF-8', newline='\n') as fp:
                fp.write(f"{self.configuration}")

        self.logging_enabled = self.configuration.get('ENABLE_LOGGING', VanillaLogs.default_enable_logging)
        global _log_level
        _log_level = self.configuration.get('LOG_LEVEL', VanillaLogs.default_log_level)
        global _groups
        _groups = self.configuration.get('GROUPS', VanillaLogs.default_groups)
        self.buffering = self.configuration.get('BUFFERING', VanillaLogs.default_buffering)
        self.force_flush = self.configuration.get('FORCE_FLUSH', VanillaLogs.default_force_flush)
        self.log_file = None
        self.open_log_file(mode='wt')

    def open_log_file(self, mode: str = 'at'):
        if self.logging_enabled and self.log_file is None:
            # noinspection PyBroadException
            try:
                self.log_file = open(self._log_file, mode=mode, encoding='UTF-8', buffering=self.buffering)
                if mode == 'wt':
                    self.log(None, f"Thank you for using '{VanillaLogs.log_name}'", 'ALWAYS', 'o19')
                    self.log(None, f"Configuration: {self.configuration}", 'ALWAYS', 'o19')
            except:
                (exc_type, exc, exc_tb) = sys.exc_info()
                sims4.log.exception('VanillaLogs', f'Error opening log file {self.log_file}', exc=exc)
                self.logging_enabled = False
                self.log_file = None

    def flush_log_file(self):
        if self.log_file:
            self.log_file.flush()

    def close_log_file(self):
        if self.log_file:
            self.log_file.close()
        self.logging_enabled = False
        self.log_file = None

    def log(self, _self, message, level, owner, *args):
        if self.log_file:
            if _self and _self.group:
                _group = f"{_self.group}"
            else:
                _group = 'None'
            if _groups and _group not in _groups:
                return

            if args:
                _message = message.format(*args)
            else:
                _message = message
            if not _message:
                _message = 'None'

            if level:
                _level = level
            else:
                _level = 'None'

            _owner = 'None'
            if owner:
                _owner = owner
            else:
                if _self and _self.default_owner:
                    _owner = _self.default_owner

            msg = f"{datetime.now().strftime(VanillaLogs.iso_data_format)} {_level:6} {_group:20} {_owner:10} '{_message}'"
            self.log_file.write(msg + '\n')

            if self.force_flush:
                self.log_file.flush()


logger = VanillaLogs()


def always(self, message, *args, owner=None, **__):
    if _log_level >= LogLevel.ALWAYS:
        logger.log(self, message, 'ALWAYS', owner, *args)


def debug(self, message, *args, owner=None, **__):
    if _log_level >= LogLevel.DEBUG:
        logger.log(self, message, 'DEBUG', owner, *args)


def info(self, message, *args, owner=None, **__):
    if _log_level >= LogLevel.INFO:
        logger.log(self, message, 'INFO', owner, *args)


def warn(self, message, *args, owner=None, **__):
    if _log_level >= LogLevel.WARN:
        logger.log(self, message, 'WARN', owner, *args)


def error(self, message, *args, owner=None, **__):
    if _log_level >= LogLevel.ERROR:
        logger.log(self, message.replace('\n', ''), 'ERROR', owner, *args)


def callback_on_error_or_exception(message):
    if _log_level >= LogLevel.FATAL:
        logger.log(None, message, 'FATAL', None)


@property
def sim_full_name(self):
    return self.sim_info.first_name + '#' + self.sim_info.last_name  # 'Al#Kim Kong' != 'Al Kim#Kong' !!1!


# noinspection SpellCheckingInspection
@property
def siminfo_full_name(self):
    return self.first_name + '#' + self.last_name  # 'Al#Kim Kong' != 'Al Kim#Kong' !!1!


sims4.log.Logger.always = always
sims4.log.Logger.debug = debug
sims4.log.Logger.info = info
sims4.log.Logger.warn = warn
sims4.log.Logger.error = error
sims4.log.callback_on_error_or_exception = callback_on_error_or_exception
# noinspection PyPropertyAccess
sims.sim_info_mixin.HasSimInfoBasicMixin.full_name = sim_full_name
# noinspection PyPropertyAccess
sims.sim_info_base_wrapper.SimInfoBaseWrapper.full_name = siminfo_full_name


@sims4.commands.Command('logs.enable', command_type=sims4.commands.CommandType.Live)
def logs_enable(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    _logger = VanillaLogs()
    _logger.open_log_file()
    output('Logs enabled')


@sims4.commands.Command('logs.disable', command_type=sims4.commands.CommandType.Live)
def logs_disable(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    _logger = VanillaLogs()
    _logger.close_log_file()
    output('Logs closed and disabled')


@sims4.commands.Command('logs.flush', command_type=sims4.commands.CommandType.Live)
def logs_enable(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    _logger = VanillaLogs()
    _logger.flush_log_file()
    output('Logs flushed')

@sims4.commands.Command('logs.level', command_type=sims4.commands.CommandType.Live)
def logs_enable(arg=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    if arg:
        if arg in {'0', '1', '2', '3', '4', '5'}:
            log_level = int(arg)
            global _log_level
            _log_level = log_level
            output(f"Log level set to '{log_level}'")


set_all_archivers_enabled(True)
