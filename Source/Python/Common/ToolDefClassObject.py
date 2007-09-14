# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of tools_def.txt file
#

import os
import re
import EdkLogger

from Dictionary import *
from BuildToolError import *
from TargetTxtClassObject import *

gMacroRefPattern = re.compile('(DEF\([^\(\)]+\))')
gEnvRefPattern = re.compile('(ENV\([^\(\)]+\))')
gMacroDefPattern = re.compile("DEFINE\s+([^\s]+)")

class ToolDefClassObject(object):
    def __init__(self, FileName = None):
        self.ToolsDefTxtDictionary = {}
        self.MacroDictionary = {}
        for Env in os.environ:
            self.MacroDictionary["ENV(%s)" % Env] = os.environ[Env]

        if FileName != None:
            self.LoadToolDefFile(FileName)

    def LoadToolDefFile(self, FileName):
        FileContent = []
        if os.path.isfile(FileName):
            try:
                F = open(FileName,'r')
                FileContent = F.readlines()
            except:
                raise ParserError(FILE_OPEN_FAILURE, name=FileName)
        else:
            raise ParserError(FILE_NOT_FOUND, name=FileName)

        self.ToolsDefTxtDatabase = {
            TAB_TOD_DEFINES_TARGET          :   [],
            TAB_TOD_DEFINES_TOOL_CHAIN_TAG  :   [],
            TAB_TOD_DEFINES_TARGET_ARCH     :   [],
            TAB_TOD_DEFINES_COMMAND_TYPE    :   []
        }

        for Index in range(len(FileContent)):
            Line = FileContent[Index].strip()
            if Line == "" or Line[0] == '#':
                continue
            NameValuePair = Line.split("=", 1)
            if len(NameValuePair) != 2:
                EdkLogger.warn("Line %d: not correct assignment statement, skipped" % (Index + 1))
                continue

            Name = NameValuePair[0].strip()
            Value = NameValuePair[1].strip()

            if Name == "IDENTIFIER":
                EdkLogger.verbose("Line %d: Found identifier statement, skipped: %s" % ((Index + 1), Value))
                continue

            MacroDefinition = gMacroDefPattern.findall(Name)
            if MacroDefinition != []:
                EnvReference = gEnvRefPattern.findall(Value)
                for Ref in EnvReference:
                    if Ref not in self.MacroDictionary:
                        raise ParserError(msg="Environment [%s] has not been defined" % Ref)
                    Value = Value.replace(Ref, self.MacroDictionary[Ref])

                MacroName = MacroDefinition[0].strip()
                self.MacroDictionary["DEF(%s)" % MacroName] = Value
                EdkLogger.verbose("Line %d: Found macro: %s = %s" % ((Index + 1), MacroName, Value))
                continue

            MacroReference = gMacroRefPattern.findall(Value)
            for Ref in MacroReference:
                if Ref not in self.MacroDictionary:
                    raise ParserError(msg="Macro [%s] has not been defined" % Ref)
                Value = Value.replace(Ref, self.MacroDictionary[Ref])

            List = Name.split('_')
            if len(List) != 5:
                EdkLogger.verbose("Line %d: Not a valid name of definition: %s" % ((Index + 1), Name))
                continue
            elif List[4] == '*':
                EdkLogger.verbose("Line %d: '*' is not allowed in last field: %s" % ((Index + 1), Name))
                continue
            else:
                self.ToolsDefTxtDictionary[Name] = Value
                if List[0] != '*':
                    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET] += [List[0]]
                if List[1] != '*':
                    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG] += [List[1]]
                if List[2] != '*':
                    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH] += [List[2]]
                if List[3] != '*':
                    self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE] += [List[3]]

        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET]                 = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET]))
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG] = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG]))
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH]        = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH]))
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE]     = list(set(self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE]))

        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET].sort()
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG].sort()
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TARGET_ARCH].sort()
        self.ToolsDefTxtDatabase[TAB_TOD_DEFINES_COMMAND_TYPE].sort()

        KeyList = [TAB_TOD_DEFINES_TARGET, TAB_TOD_DEFINES_TOOL_CHAIN_TAG, TAB_TOD_DEFINES_TARGET_ARCH, TAB_TOD_DEFINES_COMMAND_TYPE]
        for Index in range(3,-1,-1):
            for Key in dict(self.ToolsDefTxtDictionary):
                List = Key.split('_')
                if List[Index] == '*':
                    for String in self.ToolsDefTxtDatabase[KeyList[Index]]:
                        List[Index] = String
                        NewKey = '%s_%s_%s_%s_%s' % tuple(List)
                        if NewKey not in self.ToolsDefTxtDictionary:
                            self.ToolsDefTxtDictionary[NewKey] = self.ToolsDefTxtDictionary[Key]
                        continue
                    del self.ToolsDefTxtDictionary[Key]
                elif List[Index] not in self.ToolsDefTxtDatabase[KeyList[Index]]:
                    del self.ToolsDefTxtDictionary[Key]

def ToolDefDict(WorkSpace):
    Target = TargetTxtClassObject()
    Target.LoadTargetTxtFile(WorkSpace + '\\Conf\\target.txt')
    ToolDef = ToolDefClassObject()
    ToolDef.LoadToolDefFile(WorkSpace + '\\' + Target.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF])
    return ToolDef

if __name__ == '__main__':
##    td = ToolDefClassObject('tool_def.txt')
##    print td.ToolsDefTxtDatabase

    ToolDef = ToolDefDict(os.getenv("WORKSPACE"))
    pass
