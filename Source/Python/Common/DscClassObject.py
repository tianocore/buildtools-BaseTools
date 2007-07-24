# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of DSC file
#

import os
from String import *
from DataType import *
from Identification import *
from Dictionary import *
from CommonDataClass.PlatformClass import *
from BuildToolError import *

class DscObject(object):
    def __init__(self):
        object.__init__()

class DscDefines(DscObject):
    def __init__(self):
        self.DefinesDictionary = {
            #Req
            TAB_DSC_DEFINES_PLATFORM_NAME                         : [''],
            TAB_DSC_DEFINES_PLATFORM_GUID                         : [''],
            TAB_DSC_DEFINES_PLATFORM_VERSION                      : [''],
            TAB_DSC_DEFINES_DSC_SPECIFICATION                     : [''],
            TAB_DSC_DEFINES_OUTPUT_DIRECTORY                      : [''],
            TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES               : [''],
            TAB_DSC_DEFINES_BUILD_TARGETS                         : [''],
            TAB_DSC_DEFINES_SKUID_IDENTIFIER                      : [''],
            TAB_DSC_DEFINES_FLASH_DEFINITION                      : [''],
            TAB_DSC_DEFINES_BUILD_NUMBER                          : [''],
            TAB_DSC_DEFINES_MAKEFILE_NAME                         : ['']                        
        }

class DscSkuId(DscObject):
    def __init__(self):
        self.SkuId = {}         #{ [skuid : skuname], [skuid : skuname], ...}

class DscContents(DscObject):
    def __init__(self):
        self.SkuIds = []
        self.Libraries = []
        self.Components = []                #[['component name', [lib1, lib2, lib3], [bo1, bo2, bo3]], ...]
        self.LibraryClasses = []
        self.PcdsFixedAtBuild = []
        self.PcdsPatchableInModule = []
        self.PcdsFeatureFlag = []
        self.PcdsDynamicDefault = []
        self.PcdsDynamicVpd = []
        self.PcdsDynamicHii = []       
        self.PcdsDynamicExDefault = []
        self.PcdsDynamicExVpd = []
        self.PcdsDynamicExHii = []                
        self.BuildOptions = []

class Dsc(DscObject):
    def __init__(self, filename = None, isMergeAllArches = False, isToPlatform = False):
        self.identification = Identification()
        self.Defines = DscDefines()
        self.Contents = {}
        self.UserExtensions = ''
        self.Platform = PlatformClass()

        for key in DataType.ARCH_LIST_FULL:
            self.Contents[key] = DscContents()
        
        self.KeyList = [
            TAB_SKUIDS, TAB_LIBRARIES, TAB_LIBRARY_CLASSES, TAB_BUILD_OPTIONS, TAB_PCDS_FIXED_AT_BUILD_NULL, \
            TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
            TAB_PCDS_DYNAMIC_DEFAULT_NULL, TAB_PCDS_DYNAMIC_HII_NULL, TAB_PCDS_DYNAMIC_VPD_NULL, \
            TAB_PCDS_DYNAMIC_EX_DEFAULT_NULL, TAB_PCDS_DYNAMIC_EX_HII_NULL, TAB_PCDS_DYNAMIC_EX_VPD_NULL, \
            TAB_COMPONENTS, TAB_BUILD_OPTIONS
        ]
        
        if filename != None:
            self.LoadDscFile(filename)
            
        if isMergeAllArches:
            self.MergeAllArches()
        
        if isToPlatform:
            self.DscToPlatform()
        
    def ParseDsc(self, Lines, Key, KeyField):
        newKey = SplitModuleType(Key)     
        if newKey[0].find(TAB_LIBRARY_CLASSES.upper()) != -1:
            GetLibraryClassesWithModuleType(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        elif newKey[0].find(TAB_COMPONENTS.upper()) != -1:
            GetComponents(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        elif newKey[0].find(TAB_PCDS_DYNAMIC.upper()) != -1:
            GetDynamics(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        else:
            GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
    
    def MergeAllArches(self):
        for key in self.KeyList:
            for arch in DataType.ARCH_LIST:
                Command = "self.Contents[arch]." + key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ")"
                eval(Command)
            
    def LoadDscFile(self, filename):
        EdkLogger.verbose('Open Dsc File:' + filename)
        f = open(filename, 'r').read()
        sects = f.split('[')
        for sect in sects:
            tab = (sect.split(TAB_SECTION_END, 1)[0]).upper()
            if tab == TAB_INF_DEFINES.upper():
                GetSingleValueOfKeyFromLines(sect, self.Defines.DefinesDictionary, TAB_COMMENT_SPLIT, TAB_EQUAL_SPLIT, True, TAB_VALUE_SPLIT)
                continue
            for arch in DataType.ARCH_LIST_FULL + [DataType.TAB_ARCH_NULL]:
                for key in self.KeyList:
                    if arch != DataType.TAB_ARCH_NULL:
                        target = (key + DataType.TAB_SPLIT + arch).upper()
                    else:
                        target = key.upper()
                    if SplitModuleType(tab)[0] == target:
                        if arch != DataType.TAB_ARCH_NULL:
                            Command = 'self.ParseDsc(sect, tab, self.Contents[arch].' + key + ')'
                            eval(Command)
                            continue
                        else:
                            Command = "self.ParseDsc(sect, tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ')'
                            eval(Command)
                            continue

    def DscToPlatform(self):
        #
        # Get value for Header
        #
        self.Module.Header.Name = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_NAME][0]
        self.Module.Header.Guid = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_GUID][0]
        self.Module.Header.Version = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_VERSION][0]
        self.Module.Header.FileName = self.Identification.FileName
        self.Module.Header.FullPath = self.Identification.FileFullPath
        self.Module.Header.InfVersion = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_DSC_SPECIFICATION][0]
        
        
    def showDsc(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for key in self.KeyList:
            for arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                                    key + DataType.TAB_SPLIT + arch + \
                                    "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
                eval(Command)
        
if __name__ == '__main__':
    p = Dsc()
    directory = 'C:\MyWorkspace\\EdkModulePkg'
    fileList = []
    for f in os.listdir(directory):
        if os.path.splitext(os.path.normcase(f))[1] == '.dsc':
            fileList.append(os.path.join(directory, os.path.normcase(f)))
            
    for f in fileList:
        p.LoadDscFile(f)
        p.MergeAllArches()
        p.showDsc()
