## @file
# Common routines used by all tools
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import os
import sys
import string
import thread
import threading
import time
import re
import cPickle
from UserDict import IterableUserDict

from Common import EdkLogger as EdkLogger
from BuildToolError import *

## Regular expression used to find out place holders in string template
gPlaceholderPattern = re.compile("\$\{([^$()\s]+)\}", re.MULTILINE|re.UNICODE)

## Dictionary used to store file time stamp for quick re-access
gFileTimeStampCache = {}    # {file path : file time stamp}

## Dictionary used to store dependencies of files
gDependencyDatabase = {}    # arch : {file path : [dependent files list]}

## callback routine for processing variable option
#
# This function can be used to process variable number of option values. The
# typical usage of it is specify architecure list on command line.
# (e.g. <tool> -a IA32 X64 IPF)
#
# @param  Option        Standard callback function parameter
# @param  OptionString  Standard callback function parameter
# @param  Value         Standard callback function parameter
# @param  Parser        Standard callback function parameter
#
# @retval
#
def ProcessVariableArgument(Option, OptionString, Value, Parser):
    assert Value is None
    Value = []
    RawArgs = Parser.rargs
    while RawArgs:
        Arg = RawArgs[0]
        if (Arg[:2] == "--" and len(Arg) > 2) or \
           (Arg[:1] == "-" and len(Arg) > 1 and Arg[1] != "-"):
            break
        Value.append(Arg)
        del RawArgs[0]
    setattr(Parser.values, Option.dest, Value)

## Convert GUID string in xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx style to C structure style
#
#   @param      Guid    The GUID string
#
#   @retval     string  The GUID string in C structure style
#
def GuidStringToGuidStructureString(Guid):
    GuidList = Guid.split('-')
    Result = '{'
    for Index in range(0,3,1):
        Result = Result + '0x' + GuidList[Index] + ', '
    Result = Result + '{0x' + GuidList[3][0:2] + ', 0x' + GuidList[3][2:4]
    for Index in range(0,12,2):
        Result = Result + ', 0x' + GuidList[4][Index:Index+2]
    Result += '}}'
    return Result

## Convert GUID string in C structure style to xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
#
#   @param      GuidValue   The GUID value in C structure format
#
#   @retval     string      The GUID value in xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx format
#
def GuidStructureStringToGuidString(GuidValue):
    guidValueString = GuidValue.lower().replace("{", "").replace("}", "").replace(" ", "")
    guidValueList = guidValueString.split(",")
    if len(guidValueList) != 11:
        EdkLogger.error(None, None, "Invalid GUID value string %s" % GuidValue)
    return "%08x-%04x-%04x-%02x%02x-%02x%02x%02x%02x%02x%02x" % (
            int(guidValueList[0], 16),
            int(guidValueList[1], 16),
            int(guidValueList[2], 16),
            int(guidValueList[3], 16),
            int(guidValueList[4], 16),
            int(guidValueList[5], 16),
            int(guidValueList[6], 16),
            int(guidValueList[7], 16),
            int(guidValueList[8], 16),
            int(guidValueList[9], 16),
            int(guidValueList[10], 16)
            )

## Convert GUID string in C structure style to xxxxxxxx_xxxx_xxxx_xxxx_xxxxxxxxxxxx
#
#   @param      GuidValue   The GUID value in C structure format
#
#   @retval     string      The GUID value in xxxxxxxx_xxxx_xxxx_xxxx_xxxxxxxxxxxx format
#
def GuidStructureStringToGuidValueName(GuidValue):
    guidValueString = GuidValue.lower().replace("{", "").replace("}", "").replace(" ", "")
    guidValueList = guidValueString.split(",")
    if len(guidValueList) != 11:
        EdkLogger.error(None, None, "Invalid GUID value string %s" % GuidValue)
    return "%08x_%04x_%04x_%02x%02x_%02x%02x%02x%02x%02x%02x" % (
            int(guidValueList[0], 16),
            int(guidValueList[1], 16),
            int(guidValueList[2], 16),
            int(guidValueList[3], 16),
            int(guidValueList[4], 16),
            int(guidValueList[5], 16),
            int(guidValueList[6], 16),
            int(guidValueList[7], 16),
            int(guidValueList[8], 16),
            int(guidValueList[9], 16),
            int(guidValueList[10], 16)
            )

## Create directories
#
#   @param      Directory   The directory name
#
def CreateDirectory(Directory):
    if Directory == None or Directory.strip() == "":
        return
    if not os.access(Directory, os.F_OK):
        os.makedirs(Directory)

## Check if given file is changed or not
#
#  This method is used to check if a file is changed or not between two build
#  actions. It makes use a cache to store files timestamp.
#
#   @param      File    The path of file
#
#   @retval     True    If the given file is changed, doesn't exist, or can't be
#                       found in timestamp cache
#   @retval     False   If the given file is changed
#
def IsChanged(File):
    if not os.path.exists(File):
        return True

    FileState = os.stat(File)
    TimeStamp = FileState[-2]

    if File in gFileTimeStampCache and TimeStamp <= gFileTimeStampCache[File]:
        FileChanged = False
    else:
        FileChanged = True
        gFileTimeStampCache[File] = TimeStamp

    return FileChanged

## Store content in file
#
#  This method is used to save file only when its content is changed. This is
#  quite useful for "make" system to decide what will be re-built and what won't.
#
#   @param      File            The path of file
#   @param      Content         The new content of the file
#   @param      IsBinaryFile    The flag indicating if the file is binary file or not
#
#   @retval     True            If the file content is changed and the file is renewed
#   @retval     False           If the file content is the same
#
def SaveFileOnChange(File, Content, IsBinaryFile=True):
    if IsBinaryFile:
        BinaryFlag = 'b'
    else:
        BinaryFlag = ''
    Fd = None
    if os.path.exists(File):
        Fd = open(File, "r"+BinaryFlag)
        FileSize = os.fstat(Fd.fileno()).st_size
        if len(Content) == FileSize and Content == Fd.read():
            Fd.close()
            return False
        Fd.close()
    CreateDirectory(os.path.dirname(File))
    Fd = open(File, "w"+BinaryFlag)
    Fd.write(Content)
    Fd.close()
    return True

## Make a Python object persistent on file system
#
#   @param      Data    The object to be stored in file
#   @param      File    The path of file to store the object
#
def DataDump(Data, File):
    Fd = None
    try:
        Fd = open(File, 'wb')
        cPickle.dump(Data, Fd, cPickle.HIGHEST_PROTOCOL)
    except:
        EdkLogger.error("", FILE_OPEN_FAILURE, ExtraData=File, RaiseError=False)
    finally:
        if Fd != None:
            Fd.close()

## Restore a Python object from a file
#
#   @param      File    The path of file stored the object
#
#   @retval     object  A python object
#   @retval     None    If failure in file operation
#
def DataRestore(File):
    Data = None
    Fd = None
    try:
        Fd = open(File, 'rb')
        Data = cPickle.load(Fd)
    except Exception, e:
        EdkLogger.verbose("Failed to load [%s]\n\t%s" % (File, str(e)))
        Data = None
    finally:
        if Fd != None:
            Fd.close()
    return Data

## A string template class
#
#  This class implements a template for string replacement. A string template
#  looks like following
#
#       ${BEGIN} other_string ${placeholder_name} other_string ${END}
#
#  The string between ${BEGIN} and ${END} will be repeated as many times as the
#  length of "placeholder_name", which is a list passed through a dict. The
#  "placeholder_name" is the key name of the dict. The ${BEGIN} and ${END} can
#  be not used and, in this case, the "placeholder_name" must not a list and it
#  will just be replaced once.
#
class TemplateString(object):
    ## Constructor
    def __init__(self):
        self.String = ''

    ## str() operator
    #
    #   @retval     string  The string replaced
    #
    def __str__(self):
        return self.String

    ## Replace the string template with dictionary of placeholders
    #
    #   @param      AppendString    The string template to append
    #   @param      Dictionary      The placeholder dictionaries
    #
    def Append(self, AppendString, Dictionary=None):
        if Dictionary == None:
            self.String += AppendString
            return

        # replace repeat ones, enclosed by ${BEGIN} and $(END)
        while True:
            Start = AppendString.find('${BEGIN}')
            if Start < 0:
                break
            End   = AppendString.find('${END}')

            # exclude the ${BEGIN} and ${END}
            SubString = AppendString[Start + 8 : End]

            RepeatTime = -1
            SubDict = {}
            PlaceholderList = gPlaceholderPattern.findall(SubString)
            for Key in PlaceholderList:
                if Key not in Dictionary:
                    continue

                Value = Dictionary[Key]
                if type(Value) != type([]):
                    continue

                SubDict[Key] = ""
                if RepeatTime < 0:
                    RepeatTime = len(Value)
                elif RepeatTime != len(Value):
                    EdkLogger.error("TemplateString", PARAMETER_INVALID, Key + " has different repeat time from others!",
                                    ExtraData=str(Dictionary))

            NewString = ''
            for Index in range(0, RepeatTime):
                for Key in SubDict:
                    SubDict[Key] = Dictionary[Key][Index]
                NewString += string.Template(SubString).safe_substitute(SubDict)
            AppendString = AppendString[0:Start] + NewString + AppendString[End + 6:]

        # replace single ones
        SubDict = {}
        for Key in Dictionary:
            Value = Dictionary[Key]
            if type(Value) == type([]):
                continue
            SubDict[Key] = Value
        AppendString = string.Template(AppendString).safe_substitute(SubDict)

        self.String += AppendString

## Progress indicator class
#
#  This class makes use of thread to print progress on console.
#
class Progressor:
    # for avoiding deadloop
    _StopFlag = None
    _ProgressThread = None
    ## Constructor
    #
    #   @param      OpenMessage     The string printed before progress charaters
    #   @param      CloseMessage    The string printed after progress charaters
    #   @param      ProgressChar    The charater used to indicate the progress
    #   @param      Interval        The interval in seconds between two progress charaters
    #
    def __init__(self, OpenMessage="", CloseMessage="", ProgressChar='.', Interval=1):
        self.PromptMessage = OpenMessage
        self.CodaMessage = CloseMessage
        self.ProgressChar = ProgressChar
        self.Interval = Interval
        if Progressor._StopFlag == None:
            Progressor._StopFlag = threading.Event()

    ## Start to print progress charater
    #
    #   @param      OpenMessage     The string printed before progress charaters
    #
    def Start(self, OpenMessage=None):
        if OpenMessage != None:
            self.PromptMessage = OpenMessage
        Progressor._StopFlag.clear()
        if Progressor._ProgressThread == None:
            Progressor._ProgressThread = threading.Thread(target=self._ProgressThreadEntry)
            Progressor._ProgressThread.setDaemon(False)
            Progressor._ProgressThread.start()

    ## Stop printing progress charater
    #
    #   @param      CloseMessage    The string printed after progress charaters
    #
    def Stop(self, CloseMessage=None):
        OriginalCodaMessage = self.CodaMessage
        if CloseMessage != None:
            self.CodaMessage = CloseMessage
        self.Abort()
        self.CodaMessage = OriginalCodaMessage

    ## Thread entry method
    def _ProgressThreadEntry(self):
        print self.PromptMessage,
        while not Progressor._StopFlag.isSet():
            print self.ProgressChar,
            time.sleep(self.Interval)
        print self.CodaMessage
        sys.stdout.flush()

    ## Abort the progress display
    @staticmethod
    def Abort():
        if Progressor._StopFlag != None:
            Progressor._StopFlag.set()
        if Progressor._ProgressThread != None:
            Progressor._ProgressThread.join()
            Progressor._ProgressThread = None

## A dict which can access its keys and/or values orderly
#
#  The class implements a new kind of dict which its keys or values can be
#  accessed in the order they are added into the dict. It guarantees the order
#  by making use of an internal list to keep a copy of keys.
#
class sdict(IterableUserDict):
    ## Constructor
    def __init__(self):
        IterableUserDict.__init__(self)
        self._key_list = []

    ## [] operator
    def __setitem__(self, key, value):
        if key not in self._key_list:
            self._key_list.append(key)
        IterableUserDict.__setitem__(self, key, value)

    ## del operator
    def __delitem__(self, key):
        self._key_list.remove(key)
        IterableUserDict.__delitem__(self, key)

    ## used in "for k in dict" loop to ensure the correct order
    def __iter__(self):
        return self.iterkeys()

    ## len() support
    def __len__(self):
        return len(self._key_list)

    ## "in" test support
    def __contains__(self, key):
        return key in self._key_list

    def has_key(self, key):
        return key in self._key_list

    ## Empty the dict
    def clear(self):
        self._key_list = []
        IterableUserDict.clear(self)

    ## Return a copy of keys
    def keys(self):
        keys = []
        for key in self._key_list:
            keys.append(key)
        return keys

    ## Return a copy of values
    def values(self):
        values = []
        for key in self._key_list:
            values.append(self[key])
        return values

    ## Return a copy of (key, value) list
    def items(self):
        items = []
        for key in self._key_list:
            items.append((key, self[key]))
        return items

    ## Iteration support
    def iteritems(self):
        return iter(self.items())

    ## Keys interation support
    def iterkeys(self):
        return iter(self.keys())

    ## Values interation support
    def itervalues(self):
        return iter(self.values())

    ## Return value related to a key, and remove the (key, value) from the dict
    def pop(self, key, *dv):
        value = None
        if key in self._key_list:
            value = self[key]
            self.__delitem__(key)
        elif len(dv) != 0 :
            value = kv[0]
        return value

    ## Return (key, value) pair, and remove the (key, value) from the dict
    def popitem(self):
        key = self._key_list[-1]
        value = self[key]
        self.__delitem__(key)
        return key, value

## Dictionary with restricted keys
#
class rdict(dict):
    ## Constructor
    def __init__(self, KeyList):
        for Key in KeyList:
            dict.__setitem__(self, Key, "")

    ## []= operator
    def __setitem__(self, key, value):
        if key not in self:
            EdkLogger.error("RestrictedDict", ATTRIBUTE_SET_FAILURE, "Key [%s] is not allowed" % key, 
                            ExtraData=", ".join(dict.keys(self)))
        dict.__setitem__(self, key, value)

    ## =[] operator
    def __getitem__(self, key):
        if key not in self:
            return ""
        return dict.__getitem__(self, key)

    ## del operator
    def __delitem__(self, key):
        EdkLogger.error("RestrictedDict", ATTRIBUTE_ACCESS_DENIED, ExtraData="del")

    ## Empty the dict
    def clear(self):
        for Key in self:
            self.__setitem__(Key, "")

    ## Return value related to a key, and remove the (key, value) from the dict
    def pop(self, key, *dv):
        EdkLogger.error("RestrictedDict", ATTRIBUTE_ACCESS_DENIED, ExtraData="pop")

    ## Return (key, value) pair, and remove the (key, value) from the dict
    def popitem(self):
        EdkLogger.error("RestrictedDict", ATTRIBUTE_ACCESS_DENIED, ExtraData="popitem")

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    pass
