# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of Target.txt file
#
import os
import EdkLogger
import DataType
from BuildToolError import *


class TargetTxtClassObject(object):
    def __init__(self, filename = None):
        self.TargetTxtDictionary = {
            DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM                            : '',
            DataType.TAB_TAT_DEFINES_ACTIVE_MODULE                              : '',
            DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF                            : '',
            DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD                            : '',
            DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER               : '',
            DataType.TAB_TAT_DEFINES_TARGET                                     : [''],
            DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG                             : [''],
            DataType.TAB_TAT_DEFINES_TARGET_ARCH                                : ['']
        }
        if filename != None:
            self.LoadTargetTxtFile(filename)

    def LoadTargetTxtFile(self, filename):
        if os.path.exists(filename) and os.path.isfile(filename):
             return self.ConvertTextFileToDict(filename, '#', '=')
        else:
            raise ParseError('LoadTargetTxtFile() : No Target.txt file exist')
            return 1

#
# Convert a text file to a dictionary
#
    def ConvertTextFileToDict(self, FileName, CommentCharacter, KeySplitCharacter):
        """Convert a text file to a dictionary of (name:value) pairs."""
        try:
            f = open(FileName,'r')
            for Line in f:
                if Line.startswith(CommentCharacter) or Line.strip() == '':
                    continue
                LineList = Line.split(KeySplitCharacter,1)
                if len(LineList) >= 2:
                    Key = LineList[0].strip()
                    if Key.startswith(CommentCharacter) == False and Key in self.TargetTxtDictionary.keys():
                        if Key == DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM or Key == DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF \
                          or Key == DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD or Key == DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER \
                          or Key == DataType.TAB_TAT_DEFINES_ACTIVE_MODULE:
                            self.TargetTxtDictionary[Key] = LineList[1].replace('\\', '/').strip()
                        elif Key == DataType.TAB_TAT_DEFINES_TARGET or Key == DataType.TAB_TAT_DEFINES_TARGET_ARCH \
                          or Key == DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG:
                            self.TargetTxtDictionary[Key] = LineList[1].split()
            f.close()
            return 0
        except:
            EdkLogger.info('Open file failed')
            return 1

    def printDict(dict):
        if dict != None:
            KeyList = dict.keys()
            for Key in KeyList:
                if dict[Key] != '':
                    print Key + ' = ' + str(dict[Key])

    def printList(key, list):
        if type(list) == type([]):
            if len(list) > 0:
                if key.find(TAB_SPLIT) != -1:
                    print "\n" + key
                    for i in list:
                        print i

def TargetTxtDict(WorkSpace):
    Target = TargetTxtClassObject()
    Target.LoadTargetTxtFile(WorkSpace + '\\Conf\\target.txt')
    return Target


if __name__ == '__main__':
    pass
    Target = TargetTxtDict(os.getenv("WORKSPACE"))
    print Target.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER]
    print Target.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]