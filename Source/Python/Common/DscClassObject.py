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
from CommonDataClass.CommonClass import SkuInfoClass
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
        self.Identification = Identification()
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
            TAB_COMPONENTS
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
            
    def LoadDscFile(self, Filename):
        (Filepath, Name) = os.path.split(Filename)
        self.Identification.FileName = Name
        self.Identification.FileFullPath = Filename
        self.Identification.FileRelativePath = Filepath
        
        F = open(Filename, 'r').read()
        PreCheck(Filename, F, self.KeyList)
        sects = F.split('[')
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
        self.Platform.Header.Name = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_NAME][0]
        self.Platform.Header.Guid = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_GUID][0]
        self.Platform.Header.Version = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_PLATFORM_VERSION][0]
        self.Platform.Header.FileName = self.Identification.FileName
        self.Platform.Header.FullPath = self.Identification.FileFullPath
        self.Platform.Header.DscSpecification = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_DSC_SPECIFICATION][0]
        
        self.Platform.Header.SkuIdName = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_SKUID_IDENTIFIER]
        self.Platform.Header.SupArchList = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES]
        self.Platform.Header.BuildTargets = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_BUILD_TARGETS]
        self.Platform.Header.OutputDirectory = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_OUTPUT_DIRECTORY][0]
        self.Platform.Header.BuildNumber = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_BUILD_NUMBER][0]
        self.Platform.Header.MakefileName = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_MAKEFILE_NAME][0]
        
        Fdf = PlatformFlashDefinitionFileClass()
        Fdf.FilePath = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_FLASH_DEFINITION][0]
        self.Platform.FlashDefinitionFile = Fdf
        
        #BuildOptions
        BuildOptions = {}
        IncludeFiles = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].BuildOptions:
                if GenInclude(Item, IncludeFiles, Arch):
                    continue
                MergeArches(BuildOptions, GetBuildOption(Item), Arch)
        self.Platform.BuildOptions.IncludeFiles = IncludeFiles
        for Key in BuildOptions.keys():
            BuildOption = BuildOptionClass(Key[0], Key[1], Key[2])
            BuildOption.SupArchList = BuildOptions[Key]
            self.Platform.BuildOptions.BuildOptionList.append(BuildOption)
        
        #SkuIds
        IncludeFiles = {}
        self.Platform.SkuInfos.SkuInfoList['DEFAULT'] = '0'
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].SkuIds:
                if GenInclude(Item, IncludeFiles, Arch):
                    continue
                List = GetSplitValueList(Item)
                if len(List) != 2:
                    ErrorMsg = "Wrong statement '%s' found in section SkuIds in file '%s', correct format is '<Integer>|<UiName>'" % (Item, self.Platform.Header.FullPath)
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    self.Platform.SkuInfos.SkuInfoList[List[1]] = List[0]
        self.Platform.SkuInfos.IncludeFiles = IncludeFiles
        
        #Libraries
        Libraries = {}
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Libraries:
                if GenInclude(Item, IncludeFiles, Arch):
                    continue
                Status = GenDefines(Item, Arch, Defines)
                if Status == 0:       # Find DEFINE statement
                    pass
                elif Status == -1:    # Find DEFINE statement but in wrong format
                    ErrorMsg = "Wrong DEFINE statement '%s' found in section Libraries in file '%s', correct format is 'DEFINE <VarName> = <PATH>'" % (Item, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                elif Status == 1:     # Not find DEFINE statement
                    MergeArches(Libraries, Item, Arch)
        self.Platform.Libraries.IncludeFiles = IncludeFiles
        for Key in Libraries.keys():
            Library = PlatformLibraryClass()
            Library.FilePath = Key
            Library.Define = Defines
            Library.SupArchList = Libraries[Key]
            self.Platform.Libraries.LibraryList.append(Library)
        
        #LibraryClasses
        LibraryClasses = {}
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].LibraryClasses:
                if GenInclude(Item[0], IncludeFiles, Arch):
                    continue
                Status = GenDefines(Item[0], Arch, Defines)
                if Status == 0:       # Find DEFINE statement
                    pass
                elif Status == -1:    # Find DEFINE statement but in wrong format
                    ErrorMsg = "Wrong DEFINE statement '%s' found in section LibraryClasses in file '%s', correct format is 'DEFINE <VarName> = <PATH>'" % (Item, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                elif Status == 1:     # Not find DEFINE statement
                    List = GetSplitValueList(Item[0])
                    if len(List) != 2:
                        ErrorMsg = "Wrong statement '%s' found in section LibraryClasses in file '%s', correct format is '<LibraryClassKeyWord>|<LibraryInstance>'" % (Item, self.Platform.Header.FullPath) 
                        raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                    else:
                        if Item[1] == ['']:
                            Item[1] = DataType.SUP_MODULE_LIST
                        MergeArches(LibraryClasses, (List[0], List[1]) + tuple(Item[1]), Arch)
        self.Platform.LibraryClasses.IncludeFiles = IncludeFiles
        for Key in LibraryClasses.keys():
            Library = PlatformLibraryClass()
            Library.Name = Key[0]
            Library.FilePath = Key[1]
            Library.ModuleType = list(Key[2:])
            Library.Define = Defines
            Library.SupArchList = LibraryClasses[Key]
            self.Platform.LibraryClasses.LibraryList.append(Library)
        
        #Pcds
        self.GenPcds(DataType.TAB_PCDS_FIXED_AT_BUILD)
        self.GenPcds(DataType.TAB_PCDS_PATCHABLE_IN_MODULE)
        self.GenPcds(DataType.TAB_PCDS_FEATURE_FLAG)
        self.GenDynamicDefaultPcds(DataType.TAB_PCDS_DYNAMIC_DEFAULT)
        self.GenDynamicDefaultPcds(DataType.TAB_PCDS_DYNAMIC_EX_DEFAULT)
        self.GenDynamicHiiPcds(DataType.TAB_PCDS_DYNAMIC_HII)
        self.GenDynamicHiiPcds(DataType.TAB_PCDS_DYNAMIC_EX_HII)
        self.GenDynamicVpdPcds(DataType.TAB_PCDS_DYNAMIC_VPD)
        self.GenDynamicVpdPcds(DataType.TAB_PCDS_DYNAMIC_EX_VPD)
        
        #Components
        Components = {}
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Components:
                (InfFilename, ExecFilename) = GetExec(Item[0])
                LibraryClasses = Item[1]
                BuildOptions = Item[2]
                Pcds = Item[3]
                Component = PlatformModuleClass()
                Component.FilePath = InfFilename
                Component.ExecFilePath = ExecFilename
                for Lib in LibraryClasses:
                    List = GetSplitValueList(Lib)
                    if len(List) != 2:
                        ErrorMsg = "Wrong LibraryClass statement '%s' found in section Components in file '%s', correct format is '<ClassName>|<InfFilename>'" % (Lib, self.Platform.Header.FullPath) 
                        raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                    Component.LibraryClasses.LibraryList.append(PlatformLibraryClass(List[0], List[1]))
                for BuildOption in BuildOptions:
                    Key = GetBuildOption(BuildOption)
                    Component.ModuleSaBuildOption.BuildOptionList.append(BuildOptionClass(Key[0], Key[1], Key[2]))
                for Pcd in Pcds:
                    Type = Pcd[0]
                    List = GetSplitValueList(Pcd[1])
                    if Type == DataType.TAB_PCDS_FEATURE_FLAG:
                        if len(List) != 3:
                            ErrorMsg = "Wrong Pcds%s statement '%s' found in section Components in file '%s', correct format is '<Cname>|<TokenSpaceGuidCName>|<TrueFalse>'" % (Type, Pcd[1], self.Platform.Header.FullPath) 
                            raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                        else:
                            Component.PcdBuildDefinitions.append(PcdClass(List[0], '', List[1], '', '', List[2], Type, [], {}, []))
                    if Type == DataType.TAB_PCDS_FIXED_AT_BUILD or Type == DataType.TAB_PCDS_PATCHABLE_IN_MODULE:
                        if len(List.append('')) < 4:
                            ErrorMsg = "Wrong Pcds%s statement '%s' found in section Components in file '%s', correct format is '<Cname>|<TokenSpaceGuidCName>|<Value>[|<MaxDatumSize>]'" % (Type, Pcd[1], self.Platform.Header.FullPath) 
                            raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                        else:
                            Component.PcdBuildDefinitions.append(PcdClass(List[0], '', List[1], '', List[3], List[2], Type, [], {}, []))
                    if Type == DataType.TAB_PCDS_DYNAMIC or Type == DataType.TAB_PCDS_DYNAMIC_EX:
                        if len(List) != 2:
                            ErrorMsg = "Wrong Pcds%s statement '%s' found in section Components in file '%s', correct format is '<Cname>|<TokenSpaceGuidCName>|<Value>[|<MaxDatumSize>]'" % (Type, Pcd[1], self.Platform.Header.FullPath) 
                            raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                        else:
                            Component.PcdBuildDefinitions.append(PcdClass(List[0], '', List[1], '', List[3], List[2], Type, [], {}, []))                        
                    
                if GenInclude(Item[0], IncludeFiles, Arch):
                    continue
                Status = GenDefines(Item[0], Arch, Defines)
                if Status == 0:       # Find DEFINE statement
                    pass
                elif Status == -1:    # Find DEFINE statement but in wrong format
                    ErrorMsg = "Wrong DEFINE statement '%s' found in section LibraryClasses in file '%s', correct format is 'DEFINE <VarName> = <PATH>'" % (Item, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                elif Status == 1:     # Not find DEFINE statement
                    MergeArches(Components, Component, Arch)
        self.Platform.Modules.IncludeFiles = IncludeFiles
        for Key in Components.keys():
            Key.Define = Defines
            Key.SupArchList = Components[Key]
            self.Platform.Modules.ModuleList.append(Key)
        
    #End of DscToPlatform
    
    def GenPcds(self, Type = ''):
        Pcds = {}
        Items = []
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_FIXED_AT_BUILD:
                Items = self.Contents[Arch].PcdsFixedAtBuild
            elif Type == DataType.TAB_PCDS_PATCHABLE_IN_MODULE:
                Items = self.Contents[Arch].PcdsPatchableInModule
            elif Type == DataType.TAB_PCDS_FEATURE_FLAG:
                Items = self.Contents[Arch].PcdsFeatureFlag
            else:
                pass
            
            for Item in Items:
                List = GetSplitValueList(Item + DataType.TAB_VALUE_SPLIT)
                if len(List) < 4:
                    ErrorMsg = "Wrong statement '%s' found in section %s in file '%s', correct format is '<PcdTokenName>|<PcdTokenSpaceGuidCName>|<Value>[|<MaximumDatumSize>]'" % (Item, Type, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Pcds, (List[0], List[1], List[2], List[3], Type), Arch)
        for Key in Pcds:
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[3], Key[2], Key[4], [], {}, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)
    
    def GenSkuInfoList(self, SkuNameList, SkuInfo, VariableName = '', VariableGuid = '', VariableOffset = '', HiiDefaultValue = '', VpdOffset = '', DefaultValue = ''):
        if SkuNameList == None or SkuNameList == [] or SkuNameList == ['']:
                SkuNameList = ['DEFAULT']
        SkuInfoList = {}
        for Item in SkuNameList:
            if Item not in SkuInfo:
                return False, Item
            Sku = SkuInfoClass(Item, SkuInfo[Item], VariableName, VariableGuid, VariableOffset, HiiDefaultValue, VpdOffset, DefaultValue)
            SkuInfoList[Item] = Sku
        
        return True, SkuInfoList
            
    def GenDynamicDefaultPcds(self, Type = ''):
        Pcds = {}
        Items = []
        SkuInfoList = {}
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_DYNAMIC_DEFAULT:
                Items = self.Contents[Arch].PcdsDynamicDefault
            elif Type == DataType.TAB_PCDS_DYNAMIC_EX_DEFAULT:
                Items = self.Contents[Arch].PcdsDynamicExDefault
            else:
                pass
            
            for Item in Items:
                List = GetSplitValueList(Item[0] + DataType.TAB_VALUE_SPLIT)
                if len(List) < 4:
                    ErrorMsg = "Wrong statement '%s' found in section %s in file '%s', correct format is '<PcdTokenName>|<PcdTokenSpaceGuidCName>|<Value>[|<MaximumDatumSize>]'" % (Item, Type, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Pcds, (List[0], List[1], List[2], List[3], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, '', '', '', '', '', Key[2])
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' not defined in file '%s'" % (SkuInfoList, Type, self.Platform.Header.FullPath) 
                raise ParserError(PARSER_ERROR, msg = ErrorMsg)
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[3], '', Key[4], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)
         
    def GenDynamicHiiPcds(self, Type = ''):
        Pcds = {}
        Items = []
        SkuInfoList = {}
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_DYNAMIC_HII:
                Items = self.Contents[Arch].PcdsDynamicHii
            elif Type == DataType.TAB_PCDS_DYNAMIC_EX_HII:
                Items = self.Contents[Arch].PcdsDynamicExHii
            else:
                pass
            
            for Item in Items:
                List = GetSplitValueList(Item[0] + DataType.TAB_VALUE_SPLIT)
                if len(List) < 7:
                    ErrorMsg = "Wrong statement '%s' found in section %s in file '%s', correct format is '<PcdTokenName>|<PcdTokenSpaceGuidCName>|<String>|<VariableGuidCName>|<VariableOffset>|<DefaultValue>[|<MaximumDatumSize>]'" % (Item, Type, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4], List[5], List[6], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, List[2], List[3], List[4], List[5], '', '')
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' not defined in file '%s'" % (SkuInfoList, Type, self.Platform.Header.FullPath) 
                raise ParserError(PARSER_ERROR, msg = ErrorMsg)
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[3], '', Key[7], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)
    
    def GenDynamicVpdPcds(self, Type = ''):
        Pcds = {}
        Items = []
        SkuInfoList = {}
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_DYNAMIC_VPD:
                Items = self.Contents[Arch].PcdsDynamicVpd
            elif Type == DataType.TAB_PCDS_DYNAMIC_EX_VPD:
                Items = self.Contents[Arch].PcdsDynamicExVpd
            else:
                pass
            
            for Item in Items:
                List = GetSplitValueList(Item[0] + DataType.TAB_VALUE_SPLIT)
                if len(List) < 4:
                    ErrorMsg = "Wrong statement '%s' found in section %s in file '%s', correct format is '<PcdTokenName>|<PcdTokenSpaceGuidCName>|<DefaultValue>[|<MaximumDatumSize>]'" % (Item, Type, self.Platform.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Pcds, (List[0], List[1], List[2], List[3], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, '', '', '', '', List[2], '')
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' not defined in file '%s'" % (SkuInfoList, Type, self.Platform.Header.FullPath) 
                raise ParserError(PARSER_ERROR, msg = ErrorMsg)
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[3], '', Key[4], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)
    
    def ShowDsc(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for key in self.KeyList:
            for arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                                    key + DataType.TAB_SPLIT + arch + \
                                    "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
                eval(Command)
       
    def ShowPlatform(self):
        m = self.Platform
        print 'Filename =', m.Header.FileName
        print 'FullPath =', m.Header.FullPath
        print 'BaseName =', m.Header.Name
        print 'Guid =', m.Header.Guid
        print 'Version =', m.Header.Version
        print 'DscSpecification =', m.Header.DscSpecification
        print 'SkuId =', m.Header.SkuIdName
        print 'SupArchList =', m.Header.SupArchList
        print 'BuildTargets =', m.Header.BuildTargets
        print 'OutputDirectory =', m.Header.OutputDirectory
        print 'BuildNumber =', m.Header.BuildNumber
        print 'MakefileName =', m.Header.MakefileName
        print 'Fdf =', m.FlashDefinitionFile.FilePath
        print '\nBuildOptions =', m.BuildOptions, m.BuildOptions.IncludeFiles
        for Item in m.BuildOptions.BuildOptionList:
            print Item.ToolChainFamily, Item.ToolChain, Item.Option, Item.SupArchList
        print '\nSkuIds =', m.SkuInfos.SkuInfoList, m.SkuInfos.IncludeFiles
        print '\nLibraries =', m.Libraries, m.Libraries.IncludeFiles
        for Item in m.Libraries.LibraryList:
            print Item.FilePath, Item.SupArchList, Item.Define
        print '\nLibraryClasses =', m.LibraryClasses, m.LibraryClasses.IncludeFiles
        for Item in m.LibraryClasses.LibraryList:
            print Item.Name, Item.FilePath, Item.ModuleType, Item.SupArchList, Item.Define
        print '\nPcds =', m.DynamicPcdBuildDefinitions
        for Item in m.DynamicPcdBuildDefinitions:
            print Item.CName, Item.TokenSpaceGuidCName, Item.DefaultValue, Item.Token, Item.ItemType, Item.MaxDatumSize, Item.SupArchList, Item.SkuInfoList
        print '\nComponents =', m.Modules.ModuleList, m.Modules.IncludeFiles
        for Item in m.Modules.ModuleList:
            print Item.FilePath, Item.ExecFilePath, Item.SupArchList
            for Lib in Item.LibraryClasses.LibraryList:
                print Lib.Name, Lib.FilePath
            for Bo in Item.ModuleSaBuildOption.BuildOptionList:
                print Bo.ToolChainFamily, Bo.ToolChain, Bo.Option
            for Pcd in Item.PcdBuildDefinitions:
                print Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.MaxDatumSize, Pcd.DefaultValue, Pcd.ItemType
    
if __name__ == '__main__':
    p = Dsc()
    directory = 'C:\MyWorkspace\Nt32Pkg'
    fileList = []
    for f in os.listdir(directory):
        if os.path.splitext(os.path.normcase(f))[1] == '.dsc':
            fileList.append(os.path.join(directory, os.path.normcase(f)))
            
    for f in fileList:
        p = Dsc(f, True, True)
        #p.ShowDsc()
        p.ShowPlatform()
