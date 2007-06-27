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
from Dictionary import *


class TargetTxtClassObject(object):
    def __init__(self, filename = None):
        self.TargetTxtDictionary = {
            DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM                            : [''],
            DataType.TAB_TAT_DEFINES_ACTIVE_MODULE                                : [''],
            DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF                            : [''],
            DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD                            : ['Disable'],
            DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER : ['2'],
            DataType.TAB_TAT_DEFINES_TARGET                                             : [''],
            DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG                             : [''],
            DataType.TAB_TAT_DEFINES_TARGET_ARCH                                    : ['']
        }
        if filename != None:
            self.LoadTargetTxtFile(filename)

    def LoadTargetTxtFile(self, filename):
        #EdkLogger.info('LoadTargetTxtFile() Start')
        if os.path.exists(filename) and os.path.isfile(filename):
            ConvertTextFileToDictionary(filename, self.TargetTxtDictionary, '#', '=', True, None)
            if self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM] == []:
                self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]                        = ['']
            else:
                self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]                        = [self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM][0]]
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF]                            = [self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF][0]]
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD]                            = [self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD][0]]
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER] = [self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER][0]]
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]                                             = list(set(self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]))
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]                             = list(set(self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]))
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]                                    = list(set(self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]))
            if self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET] == []:
                self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET] = ['']
            if self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG] == []:
                self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG] = ['']
            if self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH] == []:
                self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH] = ['']
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET].sort()
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG].sort()
            self.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH].sort()
            
            #EdkLogger.info('LoadTargetTxtFile() End')
        else:
            EdkLogger.error('LoadTargetTxtFile() : No Target.txt file exist')

if __name__ == '__main__':
    pass