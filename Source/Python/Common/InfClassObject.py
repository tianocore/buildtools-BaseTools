## @file
# This file is used to define each component of INF file
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
import re
import EdkLogger
from CommonDataClass.CommonClass import LibraryClassClass
from CommonDataClass.ModuleClass import *
from String import *
from DataType import *
from Identification import *
from Dictionary import *
from BuildToolError import *
from Misc import sdict
import GlobalData
from Table.TableInf import TableInf
import Database as Database
from Parsing import *

#
# Global variable
#
Section = {TAB_UNKNOWN.upper() : MODEL_UNKNOWN,
           TAB_INF_DEFINES.upper() : MODEL_META_DATA_HEADER,
           TAB_BUILD_OPTIONS.upper() : MODEL_META_DATA_BUILD_OPTION,
           TAB_INCLUDES.upper() : MODEL_EFI_INCLUDE,
           TAB_LIBRARIES.upper() : MODEL_EFI_LIBRARY_INSTANCE,
           TAB_LIBRARY_CLASSES.upper() : MODEL_EFI_LIBRARY_CLASS,
           TAB_PACKAGES.upper() : MODEL_META_DATA_PACKAGE,
           TAB_NMAKE.upper() : MODEL_META_DATA_NMAKE,
           TAB_INF_FIXED_PCD.upper() : MODEL_PCD_FIXED_AT_BUILD,
           TAB_INF_PATCH_PCD.upper() : MODEL_PCD_PATCHABLE_IN_MODULE,
           TAB_INF_FEATURE_PCD.upper() : MODEL_PCD_FEATURE_FLAG,
           TAB_INF_PCD_EX.upper() : MODEL_PCD_DYNAMIC_EX,
           TAB_INF_PCD.upper() : MODEL_PCD_DYNAMIC,
           TAB_SOURCES.upper() : MODEL_EFI_SOURCE_FILE,
           TAB_GUIDS.upper() : MODEL_EFI_GUID,
           TAB_PROTOCOLS.upper() : MODEL_EFI_PROTOCOL,
           TAB_PPIS.upper() : MODEL_EFI_PPI,
           TAB_DEPEX.upper() : MODEL_EFI_DEPEX,
           TAB_BINARIES.upper() : MODEL_EFI_BINARY_FILE,
           TAB_USER_EXTENSIONS.upper() : MODEL_META_DATA_USER_EXTENSION
           }

gComponentType2ModuleType = {
    "LIBRARY"               :   "BASE",
    "SECURITY_CORE"         :   "SEC",
    "PEI_CORE"              :   "PEI_CORE",
    "COMBINED_PEIM_DRIVER"  :   "PEIM",
    "PIC_PEIM"              :   "PEIM",
    "RELOCATABLE_PEIM"      :   "PEIM",
    "PE32_PEIM"             :   "PEIM",
    "BS_DRIVER"             :   "DXE_DRIVER",
    "RT_DRIVER"             :   "DXE_RUNTIME_DRIVER",
    "SAL_RT_DRIVER"         :   "DXE_SAL_DRIVER",
#    "BS_DRIVER"             :   "DXE_SMM_DRIVER",
#    "BS_DRIVER"             :   "UEFI_DRIVER",
    "APPLICATION"           :   "UEFI_APPLICATION",
    "LOGO"                  :   "BASE",
}

gNmakeFlagPattern = re.compile("(?:EBC_)?([A-Z]+)_(?:STD_|PROJ_|ARCH_)?FLAGS(?:_DLL|_ASL|_EXE)?", re.UNICODE)
gNmakeFlagName2ToolCode = {
    "C"         :   "CC",
    "LIB"       :   "SLINK",
    "LINK"      :   "DLINK",
}

## InfObject
#
# This class defined basic Inf object which is used by inheriting
# 
# @param object:       Inherited from object class
#
class InfObject(object):
    def __init__(self):
        object.__init__()

## InfDefines
#
# This class defined basic Defines used in Inf object
# 
# @param InfObject:        Inherited from InfObject class
#
# @var DefinesDictionary:  To store value for DefinesDictionary 
#
class InfDefines(InfObject):
    def __init__(self):
        self.DefinesDictionary = {
            #
            # Required Fields
            #
            TAB_INF_DEFINES_BASE_NAME                               : [''],
            TAB_INF_DEFINES_FILE_GUID                               : [''],
            TAB_INF_DEFINES_MODULE_TYPE                             : [''],
            TAB_INF_DEFINES_EFI_SPECIFICATION_VERSION               : [''],
            TAB_INF_DEFINES_EDK_RELEASE_VERSION                     : [''],
            
            #
            # Optional Fields
            #
            TAB_INF_DEFINES_INF_VERSION                             : [''],
            TAB_INF_DEFINES_BINARY_MODULE                           : [''],
            TAB_INF_DEFINES_LIBRARY_CLASS                           : [''],
            TAB_INF_DEFINES_COMPONENT_TYPE                          : [''],
            TAB_INF_DEFINES_MAKEFILE_NAME                           : [''],
            TAB_INF_DEFINES_BUILD_NUMBER                            : [''],
            TAB_INF_DEFINES_BUILD_TYPE                              : [''],
            TAB_INF_DEFINES_FFS_EXT                                 : [''],
            TAB_INF_DEFINES_FV_EXT                                  : [''],
            TAB_INF_DEFINES_SOURCE_FV                               : [''],
            TAB_INF_DEFINES_VERSION_NUMBER                          : [''],
            TAB_INF_DEFINES_VERSION_STRING                          : [''],
            TAB_INF_DEFINES_VERSION                                 : [''],
            TAB_INF_DEFINES_PCD_IS_DRIVER                           : [''],
            TAB_INF_DEFINES_TIANO_R8_FLASHMAP_H                     : [''],
            TAB_INF_DEFINES_ENTRY_POINT                             : [''],
            TAB_INF_DEFINES_UNLOAD_IMAGE                            : [''],
            TAB_INF_DEFINES_CONSTRUCTOR                             : [''],
            TAB_INF_DEFINES_DESTRUCTOR                              : [''],
            TAB_INF_DEFINES_DEFINE                                  : [''],
            TAB_INF_DEFINES_SPEC                                    : [''],
            TAB_INF_DEFINES_CUSTOM_MAKEFILE                         : [''],
            TAB_INF_DEFINES_SHADOW                                  : [''],
            TAB_INF_DEFINES_MACRO                                   : {}
        }

    def extend(self, InfDefinesObj):
        for Item in InfDefinesObj.DefinesDictionary:
            if Item == TAB_INF_DEFINES_MACRO:
                self.DefinesDictionary[Item].update(InfDefinesObj.DefinesDictionary[Item])
            else:
                if InfDefinesObj.DefinesDictionary[Item][0] != '':
                    if self.DefinesDictionary[Item][0] == '':
                        self.DefinesDictionary[Item] = []
                    self.DefinesDictionary[Item].extend(InfDefinesObj.DefinesDictionary[Item])

## InfContents
#
# This class defined basic Contents used in Inf object
# 
# @param InfObject:   Inherited from InfObject class
#
# @var Sources:       To store value for Sources
# @var BuildOptions:  To store value for BuildOptions
# @var Binaries:      To store value for Binaries
# @var Includes:      To store value for Includes
# @var Guids:         To store value for Guids
# @var Protocols:     To store value for Protocols
# @var Ppis:          To store value for Ppis
# @var Libraries:     To store value for Libraries
# @var Packages:      To store value for Packages
# @var FixedPcd:      To store value for FixedPcd
# @var PatchPcd:      To store value for PatchPcd
# @var Pcd:           To store value for Pcd
# @var PcdEx:         To store value for PcdEx
# @var Depex:         To store value for Depex
# @var Nmake:         To store value for Nmake
#
class InfContents(InfObject):
    def __init__(self):
        self.Sources = []
        self.BuildOptions = []
        self.Binaries = []
        self.Includes = []
        self.Guids = []
        self.Protocols = []
        self.Ppis = []
        self.Libraries = []
        self.LibraryClasses = []
        self.Packages = []
        self.FixedPcd = []
        self.PatchPcd = []
        self.FeaturePcd = []
        self.Pcd = []
        self.PcdEx = []
        self.Depex = []
        self.Nmake = []

## Inf
#
# This class defined the structure used in Inf object
# 
# @param InfObject:         Inherited from InfObject class
# @param Ffilename:         Input value for Ffilename of Inf file, default is None
# @param IsMergeAllArches:  Input value for IsMergeAllArches
#                           True is to merge all arches
#                           Fales is not to merge all arches
#                           default is False
# @param IsToModule:        Input value for IsToModule
#                           True is to transfer to ModuleObject automatically
#                           False is not to transfer to ModuleObject automatically
#                           default is False
# @param WorkspaceDir:      Input value for current workspace directory, default is None
#
# @var Identification:      To store value for Identification, it is a structure as Identification
# @var Defines:             To store value for Defines, it is a structure as InfDefines
# @var UserExtensions:      To store value for UserExtensions
# @var Module:              To store value for Module, it is a structure as ModuleClass
# @var WorkspaceDir:        To store value for WorkspaceDir
# @var Contents:            To store value for Contents, it is a structure as InfContents
# @var KeyList:             To store value for KeyList, a list for all Keys used in Inf
#
class Inf(InfObject):
    def __init__(self, Filename = None, IsMergeAllArches = False, IsToModule = False, WorkspaceDir = None, Database = None, SupArchList = DataType.ARCH_LIST):
        self.Identification = Identification()
        self.Defines = {} # InfDefines()
        self.Contents = {}
        self.UserExtensions = ''
        self.Module = ModuleClass()
        self.WorkspaceDir = WorkspaceDir
        self._Macro = {}    # for inf file local replacement
        self.Cur = Database.Cur
        self.TblFile = Database.TblFile
        self.TblInf = TableInf(Database.Cur)
        self.SupArchList = SupArchList
        
        
#        for Arch in DataType.ARCH_LIST_FULL:
#            self.Contents[Arch] = InfContents()

        self.KeyList = [
            TAB_SOURCES, TAB_BUILD_OPTIONS, TAB_BINARIES, TAB_INCLUDES, TAB_GUIDS, 
            TAB_PROTOCOLS, TAB_PPIS, TAB_LIBRARY_CLASSES, TAB_PACKAGES, TAB_LIBRARIES, 
            TAB_INF_FIXED_PCD, TAB_INF_PATCH_PCD, TAB_INF_FEATURE_PCD, TAB_INF_PCD, 
            TAB_INF_PCD_EX, TAB_DEPEX, TAB_NMAKE, TAB_INF_DEFINES
        ]
        #
        # Upper all KEYs to ignore case sensitive when parsing
        #
        self.KeyList = map(lambda c: c.upper(), self.KeyList)
        
        #
        # Init RecordSet
        #
        self.RecordSet = {}        
        for Key in self.KeyList:
            self.RecordSet[Section[Key]] = []
        
        #
        # Load Inf file if filename is not None
        #
        if Filename != None:
            self.LoadInfFile(Filename)
        
        #
        # Merge contents of Inf from all arches if IsMergeAllArches is True
        #        
        if IsMergeAllArches:
            self.MergeAllArches()

        #
        # Transfer to Module Object if IsToModule is True
        #
        if IsToModule:
            self.InfToModule()

    ## Merge contents of Inf from all arches
    #
    # Find the contents defined in all arches and merge them to all
    #
    def MergeAllArches(self):
        if DataType.TAB_ARCH_COMMON in self.Defines:
            for Arch in DataType.ARCH_LIST:
                if Arch not in self.Defines:
                    self.Defines[Arch] = InfDefines()
                self.Defines[Arch].extend(self.Defines[DataType.TAB_ARCH_COMMON])
                self._Macro.update(self.Defines[Arch].DefinesDictionary[TAB_INF_DEFINES_MACRO])
        self._Macro.update(GlobalData.gGlobalDefines)

        if DataType.TAB_ARCH_COMMON in self.Contents:
            for Key in self.KeyList:
                for Arch in DataType.ARCH_LIST:
                    Command = "self.Contents[Arch]." + Key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + Key + ")"
                    eval(Command)     

    ## Parse Inf file
    #
    # Go through input lines one by one to find the value defined in Key section.
    # Save them to KeyField
    #
    # @param Lines:     Lines need to be parsed
    # @param Key:       The key value of the section to be located
    # @param KeyField:  To save the found contents
    #
    def ParseInf(self, Lines, Key, KeyField):
        newKey = SplitModuleType(Key)
        if newKey[0].upper().find(DataType.TAB_LIBRARY_CLASSES.upper()) != -1:
            GetLibraryClassesWithModuleType(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        else:
            GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)

    ## Transfer to Module Object
    # 
    # Transfer all contents of an Inf file to a standard Module Object
    #
    def InfToModule(self):
        #
        # Init global information for the file
        #
        ContainerFile = self.Identification.FileFullPath
        
        #
        # Generate Package Header
        #
        self.GenModuleHeader(ContainerFile)
        
        #
        # Generate BuildOptions
        #
        self.GenBuildOptions(ContainerFile)
        
        #
        # Generate Includes
        #
        self.GenIncludes(ContainerFile)
        
        #
        # Generate Libraries
        #
        self.GenLibraries(ContainerFile)
        
        #
        # Generate LibraryClasses
        #
        self.GenLibraryClasses(ContainerFile)
        
        #
        # Generate Packages
        #
        self.GenPackages(ContainerFile)
        
        #
        # Generate Nmakes
        #
        self.GenNmakes(ContainerFile)
        
        #
        # Generate Pcds
        #
        self.GenPcds(ContainerFile)
        
        #
        # Generate Sources
        #
        self.GenSources(ContainerFile)
        
        #
        # Generate UserExtensions
        #
        self.GenUserExtensions(ContainerFile)
        
        #
        # Generate Guids
        #
        self.GenGuids(ContainerFile)

        #
        # Generate Protocols
        #
        self.GenProtocols(ContainerFile)

        #
        # Generate Ppis
        #
        self.GenPpis(ContainerFile)
        
        #
        # Generate Depexes
        #
        self.GenDepexes(ContainerFile)
        
        #
        # Generate Binaries
        #
        self.GenBinaries(ContainerFile)
        
    ## Get Pcd Values of Inf
    #
    # Get Pcd of Inf as <TokenSpaceGuidCName>.<PcdCName>[|<Value>]
    #
    # @param Item:  The string describes pcd
    # @param Type:  The type of Pcd
    # @param File:  The file which describes the pcd, used for error report
    #
    # @retval (TokenSpcCName, TokenCName, Value, ItemType) Formatted Pcd Item
    #
    def GetPcdOfInf(self, Item, Type, File, LineNo):
        Format = '<TokenSpaceGuidCName>.<PcdCName>[|<Value>]'
        InfType = ''
        if Type == TAB_PCDS_FIXED_AT_BUILD:
            InfType = TAB_INF_FIXED_PCD
        elif Type == TAB_PCDS_PATCHABLE_IN_MODULE:
            InfType = TAB_INF_PATCH_PCD
        elif Type == TAB_PCDS_FEATURE_FLAG:
            InfType = TAB_INF_FEATURE_PCD        
        elif Type == TAB_PCDS_DYNAMIC_EX:
            InfType = TAB_INF_PCD_EX        
        elif Type == TAB_PCDS_DYNAMIC:
            InfType = TAB_INF_PCD
        List = GetSplitValueList(Item + DataType.TAB_VALUE_SPLIT)
        if len(List) < 2 or len(List) > 3:
            RaiseParserError(Item, InfType, File, Format, LineNo)
        TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
        if len(TokenInfo) != 2:
            RaiseParserError(Item, InfType, File, Format, LineNo)

        return (TokenInfo[0], TokenInfo[1], List[1], Type)

    ## Parse [Defines] section
    #
    # Parse [Defines] section into InfDefines object
    #
    # @param InfFile    The path of the INF file
    # @param Section    The title of "Defines" section
    # @param Lines      The content of "Defines" section
    #
    def ParseDefines(self, InfFile, Section, Lines):
        TokenList = Section.split(TAB_SPLIT)
        if len(TokenList) == 3:
            RaiseParserError(Section, "Defines", InfFile, "[xx.yy.%s] format (with platform) is not supported")
        if len(TokenList) == 2:
            Arch = TokenList[1].upper()
        else:
            Arch = TAB_ARCH_COMMON

        if Arch not in self.Defines:
            self.Defines[Arch] = InfDefines()
        GetSingleValueOfKeyFromLines(Lines, self.Defines[Arch].DefinesDictionary, 
                                     TAB_COMMENT_SPLIT, TAB_EQUAL_SPLIT, False, None)

    ## First time to insert records to database
    # 
    # Insert item data of a section to database
    # @param FileID:           The ID of belonging file
    # @param Filename:         The name of belonging file
    # @param CurrentSection:   The name of currect section
    # @param SectionItemList:  A list of items of the section
    # @param ArchList:         A list of arches
    # @param ThirdList:        A list of third parameters, ModuleType for LibraryClass and SkuId for Dynamic Pcds
    # @param IfDefList:        A list of all conditional statements
    #
    def InsertSectionItemsIntoDatabase(self, FileID, Filename, CurrentSection, SectionItemList, ArchList, ThirdList, IfDefList):
        #
        # Insert each item data of a section
        #
        for Index in range(0, len(ArchList)):
            Arch = ArchList[Index]
            Third = ThirdList[Index]
            if Arch == '':
                Arch = TAB_ARCH_COMMON

            Model = Section[CurrentSection.upper()]
            Records = self.RecordSet[Model]
            for SectionItem in SectionItemList:
                BelongsToItem, EndLine, EndColumn = -1, -1, -1
                LineValue, StartLine, EndLine = SectionItem[0], SectionItem[1], SectionItem[1]
                
                EdkLogger.debug(4, "Parsing %s ..." %LineValue)
                #
                # And then parse DEFINE statement
                #
                if LineValue.upper().find(DataType.TAB_DEFINE.upper() + ' ') > -1:
                    self.ParseDefine(LineValue, StartLine, self.TblInf, FileID, Filename, CurrentSection, MODEL_META_DATA_DEFINE, Arch)
                    continue
                
                #
                # At last parse other sections
                #
                if CurrentSection == TAB_LIBRARY_CLASSES or CurrentSection == TAB_INF_DEFINES:
                    ID = self.TblInf.Insert(Model, LineValue, Third, Third, '', '', Arch, -1, FileID, StartLine, -1, StartLine, -1, 0)
                    Records.append([LineValue, Arch, StartLine, ID, Third])
                    continue
                else:
                    ID = self.TblInf.Insert(Model, LineValue, '', '', '', '', Arch, -1, FileID, StartLine, -1, StartLine, -1, 0)
                    Records.append([LineValue, Arch, StartLine, ID, Third])
                    continue
            self.RecordSet[Model] = Records
    
    ## Load Inf file
    #
    # Load the file if it exists
    #
    # @param Filename:  Input value for filename of Inf file
    #
    def LoadInfFile(self, Filename):     
        #
        # Insert a record for file
        #
        Filename = NormPath(Filename)
        self.Identification.FileFullPath = Filename
        (self.Identification.FileRelativePath, self.Identification.FileName) = os.path.split(Filename)
        FileID = self.TblFile.InsertFile(Filename, MODEL_FILE_DSC)
        
        #
        # Init InfTable
        #
        self.TblInf.Table = "Inf%s" % FileID
        self.TblInf.Create()
        
        #
        # Init common datas
        #
        IfDefList, SectionItemList, CurrentSection, ArchList, ThirdList, IncludeFiles = \
        [], [], TAB_UNKNOWN, [], [], []
        LineNo = 0
        
        #
        # Parse file content
        #
        FileContent = open(Filename, 'r').read()
        for Line in FileContent.splitlines():
            LineNo = LineNo + 1
            #
            # Reomve spaces in head and tail
            #
            Line = Line.strip()
            
            #
            # Ignore comments
            #
            if Line.startswith(TAB_COMMENT_SPLIT):
                continue
            
            #
            # Remove comments at tail and remove spaces again
            #
            Line = CleanString(Line)
            if Line == '':
                continue
            
            #
            # Find a new section tab
            # First insert previous section items
            # And then parse the content of the new section
            #
            if Line.startswith(TAB_SECTION_START) and Line.endswith(TAB_SECTION_END):
                #
                # Insert items data of previous section
                #
                self.InsertSectionItemsIntoDatabase(FileID, Filename, CurrentSection, SectionItemList, ArchList, ThirdList, IfDefList)
                #
                # Parse the new section
                #
                SectionItemList = []
                ArchList = []
                ThirdList = []
                
                LineList = GetSplitValueList(Line[len(TAB_SECTION_START):len(Line) - len(TAB_SECTION_END)], TAB_COMMA_SPLIT)
                for Item in LineList:
                    ItemList = GetSplitValueList(Item, TAB_SPLIT)
                    CurrentSection = ItemList[0]
                    if CurrentSection.upper() not in self.KeyList:
                        RaiseParserError(Line, CurrentSection, Filename, '', LineNo)
                    ItemList.append('')
                    ItemList.append('')
                    if len(ItemList) > 5:
                        RaiseParserError(Line, CurrentSection, Filename, '', LineNo)
                    else:
                        if ItemList[1] != '' and ItemList[1].upper() not in ARCH_LIST_FULL:
                            EdkLogger.error("Parser", PARSER_ERROR, "Invalid Arch definition '%s' found" % ItemList[1], File=Filename, Line=LineNo)
                        ArchList.append(ItemList[1].upper())
                        ThirdList.append(ItemList[2])

                continue
            
            #
            # Not in any defined section
            #
            if CurrentSection == TAB_UNKNOWN:
                ErrorMsg = "%s is not in any defined section" % Line
                EdkLogger.error("Parser", PARSER_ERROR, ErrorMsg, File=Filename, Line=LineNo)

            #
            # Add a section item
            #
            SectionItemList.append([Line, LineNo])
            # End of parse
        #End of For
        
        #
        # Insert items data of last section
        #
        self.InsertSectionItemsIntoDatabase(FileID, Filename, CurrentSection, SectionItemList, ArchList, ThirdList, IfDefList)
        
        #
        # Replace all DEFINE macros with its actual values
        #
        ParseDefineMacro2(self.TblInf, self.RecordSet, GlobalData.gGlobalDefines)

    ## Show detailed information of Inf
    #
    # Print all members and their values of Inf class
    #
    def ShowInf(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for key in self.KeyList:
            for arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                          key + DataType.TAB_SPLIT + arch + \
                          "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
                eval(Command)
        print ""
    
    ## Show detailed information of Module
    #
    # Print all members and their values of Module class
    #
    def ShowModule(self):
        M = self.Module
        for Arch in M.Header.keys():
            print '\nArch =', Arch
            print 'Filename =', M.Header[Arch].FileName
            print 'FullPath =', M.Header[Arch].FullPath
            print 'BaseName =', M.Header[Arch].Name
            print 'Guid =', M.Header[Arch].Guid
            print 'Version =', M.Header[Arch].Version
            print 'InfVersion =', M.Header[Arch].InfVersion
            print 'EfiSpecificationVersion =', M.Header[Arch].EfiSpecificationVersion
            print 'EdkReleaseVersion =', M.Header[Arch].EdkReleaseVersion                
            print 'ModuleType =', M.Header[Arch].ModuleType
            print 'BinaryModule =', M.Header[Arch].BinaryModule
            print 'ComponentType =', M.Header[Arch].ComponentType
            print 'MakefileName =', M.Header[Arch].MakefileName
            print 'BuildNumber =', M.Header[Arch].BuildNumber
            print 'BuildType =', M.Header[Arch].BuildType
            print 'FfsExt =', M.Header[Arch].FfsExt
            print 'FvExt =', M.Header[Arch].FvExt
            print 'SourceFv =', M.Header[Arch].SourceFv
            print 'PcdIsDriver =', M.Header[Arch].PcdIsDriver
            print 'TianoR8FlashMap_h =', M.Header[Arch].TianoR8FlashMap_h
            print 'Shadow =', M.Header[Arch].Shadow
            print 'LibraryClass =', M.Header[Arch].LibraryClass
            for Item in M.Header[Arch].LibraryClass:
                print Item.LibraryClass, DataType.TAB_VALUE_SPLIT.join(Item.SupModuleList)
            print 'CustomMakefile =', M.Header[Arch].CustomMakefile
            print 'Define =', M.Header[Arch].Define
            print 'Specification =', M.Header[Arch].Specification
        for Item in self.Module.ExternImages:
            print '\nEntry_Point = %s, UnloadImage = %s' % (Item.ModuleEntryPoint, Item.ModuleUnloadImage)
        for Item in self.Module.ExternLibraries:
            print 'Constructor = %s, Destructor = %s' % (Item.Constructor, Item.Destructor)
        print '\nBuildOptions =', M.BuildOptions
        for Item in M.BuildOptions:
            print Item.ToolChainFamily, Item.ToolChain, Item.Option, Item.SupArchList
        print '\nIncludes =', M.Includes
        for Item in M.Includes:
            print Item.FilePath, Item.SupArchList
        print '\nLibraries =', M.Libraries
        for Item in M.Libraries:
            print Item.Library, Item.SupArchList
        print '\nLibraryClasses =', M.LibraryClasses
        for Item in M.LibraryClasses:
            print Item.LibraryClass, Item.RecommendedInstance, Item.FeatureFlag, Item.SupModuleList, Item.SupArchList, Item.Define
        print '\nPackageDependencies =', M.PackageDependencies
        for Item in M.PackageDependencies:
            print Item.FilePath, Item.SupArchList, Item.Define
        print '\nNmake =', M.Nmake
        for Item in M.Nmake:
            print Item.Name, Item.Value, Item.SupArchList
        print '\nPcds =', M.PcdCodes
        for Item in M.PcdCodes:
            print '\tCName=',Item.CName, 'TokenSpaceGuidCName=', Item.TokenSpaceGuidCName, 'DefaultValue=', Item.DefaultValue, 'ItemType=', Item.ItemType, Item.SupArchList
        print '\nSources =', M.Sources
        for Source in M.Sources:
            print Source.SourceFile, 'Fam=', Source.ToolChainFamily, 'Pcd=', Source.FeatureFlag, 'Tag=', Source.TagName, 'ToolCode=', Source.ToolCode, Source.SupArchList
        print '\nUserExtensions =', M.UserExtensions
        for UserExtension in M.UserExtensions:
            print UserExtension.UserID, UserExtension.Identifier,UserExtension.Content
        print '\nGuids =', M.Guids
        for Item in M.Guids:
            print Item.CName, Item.SupArchList
        print '\nProtocols =', M.Protocols
        for Item in M.Protocols:
            print Item.CName, Item.SupArchList
        print '\nPpis =', M.Ppis
        for Item in M.Ppis:
            print Item.CName, Item.SupArchList
        print '\nDepex =', M.Depex
        for Item in M.Depex:
            print Item.Depex, Item.SupArchList, Item.Define
        print '\nBinaries =', M.Binaries
        for Binary in M.Binaries:
            print 'Type=', Binary.FileType, 'Target=', Binary.Target, 'Name=', Binary.BinaryFile, 'FeatureFlag=', Binary.FeatureFlag, 'SupArchList=', Binary.SupArchList

    ## Convert [Defines] section content to ModuleHeaderClass
    #
    # Convert [Defines] section content to ModuleHeaderClass
    #
    # @param Defines        The content under [Defines] section
    # @param ModuleHeader   An object of ModuleHeaderClass
    # @param Arch           The supported ARCH
    #
    def GenModuleHeader(self, ContainerFile):
        EdkLogger.debug(2, "Generate ModuleHeader ...")
        #
        # Update all defines item in database
        #
        RecordSet = self.RecordSet[MODEL_META_DATA_HEADER]
        for Record in RecordSet:
            ValueList = GetSplitValueList(Record[0], TAB_EQUAL_SPLIT)
            if len(ValueList) != 2:
                RaiseParserError(Record[0], 'Defines', ContainerFile, '<Key> = <Value>', Record[2])
            ID, Value1, Value2, Arch, LineNo = Record[3], ValueList[0], ValueList[1], Record[1], Record[2]
            SqlCommand = """update %s set Value1 = '%s', Value2 = '%s'
                            where ID = %s""" % (self.TblInf.Table, ConvertToSqlString2(Value1), ConvertToSqlString2(Value2), ID)
            self.TblInf.Exec(SqlCommand)
        
        for Arch in DataType.ARCH_LIST:
            ModuleHeader = ModuleHeaderClass()
            ModuleHeader.Name = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_BASE_NAME, Arch)[0]
            ModuleHeader.Guid = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_FILE_GUID, Arch)[0]
            ModuleHeader.Version = QueryDefinesItem(self.TblInf, TAB_DEC_DEFINES_PACKAGE_VERSION, Arch)[0]
            ModuleHeader.FileName = self.Identification.FileName
            ModuleHeader.FullPath = self.Identification.FileFullPath
            ModuleHeader.InfVersion = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_INF_VERSION, Arch)[0]
            
            ModuleHeader.EfiSpecificationVersion = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_EFI_SPECIFICATION_VERSION, Arch)[0]
            ModuleHeader.EdkReleaseVersion = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_EDK_RELEASE_VERSION, Arch)[0]
            
            ModuleHeader.ModuleType = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_MODULE_TYPE, Arch)[0]
            ModuleHeader.BinaryModule = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_BINARY_MODULE, Arch)[0]
            ModuleHeader.ComponentType = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_COMPONENT_TYPE, Arch)[0]
            ModuleHeader.MakefileName = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_MAKEFILE_NAME, Arch)[0]
            ModuleHeader.BuildNumber = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_BUILD_NUMBER, Arch)[0]
            ModuleHeader.BuildType = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_BUILD_TYPE, Arch)[0]
            ModuleHeader.FfsExt = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_FFS_EXT, Arch)[0]
            ModuleHeader.SourceFv = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_SOURCE_FV, Arch)[0]
            ModuleHeader.PcdIsDriver = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_PCD_IS_DRIVER, Arch)[0]
            ModuleHeader.TianoR8FlashMap_h = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_TIANO_R8_FLASHMAP_H, Arch)[0]
            ModuleHeader.Shadow = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_SHADOW, Arch)[0]
        
            #
            # Get version of INF
            #
            if ModuleHeader.InfVersion != "":
                # R9 inf
                VersionNumber = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_VERSION_NUMBER, Arch)[0]
                VersionString = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_VERSION_STRING, Arch)[0]
                if len(VersionNumber) > 0 and len(VersionString) == 0:
                    EdkLogger.warn(2000, 'VERSION_NUMBER depricated; INF file %s should be modified to use VERSION_STRING instead.' % self.Identification.FileFullPath)
                    ModuleHeader.Version = VersionNumber
                if len(VersionString) > 0:
                    if len(VersionNumber) > 0:
                        EdkLogger.warn(2001, 'INF file %s defines both VERSION_NUMBER and VERSION_STRING, using VERSION_STRING' % self.Identification.FileFullPath)
                    ModuleHeader.Version = VersionString
            else:
                # R8 inf
                ModuleHeader.InfVersion = "0x00010000"
                VersionNumber = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_VERSION, Arch)[0]
                VersionString = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_VERSION_STRING, Arch)[0]
                if VersionString == '' and VersionNumber != '':
                    VersionString = VersionNumber
                if ModuleHeader.ComponentType in gComponentType2ModuleType:
                    ModuleHeader.ModuleType = gComponentType2ModuleType[ModuleHeader[Arch].ComponentType]
                elif ModuleHeader.ComponentType != '':
                    EdkLogger.error("Parser", PARSER_ERROR, "Unsupported R8 component type [%s]" % ModuleHeader[Arch].ComponentType,
                                    ExtraData=ContainerFile)
            #
            # LibraryClass of Defines
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_LIBRARY_CLASS, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    List = GetSplitValueList(Item, DataType.TAB_VALUE_SPLIT, 1)
                    Lib = LibraryClassClass()
                    Lib.LibraryClass = CleanString(List[0])
                    if len(List) == 1:
                        Lib.SupModuleList = DataType.SUP_MODULE_LIST
                    elif len(List) == 2:
                        Lib.SupModuleList = GetSplitValueList(CleanString(List[1]), ' ')
                    ModuleHeader.LibraryClass.append(Lib)
            elif ModuleHeader.ComponentType == "LIBRARY":
                Lib = LibraryClassClass()
                Lib.LibraryClass = ModuleHeader.Name
                Lib.SupModuleList = DataType.SUP_MODULE_LIST
                ModuleHeader.LibraryClass.append(Lib)
            
            #
            # Custom makefile of Defines
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_CUSTOM_MAKEFILE, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    List = Item.split(DataType.TAB_VALUE_SPLIT)
                    if len(List) == 2:
                        ModuleHeader.CustomMakefile[CleanString(List[0])] = CleanString(List[1])
                    else:
                        RaiseParserError(Item, 'CUSTOM_MAKEFILE of Defines', File, 'CUSTOM_MAKEFILE=<Family>|<Filename>')
            
            #
            # EntryPoint and UnloadImage of Defines
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_ENTRY_POINT, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    Image = ModuleExternImageClass()
                    Image.ModuleEntryPoint = CleanString(Item)
                    self.Module.ExternImages.append(Image)
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_UNLOAD_IMAGE, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    Image = ModuleExternImageClass()
                    Image.ModuleUnloadImage = CleanString(Item)
                    self.Module.ExternImages.append(Image)
            
            #
            # Constructor and Destructor of Defines
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_CONSTRUCTOR, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    LibraryClass = ModuleExternLibraryClass()
                    LibraryClass.Constructor = CleanString(Item)
                    self.Module.ExternLibraries.append(LibraryClass)
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_DESTRUCTOR, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    LibraryClass = ModuleExternLibraryClass()
                    LibraryClass.Destructor = CleanString(Item)
                    self.Module.ExternLibraries.append(LibraryClass)
            
            #
            # Define of Defines
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_DEFINE, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    List = Item.split(DataType.TAB_EQUAL_SPLIT)
                    if len(List) != 2:
                        RaiseParserError(Item, 'DEFINE of Defines', File, 'DEFINE <Word> = <Word>')
                    else:
                        ModuleHeader.Define[CleanString(List[0])] = CleanString(List[1])
            
            #
            # Spec
            #
            RecordSet = QueryDefinesItem(self.TblInf, TAB_INF_DEFINES_SPEC, Arch)
            if RecordSet[0] != '':
                for Item in RecordSet:
                    List = Item.split(DataType.TAB_EQUAL_SPLIT)
                    if len(List) != 2:
                        RaiseParserError(Item, 'SPEC of Defines', File, 'SPEC <Word> = <Version>')
                    else:
                        ModuleHeader.Specification[CleanString(List[0])] = CleanString(List[1])
            
            self.Module.Header[Arch] = ModuleHeader
    
    
    ## GenBuildOptions
    #
    # Gen BuildOptions of Inf
    # [<Family>:]<ToolFlag>=Flag
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenBuildOptions(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_BUILD_OPTIONS)
        BuildOptions = {}
        #
        # Get all BuildOptions
        #
        RecordSet = self.RecordSet[MODEL_META_DATA_BUILD_OPTION]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    (Family, ToolChain, Flag) = GetBuildOption(Record[0], ContainerFile, Record[2])
                    MergeArches(BuildOptions, (Family, ToolChain, Flag), Arch)
                    #
                    # Update to Database
                    #
                    #SqlCommand = """update %s set Value1 = '%s', Value2 = '%s', Value3 = '%s'
                    #                where ID = %s""" % (self.TblInf.Table, ConvertToSqlString2(Family), ConvertToSqlString2(ToolChain), ConvertToSqlString2(Flag), Record[3])
                    #self.TblInf.Exec(SqlCommand)

        for Key in BuildOptions.keys():
            BuildOption = BuildOptionClass(Key[0], Key[1], Key[2])
            BuildOption.SupArchList = BuildOptions[Key]
            self.Module.BuildOptions.append(BuildOption)  

    ## GenIncludes
    #
    # Gen Includes of Inf
    # 
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenIncludes(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_INCLUDES)
        Includes = sdict()
        #
        # Get all Includes
        #
        RecordSet = self.RecordSet[MODEL_EFI_INCLUDE]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Includes, Record[0], Arch)

        for Key in Includes.keys():
            Include = IncludeClass()
            Include.FilePath = NormPath(Key)
            Include.SupArchList = Includes[Key]
            self.Module.Includes.append(Include)
        
    ## GenLibraries
    #
    # Gen Libraries of Inf
    # 
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenLibraries(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_LIBRARIES)
        Libraries = sdict()
        #
        # Get all Includes
        #
        RecordSet = self.RecordSet[MODEL_EFI_LIBRARY_INSTANCE]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Libraries, Record[0], Arch)

        for Key in Libraries.keys():
            Library = ModuleLibraryClass()
            # replace macro and remove file extension
            Library.Library = Key.rsplit('.', 1)[0]
            Library.SupArchList = Libraries[Key]
            self.Module.Libraries.append(Library)
    
    ## GenLibraryClasses
    #
    # Get LibraryClass of Inf
    # <LibraryClassKeyWord>|<LibraryInstance>
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenLibraryClasses(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_LIBRARY_CLASSES)
        LibraryClasses = {}
        #
        # Get all LibraryClasses
        #
        RecordSet = self.RecordSet[MODEL_EFI_LIBRARY_CLASS]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    (LibClassName, LibClassIns, Pcd, SupModelList) = GetLibraryClassOfInf([Record[0], Record[4]], ContainerFile, self.WorkspaceDir, Record[2])
                    MergeArches(LibraryClasses, (LibClassName, LibClassIns, Pcd, SupModelList), Arch)
                    #
                    # Update to Database
                    #
                    #SqlCommand = """update %s set Value1 = '%s', Value2 = '%s', Value3 = '%s'
                    #                where ID = %s""" % (self.TblInf.Table, ConvertToSqlString2(LibClassName), ConvertToSqlString2(LibClassIns), ConvertToSqlString2(SupModelList), Record[3])
                    #self.TblInf.Exec(SqlCommand)
        
        for Key in LibraryClasses.keys():
            KeyList = Key[0].split(DataType.TAB_VALUE_SPLIT)
            LibraryClass = LibraryClassClass()
            LibraryClass.LibraryClass = Key[0]
            LibraryClass.RecommendedInstance = NormPath(Key[1])
            LibraryClass.FeatureFlag = Key[2]
            LibraryClass.SupArchList = LibraryClasses[Key]
            LibraryClass.SupModuleList = GetSplitValueList(Key[3])
            self.Module.LibraryClasses.append(LibraryClass)

    ## GenPackages
    #
    # Gen Packages of Inf
    # 
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenPackages(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_PACKAGES)
        Packages = {}
        #
        # Get all Packages
        #
        RecordSet = self.RecordSet[MODEL_META_DATA_PACKAGE]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    CheckFileType(Record[0], '.Dec', ContainerFile, 'package', Record[0], Record[2])
                    CheckFileExist(self.WorkspaceDir, Record[0], ContainerFile, 'Packages', Record[0], Record[2])
                    MergeArches(Packages, Record[0], Arch)
                    
        for Key in Packages.keys():
            Package = ModulePackageDependencyClass()
            Package.FilePath = NormPath(Key)
            Package.SupArchList = Packages[Key]
            self.Module.PackageDependencies.append(Package)

    ## GenNmakes
    #
    # Gen Nmakes of Inf
    # 
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenNmakes(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_NMAKE)
        Nmakes = sdict()
        #
        # Get all Nmakes
        #
        RecordSet = self.RecordSet[MODEL_META_DATA_NMAKE]

        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Nmakes, Record[0], Arch)
                
        for Key in Nmakes.keys():
            List = GetSplitValueList(Key, DataType.TAB_EQUAL_SPLIT, MaxSplit=1)
            if len(List) != 2:
                RaiseParserError(Key, 'Nmake', ContainerFile, '<MacroName> = <Value>')
            Nmake = ModuleNmakeClass()
            Nmake.Name = List[0]
            Nmake.Value = List[1]
            Nmake.SupArchList = Nmakes[Key]
            self.Module.Nmake.append(Nmake)

            # convert R8 format to R9 format
            if Nmake.Name == "IMAGE_ENTRY_POINT":
                Image = ModuleExternImageClass()
                Image.ModuleEntryPoint = Nmake.Value
                self.Module.ExternImages.append(Image)
            elif Nmake.Name == "DPX_SOURCE":
                Source = ModuleSourceFileClass(NormPath(Nmake.Value), "", "", "", "", Nmake.SupArchList)
                self.Module.Sources.append(Source)
            else:
                ToolList = gNmakeFlagPattern.findall(Nmake.Name)
                if len(ToolList) == 0 or len(ToolList) != 1:
                    EdkLogger.warn("\nParser", "Don't know how to do with MACRO: %s" % Nmake.Name, 
                                   ExtraData=ContainerFile)
                else:
                    if ToolList[0] in gNmakeFlagName2ToolCode:
                        Tool = gNmakeFlagName2ToolCode[ToolList[0]]
                    else:
                        Tool = ToolList[0]
                    BuildOption = BuildOptionClass("MSFT", "*_*_*_%s_FLAGS" % Tool, Nmake.Value)
                    BuildOption.SupArchList = Nmake.SupArchList
                    self.Module.BuildOptions.append(BuildOption)
    
    ## GenPcds
    #
    # Gen Pcds of Inf
    # <TokenSpaceGuidCName>.<PcdCName>[|<Value>]
    #
    # @param ContainerFile: The Dec file full path 
    #
    def GenPcds(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_PCDS)
        Pcds = {}
        
        #
        # Get all Guids
        #
        RecordSet1 = self.RecordSet[MODEL_PCD_FIXED_AT_BUILD]
        RecordSet2 = self.RecordSet[MODEL_PCD_PATCHABLE_IN_MODULE]
        RecordSet3 = self.RecordSet[MODEL_PCD_FEATURE_FLAG]
        RecordSet4 = self.RecordSet[MODEL_PCD_DYNAMIC_EX]
        RecordSet5 = self.RecordSet[MODEL_PCD_DYNAMIC]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet1:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    if self.Module.Header[Arch].LibraryClass != {}:
                        pass
                    MergeArches(Pcds, self.GetPcdOfInf(Record[0], TAB_PCDS_FIXED_AT_BUILD, ContainerFile, Record[2]), Arch)
            for Record in RecordSet2:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Pcds, self.GetPcdOfInf(Record[0], TAB_PCDS_PATCHABLE_IN_MODULE, ContainerFile, Record[2]), Arch)
            for Record in RecordSet3:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Pcds, self.GetPcdOfInf(Record[0], TAB_PCDS_FEATURE_FLAG, ContainerFile, Record[2]), Arch)
            for Record in RecordSet4:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Pcds, self.GetPcdOfInf(Record[0], TAB_PCDS_DYNAMIC_EX, ContainerFile, Record[2]), Arch)
            for Record in RecordSet5:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Pcds, self.GetPcdOfInf(Record[0], "", ContainerFile, Record[2]), Arch)

        for Key in Pcds.keys():
            Pcd = PcdClass()
            Pcd.CName = Key[1]
            Pcd.TokenSpaceGuidCName = Key[0]
            Pcd.DefaultValue = Key[2]
            Pcd.ItemType = Key[3]
            Pcd.SupArchList = Pcds[Key]
            self.Module.PcdCodes.append(Pcd)
    
    ## GenSources
    #
    # Gen Sources of Inf
    # <Filename>[|<Family>[|<TagName>[|<ToolCode>[|<PcdFeatureFlag>]]]]
    #
    # @param ContainerFile: The Dec file full path 
    #
    def GenSources(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_SOURCES)
        Sources = {}

        #
        # Get all Nmakes
        #
        RecordSet = self.RecordSet[MODEL_EFI_SOURCE_FILE]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Sources, GetSource(Record[0], ContainerFile, self.Identification.FileRelativePath, Record[2]), Arch)

        for Key in Sources.keys():
            Source = ModuleSourceFileClass(Key[0], Key[2], Key[3], Key[1], Key[4], Sources[Key])
            self.Module.Sources.append(Source)
    
    ## GenUserExtensions
    #
    # Gen UserExtensions of Inf
    #
    def GenUserExtensions(self, ContainerFile):
#        #
#        # UserExtensions
#        #
#        if self.UserExtensions != '':
#            UserExtension = UserExtensionsClass()
#            Lines = self.UserExtensions.splitlines()
#            List = GetSplitValueList(Lines[0], DataType.TAB_SPLIT, 2)
#            if len(List) != 3:
#                RaiseParserError(Lines[0], 'UserExtensions', File, "UserExtensions.UserId.'Identifier'")
#            else:
#                UserExtension.UserID = List[1]
#                UserExtension.Identifier = List[2][0:-1].replace("'", '').replace('\"', '')
#                for Line in Lines[1:]:
#                    UserExtension.Content = UserExtension.Content + CleanString(Line) + '\n'
#            self.Module.UserExtensions.append(UserExtension)
        pass

    ## GenGuids
    #
    # Gen Guids of Inf
    # <CName>=<GuidValue>
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenGuids(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_GUIDS)
        Guids = {}
        #
        # Get all Guids
        #
        RecordSet = self.RecordSet[MODEL_EFI_GUID]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Guids, Record[0], Arch)
        
        for Key in Guids.keys():
            Guid = GuidClass()
            Guid.CName = Key
            Guid.SupArchList = Guids[Key]
            self.Module.Guids.append(Guid)

    ## GenProtocols
    #
    # Gen Protocols of Inf
    # <CName>
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenProtocols(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_PROTOCOLS)
        Protocols = {}
        #
        # Get all Guids
        #
        RecordSet = self.RecordSet[MODEL_EFI_PROTOCOL]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Protocols, Record[0], Arch)
                
        for Key in Protocols.keys():
            Protocol = ProtocolClass()
            Protocol.CName = Key
            Protocol.SupArchList = Protocols[Key]
            self.Module.Protocols.append(Protocol)
    
    ## GenPpis
    #
    # Gen Ppis of Inf
    # <CName>
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenPpis(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_PPIS)
        Ppis = {}
        #
        # Get all Guids
        #
        RecordSet = self.RecordSet[MODEL_EFI_PPI]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Ppis, Record[0], Arch)

        for Key in Ppis.keys():
            Ppi = PpiClass()
            Ppi.CName = Key
            Ppi.SupArchList = Ppis[Key]
            self.Module.Ppis.append(Ppi)

    ## GenDepexes
    #
    # Gen Depex of Inf
    #
    # @param ContainerFile: The Inf file full path 
    #
    def GenDepexes(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_DEPEX)
        Depex = {}
        #
        # Get all Depexes
        #
        RecordSet = self.RecordSet[MODEL_EFI_DEPEX]
        
        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            Line = ''
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    Line = Line + Record[0] + ' '
            MergeArches(Depex, Line, Arch)

        for Key in Depex.keys():
            Dep = ModuleDepexClass()
            Dep.Depex = Key
            Dep.SupArchList = Depex[Key]
            self.Module.Depex.append(Dep)

    ## GenBinaries
    #
    # Gen Binary of Inf
    # <FileType>|<Filename>|<Target>[|<TokenSpaceGuidCName>.<PcdCName>]
    #
    # @param ContainerFile: The Dec file full path 
    #
    def GenBinaries(self, ContainerFile):
        EdkLogger.debug(2, "Generate %s ..." % TAB_BINARIES)
        Binaries = {}
        
        #
        # Get all Guids
        #
        RecordSet = self.RecordSet[MODEL_EFI_BINARY_FILE]

        #
        # Go through each arch
        #
        for Arch in self.SupArchList:
            for Record in RecordSet:
                if Record[1] == Arch or Record[1] == TAB_ARCH_COMMON:
                    MergeArches(Binaries, GetBinary(Record[0], ContainerFile, self.Identification.FileRelativePath, Record[2]), Arch)

        for Key in Binaries.keys():
            Binary = ModuleBinaryFileClass(NormPath(Key[1]), Key[0], Key[2], Key[3], Binaries[Key])
            self.Module.Binaries.append(Binary)

    ## Parse DEFINE statement
    #
    # Get DEFINE macros
    #
    # 1. Insert a record into TblDec
    # Value1: Macro Name
    # Value2: Macro Value
    #
    def ParseDefine(self, LineValue, StartLine, Table, FileID, Filename, SectionName, Model, Arch):
        EdkLogger.debug(EdkLogger.DEBUG_2, "DEFINE statement '%s' found in section %s" % (LineValue, SectionName))
        SectionModel = Section[SectionName.upper()]
        Define = GetSplitValueList(CleanString(LineValue[LineValue.upper().find(DataType.TAB_DEFINE.upper() + ' ') + len(DataType.TAB_DEFINE + ' ') : ]), TAB_EQUAL_SPLIT, 1)
        Table.Insert(Model, Define[0], Define[1], '', '', '', Arch, SectionModel, FileID, StartLine, -1, StartLine, -1, 0)

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.DEBUG_0)
        
    W = os.getenv('WORKSPACE')
    F = os.path.join(W, 'MdeModulePkg/Application/HelloWorld/HelloWorld.inf')
    
    Db = Database.Database(DATABASE_PATH)
    Db.InitDatabase()
    
    P = Inf(os.path.normpath(F), False, True, W, Db)
    P.ShowModule()
    
    Db.Close()
