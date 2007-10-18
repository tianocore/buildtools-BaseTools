## @file
# This file is used to define each component of DEC file
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
from String import *
from DataType import *
from Identification import *
from Dictionary import *
from CommonDataClass.PackageClass import *
from BuildToolError import *

## DecObject
#
# This class defined basic Dec object which is used by inheriting
# 
# @param object:       Inherited from object class
#
class DecObject(object):
    def __init__(self):
        object.__init__()

## DecDefines
#
# This class defined basic Defines used in Dec object
# 
# @param DecObject:        Inherited from DecObject class
#
# @var DefinesDictionary:  To store value for DefinesDictionary 
#
class DecDefines(DecObject):
    def __init__(self):
        self.DefinesDictionary = {
            #
            # Required Fields
            #
            TAB_DEC_DEFINES_DEC_SPECIFICATION           : [''],
            TAB_DEC_DEFINES_PACKAGE_NAME                : [''],
            TAB_DEC_DEFINES_PACKAGE_GUID                : [''],
            TAB_DEC_DEFINES_PACKAGE_VERSION             : ['']
        }

## DecContents
#
# This class defined basic Contents used in Dec object
# 
# @param DecObject:            Inherited from DecObject class
#
# @var Includes:               To store value for Includes
# @var Guids:                  To store value for Guids
# @var Protocols:              To store value for Protocols
# @var Ppis:                   To store value for Ppis
# @var LibraryClasses:         To store value for LibraryClasses
# @var PcdsFixedAtBuild:       To store value for PcdsFixedAtBuild
# @var PcdsPatchableInModule:  To store value for PcdsPatchableInModule
# @var PcdsFeatureFlag:        To store value for PcdsFeatureFlag
# @var PcdsDynamic:            To store value for PcdsDynamic
# @var PcdsDynamicEx:          To store value for PcdsDynamicEx
#
class DecContents(DecObject):
    def __init__(self):
        self.Includes = []
        self.Guids = []
        self.Protocols = []
        self.Ppis = []
        self.LibraryClasses = []
        self.PcdsFixedAtBuild = []
        self.PcdsPatchableInModule = []
        self.PcdsFeatureFlag = []
        self.PcdsDynamic = []
        self.PcdsDynamicEx = []

## Dec
#
# This class defined the structure used in Dec object
# 
# @param DecObject:         Inherited from DecObject class
# @param Filename:          Input value for Filename of Dec file, default is None
# @param IsMergeAllArches:  Input value for IsMergeAllArches
#                           True is to merge all arches
#                           Fales is not to merge all arches
#                           default is False
# @param IsToPackage:       Input value for IsToPackage
#                           True is to transfer to PackageObject automatically
#                           False is not to transfer to PackageObject automatically
#                           default is False
# @param WorkspaceDir:      Input value for current workspace directory, default is None
#
# @var Identification:      To store value for Identification, it is a structure as Identification
# @var Defines:             To store value for Defines, it is a structure as DecDefines
# @var UserExtensions:      To store value for UserExtensions
# @var Package:             To store value for Package, it is a structure as PackageClass
# @var WorkspaceDir:        To store value for WorkspaceDir
# @var Contents:            To store value for Contents, it is a structure as DecContents
# @var KeyList:             To store value for KeyList, a list for all Keys used in Dec
#
class Dec(DecObject):
    def __init__(self, Filename = None, IsMergeAllArches = False, IsToPackage = False, WorkspaceDir = None):
        self.Identification = Identification()
        self.Defines = DecDefines()
        self.UserExtensions = ''
        self.Package = PackageClass()
        self.WorkspaceDir = WorkspaceDir
        
        self.Contents = {}
        for Arch in DataType.ARCH_LIST_FULL:
            self.Contents[Arch] = DecContents()
        
        self.KeyList = [
            TAB_INCLUDES, TAB_GUIDS, TAB_PROTOCOLS, TAB_PPIS, TAB_LIBRARY_CLASSES, \
            TAB_PCDS_FIXED_AT_BUILD_NULL, TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
            TAB_PCDS_DYNAMIC_NULL, TAB_PCDS_DYNAMIC_EX_NULL
        ]
    
        #
        # Load Dec file if filename is not None
        #
        if Filename != None:
            self.LoadDecFile(Filename)
        
        #
        # Merge contents of Dec from all arches if IsMergeAllArches is True
        #
        if IsMergeAllArches:
            self.MergeAllArches()
        
        #
        # Transfer to Package Object if IsToPackage is True
        #
        if IsToPackage:
            self.DecToPackage()
    
    ## Parse Dec file
    #
    # Go through input lines one by one to find the value defined in Key section.
    # Save them to KeyField
    #
    # @param Lines:     Lines need to be parsed
    # @param Key:       The key value of the section to be located
    # @param KeyField:  To save the found contents
    #
    def ParseDec(self, Lines, Key, KeyField):
        newKey = SplitModuleType(Key)
        if newKey[0].upper().find(DataType.TAB_LIBRARY_CLASSES.upper()) != -1:
            GetLibraryClassesWithModuleType(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        else:
            GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)

    ## Merge contents of Dec from all arches
    #
    # Find the contents defined in all arches and merge them to all
    #   
    def MergeAllArches(self):
        for Key in self.KeyList:
            for Arch in DataType.ARCH_LIST:
                Command = "self.Contents[Arch]." + Key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + Key + ")"
                eval(Command)

    ## Load Dec file
    #
    # Load the file if it exists
    #
    # @param Filename:  Input value for filename of Dec file
    #
    def LoadDecFile(self, Filename):
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
                        if Tab.upper() == Target:
                            if Arch != DataType.TAB_ARCH_NULL:
                                Command = 'self.ParseDec(Sect, Tab, self.Contents[Arch].' + Key + ')'
                                eval(Command)
                                continue
                            else:
                                Command = "self.ParseDec(Sect, Tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + Key + ')'
                                eval(Command)
                                continue
        #EndFor

    ## Transfer to Package Object
    # 
    # Transfer all contents of a Dec file to a standard Package Object
    #
    def DecToPackage(self):
        #
        # Get value for Header
        #
        self.Package.Header.Name = self.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_NAME][0]
        self.Package.Header.Guid = self.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_GUID][0]
        self.Package.Header.Version = self.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_VERSION][0]
        self.Package.Header.FileName = self.Identification.FileName
        self.Package.Header.FullPath = self.Identification.FileFullPath
        self.Package.Header.DecSpecification = self.Defines.DefinesDictionary[TAB_DEC_DEFINES_DEC_SPECIFICATION][0]
        File = self.Package.Header.FullPath
        
        #
        # Includes
        # <IncludeDirectory>
        #
        Includes = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Includes:
                MergeArches(Includes, Item, Arch)
        for Key in Includes.keys():
            Include = IncludeClass()
            Include.FilePath = Key
            Include.SupArchList = Includes[Key]
            self.Package.Includes.append(Include)
            
        #
        # Guids
        # <CName>=<GuidValue>
        #
        Guids = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Guids:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    RaiseParserError(Item, 'Guids', File, '<CName>=<GuidValue>')
                else:
                    MergeArches(Guids, (List[0], List[1]), Arch)
        for Key in Guids.keys():
            Guid = GuidClass()
            Guid.CName = Key[0]
            Guid.Guid = Key[1]
            Guid.SupArchList = Guids[Key]
            self.Package.GuidDeclarations.append(Guid)

        # 
        # Protocols
        # <CName>=<GuidValue>
        #
        Protocols = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Protocols:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    RaiseParserError(Item, 'Protocols', File, '<CName>=<GuidValue>')
                else:
                    MergeArches(Protocols, (List[0], List[1]), Arch)
        for Key in Protocols.keys():
            Protocol = ProtocolClass()
            Protocol.CName = Key[0]
            Protocol.Guid = Key[1]
            Protocol.SupArchList = Protocols[Key]
            self.Package.ProtocolDeclarations.append(Protocol)
        
        #
        # Ppis
        # <CName>=<GuidValue>
        #
        Ppis = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Ppis:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    RaiseParserError(Item, 'Ppis', File, '<CName>=<GuidValue>')
                else:
                    MergeArches(Ppis, (List[0], List[1]), Arch)
        for Key in Ppis.keys():
            Ppi = PpiClass()
            Ppi.CName = Key[0]
            Ppi.Guid = Key[1]
            Ppi.SupArchList = Ppis[Key]
            self.Package.PpiDeclarations.append(Ppi)
            
        #
        # LibraryClasses
        # <LibraryClassName>|<LibraryClassInstance>
        #
        LibraryClasses = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].LibraryClasses:
                List = GetSplitValueList(Item[0], DataType.TAB_VALUE_SPLIT)
                if len(List) != 2:
                    RaiseParserError(Item[0], 'LibraryClasses', File, '<LibraryClassName>|<LibraryClassInstanceFilename>')
                else:
                    CheckFileExist(self.WorkspaceDir, os.path.join(self.Identification.FileRelativePath, List[1]), File, 'LibraryClasses', Item[0])
                    if Item[1] == ['']:
                            Item[1] = DataType.SUP_MODULE_LIST
                    MergeArches(LibraryClasses, (List[0], List[1]) + tuple(Item[1]), Arch)
        for Key in LibraryClasses.keys():
            LibraryClass = LibraryClassClass()
            LibraryClass.LibraryClass = Key[0]
            LibraryClass.RecommendedInstance = Key[1]
            LibraryClass.SupModuleList = list(Key[2:])
            LibraryClass.SupArchList = LibraryClasses[Key]
            self.Package.LibraryClassDeclarations.append(LibraryClass)
        
        #
        # Pcds
        # <TokenSpcCName>.<TokenCName>|<Value>|<DatumType>|<Token>
        #
        Pcds = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].PcdsFixedAtBuild:
                MergeArches(Pcds, self.GetPcdOfDec(Item, TAB_PCDS_FIXED_AT_BUILD, File), Arch)
            
            for Item in self.Contents[Arch].PcdsPatchableInModule:
                MergeArches(Pcds, self.GetPcdOfDec(Item, TAB_PCDS_PATCHABLE_IN_MODULE, File), Arch)
            
            for Item in self.Contents[Arch].PcdsFeatureFlag:
                MergeArches(Pcds, self.GetPcdOfDec(Item, TAB_PCDS_FEATURE_FLAG, File), Arch)
            
            for Item in self.Contents[Arch].PcdsDynamicEx:
                MergeArches(Pcds, self.GetPcdOfDec(Item, TAB_PCDS_DYNAMIC_EX, File), Arch)
            
            for Item in self.Contents[Arch].PcdsDynamic:
                MergeArches(Pcds, self.GetPcdOfDec(Item, TAB_PCDS_DYNAMIC, File), Arch)

        for Key in Pcds.keys():
            Pcd = PcdClass()
            Pcd.CName = Key[1]
            Pcd.Token = Key[4]
            Pcd.TokenSpaceGuidCName = Key[0]
            Pcd.DatumType = Key[3]
            Pcd.DefaultValue = Key[2]
            Pcd.ItemType = Key[5]
            Pcd.SupArchList = Pcds[Key]
            self.Package.PcdDeclarations.append(Pcd)
    
    ## Get Pcd Values of Dec
    #
    # Get Pcd of Dec as <TokenSpcCName>.<TokenCName>|<Value>|<DatumType>|<Token>
    # @retval (TokenSpcCName, TokenCName, Value, DatumType, Token, ItemType) Formatted Pcd Item
    #
    def GetPcdOfDec(self, Item, Type, File):
        Format = '<TokenSpaceGuidCName>.<PcdCName>|<Value>|<DatumType>|<Token>'
        List = GetSplitValueList(Item)
        if len(List) != 4:
            RaiseParserError(Item, 'Pcds' + Type, File, Format)
        TokenInfo = GetSplitValueList(List[0], DataType.TAB_SPLIT)
        if len(TokenInfo) != 2:
            RaiseParserError(Item, 'Pcds' + Type, File, Format)
        
        return (TokenInfo[0], TokenInfo[1], List[1], List[2], List[3], Type)
    
    ## Show detailed information of Dec
    #
    # Print all members and their values of Dec class
    #
    def ShowDec(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for key in self.KeyList:
            for arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                                    key + DataType.TAB_SPLIT + arch + \
                                    "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
                eval(Command)
    
    ## Show detailed information of Package
    #
    # Print all members and their values of Package class
    #
    def ShowPackage(self):
        M = self.Package
        print 'Filename =', M.Header.FileName
        print 'FullPath =', M.Header.FullPath
        print 'BaseName =', M.Header.Name
        print 'Guid =', M.Header.Guid
        print 'Version =', M.Header.Version
        print 'DecSpecification =', M.Header.DecSpecification
        print '\nIncludes =', M.Includes
        for Item in M.Includes:
            print Item.FilePath, Item.SupArchList
        print '\nGuids =', M.GuidDeclarations
        for Item in M.GuidDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nProtocols =', M.ProtocolDeclarations
        for Item in M.ProtocolDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nPpis =', M.PpiDeclarations
        for Item in M.PpiDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nLibraryClasses =', M.LibraryClassDeclarations
        for Item in M.LibraryClassDeclarations:
            print Item.LibraryClass, Item.RecommendedInstance, Item.SupModuleList, Item.SupArchList
        print '\nPcds =', M.PcdDeclarations
        for Item in M.PcdDeclarations:
            print 'CName=', Item.CName, 'TokenSpaceGuidCName=', Item.TokenSpaceGuidCName, 'DefaultValue=', Item.DefaultValue, 'ItemType=', Item.ItemType, 'Token=', Item.Token, 'DatumType=', Item.DatumType, Item.SupArchList

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    W = os.getenv('WORKSPACE')
    F = os.path.join(W, 'Nt32Pkg/Nt32Pkg.dec')
    P = Dec(os.path.normpath(F), True, True, W)
    P.ShowPackage()
