import sys, os, logging, traceback, inspect

DEBUG   = logging.DEBUG
VERBOSE = logging.INFO
INFO    = logging.WARN
WARNING = logging.ERROR
ERROR   = logging.CRITICAL

_log_levels = [DEBUG, VERBOSE, INFO, WARNING, ERROR]

_debug_logger = logging.getLogger("edk2_debug")
_debug_logger.setLevel(INFO)
_debug_ch = logging.StreamHandler()
# _ch.setLevel(logging.INFO)
_debug_formatter = logging.Formatter("%(pathname)s:%(lineno)d: [%(asctime)s] %(funcName)s() : %(message)s")
_debug_ch.setFormatter(_debug_formatter)
_debug_logger.addHandler(_debug_ch)

_verbose_logger = logging.getLogger("edk2_verbose")
_verbose_logger.setLevel(INFO)
_verbose_ch = logging.StreamHandler()
# _ch.setLevel(logging.CRITICAL)
_verbose_formatter = logging.Formatter("%(message)s")
_verbose_ch.setFormatter(_verbose_formatter)
_verbose_logger.addHandler(_verbose_ch)

_info_logger = logging.getLogger("edk2_info")
_info_logger.setLevel(INFO)
_info_ch = logging.StreamHandler()
#_ch.setLevel(logging.INFO)
_info_formatter = logging.Formatter("%(message)s")
_info_ch.setFormatter(_info_formatter)
_info_logger.addHandler(_info_ch)

_warn_logger = logging.getLogger("edk2_warn")
_warn_logger.setLevel(INFO)
_warn_ch = logging.StreamHandler()
# _ch.setLevel(logging.INFO)
_warn_formatter = logging.Formatter("\t%(pathname)s:%(lineno)d: [WARNING] %(funcName)s() : %(message)s")
_warn_ch.setFormatter(_warn_formatter)
_warn_logger.addHandler(_warn_ch)


_error_logger = logging.getLogger("edk2_error")
_error_logger.setLevel(INFO)
_error_ch = logging.StreamHandler()
# _ch.setLevel(logging.ERROR)
_error_formatter = logging.Formatter("\t%(pathname)s:%(lineno)d: [ERROR] %(funcName)s() : %(message)s")
_error_ch.setFormatter(_error_formatter)
_error_logger.addHandler(_error_ch)

debug   = _debug_logger.debug
verbose = _verbose_logger.info
info    = _info_logger.warn
warn    = _warn_logger.error
error   = _error_logger.critical

def setLevel(level):
    if level not in _log_levels:
        warn("Not supported log level (%d)" % level)
        level = INFO
    _debug_logger.setLevel(level)
    _verbose_logger.setLevel(level)
    _info_logger.setLevel(level)
    _warn_logger.setLevel(level)
    _error_logger.setLevel(level)
    
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

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_warn_formatter)
    _warn_logger.addHandler(_ch)

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_error_formatter)
    _error_logger.addHandler(_ch)
