# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define each component of DEC file
#

import os
from String import *
from DataType import *
from Identification import *
from Dictionary import *
from CommonDataClass.PackageClass import *
from BuildToolError import *

class DecObject(object):
    def __init__(self):
        object.__init__()

class DecDefines(DecObject):
    def __init__(self):
        self.DefinesDictionary = {
            #Req
            TAB_DEC_DEFINES_DEC_SPECIFICATION           : [''],
            TAB_DEC_DEFINES_PACKAGE_NAME                : [''],
            TAB_DEC_DEFINES_PACKAGE_GUID                : [''],
            TAB_DEC_DEFINES_PACKAGE_VERSION             : ['']
        }
        
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

class Dec(DecObject):
    def __init__(self, filename = None, isMergeAllArches = False, isToPackage = False):
        self.Identification = Identification()
        self.Defines = DecDefines()
        self.UserExtensions = ''
        self.Package = PackageClass()
        
        self.Contents = {}
        for key in DataType.ARCH_LIST_FULL:
            self.Contents[key] = DecContents()
        
        self.KeyList = [
            TAB_INCLUDES, TAB_GUIDS, TAB_PROTOCOLS, TAB_PPIS, TAB_LIBRARY_CLASSES, \
            TAB_PCDS_FIXED_AT_BUILD_NULL, TAB_PCDS_PATCHABLE_IN_MODULE_NULL, TAB_PCDS_FEATURE_FLAG_NULL, \
            TAB_PCDS_DYNAMIC_NULL, TAB_PCDS_DYNAMIC_EX_NULL
        ]
    
        if filename != None:
            self.LoadDecFile(filename)
            
        if isMergeAllArches:
            self.MergeAllArches()
        
        if isToPackage:
            self.DecToPackage()
    
    def ParseDec(self, Lines, Key, KeyField):
        newKey = SplitModuleType(Key)
        if newKey[0].find(DataType.TAB_LIBRARY_CLASSES.upper()) != -1:
            GetLibraryClassesWithModuleType(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
        else:
            GetMultipleValuesOfKeyFromLines(Lines, Key, KeyField, TAB_COMMENT_SPLIT)
            
    def MergeAllArches(self):
        for key in self.KeyList:
            for arch in DataType.ARCH_LIST:
                Command = "self.Contents[arch]." + key + ".extend(" + "self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ")"
                eval(Command)

    def LoadDecFile(self, Filename):
        (Filepath, Name) = os.path.split(Filename)
        self.Identification.FileName = Name
        self.Identification.FileFullPath = Filename
        self.Identification.FileRelativePath = Filepath
        
        f = open(Filename, 'r').read()
        PreCheck(Filename, f, self.KeyList)
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
                    if tab == target:
                        if arch != DataType.TAB_ARCH_NULL:
                            Command = 'self.ParseDec(sect, tab, self.Contents[arch].' + key + ')'
                            eval(Command)
                            continue
                        else:
                            Command = "self.ParseDec(sect, tab, self.Contents['" + DataType.TAB_ARCH_COMMON + "']." + key + ')'
                            eval(Command)
                            continue
        #EndFor

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
        
        #Includes
        Includes = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Includes:
                MergeArches(Includes, Item, Arch)
        for Key in Includes.keys():
            Include = IncludeClass()
            Include.FilePath = Key
            Include.SupArchList = Includes[Key]
            self.Package.Includes.append(Include)
            
        #Guids
        Guids = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Guids:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    ErrorMsg = "Wrong statement '%s' found in section Guids in file '%s', correct format is '<CName>=<GuidValue>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Guids, (List[0], List[1]), Arch)
        for Key in Guids.keys():
            Guid = GuidClass()
            Guid.CName = Key[0]
            Guid.Guid = Key[1]
            Guid.SupArchList = Guids[Key]
            self.Package.GuidDeclarations.append(Guid)

        #Protocols
        Protocols = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Protocols:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    ErrorMsg = "Wrong statement '%s' found in section Protocols in file '%s', correct format is '<CName>=<GuidValue>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Protocols, (List[0], List[1]), Arch)
        for Key in Protocols.keys():
            Protocol = ProtocolClass()
            Protocol.CName = Key[0]
            Protocol.Guid = Key[1]
            Protocol.SupArchList = Protocols[Key]
            self.Package.ProtocolDeclarations.append(Protocol)
        
        #Ppis
        Ppis = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].Ppis:
                List = GetSplitValueList(Item, DataType.TAB_EQUAL_SPLIT)
                if len(List) != 2:
                    ErrorMsg = "Wrong statement '%s' found in section Ppis in file '%s', correct format is '<CName>=<GuidValue>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
                    MergeArches(Ppis, (List[0], List[1]), Arch)
        for Key in Ppis.keys():
            Ppi = PpiClass()
            Ppi.CName = Key[0]
            Ppi.Guid = Key[1]
            Ppi.SupArchList = Ppis[Key]
            self.Package.PpiDeclarations.append(Ppi)
            
        #LibraryClasses
        LibraryClasses = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].LibraryClasses:
                List = GetSplitValueList(Item[0], DataType.TAB_VALUE_SPLIT)
                if len(List) != 2:
                    ErrorMsg = "Wrong statement '%s' found in section LibraryClasses in file '%s', correct format is '<CName>=<GuidValue>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                else:
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
        
        #Pcds
        Pcds = {}
        for Arch in DataType.ARCH_LIST:
            for Item in self.Contents[Arch].PcdsFixedAtBuild:
                List = GetSplitValueList(Item)
                if len(List) != 5:
                    ErrorMsg = "Wrong statement '%s' found in section PcdsFixedAtBuild in file '%s', correct format is '<TokenCName>|<Token>|<CName>|<DatumType>|<Default>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4],TAB_PCDS_FIXED_AT_BUILD), Arch)
            for Item in self.Contents[Arch].PcdsPatchableInModule:
                List = GetSplitValueList(Item)
                if len(List) != 5:
                    ErrorMsg = "Wrong statement '%s' found in section PcdsPatchableInModule in file '%s', correct format is '<TokenCName>|<Token>|<CName>|<DatumType>|<Default>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4], TAB_PCDS_PATCHABLE_IN_MODULE), Arch)
            for Item in self.Contents[Arch].PcdsFeatureFlag:
                List = GetSplitValueList(Item)
                if len(List) != 5:
                    ErrorMsg = "Wrong statement '%s' found in section PcdsFeatureFlag in file '%s', correct format is '<TokenCName>|<Token>|<CName>|<DatumType>|<Default>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4], TAB_PCDS_FEATURE_FLAG), Arch)
            for Item in self.Contents[Arch].PcdsDynamicEx:
                List = GetSplitValueList(Item)
                if len(List) != 5:
                    ErrorMsg = "Wrong statement '%s' found in section PcdsDynamicEx in file '%s', correct format is '<TokenCName>|<Token>|<CName>|<DatumType>|<Default>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4], TAB_PCDS_DYNAMIC_EX), Arch)
            for Item in self.Contents[Arch].PcdsDynamic:
                List = GetSplitValueList(Item)
                if len(List) != 5:
                    ErrorMsg = "Wrong statement '%s' found in section PcdsDynamic in file '%s', correct format is '<TokenCName>|<Token>|<CName>|<DatumType>|<Default>'" % (Item, self.Package.Header.FullPath) 
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
                MergeArches(Pcds, (List[0], List[1], List[2], List[3], List[4], TAB_PCDS_DYNAMIC), Arch)
        for Key in Pcds.keys():
            Pcd = PcdClass()
            Pcd.CName = Key[0]
            Pcd.Token = Key[1]
            Pcd.TokenSpaceGuidCName = Key[2]
            Pcd.DatumType = Key[3]
            Pcd.DefaultValue = Key[4]
            Pcd.ItemType = Key[5]
            Pcd.SupArchList = Pcds[Key]
            self.Package.PcdDeclarations.append(Pcd)
    
    def ShowDec(self):
        print TAB_SECTION_START + TAB_INF_DEFINES + TAB_SECTION_END
        printDict(self.Defines.DefinesDictionary)

        for key in self.KeyList:
            for arch in DataType.ARCH_LIST_FULL:
                Command = "printList(TAB_SECTION_START + '" + \
                                    key + DataType.TAB_SPLIT + arch + \
                                    "' + TAB_SECTION_END, self.Contents[arch]." + key + ')'
                eval(Command)
    
    def ShowPackage(self):
        m = self.Package
        print 'Filename =', m.Header.FileName
        print 'FullPath =', m.Header.FullPath
        print 'BaseName =', m.Header.Name
        print 'Guid =', m.Header.Guid
        print 'Version =', m.Header.Version
        print 'DecSpecification =', m.Header.DecSpecification
        print '\nIncludes =', m.Includes
        for Item in m.Includes:
            print Item.FilePath, Item.SupArchList
        print '\nGuids =', m.GuidDeclarations
        for Item in m.GuidDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nProtocols =', m.ProtocolDeclarations
        for Item in m.ProtocolDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nPpis =', m.PpiDeclarations
        for Item in m.PpiDeclarations:
            print Item.CName, Item.Guid, Item.SupArchList
        print '\nLibraryClasses =', m.LibraryClassDeclarations
        for Item in m.LibraryClassDeclarations:
            print Item.LibraryClass, Item.RecommendedInstance, Item.SupModuleList, Item.SupArchList
        print '\nPcds =', m.PcdDeclarations
        for Item in m.PcdDeclarations:
            print Item.CName, Item.TokenSpaceGuidCName, Item.DefaultValue, Item.ItemType, Item.Token, Item.DatumType, Item.SupArchList

if __name__ == '__main__':
    p = Dec()
    directory = 'C:\Documents and Settings\\hchen30\\Desktop\\prototype\\dec'
    fileList = []
    for f in os.listdir(directory):
        if os.path.splitext(os.path.normcase(f))[1] == '.dec':
            fileList.append(os.path.join(directory, os.path.normcase(f)))
            
    for f in fileList:
        p = Dec(f, True, True)
        #p.ShowDec()
        p.ShowPackage()
