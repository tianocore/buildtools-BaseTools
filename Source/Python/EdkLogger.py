import sys, os, logging, traceback, inspect

DEBUG_0 = 0
DEBUG_1 = 1
DEBUG_2 = 2
DEBUG_3 = 3
DEBUG_4 = 4
DEBUG_5 = 5
DEBUG_6 = 6
DEBUG_7 = 7
DEBUG_8 = 8
DEBUG_9 = 9
VERBOSE = 15
INFO    = logging.INFO      # 20
QUIET   = 30
##WARNING = logging.WARNING   # 30
##ERROR   = logging.ERROR     # 40

_log_levels = [DEBUG_0, DEBUG_1, DEBUG_2, DEBUG_3, DEBUG_4, DEBUG_5, DEBUG_6, DEBUG_7, DEBUG_8, DEBUG_9, VERBOSE, INFO, WARNING, ERROR]

_debug_logger = logging.getLogger("tool_debug")
_debug_logger.setLevel(INFO)
_debug_ch = logging.StreamHandler(sys.stdout)
# _ch.setLevel(logging.INFO)
_debug_formatter = logging.Formatter("%(pathname)s:%(lineno)d: [%(asctime)s] %(funcName)s() : %(message)s")
_debug_ch.setFormatter(_debug_formatter)
_debug_logger.addHandler(_debug_ch)

_verbose_logger = logging.getLogger("tool_verbose")
_verbose_logger.setLevel(INFO)
_verbose_ch = logging.StreamHandler(sys.stdout)
# _ch.setLevel(logging.CRITICAL)
_verbose_formatter = logging.Formatter("%(message)s")
_verbose_ch.setFormatter(_verbose_formatter)
_verbose_logger.addHandler(_verbose_ch)

_info_logger = logging.getLogger("tool_info")
_info_logger.setLevel(INFO)
_info_ch = logging.StreamHandler(sys.stdout)
#_ch.setLevel(logging.INFO)
_info_formatter = logging.Formatter("%(message)s")
_info_ch.setFormatter(_info_formatter)
_info_logger.addHandler(_info_ch)

##_warn_logger = logging.getLogger("tool_warn")
##_warn_logger.setLevel(INFO)
##_warn_ch = logging.StreamHandler(sys.stderr)
### _ch.setLevel(logging.INFO)
##_warn_formatter = logging.Formatter("WARNING: %(message)s")
##_warn_ch.setFormatter(_warn_formatter)
##_warn_logger.addHandler(_warn_ch)
##
##
##_error_logger = logging.getLogger("tool_error")
##_error_logger.setLevel(INFO)
##_error_ch = logging.StreamHandler(sys.stderr)
### _ch.setLevel(logging.ERROR)
###_error_formatter = logging.Formatter("\t%(pathname)s:%(lineno)d: [ERROR] %(funcName)s() : %(message)s")
##_error_formatter = logging.Formatter("ERROR: %(message)s")
##_error_ch.setFormatter(_error_formatter)
##_error_logger.addHandler(_error_ch)

def debug(level, msg):
    return _debug_logger.log(_log_levels[level], msg)

def verbose(msg):
    return _verbose_logger.log(VERBOSE, msg)

info    = _info_logger.info
##warn    = _warn_logger.warn
##error   = _error_logger.error

def setLevel(level):
    if level not in _log_levels:
        warn("Not supported log level (%d)" % level)
        level = INFO
    _debug_logger.setLevel(level)
    _verbose_logger.setLevel(level)
    _info_logger.setLevel(level)
##    _warn_logger.setLevel(level)
##    _error_logger.setLevel(level)

def setLogFile(log):
    if os.path.exists(log):
        os.remove(log)
        
    _ch = logging.FileHandler(log)
    _ch.setFormatter(_debug_formatter)
    _debug_logger.addHandler(_ch)
    
    _ch = logging.FileHandler(log)
    _ch.setFormatter(_verbose_formatter)
    _verbose_logger.addHandler(_ch)

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_info_formatter)
    _info_logger.addHandler(_ch)

##    _ch = logging.FileHandler(log)
##    _ch.setFormatter(_warn_formatter)
##    _warn_logger.addHandler(_ch)
##
##    _ch = logging.FileHandler(log)
##    _ch.setFormatter(_error_formatter)
##    _error_logger.addHandler(_ch)
