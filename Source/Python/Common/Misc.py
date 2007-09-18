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

from Common.BuildToolError import *

gPlaceholderPattern = re.compile("\$\{([^$()\s]+)\}", re.MULTILINE|re.UNICODE)
gFileTimeStampCache = {}    # {file path : file time stamp}
gDependencyDatabase = {}    # file path : [dependent files list]

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

def GuidStructureStringToGuidString(GuidValue):
    guidValueString = GuidValue.lower().replace("{", "").replace("}", "").replace(" ", "")
    guidValueList = guidValueString.split(",")
    if len(guidValueList) != 11:
        raise AutoGenError(msg="Invalid GUID value string %s" % GuidValue)
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

def GuidStructureStringToGuidValueName(GuidValue):
    guidValueString = GuidValue.lower().replace("{", "").replace("}", "").replace(" ", "")
    guidValueList = guidValueString.split(",")
    if len(guidValueList) != 11:
        raise AutoGenError(msg="Invalid GUID value string %s" % GuidValue)
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

def CreateDirectory(Directory):
    if not os.access(Directory, os.F_OK):
        os.makedirs(Directory)

def IsChanged(File):
    FileState = os.stat(File)
    TimeStamp = FileState[-2]

    if File in gFileTimeStampCache and TimeStamp <= gFileTimeStampCache[File]:
        FileChanged = False
    else:
        FileChanged = True
        gFileTimeStampCache[File] = TimeStamp

    return FileChanged

def SaveFileOnChange(File, Content, IsBinaryFile=False):
    if IsBinaryFile:
        BinaryFlag = 'b'
    else:
        BinaryFlag = ''
    Fd = None
    if os.path.exists(File):
        Fd = open(File, "r"+BinaryFlag)
        if Content == Fd.read():
            Fd.close()
            return False
        Fd.close()
    CreateDirectory(os.path.dirname(File))
    Fd = open(File, "w"+BinaryFlag)
    Fd.write(Content)
    Fd.close()
    return True

def Cache(Data, File):
    Fd = None
    try:
        Fd = open(File, 'w')
        cPickle.dump(Data, Fd)
    except:
        raise AutoGenError(FILE_OPEN_FAILURE, name=File)
    finally:
        if Fd != None:
            Fd.close()

def Restore(File):
    try:
        Fd = open(File, 'r')
        return cPickle.load(Fd)
    except Exception, e:
        raise AutoGenError(FILE_OPEN_FAILURE, name=File)
    finally:
        if Fd != None:
            Fd.close()

class TemplateString(object):
    def __init__(self):
        self.String = ''

    def __str__(self):
        return self.String

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
                    raise AutoGenError(msg=Key + " has different repeat time from others!")

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

class Progressor:
    def __init__(self, OpenMessage="", CloseMessage="", ProgressChar='.', Interval=1):
        self.StopFlag = threading.Event()
        self.ProgressThread = None
        self.PromptMessage = OpenMessage
        self.CodaMessage = CloseMessage
        self.ProgressChar = ProgressChar
        self.Interval = Interval

    def Start(self, OpenMessage=None):
        if OpenMessage != None:
            self.PromptMessage = OpenMessage
        self.StopFlag.clear()
        self.ProgressThread = threading.Thread(target=self._ProgressThreadEntry)
        self.ProgressThread.setDaemon(True)
        self.ProgressThread.start()

    def Stop(self, CloseMessage=None):
        if CloseMessage != None:
            self.CodaMessage = CloseMessage
        self.StopFlag.set()
        self.ProgressThread.join()
        self.ProgressThread = None

    def _ProgressThreadEntry(self):
        print self.PromptMessage,
        while not self.StopFlag.isSet():
            time.sleep(self.Interval)
            print self.ProgressChar,
        print self.CodaMessage

class sdict(dict):
    def __init__(self):
        self._key_list = []

    def __setitem__(self, key, value):
        if key not in self._key_list:
            self._key_list.append(key)
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        self._key_list.remove(key)
        dict.__delitem__(self, key)
    #
    # used in "for k in dict" loop to ensure the correct order
    #
    def __iter__(self):
        return self.iterkeys()

    def __len__(self):
        return len(self._key_list)

    def __contains__(self, key):
        return key in self._key_list

    def has_key(self, key):
        return key in self._key_list

    def clear(self):
        self._key_list = []
        dict.clear(self)

    def keys(self):
        keys = []
        for key in self._key_list:
            keys.append(key)
        return keys

    def values(self):
        values = []
        for key in self._key_list:
            values.append(self[key])
        return values

    def items(self):
        items = []
        for key in self._key_list:
            items.append((key, self[key]))
        return items

    def iteritems(self):
        return iter(self.items())

    def iterkeys(self):
        return iter(self.keys())

    def itervalues(self):
        return iter(self.values())

    def pop(self, key, *dv):
        value = None
        if key in self._key_list:
            value = self[key]
            dict.__delitem__(self, key)
        elif len(dv) != 0 :
            value = kv[0]
        return value

    def popitem(self):
        key = self._key_list[0]
        value = self[key]
        dict.__delitem__(self, key)
        return key, value


if gFileTimeStampCache == {} and os.path.exists(".TsCache"):
    gFileTimeStampCache = Restore(".TsCache")

if gDependencyDatabase == {} and os.path.exists(".DepCache"):
    gDependencyDatabase = Restore(".DepCache")
