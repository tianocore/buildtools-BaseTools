import sys, os, logging

DEBUG_0 = 1
DEBUG_1 = 2
DEBUG_2 = 3
DEBUG_3 = 4
DEBUG_4 = 5
DEBUG_5 = 6
DEBUG_6 = 7
DEBUG_7 = 8
DEBUG_8 = 9
DEBUG_9 = 10
VERBOSE = 15
WARN    = VERBOSE
INFO    = logging.INFO      # 20
ERROR   = 40
QUIET   = 50

_log_levels = [DEBUG_0, DEBUG_1, DEBUG_2, DEBUG_3, DEBUG_4, DEBUG_5, DEBUG_6, DEBUG_7, DEBUG_8, DEBUG_9, VERBOSE, WARN, INFO, ERROR, QUIET]

_debug_logger = logging.getLogger("tool_debug")
_debug_logger.setLevel(INFO)
_debug_ch = logging.StreamHandler(sys.stdout)
_debug_formatter = logging.Formatter("> %(filename)s : %(lineno)d : %(funcName)s():\n>\t%(message)s")
_debug_ch.setFormatter(_debug_formatter)
_debug_logger.addHandler(_debug_ch)

_verbose_logger = logging.getLogger("tool_verbose")
_verbose_logger.setLevel(INFO)
_verbose_ch = logging.StreamHandler(sys.stdout)
#_verbose_formatter = logging.Formatter("[%(asctime)s]%(message)s")
_verbose_formatter = logging.Formatter("> %(message)s")
_verbose_ch.setFormatter(_verbose_formatter)
_verbose_logger.addHandler(_verbose_ch)

_warn_logger = logging.getLogger("tool_warn")
_warn_logger.setLevel(INFO)
_warn_ch = logging.StreamHandler(sys.stdout)
_warn_formatter = logging.Formatter("! %(message)s")
_warn_ch.setFormatter(_warn_formatter)
_warn_logger.addHandler(_warn_ch)

_info_logger = logging.getLogger("tool_info")
_info_logger.setLevel(INFO)
_info_ch = logging.StreamHandler(sys.stdout)
_info_formatter = logging.Formatter("%(message)s")
_info_ch.setFormatter(_info_formatter)
_info_logger.addHandler(_info_ch)

_error_logger = logging.getLogger("tool_error")
_error_logger.setLevel(INFO)
_error_ch = logging.StreamHandler(sys.stderr)
_error_formatter = logging.Formatter("? %(message)s")
_error_ch.setFormatter(_error_formatter)
_error_logger.addHandler(_error_ch)

_quiet_logger = logging.getLogger("tool_quiet")
_quiet_logger.setLevel(INFO)
_quiet_ch = logging.StreamHandler(sys.stderr)
_quiet_formatter = logging.Formatter("%(message)s")
_quiet_ch.setFormatter(_quiet_formatter)
_quiet_logger.addHandler(_quiet_ch)


debug   = _debug_logger.log

def verbose(msg):
    return _verbose_logger.log(VERBOSE, msg)

def warn(msg):
    return _warn_logger.log(WARN, msg)

info    = _info_logger.info

error   = _error_logger.error

quiet   = _quiet_logger.critical

def setLevel(level):
    if level not in _log_levels:
        info("Not supported log level (%d)" % level)
        level = INFO
    _debug_logger.setLevel(level)
    _verbose_logger.setLevel(level)
    _info_logger.setLevel(level)
    _warn_logger.setLevel(level)
    _error_logger.setLevel(level)
    _quiet_logger.setLevel(level)

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
    _ch.setFormatter(_warn_formatter)
    _warn_logger.addHandler(_ch)

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_info_formatter)
    _info_logger.addHandler(_ch)

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_error_formatter)
    _error_logger.addHandler(_ch)

    _ch = logging.FileHandler(log)
    _ch.setFormatter(_quiet_formatter)
    _quiet_logger.addHandler(_ch)

if __name__ == '__main__':
    setLevel(QUIET)
    quiet('hello')

    setLevel(ERROR)
    error('hello')

    setLevel(WARN)
    warn('hello')
