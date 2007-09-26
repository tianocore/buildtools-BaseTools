import sys, os, logging
import traceback
from  Common.BuildToolError import *

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
INFO    = 20
QUIET   = 40
ERROR   = 50

_LogLevels = [DEBUG_0, DEBUG_1, DEBUG_2, DEBUG_3, DEBUG_4, DEBUG_5, DEBUG_6, DEBUG_7, DEBUG_8, DEBUG_9, VERBOSE, WARN, INFO, ERROR, QUIET]

_DebugLogger = logging.getLogger("tool_debug")
_DebugLogger.setLevel(INFO)
_DebugChannel = logging.StreamHandler(sys.stdout)
_DebugFormatter = logging.Formatter("[%(asctime)s.%(msecs)d]: %(message)s", datefmt="%H:%M:%S")
_DebugChannel.setFormatter(_DebugFormatter)
_DebugLogger.addHandler(_DebugChannel)

##_VerboseLogger = logging.getLogger("tool_verbose")
##_VerboseLogger.setLevel(INFO)
##_VerboseChannel = logging.StreamHandler(sys.stdout)
##_VerboseFormatter = logging.Formatter("%(message)s")
##_VerboseChannel.setFormatter(_VerboseFormatter)
##_VerboseLogger.addHandler(_VerboseChannel)
##
##_WarnLogger = logging.getLogger("tool_warn")
##_WarnLogger.setLevel(INFO)
##_WarnChannel = logging.StreamHandler(sys.stdout)
##_WarnFormatter = logging.Formatter("%(message)s")
##_WarnChannel.setFormatter(_WarnFormatter)
##_WarnLogger.addHandler(_WarnChannel)

_InfoLogger = logging.getLogger("tool_info")
_InfoLogger.setLevel(INFO)
_InfoChannel = logging.StreamHandler(sys.stdout)
_InfoFormatter = logging.Formatter("%(message)s")
_InfoChannel.setFormatter(_InfoFormatter)
_InfoLogger.addHandler(_InfoChannel)

_ErrorLogger = logging.getLogger("tool_error")
_ErrorLogger.setLevel(INFO)
_ErrorCh = logging.StreamHandler(sys.stderr)
_ErrorFormatter = logging.Formatter("%(message)s")
_ErrorCh.setFormatter(_ErrorFormatter)
_ErrorLogger.addHandler(_ErrorCh)

_ErrorMessageTemplate = '\n%(tool)s...\n%(file)s(%(line)s): error %(errorcode)X: %(msg)s'
_ErrorMessageTemplateWithoutFile = '\n%(tool)s: : error %(errorcode)X: %(msg)s'
_WarningMessageTemplate = '%(tool)s...\n%(file)s(%(line)s): warning: %(msg)s'
_WarningMessageTemplateWithoutFile = '%(tool)s: : warning: %(msg)s'
_DebugMessageTemplate = '%(file)s(%(line)s): debug: %(msg)s'

_WarningAsError = False


def debug(Level, Message, ExtraData=None):
    if _DebugLogger.getEffectiveLevel() > Level:
        return
    if Level > DEBUG_9:
        return

    CallerStack = traceback.extract_stack()[-2]
    TemplateDict = {
        "file"      : CallerStack[0],
        "line"      : CallerStack[1],
        "msg"       : Message,
    }

    if ExtraData != None:
        LogText = _DebugMessageTemplate % TemplateDict + "\n  " + ExtraData
    else:
        LogText = _DebugMessageTemplate % TemplateDict

    _DebugLogger.log(Level, LogText)

def verbose(Message):
    return _InfoLogger.log(VERBOSE, Message)

def warn(ToolName, Message, File=None, Line=None, ExtraData=None):
    if _InfoLogger.getEffectiveLevel() > WARN:
        return

    # if no tool name given, use caller's source file name as tool name
    if ToolName == None or ToolName == "":
        ToolName = os.path.basename(traceback.extract_stack()[-2][0])

    if Line == None:
        Line = "..."
    else:
        Line = "%d" % Line

    TemplateDict = {
        "tool"      : ToolName,
        "file"      : File,
        "line"      : Line,
        "msg"       : Message,
    }

    if File != None:
        LogText = _WarningMessageTemplate % TemplateDict
    else:
        LogText = _WarningMessageTemplateWithoutFile % TemplateDict

    if ExtraData != None:
        LogText += "\n  " + ExtraData

    _InfoLogger.log(WARN, LogText)

    if _WarningAsError == True:
        raise FatalError("%s failed by warning!" % ToolName)

info    = _InfoLogger.info

def error(ToolName, ErrorCode, Message=None, File=None, Line=None, ExtraData=None):
    # if no tool name given, use caller's source file name as tool name
    if ToolName == None or ToolName == "":
        ToolName = os.path.basename(traceback.extract_stack()[-2][0])

    if Line == None:
        Line = "..."
    else:
        Line = "%d" % Line

    if Message == None:
        if ErrorCode in gErrorMessage:
            Message = gErrorMessage[ErrorCode]
        else:
            Message = gErrorMessage[UNKNOWN_ERROR]

    TemplateDict = {
        "tool"      : ToolName,
        "file"      : File,
        "line"      : Line,
        "errorcode" : ErrorCode,
        "msg"       : Message,
        "extra"     : ExtraData
    }

    if File != None:
        LogText =  _ErrorMessageTemplate % TemplateDict
    else:
        LogText = _ErrorMessageTemplateWithoutFile % TemplateDict

    if ExtraData != None:
        LogText += "\n  " + ExtraData

    _ErrorLogger.log(ERROR, LogText)
    raise FatalError("%s failed!" % ToolName)

quiet   = _ErrorLogger.error

def SetLevel(Level):
    if Level not in _LogLevels:
        info("Not supported log level (%d)" % Level)
        Level = INFO
    _DebugLogger.setLevel(Level)
    #_VerboseLogger.setLevel(Level)
    _InfoLogger.setLevel(Level)
    #_WarnLogger.setLevel(Level)
    _ErrorLogger.setLevel(Level)
    #_QuietLogger.setLevel(Level)

def SetWarningAsError():
    global _WarningAsError
    _WarningAsError = True

def SetLogFile(LogFile):
    if os.path.exists(LogFile):
        os.remove(LogFile)

    _Ch = logging.FileHandler(LogFile)
    _Ch.setFormatter(_DebugFormatter)
    _DebugLogger.addHandler(_Ch)

    #_Ch = logging.FileHandler(LogFile)
    #_Ch.setFormatter(_VerboseFormatter)
    #_VerboseLogger.addHandler(_Ch)

    #_Ch = logging.FileHandler(LogFile)
    #_Ch.setFormatter(_WarnFormatter)
    #_WarnLogger.addHandler(_Ch)

    _Ch= logging.FileHandler(LogFile)
    _Ch.setFormatter(_InfoFormatter)
    _InfoLogger.addHandler(_Ch)

    _Ch = logging.FileHandler(LogFile)
    _Ch.setFormatter(_ErrorFormatter)
    _ErrorLogger.addHandler(_Ch)
    
    #
    #_ch = logging.FileHandler(log)
    #_ch.setFormatter(_quiet_formatter)
    #_QuietLogger.addHandler(_ch)

if __name__ == '__main__':
    pass

