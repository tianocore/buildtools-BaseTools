## @file
# This file is used to define each component of DSC file
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
import EdkLogger
from String import *
from DataType import *
from Identification import *
from Dictionary import *
from CommonDataClass.PlatformClass import *
from CommonDataClass.CommonClass import SkuInfoClass
from BuildToolError import *
from Misc import sdict

## DscObject
#
# This class defined basic Dsc object which is used by inheriting
# 
# @param object:       Inherited from object class
#
class DscObject(object):
    def __init__(self):
        object.__init__()

## DscDefines
#
# This class defined basic Defines used in Dsc object
# 
# @param DscDefines:       Inherited from DscDefines class
#
# @var DefinesDictionary:  To store value for DefinesDictionary 
#
class DscDefines(DscObject):
    def __init__(self):
        self.DefinesDictionary = {
            #
            # Required Fields
            #
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
            TAB_DSC_DEFINES_MAKEFILE_NAME                         : [''],
            TAB_DSC_DEFINES_BS_BASE_ADDRESS                       : [''],
            TAB_DSC_DEFINES_RT_BASE_ADDRESS                       : [''],
            TAB_DSC_DEFINES_DEFINE                                : ['']
        }

## DscSkuId
#
# This class defined SkuId used in Dsc object
# 
# @param DscObject:  Inherited from DscObject class
#
# @var SkuId:        To store value for SkuId, it is a set structure as
#                    { [skuid : skuname], [skuid : skuname], ...}
#
class DscSkuId(DscObject):
    def __init__(self):
        self.SkuId = {}

## DscContents
#
# This class defined basic Contents used in Dsc object
# 
# @param DscObject:   Inherited from DscObject class
#
# @var SkuIds:                 To store value for SkuIds
# @var Libraries:              To store value for Libraries
# @var Components:             To store value for Components, it is a list structure as
#                              [['component name', [lib1, lib2, lib3], [bo1, bo2, bo3]], ...]
# @var LibraryClasses:         To store value for LibraryClasses
# @var PcdsFixedAtBuild:       To store value for PcdsFixedAtBuild
# @var PcdsPatchableInModule:  To store value for PcdsPatchableInModule
# @var PcdsFeatureFlag:        To store value for PcdsFeatureFlag
# @var PcdsDynamicDefault:     To store value for PcdsDynamicDefault
# @var PcdsDynamicVpd:         To store value for PcdsDynamicVpd
# @var PcdsDynamicHii:         To store value for PcdsDynamicHii
# @var PcdsDynamicExDefault:   To store value for PcdsDynamicExDefault
# @var PcdsDynamicExVpd:       To store value for PcdsDynamicExVpd
# @var PcdsDynamicExHii:       To store value for PcdsDynamicExHii
#
class DscContents(DscObject):
    def __init__(self):
        self.SkuIds = []
        self.Libraries = []
        self.Components = []
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

## Dsc
#
# This class defined the structure used in Dsc object
# 
# @param DscObject:         Inherited from InfObject class
# @param Ffilename:         Input value for Ffilename of Inf file, default is None
# @param IsMergeAllArches:  Input value for IsMergeAllArches
#                           True is to merge all arches
#                           Fales is not to merge all arches
#                           default is False
# @param IsToPlatform:      Input value for IsToPlatform
#                           True is to transfer to ModuleObject automatically
#                           False is not to transfer to ModuleObject automatically
#                           default is False
# @param WorkspaceDir:      Input value for current workspace directory, default is None
#
# @var _NullClassIndex:     To store value for _NullClassIndex, default is 0
# @var Identification:      To store value for Identification, it is a structure as Identification
# @var Defines:             To store value for Defines, it is a structure as DscDefines
# @var Contents:            To store value for Contents, it is a structure as DscContents
# @var UserExtensions:      To store value for UserExtensions
# @var Platform:            To store value for Platform, it is a structure as PlatformClass
# @var WorkspaceDir:        To store value for WorkspaceDir
# @var KeyList:             To store value for KeyList, a list for all Keys used in Dec
#
class Dsc(DscObject):
    _NullClassIndex = 0

    def __init__(self, Filename = None, IsMergeAllArches = False, IsToPlatform = False, WorkspaceDir = None):
        self.Identification = Identification()
        self.Defines = DscDefines()
        self.Contents = {}
        self.UserExtensions = ''
        self.Platform = PlatformClass()
        self.WorkspaceDir = WorkspaceDir

        for Arch in DataType.ARCH_LIST_FULL:
            self.Contents[Arch] = DscContents()

        self.KeyList = [
            TAB_SKUIDS, TAB_LIBRARIES, TAB_LIBRARY_CLASSES, TAB_BUILD_OPTIONS, TAB_PCDS_FIXED_AT_BUILD_NULL, \
            TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
            TAB_PCDS_DYNAMIC_DEFAULT_NULL, TAB_PCDS_DYNAMIC_HII_NULL, TAB_PCDS_DYNAMIC_VPD_NULL, \
            TAB_PCDS_DYNAMIC_EX_DEFAULT_NULL, TAB_PCDS_DYNAMIC_EX_HII_NULL, TAB_PCDS_DYNAMIC_EX_VPD_NULL, \
            TAB_COMPONENTS
        ]

        #
        # Load Dsc file if filename is not None
        #
        if Filename != None:
            self.LoadDscFile(Filename)

        #
        # Merge contents of Dsc from all arches if IsMergeAllArches is True
        #
        if IsMergeAllArches:
            self.MergeAllArches()

        #
        # Transfer to Platform Object if IsToPlatform is True
        #
        if IsToPlatform:
            self.DscToPlatform()

    ## Parse Dsc file
    #
    # Go through input lines one by one to find the value defined in Key section.
    # Save them to KeyField
    #
    # @param Lines:     Lines need to be parsed
    # @param Key:       The key value of the section to be located
    # @param KeyField:  To save the found contents
    #
    def ParseDsc(self, Lines, Key, KeyField):
        newKey = SplitModuleType(Key)
        if newKey[0].upper().find(TAB_LIBRARY_CLASSES.upper()) != -1:
            GetLibraryClassesWithModuleType(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        elif newKey[0].upper().find(TAB_COMPONENTS.upper()) != -1:
            GetComponents(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        elif newKey[0].upper().find(TAB_PCDS_DYNAMIC.upper()) != -1:
            GetDynamics(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        else:
            GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)

    ## Merge contents of Dsc from all arches
    #
    # Find the contents defined in all arches and merge them to all
    #
    def MergeAllArches(self):
        for Key in self.KeyList:
            for Arch in DataType.ARCH_LIST:
                Command = "self.Contents[Arch]." + Key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + Key + ")"
                eval(Command)

    ## Load Dsc file
    #
    # Load the file if it exists
    #
    # @param Filename:  Input value for filename of Dsc file
    #
    def LoadDscFile(self, Filename):
        (Filepath, Name) = os.path.split(Filename)
        self.Identification.FileName = Name
        self.Identification.FileFullPath = Filename
        self.Identification.FileRelativePath = Filepath

        F = open(Filename, 'r').read()
        PreCheck(Filename, F, self.KeyList)
        Sects = F.split(DataType.TAB_SECTION_START)
        for Sect in Sects:
            TabList = GetSplitValueList(Sect.split(TAB_SECTION_END, 1)[0], DataType.TAB_COMMA_SPLIT)
            for Tab in TabList:
                if Tab.upper() == TAB_INF_DEFINES.upper():
                    GetSingleValueOfKeyFromLines(Sect, self.Defines.DefinesDictionary, TAB_COMMENT_SPLIT, TAB_EQUAL_SPLIT, True, TAB_VALUE_SPLIT)
                    continue
                for Arch in DataType.ARCH_LIST_FULL + [DataType.TAB_ARCH_NULL]:
                    for Key in self.KeyList:
                        if Arch != DataType.TAB_ARCH_NULL:
                            Target = (Key + DataType.TAB_SPLIT + Arch).upper()
                        else:
                            Target = Key.upper()
                        if SplitModuleType(Tab)[0].upper() == Target:
                            if Arch != DataType.TAB_ARCH_NULL:
                                Command = 'self.ParseDsc(Sect, Tab, self.Contents[Arch].' + Key + ')'
                                eval(Command)
                                continue
                            else:
                                Command = "self.ParseDsc(Sect, Tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + Key + ')'
                                eval(Command)
                                continue

    ## Transfer to Platform Object
    # 
    # Transfer all contents of an Inf file to a standard Module Object
    #
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
        File = self.Platform.Header.FullPath

        self.Platform.Header.SkuIdName = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_SKUID_IDENTIFIER]
        self.Platform.Header.SupArchList = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES]
        self.Platform.Header.BuildTargets = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_BUILD_TARGETS]
        self.Platform.Header.OutputDirectory = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_OUTPUT_DIRECTORY][0]
        self.Platform.Header.BuildNumber = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_BUILD_NUMBER][0]
        self.Platform.Header.MakefileName = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_MAKEFILE_NAME][0]

        self.Platform.Header.BsBaseAddress = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_BS_BASE_ADDRESS][0]
        self.Platform.Header.RtBaseAddress = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_RT_BASE_ADDRESS][0]

        #
        # Define of Defines
        #
        if self.Defines.DefinesDictionary[TAB_DSC_DEFINES_DEFINE][0] != '':
            for Item in self.Defines.DefinesDictionary[TAB_DSC_DEFINES_DEFINE]:
                List = Item.split(DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    RaiseParserError(Item, 'DEFINE of Defines', File, 'DEFINE <MACRO> = <PATH>')
                else:
                    self.Platform.Header.Define[CleanString(List[0])] = CleanString(List[1])

        Fdf = PlatformFlashDefinitionFileClass()
        Fdf.FilePath = self.Defines.DefinesDictionary[TAB_DSC_DEFINES_FLASH_DEFINITION][0]
        self.Platform.FlashDefinitionFile = Fdf

        #
        # BuildOptions
        # [<Family>:]<ToolFlag>=Flag
        #
        BuildOptions = {}
        IncludeFiles = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].BuildOptions:
                if GenInclude(Item, IncludeFiles, Arch):
                    IncludeFile = CleanString(Item[Item.upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
                    CheckFileExist(self.WorkspaceDir, IncludeFile, self.Platform.Header.FullPath, 'BuildOptions', Item)
                    for NewItem in open(WorkspaceFile(self.WorkspaceDir, IncludeFile), 'r').readlines():
                        MergeArches(BuildOptions, GetBuildOption(NewItem, File), Arch)
                    continue
                MergeArches(BuildOptions, GetBuildOption(Item, File), Arch)

        self.Platform.BuildOptions.IncludeFiles = IncludeFiles
        for Key in BuildOptions.keys():
            BuildOption = BuildOptionClass(Key[0], Key[1], Key[2])
            BuildOption.SupArchList = BuildOptions[Key]
            self.Platform.BuildOptions.BuildOptionList.append(BuildOption)

        #
        # SkuIds
        # <Integer>|<UiName>
        #
        IncludeFiles = {}
        self.Platform.SkuInfos.SkuInfoList['DEFAULT'] = '0'
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].SkuIds:
                if GenInclude(Item, IncludeFiles, Arch):
                    IncludeFile = CleanString(Item[Item.upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
                    CheckFileExist(self.WorkspaceDir, IncludeFile, self.Platform.Header.FullPath, 'SkuIds', Item)
                    for NewItem in open(WorkspaceFile(self.WorkspaceDir, IncludeFile), 'r').readlines():
                        List = GetSplitValueList(NewItem)
                        if len(List) != 2:
                            RaiseParserError(NewItem, 'SkuIds', WorkspaceFile(self.WorkspaceDir, IncludeFile), '<Integer>|<UiName>')
                        else:
                            self.Platform.SkuInfos.SkuInfoList[List[1]] = List[0]
                    continue
                List = GetSplitValueList(Item)
                if len(List) != 2:
                    RaiseParserError(Item, 'SkuIds', File, '<Integer>|<UiName>')
                else:
                    self.Platform.SkuInfos.SkuInfoList[List[1]] = List[0]
        self.Platform.SkuInfos.IncludeFiles = IncludeFiles

        #
        # Libraries
        # <PathAndFilename>
        #
        Libraries = {}
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Libraries:
                if GenInclude(Item, IncludeFiles, Arch):
                    IncludeFile = CleanString(Item[Item.upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
                    CheckFileExist(self.WorkspaceDir, IncludeFile, self.Platform.Header.FullPath, 'Libraries', Item)
                    for NewItem in open(WorkspaceFile(self.WorkspaceDir, IncludeFile), 'r').readlines():
                        MergeArches(Libraries, Item, Arch)
                    continue
                Status = GenDefines(Item, Arch, Defines)
                #
                # Find DEFINE statement
                #
                if Status == 0:
                    pass
                #
                # Find DEFINE statement but in wrong format
                #
                elif Status == -1:
                    RaiseParserError(Item, 'Libraries', File, 'DEFINE <VarName> = <PATH>')
                #
                # Not find DEFINE statement
                #
                elif Status == 1:
                    MergeArches(Libraries, Item, Arch)
        self.Platform.Libraries.IncludeFiles = IncludeFiles
        for Key in Libraries.keys():
            Library = PlatformLibraryClass()
            Library.FilePath = Key
            Library.Define = Defines
            Library.SupArchList = Libraries[Key]
            self.Platform.Libraries.LibraryList.append(Library)

        #
        # LibraryClasses
        # <LibraryClassKeyWord>|<LibraryInstance>
        #
        LibraryClasses = {}
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].LibraryClasses:
                if GenInclude(Item[0], IncludeFiles, Arch):
                    IncludeFile = CleanString(Item[0][Item[0].upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
                    IncludeFilePath = WorkspaceFile(self.WorkspaceDir, IncludeFile)
                    CheckFileExist(self.WorkspaceDir, IncludeFile, self.Platform.Header.FullPath, 'LibraryClasses', Item[0])
                    for NewItem in open(IncludeFilePath, 'r').readlines():
                        MergeArches(LibraryClasses, self.GenLibraryClass([NewItem, Item[1]], IncludeFilePath), Arch)
                    continue
                Status = GenDefines(Item[0], Arch, Defines)
                #
                # Find DEFINE statement
                #
                if Status == 0:
                    pass
                #
                # Find DEFINE statement but in wrong format
                #
                elif Status == -1:
                    RaiseParserError(Item[0], 'LibraryClasses', File, 'DEFINE <VarName> = <PATH>')
                #
                # Not find DEFINE statement
                #
                elif Status == 1:
                    MergeArches(LibraryClasses, self.GenLibraryClass(Item, self.Platform.Header.FullPath), Arch)
        self.Platform.LibraryClasses.IncludeFiles = IncludeFiles
        for Key in LibraryClasses.keys():
            Library = PlatformLibraryClass()
            Library.Name = Key[0]
            Library.FilePath = Key[1]
            Library.SupModuleList = list(Key[2:])
            Library.Define = Defines
            Library.SupArchList = LibraryClasses[Key]
            self.Platform.LibraryClasses.LibraryList.append(Library)

        #
        # Pcds
        #
        self.GenPcds(DataType.TAB_PCDS_FIXED_AT_BUILD, File)
        self.GenPcds(DataType.TAB_PCDS_PATCHABLE_IN_MODULE, File)
        self.GenFeatureFlagPcds(DataType.TAB_PCDS_FEATURE_FLAG, File)
        self.GenDynamicDefaultPcds(DataType.TAB_PCDS_DYNAMIC_DEFAULT, File)
        self.GenDynamicDefaultPcds(DataType.TAB_PCDS_DYNAMIC_EX_DEFAULT, File)
        self.GenDynamicHiiPcds(DataType.TAB_PCDS_DYNAMIC_HII, File)
        self.GenDynamicHiiPcds(DataType.TAB_PCDS_DYNAMIC_EX_HII, File)
        self.GenDynamicVpdPcds(DataType.TAB_PCDS_DYNAMIC_VPD, File)
        self.GenDynamicVpdPcds(DataType.TAB_PCDS_DYNAMIC_EX_VPD, File)

        #
        # Components
        #
        Components = sdict()
        IncludeFiles = {}
        Defines = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Components:
                if GenInclude(Item[0], IncludeFiles, Arch):
                    IncludeFile = CleanString(Item[0][Item[0].upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
                    IncludeFilePath = WorkspaceFile(self.WorkspaceDir, IncludeFile)
                    CheckFileExist(self.WorkspaceDir, IncludeFile, self.Platform.Header.FullPath, 'Components', Item[0])
                    NewItems = []
                    GetComponents(open(IncludeFilePath, 'r').read(), TAB_COMPONENTS, NewItems, TAB_COMMENT_SPLIT)
                    for NewItem in NewItems:
                        MergeArches(Components, self.GenComponent(NewItem, IncludeFilePath), Arch)
                    continue
                Status = GenDefines(Item[0], Arch, Defines)
                #
                # Find DEFINE statement
                #
                if Status == 0:
                    pass
                #
                # Find DEFINE statement but in wrong format
                #
                elif Status == -1:
                    RaiseParserError(Item[0], 'Components', File, 'DEFINE <VarName> = <PATH>')
                #
                # Not find DEFINE statement
                #
                elif Status == 1:
                    MergeArches(Components, self.GenComponent(Item, self.Platform.Header.FullPath), Arch)
        self.Platform.Modules.IncludeFiles = IncludeFiles
        for Key in Components.keys():
            Key.Define = Defines
            Key.SupArchList = Components[Key]
            self.Platform.Modules.ModuleList.append(Key)

    #End of DscToPlatform

    ## Get Library Class
    #
    # Get Library of Dsc as <LibraryClassKeyWord>|<LibraryInstance>
    # 
    # @param Item:           String as <LibraryClassKeyWord>|<LibraryInstance>
    # @param ContainerFile:  The file which describes the library class, used for error report
    #
    # @retval (LibraryClassKeyWord, LibraryInstance, [SUP_MODULE_LIST]) Formatted Library Item
    #
    def GenLibraryClass(self, Item, ContainerFile):
        List = GetSplitValueList(Item[0])
        if len(List) != 2:
            RaiseParserError(Item[0], 'LibraryClasses', ContainerFile, '<LibraryClassKeyWord>|<LibraryInstance>')
        else:
            CheckFileType(List[1], '.Inf', ContainerFile, 'library class instance', Item[0])
            CheckFileExist(self.WorkspaceDir, List[1], ContainerFile, 'LibraryClasses', Item[0])
            if Item[1] == ['']:
                Item[1] = DataType.SUP_MODULE_LIST
        return (List[0], List[1]) + tuple(Item[1])

    ## Get Component 
    #
    # Get Component section defined in Dsc file
    #
    # @param Item:           Contents includes a component block
    # @param ContainerFile:  The file which describes the library class, used for error report
    #
    # @retval PlatformModuleClass() A instance for PlatformModuleClass
    #
    def GenComponent(self, Item, ContainerFile):
        (InfFilename, ExecFilename) = GetExec(Item[0])
        CheckFileType(InfFilename, '.Inf', ContainerFile, 'component name', Item[0])
        CheckFileExist(self.WorkspaceDir, InfFilename, ContainerFile, 'component', Item[0])
        LibraryClasses = Item[1]
        BuildOptions = Item[2]
        Pcds = Item[3]
        Component = PlatformModuleClass()
        Component.FilePath = InfFilename
        Component.ExecFilePath = ExecFilename
        for Lib in LibraryClasses:
            List = GetSplitValueList(Lib)
            if len(List) != 2:
                RaiseParserError(Lib, 'LibraryClasses', ContainerFile, '<ClassName>|<InfFilename>')
            LibName = List[0]
            LibFile = List[1]
            if LibName == "" or LibName == "NULL":
                LibName = "NULL%d" % self._NullClassIndex
                self._NullClassIndex += 1
            CheckFileType(LibFile, '.Inf', ContainerFile, 'library instance of component ', Lib)
            CheckFileExist(self.WorkspaceDir, LibFile, ContainerFile, 'library instance of component', Lib)
            Component.LibraryClasses.LibraryList.append(PlatformLibraryClass(LibName, LibFile))
        for BuildOption in BuildOptions:
            Key = GetBuildOption(BuildOption, ContainerFile)
            Component.ModuleSaBuildOption.BuildOptionList.append(BuildOptionClass(Key[0], Key[1], Key[2]))
        for Pcd in Pcds:
            Type = Pcd[0]
            List = GetSplitValueList(Pcd[1])

            #
            # For FeatureFlag
            #
            if Type == DataType.TAB_PCDS_FEATURE_FLAG:
                if len(List) != 2:
                    RaiseParserError(Pcd[1], 'Components', ContainerFile, '<PcdTokenSpaceGuidCName>.<PcdTokenName>|TRUE/FALSE')

                CheckPcdTokenInfo(List[0], 'Components', ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                Component.PcdBuildDefinitions.append(PcdClass(TokenInfo[1], '', TokenInfo[0], '', '', List[1], Type, [], {}, []))
            #
            # For FixedAtBuild or PatchableInModule
            #
            if Type == DataType.TAB_PCDS_FIXED_AT_BUILD or Type == DataType.TAB_PCDS_PATCHABLE_IN_MODULE:
                List.append('')
                if len(List) != 3 and len(List) != 4:
                    RaiseParserError(Pcd[1], 'Components', ContainerFile, '<PcdTokenSpaceGuidCName>.<PcdTokenName>|<Value>[|<MaxDatumSize>]')

                CheckPcdTokenInfo(List[0], 'Components', ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                Component.PcdBuildDefinitions.append(PcdClass(TokenInfo[1], '', TokenInfo[0], '', List[2], List[1], Type, [], {}, []))

            #
            # For Dynamic or DynamicEx
            #
            if Type == DataType.TAB_PCDS_DYNAMIC or Type == DataType.TAB_PCDS_DYNAMIC_EX:
                if len(List) != 1:
                    RaiseParserError(Pcd[1], 'Components', ContainerFile, '<PcdTokenSpaceGuidCName>.<PcdTokenName>')

                CheckPcdTokenInfo(List[0], 'Components', ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                Component.PcdBuildDefinitions.append(PcdClass(TokenInfo[1], '', TokenInfo[0], '', '', '', Type, [], {}, []))

        return Component
    #End of GenComponent

    ## Gen FeatureFlagPcds
    #
    # Gen FeatureFlagPcds of Dsc file as <PcdTokenSpaceGuidCName>.<TokenCName>|TRUE/FALSE
    #
    # @param Type:           The type of Pcd
    # @param ContainerFile:  The file which describes the pcd, used for error report
    #
    def GenFeatureFlagPcds(self, Type = '', ContainerFile = ''):
        Pcds = {}
        Items = []
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_FEATURE_FLAG:
                Items = self.Contents[Arch].PcdsFeatureFlag
            else:
                pass

            for Item in Items:
                List = GetSplitValueList(Item)
                if len(List) != 2:
                    RaiseParserError(Item, 'Pcds' + Type, ContainerFile, '<PcdTokenSpaceGuidCName>.<TokenCName>|TRUE/FALSE')

                CheckPcdTokenInfo(List[0], 'Pcds' + Type, ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                MergeArches(Pcds, (TokenInfo[1], TokenInfo[0], List[1], Type), Arch)
        for Key in Pcds:
            Pcd = PcdClass(Key[0], '', Key[1], '', '', Key[2], Key[3], [], {}, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)

    ## Gen Pcds
    #
    # Gen Pcd of Dsc as <PcdTokenSpaceGuidCName>.<TokenCName>|<Value>[|<Type>|<MaximumDatumSize>]
    #
    # @param Type:           The type of Pcd
    # @param ContainerFile:  The file which describes the pcd, used for error report
    #
    def GenPcds(self, Type = '', ContainerFile = ''):
        Pcds = {}
        Items = []
        for Arch in DataType.ARCH_LIST:
            if Type == DataType.TAB_PCDS_PATCHABLE_IN_MODULE:
                Items = self.Contents[Arch].PcdsPatchableInModule
            elif Type == DataType.TAB_PCDS_FIXED_AT_BUILD:
                Items = self.Contents[Arch].PcdsFixedAtBuild
            else:
                pass

            for Item in Items:
                List = GetSplitValueList(Item + DataType.TAB_VALUE_SPLIT * 2)
                if len(List) < 4:
                    RaiseParserError(Item, 'Pcds' + Type, ContainerFile, '<PcdTokenSpaceGuidCName>.<TokenCName>|<Value>[|<Type>|<MaximumDatumSize>]')

                CheckPcdTokenInfo(List[0], 'Pcds' + Type, ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                MergeArches(Pcds, (TokenInfo[1], TokenInfo[0], List[1], List[2], List[3], Type), Arch)
        for Key in Pcds:
            Pcd = PcdClass(Key[0], '', Key[1], Key[3], Key[4], Key[2], Key[5], [], {}, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)

    ## Gen SkuInfoList
    #
    # Gen SkuInfoList section defined in Dsc file
    #
    # @param SkuNameList:      Input value for SkuNameList
    # @param SkuInfo:          Input value for SkuInfo
    # @param VariableName:     Input value for VariableName
    # @param VariableGuid:     Input value for VariableGuid
    # @param VariableOffset:   Input value for VariableOffset
    # @param HiiDefaultValue:  Input value for HiiDefaultValue
    # @param VpdOffset:        Input value for VpdOffset
    # @param DefaultValue:     Input value for DefaultValue
    #
    # @retval (False, SkuName)     Not found in section SkuId Dsc file
    # @retval (True, SkuInfoList)  Found in section SkuId of Dsc file
    #
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

    ## Gen DynamicDefaultPcds
    #
    # Gen DynamicDefaultPcds of Dsc as <PcdTokenSpaceGuidCName>.<TokenCName>|<Value>[|<DatumTyp>[|<MaxDatumSize>]]
    #
    # @param Type:           The type of Pcd
    # @param ContainerFile:  The file which describes the pcd, used for error report
    #
    def GenDynamicDefaultPcds(self, Type = '', ContainerFile = ''):
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
                List = GetSplitValueList(Item[0] + DataType.TAB_VALUE_SPLIT * 2)
                if len(List) < 4 or len(List) > 8:
                    RaiseParserError(Item[0], 'Pcds' + Type, ContainerFile, '<PcdTokenSpaceGuidCName>.<TokenCName>|<Value>[|<DatumTyp>[|<MaxDatumSize>]]')

                CheckPcdTokenInfo(List[0], 'Pcds' + Type, ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                MergeArches(Pcds, (TokenInfo[1], TokenInfo[0], List[1], List[2], List[3], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, '', '', '', '', '', Key[2])
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' is not defined" % (SkuInfoList, Type)
                EdkLogger.error("DSC File Parser", PARSER_ERROR, ErrorMsg, File=self.Platform.Header.FullPath)
            Pcd = PcdClass(Key[0], '', Key[1], Key[3], Key[4], Key[2], Key[5], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)

    ## Gen DynamicHiiPcds
    #
    # Gen DynamicHiiPcds of Dsc as <PcdTokenSpaceGuidCName>.<TokenCName>|<String>|<VariableGuidCName>|<VariableOffset>[|<DefaultValue>[|<MaximumDatumSize>]]
    #
    # @param Type:           The type of Pcd
    # @param ContainerFile:  The file which describes the pcd, used for error report
    #
    def GenDynamicHiiPcds(self, Type = '', ContainerFile = ''):
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
                List = GetSplitValueList(Item[0] + DataType.TAB_VALUE_SPLIT * 2)
                if len(List) < 6:
                    RaiseParserError(Item[0], 'Pcds' + Type, ContainerFile, '<PcdTokenSpaceGuidCName>.<TokenCName>|<String>|<VariableGuidCName>|<VariableOffset>[|<DefaultValue>[|<MaximumDatumSize>]]')

                CheckPcdTokenInfo(List[0], 'Pcds' + Type, ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                MergeArches(Pcds, (TokenInfo[1], TokenInfo[0], List[1], List[2], List[3], List[4], List[5], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, Key[2], Key[3], Key[4], Key[5], '', '')
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' is not defined" % (SkuInfoList, Type)
                EdkLogger.error("DSC File Parser", PARSER_ERROR, ErrorMsg, File=self.Platform.Header.FullPath)
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[6], Key[5], Key[7], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)

    ## Gen DynamicVpdPcds
    #
    # Gen DynamicVpdPcds of Dsc as <PcdTokenSpaceGuidCName>.<TokenCName>|<VpdOffset>[|<MaximumDatumSize>]
    #
    # @param Type:           The type of Pcd
    # @param ContainerFile:  The file which describes the pcd, used for error report
    #
    def GenDynamicVpdPcds(self, Type = '', ContainerFile = ''):
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
                if len(List) < 3:
                    RaiseParserError(Item[0], 'Pcds' + Type, ContainerFile, '<PcdTokenSpaceGuidCName>.<TokenCName>|<VpdOffset>[|<MaximumDatumSize>]')

                CheckPcdTokenInfo(List[0], 'Pcds' + Type, ContainerFile)
                TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
                MergeArches(Pcds, (TokenInfo[1], TokenInfo[0], List[1], List[2], Type), Arch)
        for Key in Pcds:
            (Status, SkuInfoList) = self.GenSkuInfoList(Item[1], self.Platform.SkuInfos.SkuInfoList, '', '', '', '', Key[2], '')
            if Status == False:
                ErrorMsg = "SKUID '%s' of '%s' is not defined." % (SkuInfoList, Type)
                EdkLogger.error("DSC File Parser", PARSER_ERROR, ErrorMsg, File=self.Platform.Header.FullPath)
            Pcd = PcdClass(Key[0], '', Key[1], '', Key[3], '', Key[4], [], SkuInfoList, [])
            Pcd.SupArchList = Pcds[Key]
            self.Platform.DynamicPcdBuildDefinitions.append(Pcd)

    ## Show detailed information of Dsc
    #
    # Print all members and their values of Dsc class
    #
    def ShowDsc(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for Key in self.KeyList:
            for Arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                                    Key + DataType.TAB_SPLIT + Arch + \
                                    "' + TAB_SECTION_END, self.Contents[arch]." + Key + ')'
                eval(Command)

    ## Show detailed information of Platform
    #
    # Print all members and their values of Platform class
    #
    def ShowPlatform(self):
        M = self.Platform
        print 'Filename =', M.Header.FileName
        print 'FullPath =', M.Header.FullPath
        print 'BaseName =', M.Header.Name
        print 'Guid =', M.Header.Guid
        print 'Version =', M.Header.Version
        print 'DscSpecification =', M.Header.DscSpecification
        print 'SkuId =', M.Header.SkuIdName
        print 'SupArchList =', M.Header.SupArchList
        print 'BuildTargets =', M.Header.BuildTargets
        print 'OutputDirectory =', M.Header.OutputDirectory
        print 'BuildNumber =', M.Header.BuildNumber
        print 'MakefileName =', M.Header.MakefileName
        print 'Fdf =', M.FlashDefinitionFile.FilePath
        print 'BsBaseAddress =', M.Header.BsBaseAddress
        print 'RtBaseAddress =', M.Header.RtBaseAddress
        print 'Define =', M.Header.Define
        print '\nBuildOptions =', M.BuildOptions, M.BuildOptions.IncludeFiles
        for Item in M.BuildOptions.BuildOptionList:
            print '\t', Item.ToolChainFamily, Item.ToolChain, Item.Option, Item.SupArchList
        print '\nSkuIds =', M.SkuInfos.SkuInfoList, M.SkuInfos.IncludeFiles
        print '\nLibraries =', M.Libraries, M.Libraries.IncludeFiles
        for Item in M.Libraries.LibraryList:
            print '\t', Item.FilePath, Item.SupArchList, Item.Define
        print '\nLibraryClasses =', M.LibraryClasses, M.LibraryClasses.IncludeFiles
        for Item in M.LibraryClasses.LibraryList:
            print '\t', Item.Name, Item.FilePath, Item.SupModuleList, Item.SupArchList, Item.Define
        print '\nPcds =', M.DynamicPcdBuildDefinitions
        for Item in M.DynamicPcdBuildDefinitions:
            print '\tCname=', Item.CName, 'TSG=', Item.TokenSpaceGuidCName, 'Value=', Item.DefaultValue, 'Token=', Item.Token, 'Type=', Item.ItemType, 'Datum=', Item.DatumType, 'Size=', Item.MaxDatumSize, 'Arch=', Item.SupArchList, Item.SkuInfoList
            for Sku in Item.SkuInfoList.values():
                print '\t\t', str(Sku)
        print '\nComponents =', M.Modules.ModuleList, M.Modules.IncludeFiles
        for Item in M.Modules.ModuleList:
            print '\t', Item.FilePath, Item.ExecFilePath, Item.SupArchList
            for Lib in Item.LibraryClasses.LibraryList:
                print '\t\tLib:', Lib.Name, Lib.FilePath
            for Bo in Item.ModuleSaBuildOption.BuildOptionList:
                print '\t\tBuildOption:', Bo.ToolChainFamily, Bo.ToolChain, Bo.Option
            for Pcd in Item.PcdBuildDefinitions:
                print '\t\tPcd:', Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.MaxDatumSize, Pcd.DefaultValue, Pcd.ItemType

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    W = os.getenv('WORKSPACE')
    F = os.path.join(W, 'Nt32Pkg/Nt32Pkg.dsc')
    P = Dsc(os.path.normpath(F), True, True, W)
    P.ShowPlatform()
