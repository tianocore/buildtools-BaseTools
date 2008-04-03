## @file
# This file is used to create a database used by ECC tool
#
# Copyright (c) 2007 ~ 2008, Intel Corporation
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
import sqlite3
import os
import os.path

import Common.EdkLogger as EdkLogger
from CommonDataClass.DataClass import *
from CommonDataClass.ModuleClass import *
from Common.String import *
from Common.DataType import *
from Common.Misc import tdict
from Common.Misc import sdict

from MetaDataTable import *
from MetaFileTable import *
from MetaFileParser import *
from BuildClassObject import *

def ValidFile(File, Dir='.'):
    Wd = os.getcwd()
    os.chdir(Dir)
    if not os.path.exists(File):
        os.chdir(Wd)
        return False
    os.chdir(Wd)
    return True

class DscBuildData(PlatformBuildClassObject):
    #_PROPERTY_ = {
    #    TAB_DSC_DEFINES_PLATFORM_NAME           : '_PlatformName'
    #    TAB_DSC_DEFINES_PLATFORM_GUID           : '_Guid'
    #    TAB_DSC_DEFINES_PLATFORM_VERSION        : '_Version'
    #    TAB_DSC_DEFINES_DSC_SPECIFICATION       : '_DscSpecification'
    #    TAB_DSC_DEFINES_OUTPUT_DIRECTORY        : '_OutputDirectory'
    #    TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES : '_SupArchList'
    #    TAB_DSC_DEFINES_BUILD_TARGETS           : '_BuildTargets'
    #    TAB_DSC_DEFINES_SKUID_IDENTIFIER        : '_SkuId'
    #    TAB_DSC_DEFINES_FLASH_DEFINITION        : '_FlashDefinition'
    #    TAB_DSC_DEFINES_BUILD_NUMBER            : '_BuildNumber'
    #    TAB_DSC_DEFINES_MAKEFILE_NAME           : '_MakefileName'
    #    TAB_DSC_DEFINES_BS_BASE_ADDRESS         : '_BsBaseAddress'
    #    TAB_DSC_DEFINES_RT_BASE_ADDRESS         : '_RtBaseAddress'
    #}
    _PCD_TYPE_STRING_ = {
        MODEL_PCD_FIXED_AT_BUILD        :   "FixedAtBuild",
        MODEL_PCD_PATCHABLE_IN_MODULE   :   "PatchableInModule",
        MODEL_PCD_FEATURE_FLAG          :   "FeatureFlag",
        MODEL_PCD_DYNAMIC               :   "Dynamic",
        MODEL_PCD_DYNAMIC_DEFAULT       :   "Dynamic",
        MODEL_PCD_DYNAMIC_HII           :   "DynamicHii",
        MODEL_PCD_DYNAMIC_VPD           :   "DynamicVpd",
        MODEL_PCD_DYNAMIC_EX            :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_DEFAULT    :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_HII        :   "DynamicExHii",
        MODEL_PCD_DYNAMIC_EX_VPD        :   "DynamicExVpd",
    }

    _NullLibraryNumber = 0

    def __init__(self, FilePath, Table, Db, Arch='COMMON', Macros={}):
        self.DescFilePath = FilePath
        self._Table = Table
        self._Db = Db
        self._Arch = Arch
        self._Macros = Macros
        self._Clear()

    def __repr__(self):
        S = '[Platform.%s]\n' % self.Arch
        S += "\tName = %s\n" % self.PlatformName
        S += "\tGuid = %s\n" % self.Guid
        S += "\tVer = %s\n" % self.Version
        S += "\n"
        S += "\tSpecification = %s\n" % self.DscSpecification
        S += "\tOutputDirectory = %s\n" % self.OutputDirectory 
        S += "\tSupArchList = %s\n" % self.SupArchList     
        S += "\tBuildTargets = %s\n" % self.BuildTargets    
        S += "\tSkuName = %s\n" % self.SkuName           
        S += "\tFlashDefinition = %s\n" % self.FlashDefinition 
        S += "\tBuildNumber = %s\n" % self.BuildNumber     
        S += "\tMakefileName = %s\n" % self.MakefileName    
        S += "\tBsBaseAddress = %s\n" % self.BsBaseAddress   
        S += "\tRtBaseAddress = %s\n" % self.RtBaseAddress   

        S += '  <SkuId>\n'
        for SkuName in self.SkuIds:
            S += "\t%s = %s\n" % (SkuName, self.SkuIds[SkuName])

        #S += '  <LibraryClass>\n'
        #ModuleTypeList = set()
        #LibraryClassList = set()
        #for LibraryClass,ModuleType in self.LibraryClasses:
        #    LibraryClassList.add(LibraryClass)
        #    ModuleTypeList.add(ModuleType)
        #LibraryClassList = list(LibraryClassList)
        #ModuleTypeList = list(ModuleTypeList)
        #LibraryClassList.sort()
        #ModuleTypeList.sort()
        #for LibraryClass in LibraryClassList:
        #    for ModuleType in ModuleTypeList:
        #        if not (LibraryClass,ModuleType) in self.LibraryClasses:
        #            continue 
        #        S += "\t%32s, %-24s = %s\n" % (LibraryClass, ModuleType, self.LibraryClasses[LibraryClass,ModuleType])
        
        S += '  <PCD>\n'
        for Name, Guid in self.Pcds:
            S += "\t%s.%s\n\t\t%s\n" % (Guid, Name, str(self.Pcds[Name, Guid]))
        
        S += '  <BuildOption>\n'
        for ToolChainFamily,ToolChain in self.BuildOptions:
            S += "\t%s:%s = %s\n" % (ToolChainFamily, ToolChain, self.BuildOptions[ToolChainFamily, ToolChain])

        S += '  <Module>\n'
        S += "\t" + "\n\t".join([str(M) for M in self.Modules]) + '\n'
        return S

    ## XXX[key] = value
    #def __setitem__(self, key, value):
    #    self.__dict__[self._PROPERTY_[key]] = value
    #
    ### variable = XXX[key]
    #def __getitem__(self, key):
    #    return self.__dict__[self._PROPERTY_[key]]
    #
    ### "in" test support
    #def __contains__(self, key):
    #    return key in self._PROPERTY_

    def _Clear(self):
        self._PlatformName      = None
        self._Guid              = None
        self._Version           = None
        self._DscSpecification  = None
        self._OutputDirectory   = None
        self._SupArchList       = None
        self._BuildTargets      = None
        self._SkuName           = None
        self._FlashDefinition   = None
        self._BuildNumber       = None
        self._MakefileName      = None
        self._BsBaseAddress     = None
        self._RtBaseAddress     = None
        self._SkuIds            = None
        self._Modules           = None
        self._LibraryInstances  = None
        self._LibraryClasses    = None
        self._Libraries         = None
        self._Pcds              = None
        self._BuildOptions      = None

    def _GetArch(self):
        return self._Arch

    def _SetArch(self, Value):
        if self._Arch == Value:
            return
        self._Arch = Value
        self._Clear()

    def _GetPlatformName(self):
        if self._PlatformName == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_PLATFORM_NAME, self.Arch)
            self._PlatformName = RecordList[0][0]
        return self._PlatformName

    def _GetFileGuid(self):
        if self._Guid == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_PLATFORM_GUID, self.Arch)
            self._Guid = RecordList[0][0]
        return self._Guid

    def _GetVersion(self):
        if self._Version == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_PLATFORM_VERSION, self.Arch)
            self._Version = RecordList[0][0]
        return self._Version

    def _GetDscSpec(self):
        if self._DscSpecification == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_DSC_SPECIFICATION, self.Arch)
            self._DscSpecification = RecordList[0][0]
        return self._DscSpecification

    def _GetOutpuDir(self):
        if self._OutputDirectory == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_OUTPUT_DIRECTORY, self.Arch)
            File = NormPath(RecordList[0][0], self._Macros)
            LineNo = RecordList[0][-1]
            self._OutputDirectory = File
        return self._OutputDirectory

    def _GetSupArch(self):
        if self._SupArchList == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES, self.Arch)
            self._SupArchList = GetSplitValueList(RecordList[0][0], TAB_VALUE_SPLIT)
        return self._SupArchList

    def _GetBuildTarget(self):
        if self._BuildTargets == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_BUILD_TARGETS, self.Arch)
            self._BuildTargets = GetSplitValueList(RecordList[0][0])
        return self._BuildTargets

    def _GetSkuName(self):
        if self._SkuName == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_SKUID_IDENTIFIER, self.Arch)
            if len(RecordList) > 0:
                self._SkuName = RecordList[0][0]
                if self._SkuName not in self.SkuIds:
                    self._SkuName = 'DEFAULT'
            else:
                self._SkuName = 'DEFAULT'
        return self._SkuName

    def _GetFdfFile(self):
        if self._FlashDefinition == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_FLASH_DEFINITION, self.Arch)
            if len(RecordList) > 0:
                self._FlashDefinition = NormPath(RecordList[0][0])
            else:
                self._FlashDefinition = ''
        return self._FlashDefinition

    def _GetBuildNumber(self):
        if self._BuildNumber == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_BUILD_NUMBER, self.Arch)
            if len(RecordList) > 0:
                self._BuildNumber = RecordList[0][0]
        return self._BuildNumber

    def _GetMakefileName(self):
        if self._MakefileName == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_MAKEFILE_NAME, self.Arch)
            if len(RecordList):
                self._MakefileName = RecordList[0][0]
        return self._MakefileName

    def _GetBsBaseAddress(self):
        if self._BsBaseAddress == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_BS_BASE_ADDRESS, self.Arch)
            if len(RecordList) != 0:
                self._BsBaseAddress = RecordList[0][0]
        return self._BsBaseAddress

    def _GetRtBaseAddress(self):
        if self._RtBaseAddress == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DSC_DEFINES_RT_BASE_ADDRESS, self.Arch)
            if len(RecordList):
                self._RtBaseAddress = RecordList[0][0]
        return self._RtBaseAddress

    def _GetSkuIds(self):
        if self._SkuIds == None:
            self._SkuIds = {}
            RecordList = self._Table.Query(MODEL_EFI_SKU_ID)
            for Record in RecordList:
                self._SkuIds[Record[1]] = Record[0]
        return self._SkuIds

    def _GetModules(self):
        if self._Modules == None:
            self._Modules = []
            RecordList = self._Table.Query(MODEL_META_DATA_COMPONENT, Scope1=self.Arch)
            for Record in RecordList:
                ModuleFile = NormPath(Record[0], self._Macros)
                ModuleId = Record[5]
                LineNo = Record[6]
                if not ValidFile(ModuleFile):
                    EdkLogger.error('build', FILE_NOT_FOUND, File=self.DescFilePath, 
                                    ExtraData=ModuleFile, Line=LineNo)
                if ModuleFile in self._Modules:
                    continue
                Module = self._Db.BuildObject[ModuleFile, MODEL_FILE_INF, self._Arch]
                # only merge library classes and PCD for non-library module
                if Module.LibraryClass == None or Module.LibraryClass == []:
                    if Module.AutoGenVersion < 0x00010005:
                        self._ResolveLibraryReference(Module)
                    else:
                        self._MergeModuleInfo(Module, ModuleId)
                self._UpdateModulePcd(Module, ModuleId)
                self._MergeModuleBuildOption(Module, ModuleId)
                self._Modules.append(Module)
        return self._Modules

    def _MergeModuleInfo(self, Module, ModuleId):
        ModuleType = Module.ModuleType
        # merge library class/instance information
        for LibraryClass in Module.LibraryClasses:
            if self.LibraryClasses[LibraryClass, ModuleType] == None: continue
            Module.LibraryClasses[LibraryClass] = self.LibraryClasses[LibraryClass, ModuleType]
        RecordList = self._Table.Query(MODEL_EFI_LIBRARY_CLASS, Scope1=self.Arch, BelongsToItem=ModuleId)
        for Record in RecordList:
            LibraryClass = Record[0]
            LibraryPath = NormPath(Record[1], self._Macros)
            LineNo = Record[-1]
            if not ValidFile(LibraryPath):
                EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=LibraryPath,
                                File=self.DescFilePath, Line=LineNo)
            if LibraryClass == '' or LibraryClass == 'NULL':
                LibraryClass = 'NULL%d' % (self._NullLibraryNumber + 1)
                LibraryInstance = self._Db.BuildObject[LibraryPath, MODEL_FILE_INF, self._Arch]
                LibraryInstance.LibraryClass.append(LibraryClassObject(LibraryClass, [ModuleType]))
            Module.LibraryClasses[LibraryClass] = LibraryPath

        # R9 module
        LibraryConsumerList = [Module]
        Constructor         = []
        ConsumedByList      = sdict()
        LibraryInstance     = sdict()

        EdkLogger.verbose("")
        EdkLogger.verbose("Library instances of module [%s] [%s]:" % (str(Module), self.Arch))
        while len(LibraryConsumerList) > 0:
            M = LibraryConsumerList.pop()
            for LibraryClassName in M.LibraryClasses:
                LibraryPath = M.LibraryClasses[LibraryClassName]
                if LibraryPath == None or LibraryPath == "":
                    LibraryPath = self.LibraryClasses[LibraryClassName, ModuleType]
                    if LibraryPath == None and LibraryClassName not in LibraryInstance:
                        LibraryInstance[LibraryClassName] = None
                        continue
                if LibraryClassName not in LibraryInstance:
                    LibraryModule = self._Db.BuildObject[LibraryPath, MODEL_FILE_INF, self._Arch]
                    LibraryInstance[LibraryClassName] = LibraryModule
                    LibraryConsumerList.append(LibraryModule)
                    EdkLogger.verbose("\t" + str(LibraryClassName) + " : " + str(LibraryModule))
                else:
                    LibraryModule = LibraryInstance[LibraryClassName]

                if LibraryModule.ConstructorList != [] and LibraryModule not in Constructor:
                    Constructor.append(LibraryModule)

                if LibraryModule not in ConsumedByList:
                    ConsumedByList[LibraryModule] = []
                if M != Module:
                    if M in ConsumedByList[LibraryModule]:
                        continue
                    ConsumedByList[LibraryModule].append(M)
        #
        # Initialize the sorted output list to the empty set
        #
        SortedLibraryList = []
        #
        # Q <- Set of all nodes with no incoming edges
        #
        LibraryList = [] #LibraryInstance.values()
        Q = []
        for LibraryClassName in LibraryInstance:
            M = LibraryInstance[LibraryClassName]
            if M == None:
                EdkLogger.error("AutoGen", AUTOGEN_ERROR,
                                "Library instance for library class [%s] is not found" % LibraryClassName,
                                ExtraData="\t%s [%s]" % (str(Module), self.Arch))
            LibraryList.append(M)
            #
            # check if there're duplicate library classes
            #
            for Lc in M.LibraryClass:
                if Lc.SupModList != None and ModuleType not in Lc.SupModList:
                    EdkLogger.error("AutoGen", AUTOGEN_ERROR,
                                    "Module type [%s] is not supported by library instance [%s]" % (ModuleType, str(M)),
                                    ExtraData="\t%s" % str(Module))

                if Lc.LibraryClass in LibraryInstance and str(M) != str(LibraryInstance[Lc.LibraryClass]):
                    EdkLogger.error("AutoGen", AUTOGEN_ERROR,
                                    "More than one library instance found for library class [%s] in module [%s]" % (Lc.LibraryClass, Module),
                                    ExtraData="\t%s\n\t%s" % (LibraryInstance[Lc.LibraryClass], str(M))
                                    )
            if ConsumedByList[M] == []:
                Q.insert(0, M)
        #
        # while Q is not empty do
        #
        while Q != []:
            #
            # remove node from Q
            #
            Node = Q.pop()
            #
            # output Node
            #
            SortedLibraryList.append(Node)
            #
            # for each node Item with an edge e from Node to Item do
            #
            for Item in LibraryList:
                if Node not in ConsumedByList[Item]:
                    continue
                #
                # remove edge e from the graph
                #
                ConsumedByList[Item].remove(Node)
                #
                # If Item has no other incoming edges then
                #
                if ConsumedByList[Item] == []:
                    #
                    # insert Item into Q
                    #
                    Q.insert(0, Item)

            EdgeRemoved = True
            while Q == [] and EdgeRemoved:
                EdgeRemoved = False
                #
                # for each node Item with a Constructor
                #
                for Item in LibraryList:
                    if Item in Constructor:
                        #
                        # for each Node without a constructor with an edge e from Item to Node
                        #
                        for Node in ConsumedByList[Item]:
                            if Node not in Constructor:
                                #
                                # remove edge e from the graph
                                #
                                ConsumedByList[Item].remove(Node)
                                EdgeRemoved = True
                                if ConsumedByList[Item] == []:
                                    #
                                    # insert Item into Q
                                    #
                                    Q.insert(0, Item)
                                    break
                    if Q != []:
                        break

        #
        # if any remaining node Item in the graph has a constructor and an incoming edge, then the graph has a cycle
        #
        for Item in LibraryList:
            if ConsumedByList[Item] != [] and Item in Constructor and len(Constructor) > 1:
                ErrorMessage = 'Library [%s] with constructors has a cycle' % str(Item)
                EdkLogger.error("AutoGen", AUTOGEN_ERROR, ErrorMessage,
                                "\tconsumed by " + "\n\tconsumed by ".join([str(L) for L in ConsumedByList[Item]]))
            if Item not in SortedLibraryList:
                SortedLibraryList.append(Item)

        #
        # Build the list of constructor and destructir names
        # The DAG Topo sort produces the destructor order, so the list of constructors must generated in the reverse order
        #
        SortedLibraryList.reverse()
        Module.LibraryClasses = sdict()
        for L in SortedLibraryList:
            Module.LibraryClasses[L.LibraryClass[0].LibraryClass, ModuleType] = L
            #
            # Merge PCDs from library instance
            #
            for Key in L.Pcds:
                if Key not in Module.Pcds:
                    Module.Pcds[Key] = L.Pcds[Key]
            #
            # Merge GUIDs from library instance
            #
            for CName in L.Guids:
                if CName not in Module.Guids:
                    Module.Guids.append(CName)
            #
            # Merge Protocols from library instance
            #
            for CName in L.Protocols:
                if CName not in Module.Protocols:
                    Module.Protocols.append(CName)
            #
            # Merge Ppis from library instance
            #
            for CName in L.Ppis:
                if CName not in Module.Ppis:
                    Module.Ppis.append(CName)

    ##
    # for R8.x modules
    # 
    def _ResolveLibraryReference(self, Module):
        EdkLogger.verbose("")
        EdkLogger.verbose("Library instances of module [%s] [%s]:" % (str(Module), self._Arch))
        LibraryConsumerList = [Module]

        # "CompilerStub" is a must for R8 modules
        Module.Libraries.append("CompilerStub")
        while len(LibraryConsumerList) > 0:
            M = LibraryConsumerList.pop()
            for LibraryName in M.Libraries:
                if LibraryName not in self.Libraries:
                    EdkLogger.warn("AutoGen", "Library [%s] is not found" % LibraryName,
                                    ExtraData="\t%s [%s]" % (str(Module), Arch))
                    continue

                Library = self.Libraries[LibraryName]
                if (LibraryName, Module.ModuleType) not in Module.LibraryClasses:
                    Module.LibraryClasses[LibraryName, Module.ModuleType] = Library
                    LibraryConsumerList.append(Library)
                    EdkLogger.verbose("\t" + LibraryName + " : " + str(Library))

    def _UpdateModulePcd(self, Module, ModuleId):
        for Name,Guid in Module.Pcds:
            PcdInModule = Module.Pcds[Name,Guid]
            if (Name,Guid) in self.Pcds:
                PcdInPlatform = self.Pcds[Name,Guid]
                # 
                # in case there's PCDs coming from FDF file, which have no type given.
                # at this point, PcdInModule.Type has the type found from dependent
                # package
                # 
                if PcdInPlatform.Type != None and PcdInPlatform.Type != '':
                    PcdInModule.Type = PcdInPlatform.Type
                PcdInModule.MaxDatumSize = PcdInPlatform.MaxDatumSize
                PcdInModule.SkuInfoList = PcdInPlatform.SkuInfoList
                if PcdInPlatform.DefaultValue not in [None, '']:
                    PcdInModule.DefaultValue = PcdInPlatform.DefaultValue
                if PcdInPlatform.TokenValue not in [None, '']:
                    PcdInModule.TokenValue = PcdInPlatform.TokenValue
                if PcdInPlatform.MaxDatumSize not in [None, '']:
                    PcdInModule.MaxDatumSize = PcdInPlatform.MaxDatumSize
                if PcdInPlatform.DatumType not in [None, '']:
                    PcdInModule.DatumType = PcdInPlatform.DatumType

            if PcdInModule.DatumType == "VOID*" and PcdInModule.MaxDatumSize in ['', None]:
                EdkLogger.verbose("No MaxDatumSize specified for PCD %s.%s in module [%s]" % (Guid, Name, str(Module)))
                Value = PcdInModule.DefaultValue
                if Value[0] == 'L':
                    PcdInModule.MaxDatumSize = str(len(Value) * 2)
                elif Value[0] == '{':
                    PcdInModule.MaxDatumSize = str(len(Value.split(',')))
                else:
                    PcdInModule.MaxDatumSize = str(len(Value))

        RecordList = self._Table.Query(MODEL_PCD_FIXED_AT_BUILD, Scope1=self.Arch, BelongsToItem=ModuleId)
        for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (PcdCName, TokenSpaceGuid) not in Module.Pcds:
                continue
            TokenList = GetSplitValueList(Setting)
            Pcd = Module.Pcds[PcdCName, TokenSpaceGuid]
            Pcd.DefaultValue = TokenList[0]
            if len(TokenList) > 1:
                Pcd.MaxDatumSize = TokenList[1]
            Pcd.Type = self._PCD_TYPE_STRING_[MODEL_PCD_FIXED_AT_BUILD]

        RecordList = self._Table.Query(MODEL_PCD_PATCHABLE_IN_MODULE, Scope1=self.Arch, BelongsToItem=ModuleId)
        for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (PcdCName, TokenSpaceGuid) not in Module.Pcds:
                continue
            TokenList = GetSplitValueList(Setting)
            Pcd = Module.Pcds[PcdCName, TokenSpaceGuid]
            Pcd.DefaultValue = TokenList[0]
            if len(TokenList) > 1:
                Pcd.MaxDatumSize = TokenList[1]
            Pcd.Type = self._PCD_TYPE_STRING_[MODEL_PCD_PATCHABLE_IN_MODULE]

        RecordList = self._Table.Query(MODEL_PCD_FEATURE_FLAG, Scope1=self.Arch, BelongsToItem=ModuleId)
        for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (PcdCName, TokenSpaceGuid) not in Module.Pcds:
                continue
            TokenList = GetSplitValueList(Setting)
            Pcd = Module.Pcds[PcdCName, TokenSpaceGuid]
            Pcd.DefaultValue = TokenList[0]
            if len(TokenList) > 1:
                Pcd.MaxDatumSize = TokenList[1]
            Pcd.Type = self._PCD_TYPE_STRING_[MODEL_PCD_FEATURE_FLAG]

        RecordList = self._Table.Query(MODEL_PCD_DYNAMIC, Scope1=self.Arch, BelongsToItem=ModuleId)
        for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (PcdCName, TokenSpaceGuid) not in Module.Pcds:
                continue
            Pcd.DefaultValue = Setting
            Pcd.Type = self._PCD_TYPE_STRING_[MODEL_PCD_DYNAMIC]

        RecordList = self._Table.Query(MODEL_PCD_DYNAMIC_EX, Scope1=self.Arch, BelongsToItem=ModuleId)
        for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (PcdCName, TokenSpaceGuid) not in Module.Pcds:
                continue
            Pcd.DefaultValue = Setting
            Pcd.Type = self._PCD_TYPE_STRING_[MODEL_PCD_DYNAMIC_EX]

    def _MergeModuleBuildOption(self, Module, ModuleId):
        RecordList = self._Table.Query(MODEL_META_DATA_BUILD_OPTION, Scope1=self.Arch, BelongsToItem=ModuleId)
        for ToolChainFamily, ToolChain, Option, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
            if (ToolChainFamily, ToolChain) not in Module.BuildOptions:
                Module.BuildOptions[ToolChainFamily, ToolChain] = Option
            else:
                OptionString = Module.BuildOptions[ToolChainFamily, ToolChain]
                Module.BuildOptions[ToolChainFamily, ToolChain] = OptionString + " " + Option

    def _GetLibraryInstances(self):
        if self._LibraryInstances == None:
            self._LibraryInstances = []
            for Module in self.Modules:
                for Key in Module.LibraryClasses:
                    Lib = Module.LibraryClasses[Key]
                    if Lib in [None, ''] or Lib in self._LibraryInstances:
                        continue
                    self._LibraryInstances.append(Lib)
        return self._LibraryInstances

    def _GetLibraryClasses(self):
        if self._LibraryClasses == None:
            LibraryClassDict = tdict(True, 3)
            LibraryClassSet = set()
            ModuleTypeSet = set()
            RecordList = self._Table.Query(MODEL_EFI_LIBRARY_CLASS, Scope1=self.Arch)
            for LibraryClass, LibraryInstance, Dummy, Arch, ModuleType, Dummy, LineNo in RecordList:
                LibraryClassSet.add(LibraryClass)
                ModuleTypeSet.add(ModuleType)
                LibraryInstance = NormPath(LibraryInstance, self._Macros)
                if not ValidFile(LibraryInstance):
                    EdkLogger.error('build', FILE_NOT_FOUND, File=self.DescFilePath, 
                                    ExtraData=LibraryInstance, Line=LineNo)
                LibraryClassDict[Arch, ModuleType, LibraryClass] = LibraryInstance

            self._LibraryClasses = tdict(True)
            for LibraryClass in LibraryClassSet:
                for ModuleType in ModuleTypeSet:
                    LibraryInstance = LibraryClassDict[self.Arch, ModuleType, LibraryClass]
                    if LibraryInstance == None:
                        continue
                    self._LibraryClasses[LibraryClass, ModuleType] = LibraryInstance
        return self._LibraryClasses

    def _GetLibraries(self):
        if self._Libraries == None:
            self._Libraries = sdict()
            RecordList = self._Table.Query(MODEL_EFI_LIBRARY_INSTANCE, Scope1=self.Arch)
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                Library = self._Db.BuildObject[File, MODEL_FILE_INF, self._Arch]
                self._Libraries[Library.BaseName] = Library
        return self._Libraries

    def _GetPcds(self):
        if self._Pcds == None:
            self._Pcds = {}
            self._Pcds.update(self._GetPcd(MODEL_PCD_FIXED_AT_BUILD))
            self._Pcds.update(self._GetPcd(MODEL_PCD_PATCHABLE_IN_MODULE))
            self._Pcds.update(self._GetPcd(MODEL_PCD_FEATURE_FLAG))
            self._Pcds.update(self._GetDynamicPcd(MODEL_PCD_DYNAMIC_DEFAULT))
            self._Pcds.update(self._GetDynamicHiiPcd(MODEL_PCD_DYNAMIC_HII))
            self._Pcds.update(self._GetDynamicVpdPcd(MODEL_PCD_DYNAMIC_VPD))
            self._Pcds.update(self._GetDynamicPcd(MODEL_PCD_DYNAMIC_EX_DEFAULT))
            self._Pcds.update(self._GetDynamicHiiPcd(MODEL_PCD_DYNAMIC_EX_HII))
            self._Pcds.update(self._GetDynamicVpdPcd(MODEL_PCD_DYNAMIC_EX_VPD))
        return self._Pcds

    def _GetBuildOptions(self):
        if self._BuildOptions == None:
            self._BuildOptions = {}
            RecordList = self._Table.Query(MODEL_META_DATA_BUILD_OPTION)
            for ToolChainFamily, ToolChain, Option, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
                self._BuildOptions[ToolChainFamily, ToolChain] = Option
        return self._BuildOptions

    def _GetPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 3)
        PcdSet = set()
        # Find out all possible PCD candidates for self.Arch
        RecordList = self._Table.Query(Type, Scope1=self.Arch)
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, PcdCName, TokenSpaceGuid] = Setting
        # Remove redundant PCD candidates
        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self.Arch, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            PcdValue, DatumType, MaxDatumSize = ValueList
            Pcds[PcdCName, TokenSpaceGuid] = PcdClassObject(
                                                PcdCName,
                                                TokenSpaceGuid,
                                                self._PCD_TYPE_STRING_[Type],
                                                DatumType,
                                                PcdValue,
                                                '',
                                                MaxDatumSize,
                                                {},
                                                True
                                                )
        return Pcds

    def _GetDynamicPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._Table.Query(Type, Scope1=self.Arch)
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self.Arch, self.SkuName, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            PcdValue, DatumType, MaxDatumSize = ValueList

            SkuInfo = SkuInfoClass(self.SkuName, self.SkuIds[self.SkuName], '', '', '', '', '', PcdValue)
            Pcds[PcdCName, TokenSpaceGuid] = PcdClassObject(
                                                PcdCName,
                                                TokenSpaceGuid,
                                                self._PCD_TYPE_STRING_[Type],
                                                DatumType,
                                                PcdValue,
                                                '',
                                                MaxDatumSize,
                                                {self.SkuName : SkuInfo},
                                                True
                                                )
        return Pcds

    def _GetDynamicHiiPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._Table.Query(Type, Scope1=self.Arch)
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '', '']
            Setting = PcdDict[self.Arch, self.SkuName, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            VariableName, VariableGuid, VariableOffset, DefaultValue = ValueList
            SkuInfo = SkuInfoClass(self.SkuName, self.SkuIds[self.SkuName], VariableName, VariableGuid, VariableOffset, DefaultValue)
            Pcds[PcdCName, TokenSpaceGuid] = PcdClassObject(
                                                PcdCName,
                                                TokenSpaceGuid,
                                                self._PCD_TYPE_STRING_[Type],
                                                '',
                                                DefaultValue,
                                                '',
                                                '',
                                                {self.SkuName : SkuInfo},
                                                True
                                                )
        return Pcds

    def _GetDynamicVpdPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._Table.Query(Type, Scope1=self.Arch)
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '']
            Setting = PcdDict[self.Arch, self.SkuName, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            VpdOffset, MaxDatumSize = ValueList

            SkuInfo = SkuInfoClass(self.SkuName, self.SkuIds[self.SkuName], '', '', '', '', VpdOffset)
            Pcds[PcdCName, TokenSpaceGuid] = PcdClassObject(
                                                PcdCName,
                                                TokenSpaceGuid,
                                                self._PCD_TYPE_STRING_[Type],
                                                '',
                                                '',
                                                '',
                                                MaxDatumSize,
                                                {self.SkuName : SkuInfo},
                                                True
                                                )
        return Pcds

    def AddModule(self, FilePath):
        Module = self._Db.BuildObject[FilePath, MODEL_FILE_INF, self._Arch]
        self._Modules.append(NormPath(Module))

    def AddPcd(self, Name, Guid, Value):
        if (Name, Guid) not in self.Pcds:
            self.Pcds[Name, Guid] = PcdClassObject(
                                        Name,
                                        Guid,
                                        '',
                                        '',
                                        '',
                                        '',
                                        '',
                                        {},
                                        True
                                        )
        self.Pcds[Name, Guid].DefaultValue = Value

    Arch                = property(_GetArch, _SetArch)
    Platform            = property(_GetPlatformName)
    PlatformName        = property(_GetPlatformName)
    Guid                = property(_GetFileGuid)
    Version             = property(_GetVersion)
    DscSpecification    = property(_GetDscSpec)
    OutputDirectory     = property(_GetOutpuDir)
    SupArchList         = property(_GetSupArch)
    BuildTargets        = property(_GetBuildTarget)
    SkuName             = property(_GetSkuName)
    FlashDefinition     = property(_GetFdfFile)
    BuildNumber         = property(_GetBuildNumber)
    MakefileName        = property(_GetMakefileName)
    BsBaseAddress       = property(_GetBsBaseAddress)
    RtBaseAddress       = property(_GetRtBaseAddress)

    SkuIds              = property(_GetSkuIds)
    Modules             = property(_GetModules)
    LibraryInstances    = property(_GetLibraryInstances)
    LibraryClasses      = property(_GetLibraryClasses)
    Libraries           = property(_GetLibraries)
    Pcds                = property(_GetPcds)
    BuildOptions        = property(_GetBuildOptions)

class DecBuildData(PackageBuildClassObject):
    _PCD_TYPE_STRING_ = {
        MODEL_PCD_FIXED_AT_BUILD        :   "FixedAtBuild",
        MODEL_PCD_PATCHABLE_IN_MODULE   :   "PatchableInModule",
        MODEL_PCD_FEATURE_FLAG          :   "FeatureFlag",
        MODEL_PCD_DYNAMIC               :   "Dynamic",
        MODEL_PCD_DYNAMIC_DEFAULT       :   "Dynamic",
        MODEL_PCD_DYNAMIC_HII           :   "DynamicHii",
        MODEL_PCD_DYNAMIC_VPD           :   "DynamicVpd",
        MODEL_PCD_DYNAMIC_EX            :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_DEFAULT    :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_HII        :   "DynamicExHii",
        MODEL_PCD_DYNAMIC_EX_VPD        :   "DynamicExVpd",
    }

    def __init__(self, FilePath, Table, Db, Arch='COMMON', Macros={}):
        self.DescFilePath = FilePath
        self._PackageDir = os.path.dirname(FilePath)
        self._Table = Table
        self._Arch = Arch
        self._Macros = Macros
        self._Clear()

    def __repr__(self):
        S = "[Package]\n"
        S += "\tNAME = %s\n" % self.PackageName
        S += "\tGUID = %s\n" % self.Guid
        S += "\tVER  = %s\n" % self.Version

        S += '  <Protocol>\n'
        for Name in self.Protocols:
            S += "\t%s = %s\n" % (Name, self.Protocols[Name])

        S += '  <Ppi>\n'
        for Name in self.Ppis:
            S += "\t%s = %s\n" % (Name, self.Ppis[Name])

        S += '  <Guid>\n'
        for Name in self.Guids:
            S += "\t%s = %s\n" % (Name, self.Guids[Name])

        S += '  <Include>\n\t'
        S += "\n\t".join(self.Includes) + '\n'

        S += '  <LibraryClass>\n'
        for LibraryClass in self.LibraryClasses:
            S += "\t%s = %s\n" % (LibraryClass, self.LibraryClasses[LibraryClass])

        S += '  <PCD>\n'
        for Name,Guid,Type in self.Pcds:
            S += "\t%s.%s-%s\n\t\t%s\n" % (Guid, Name, Type, str(self.Pcds[Name, Guid, Type]))
        return S

    def _Clear(self):
        self._PackageName       = None
        self._Guid              = None
        self._Version           = None
        self._Protocols         = None
        self._Ppis              = None
        self._Guids             = None
        self._Includes          = None
        self._LibraryClasses    = None
        self._Pcds              = None

    def _GetArch(self):
        return self._Arch

    def _SetArch(self, Value):
        if self._Arch == Value:
            return
        self._Arch = Value
        self._Clear()

    def _GetPackageName(self):
        if self._PackageName == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DEC_DEFINES_PACKAGE_NAME)
            if len(RecordList) == 0:
                EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "No PACKAGE_NAME", ExtraData=self.DescFilePath)
            self._PackageName = RecordList[0][0]
        return self._PackageName

    def _GetFileGuid(self):
        if self._Guid == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DEC_DEFINES_PACKAGE_GUID)
            if len(RecordList) == 0:
                EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "No PACKAGE_GUID", ExtraData=self.DescFilePath)
            self._Guid = RecordList[0][0]
        return self._Guid

    def _GetVersion(self):
        if self._Version == None:
            RecordList = self._Table.Query(MODEL_META_DATA_HEADER, TAB_DEC_DEFINES_PACKAGE_VERSION)
            if len(RecordList) == 0:
                self._Version = ''
            self._Version = RecordList[0][0]
        return self._Version

    def _GetProtocol(self):
        if self._Protocols == None:
            ProtocolDict = tdict(True)
            NameSet = set()
            RecordList = self._Table.Query(MODEL_EFI_PROTOCOL, Arch=self.Arch)
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                NameSet.add(Name)
                ProtocolDict[Arch, Name] = Guid
            self._Protocols = sdict()
            for Name in NameSet:
                self._Protocols[Name] = ProtocolDict[self.Arch, Name]
        return self._Protocols

    def _GetPpi(self):
        if self._Ppis == None:
            PpiDict = tdict(True)
            NameSet = set()
            RecordList = self._Table.Query(MODEL_EFI_PPI, Arch=self.Arch)
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                NameSet.add(Name)
                PpiDict[Arch, Name] = Guid
            self._Ppis = sdict()
            for Name in NameSet:
                self._Ppis[Name] = PpiDict[self.Arch, Name]
        return self._Ppis

    def _GetGuid(self):
        if self._Guids == None:
            GuidDict = tdict(True)
            NameSet = set()
            RecordList = self._Table.Query(MODEL_EFI_GUID, Arch=self.Arch)
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                NameSet.add(Name)
                GuidDict[Arch, Name] = Guid
            self._Guids = sdict()
            for Name in NameSet:
                self._Guids[Name] = GuidDict[self.Arch, Name]
        return self._Guids

    def _GetInclude(self):
        if self._Includes == None:
            self._Includes = []
            RecordList = self._Table.Query(MODEL_EFI_INCLUDE, Arch=self.Arch)
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File, self._PackageDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                self._Includes.append(File)
        return self._Includes

    def _GetLibraryClass(self):
        if self._LibraryClasses == None:
            LibraryClassDict = tdict(True)
            LibraryClassSet = set()
            RecordList = self._Table.Query(MODEL_EFI_LIBRARY_CLASS, Arch=self.Arch)
            for LibraryClass, File, Dummy, Arch, ID, LineNo in RecordList:
                File = NormPath(File, self._Macros)
                if not ValidFile(File, self._PackageDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                LibraryClassSet.add(LibraryClass)
                LibraryClassDict[Arch, LibraryClass] = File
            self._LibraryClasses = sdict()
            for LibraryClass in LibraryClassSet:
                self._LibraryClasses[LibraryClass] = LibraryClassDict[self.Arch, LibraryClass]
        return self._LibraryClasses

    def _GetPcds(self):
        if self._Pcds == None:
            self._Pcds = {}
            self._Pcds.update(self._GetPcd(MODEL_PCD_FIXED_AT_BUILD))
            self._Pcds.update(self._GetPcd(MODEL_PCD_PATCHABLE_IN_MODULE))
            self._Pcds.update(self._GetPcd(MODEL_PCD_FEATURE_FLAG))
            self._Pcds.update(self._GetPcd(MODEL_PCD_DYNAMIC))
            self._Pcds.update(self._GetPcd(MODEL_PCD_DYNAMIC_EX))
        return self._Pcds

    def _GetPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 3)
        PcdSet = set()
        RecordList = self._Table.Query(Type, Arch=self._Arch)
        for TokenSpaceGuid, PcdCName, Setting, Arch, Dummy1, Dummy2 in RecordList:
            PcdDict[Arch, PcdCName, TokenSpaceGuid] = Setting
            PcdSet.add((PcdCName, TokenSpaceGuid))

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self.Arch, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            DefaultValue, DatumType, TokenNumber = ValueList
            Pcds[PcdCName, TokenSpaceGuid, self._PCD_TYPE_STRING_[Type]] = PcdClassObject(
                                                                            PcdCName,
                                                                            TokenSpaceGuid,
                                                                            self._PCD_TYPE_STRING_[Type],
                                                                            DatumType,
                                                                            DefaultValue,
                                                                            TokenNumber,
                                                                            '',
                                                                            {},
                                                                            True
                                                                            )
        return Pcds


    Arch            = property(_GetArch, _SetArch)
    PackageName     = property(_GetPackageName)
    Guid            = property(_GetFileGuid)
    Version         = property(_GetVersion)

    Protocols       = property(_GetProtocol)
    Ppis            = property(_GetPpi)
    Guids           = property(_GetGuid)
    Includes        = property(_GetInclude)
    LibraryClasses  = property(_GetLibraryClass)
    Pcds            = property(_GetPcds)

class InfBuildData(ModuleBuildClassObject):
    _PCD_TYPE_STRING_ = {
        MODEL_PCD_FIXED_AT_BUILD        :   "FixedAtBuild",
        MODEL_PCD_PATCHABLE_IN_MODULE   :   "PatchableInModule",
        MODEL_PCD_FEATURE_FLAG          :   "FeatureFlag",
        MODEL_PCD_DYNAMIC               :   "Dynamic",
        MODEL_PCD_DYNAMIC_DEFAULT       :   "Dynamic",
        MODEL_PCD_DYNAMIC_HII           :   "DynamicHii",
        MODEL_PCD_DYNAMIC_VPD           :   "DynamicVpd",
        MODEL_PCD_DYNAMIC_EX            :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_DEFAULT    :   "DynamicEx",
        MODEL_PCD_DYNAMIC_EX_HII        :   "DynamicExHii",
        MODEL_PCD_DYNAMIC_EX_VPD        :   "DynamicExVpd",
    }

    _PROPERTY_ = {
        #
        # Required Fields
        #
        TAB_INF_DEFINES_BASE_NAME                   : "_BaseName",
        TAB_INF_DEFINES_FILE_GUID                   : "_Guid",
        TAB_INF_DEFINES_MODULE_TYPE                 : "_ModuleType",
        #
        # Optional Fields
        #
        TAB_INF_DEFINES_INF_VERSION                 : "_AutoGenVersion",
        TAB_INF_DEFINES_COMPONENT_TYPE              : "_ComponentType",
        TAB_INF_DEFINES_MAKEFILE_NAME               : "_CustomMakefile",
        TAB_INF_DEFINES_CUSTOM_MAKEFILE             : "_CustomMakefile",
        TAB_INF_DEFINES_VERSION_NUMBER              : "_Version",
        TAB_INF_DEFINES_VERSION_STRING              : "_Version",
        TAB_INF_DEFINES_VERSION                     : "_Version",
        TAB_INF_DEFINES_PCD_IS_DRIVER               : "_PcdIsDriver",
        TAB_INF_DEFINES_SHADOW                      : "_Shadow",
        TAB_INF_DEFINES_CUSTOM_MAKEFILE             : "_CustomMakefile",
    }

    _MODULE_TYPE_ = {
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
    
    _NMAKE_FLAG_PATTERN_ = re.compile("(?:EBC_)?([A-Z]+)_(?:STD_|PROJ_|ARCH_)?FLAGS(?:_DLL|_ASL|_EXE)?", re.UNICODE)
    _TOOL_CODE_ = {
        "C"         :   "CC",
        "LIB"       :   "SLINK",
        "LINK"      :   "DLINK",
    }
    

    def __init__(self, FilePath, Table, Db, Arch='COMMON', Macros={}):
        self.DescFilePath = FilePath
        self._ModuleDir = os.path.dirname(FilePath)
        self._Table = Table
        self._Db = Db
        self._Arch = Arch
        self._Platform = 'COMMON'
        self._Macros = Macros
        self._Clear()

    def Print(self):
        S = '[%s.%s]\n' % (self.DescFilePath, self.Arch)
        S += '\tName = ' + self.BaseName + '\n'
        S += '\tGuid = ' + self.Guid + '\n'
        S += '\tVer  = ' + self.Version + '\n'
        S += '\tInfVersion = ' + self.AutoGenVersion + '\n'
        S += '\tModuleType = ' + self.ModuleType + '\n'
        S += '\tComponentType = ' + self.ComponentType + '\n'
        S += '\tPcdIsDriver = ' + str(self.PcdIsDriver) + '\n'
        S += '\tCustomMakefile = ' + self.CustomMakefile + '\n'
        S += '\tSpecification = ' + str(self.Specification) + '\n'
        S += '\tShadow = ' + str(self.Shadow) + '\n'
        S += '\tPcdIsDriver = ' + str(self.PcdIsDriver) + '\n'
        for Lib in self.LibraryClass:
            S += '\tLibraryClassDefinition = ' + str(Lib.LibraryClass) + ' SupModList = ' + str(Lib.SupModList) + '\n'
        S += '\tModuleEntryPointList = ' + str(self.ModuleEntryPointList) + '\n'
        S += '\tModuleUnloadImageList = ' + str(self.ModuleUnloadImageList) + '\n'
        S += '\tConstructorList = ' + str(self.ConstructorList) + '\n'
        S += '\tDestructorList = ' + str(self.DestructorList) + '\n'

        S += '  <Binaries>\n'
        for item in self.Binaries:
            S += "\t" + item.BinaryFile + item.FeatureFlag + item.SupArchList + '\n'

        S += '  <Sources>\n'
        for item in self.Sources:
            S += "\t" + item.SourceFile + '\n'

        S += '  <LibraryClasses>\n'
        S += '\t' + '\n\t'.join([Key for Key in self.LibraryClasses]) + '\n'

        S += '  <Protocols>\n'
        S += '\t' + '\n\t'.join(self.Protocols) + '\n'

        S += '  <Ppis>\n'
        S += '\t' + '\n\t'.join(self.Ppis) + '\n'

        S += '  <Guids>\n'
        S += '\t' + '\n\t'.join(self.Guids) + '\n'

        S += '  <Includes>\n'
        S += '\t' + '\n\t'.join(self.Includes) + '\n'

        S += '  <Packages>\n'
        S += '\t' + '\n\t'.join([str(P) for P in self.Packages]) + '\n'

        S += '  <Pcds>\n'
        for Name,Guid in self.Pcds.keys():
            S += "\t%s.%s\n\t\t%s\n" % (Guid, Name, str(self.Pcds[Name,Guid]))

        S += '  <BuildOptions\n'
        S += '\t' + '\n\t'.join(self.BuildOptions.values()) + '\n'

        S += '  <Depex>\n'
        S += '\t' + str(self.Depex) + '\n'

        S += '\n'
        return S

    ## XXX[key] = value
    def __setitem__(self, key, value):
        self.__dict__[self._PROPERTY_[key]] = value
    ## value = XXX[key]
    def __getitem__(self, key):
        return self.__dict__[self._PROPERTY_[key]]
    ## "in" test support
    def __contains__(self, key):
        return key in self._PROPERTY_

    def _Clear(self):
        self._Header_               = None
        self._AutoGenVersion        = None
        self._DescFilePath          = None
        self._BaseName              = None
        self._ModuleType            = None
        self._ComponentType         = None
        self._Guid                  = None
        self._Version               = None
        self._PcdIsDriver           = None
        self._BinaryModule          = None
        self._Shadow                = None
        self._CustomMakefile        = None
        self._Specification         = None
        self._LibraryClass          = None
        self._ModuleEntryPointList  = None
        self._ModuleUnloadImageList = None
        self._ConstructorList       = None
        self._DestructorList        = None
        self._Binaries              = None
        self._Sources               = None
        self._LibraryClasses        = None
        self._Libraries             = None
        self._Protocols             = None
        self._Ppis                  = None
        self._Guids                 = None
        self._Includes              = None
        self._Packages              = None
        self._Pcds                  = None
        self._BuildOptions          = None
        self._Depex                 = None

    def _GetArch(self):
        return self._Arch

    def _SetArch(self, Value):
        if self._Arch == Value:
            return
        self._Arch = Value
        self._Clear()

    def _GetPlatform(self):
        return self._Platform

    def _SetPlatform(self, Value):
        self._Platform = Value

    def _GetHeaderInfo(self):
        RecordList = self._Table.Query(MODEL_META_DATA_HEADER, Arch=self._Arch, Platform=self._Platform)
        for Record in RecordList:
            Name = Record[0]
            if Name in self:
                self[Name] = Record[1]
            elif Name == 'EFI_SPECIFICATION_VERSION':
                if self._Specification == None:
                    self._Specification = sdict()
                self._Specification[Name] = Record[1]
            elif Name == 'EDK_RELEASE_VERSION':
                if self._Specification == None:
                    self._Specification = sdict()
                self._Specification[Name] = Record[1]
            elif Name == 'LIBRARY_CLASS':
                if self._LibraryClass == None:
                    self._LibraryClass = []
                ValueList = GetSplitValueList(Record[1])
                LibraryClass = ValueList[0]
                if len(ValueList) > 1:
                    SupModuleList = GetSplitValueList(ValueList[1], ' ')
                else:
                    SupModuleList = SUP_MODULE_LIST
                self._LibraryClass.append(LibraryClassObject(LibraryClass, SupModuleList))
            elif Name == 'ENTRY_POINT':
                if self._ModuleEntryPointList == None:
                    self._ModuleEntryPointList = []
                self._ModuleEntryPointList.append(Record[1])
            elif Name == 'UNLOAD_IMAGE':
                if self._ModuleUnloadImageList == None:
                    self._ModuleUnloadImageList = []
                if Record[1] == '':
                    continue
                self._ModuleUnloadImageList.append(Record[1])
            elif Name == 'CONSTRUCTOR':
                if self._ConstructorList == None:
                    self._ConstructorList = []
                if Record[1] == '':
                    continue
                self._ConstructorList.append(Record[1])
            elif Name == 'DESTRUCTOR':
                if self._DestructorList == None:
                    self._DestructorList = []
                if Record[1] == '':
                    continue
                self._DestructorList.append(Record[1])

        # 
        # R8.x modules
        # 
        if self._AutoGenVersion < 0x00010005:   # _AutoGenVersion may be None, which is less than anything
            if self._ComponentType in self._MODULE_TYPE_:
                self._ModuleType = self._MODULE_TYPE_[self._ComponentType]
            if self._ComponentType == 'LIBRARY':
                self._LibraryClass = [LibraryClassObject(self._BaseName, SUP_MODULE_LIST)]
            # make use some [nmake] section macros
            RecordList = self._Table.Query(MODEL_META_DATA_NMAKE, Arch=self._Arch, Platform=self._Platform)
            for Name,Value,Dummy,Arch,Platform,ID,LineNo in RecordList:
                if Name == "IMAGE_ENTRY_POINT":
                    if self._ModuleEntryPointList == None:
                        self._ModuleEntryPointList = []
                    self._ModuleEntryPointList.append(Value)
                elif Name == "DPX_SOURCE":
                    File = NormPath(Value, self._Macros)
                    if not ValidFile(Source, self._ModuleDir):
                        EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                        File=self.DescFilePath, Line=LineNo)
                    self._Sources.append(ModuleSourceFileClass(File, "", "", "", ""))
                else:
                    ToolList = self._NMAKE_FLAG_PATTERN_.findall(Name)
                    if len(ToolList) == 0 or len(ToolList) != 1:
                        EdkLogger.warn("\nbuild", "Don't know how to do with MACRO: %s" % Name, 
                                       ExtraData=ContainerFile)
                    else:
                        if self._BuildOptions == None:
                            self._BuildOptions = sdict()

                        if ToolList[0] in self._TOOL_CODE_:
                            Tool = self._TOOL_CODE_[ToolList[0]]
                        else:
                            Tool = ToolList[0]
                        ToolChain = "*_*_*_%s_FLAGS" % Tool
                        ToolChainFamily = 'MSFT'    # R8.x only support MSFT tool chain
                        if (ToolChainFamily, ToolChain) not in self._BuildOptions:
                            self._BuildOptions[ToolChainFamily, ToolChain] = Value
                        else:
                            OptionString = self._BuildOptions[ToolChainFamily, ToolChain]
                            self._BuildOptions[ToolChainFamily, ToolChain] = OptionString + " " + Value

        self._Header_ = 'DUMMY'

    def _GetInfVersion(self):
        if self._AutoGenVersion == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._AutoGenVersion == None:
                self._AutoGenVersion = 0x00010000
        return self._AutoGenVersion

    def _GetBaseName(self):
        if self._BaseName == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._BaseName == None:
                self._BaseName = ''
        return self._BaseName

    def _GetModuleType(self):
        if self._ModuleType == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._ModuleType == None:
                self._ModuleType = 'BASE'
        return self._ModuleType

    def _GetComponentType(self):
        if self._ComponentType == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._ComponentType == None:
                self._ComponentType = ''
        return self._ComponentType

    def _GetFileGuid(self):
        if self._Guid == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._Guid == None:
                self._Guid = '00000000-0000-0000-000000000000'
        return self._Guid

    def _GetVersion(self):
        if self._Version == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._Version == None:
                self._Version = '0.0'
        return self._Version

    def _GetPcdIsDriver(self):
        if self._PcdIsDriver == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._PcdIsDriver == None:
                self._PcdIsDriver = ''
        return self._PcdIsDriver

    def _GetShadow(self):
        if self._Shadow == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._Shadow != None and self._Shadow.upper() == 'TRUE':
                self._Shadow = True
            else:
                self._Shadow = False
        return self._Shadow

    def _GetMakefile(self):
        if self._CustomMakefile == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._CustomMakefile == None:
                self._CustomMakefile = ''
        return self._CustomMakefile

    def _GetSpec(self):
        if self._Specification == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._Specification == None:
                self._Specification = {}
        return self._Specification

    def _GetLibraryClass(self):
        if self._LibraryClass == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._LibraryClass == None:
                self._LibraryClass = []
        return self._LibraryClass

    def _GetEntryPoint(self):
        if self._ModuleEntryPointList == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._ModuleEntryPointList == None:
                self._ModuleEntryPointList = []
        return self._ModuleEntryPointList

    def _GetUnloadImage(self):
        if self._ModuleUnloadImageList == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._ModuleUnloadImageList == None:
                self._ModuleUnloadImageList = []
        return self._ModuleUnloadImageList

    def _GetConstructor(self):
        if self._ConstructorList == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._ConstructorList == None:
                self._ConstructorList = []
        return self._ConstructorList

    def _GetDestructor(self):
        if self._DestructorList == None:
            if self._Header_ == None:
                self._GetHeaderInfo()
            if self._DestructorList == None:
                self._DestructorList = []
        return self._DestructorList
                        
    def _GetBinaryFiles(self):
        if self._Binaries == None:
            self._Binaries = []
            RecordList = self._Table.Query(MODEL_EFI_BINARY_FILE, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                FileType = Record[0]
                File = NormPath(Record[1], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File, self._ModuleDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                Target = Record[2]
                FeatureFlag = Record[3]
                self._Binaries.append(ModuleBinaryFileClass(File, FileType, Target, FeatureFlag, self._Arch))
        return self._Binaries

    def _GetSourceFiles(self):
        if self._Sources == None:
            self._Sources = []
            RecordList = self._Table.Query(MODEL_EFI_SOURCE_FILE, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File, self._ModuleDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                ToolChainFamily = Record[1]
                TagName = Record[2]
                ToolCode = Record[3]
                FeatureFlag = Record[4]
                self._Sources.append(ModuleSourceFileClass(File, TagName, ToolCode, ToolChainFamily, FeatureFlag))
        return self._Sources

    def _GetLibraryClassUses(self):
        if self._LibraryClasses == None:
            self._LibraryClasses = sdict()
            RecordList = self._Table.Query(MODEL_EFI_LIBRARY_CLASS, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                Lib = Record[0]
                Instance = Record[1]
                if Instance != None and Instance != '':
                    Instance = NormPath(Instance, self._Macros)
                self._LibraryClasses[Lib] = Instance
        return self._LibraryClasses

    def _SetLibraryClassUses(self, Value):
        self._LibraryClasses = Value

    def _GetLibraryInstances(self):
        if self._Libraries == None:
            self._Libraries = []
            RecordList = self._Table.Query(MODEL_EFI_LIBRARY_INSTANCE, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                self._Libraries.append(Record[0])
        return self._Libraries

    def _GetProtocols(self):
        if self._Protocols == None:
            self._Protocols = []
            RecordList = self._Table.Query(MODEL_EFI_PROTOCOL, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                self._Protocols.append(Record[0])
        return self._Protocols

    def _GetPpis(self):
        if self._Ppis == None:
            self._Ppis = []
            RecordList = self._Table.Query(MODEL_EFI_PPI, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                self._Ppis.append(Record[0])
        return self._Ppis

    def _GetGuids(self):
        if self._Guids == None:
            self._Guids = []
            RecordList = self._Table.Query(MODEL_EFI_GUID, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                self._Guids.append(Record[0])
        return self._Guids

    def _GetIncludes(self):
        if self._Includes == None:
            self._Includes = []
            RecordList = self._Table.Query(MODEL_EFI_INCLUDE, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                #if File[0] == '.':
                #    if not ValidFile(File, self._ModuleDir):
                #        EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                #                        File=self.DescFilePath, Line=LineNo)
                #else:
                #    if not ValidFile(File):
                #        EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                #                        File=self.DescFilePath, Line=LineNo)
                self._Includes.append(File)
        return self._Includes

    def _GetPackages(self):
        if self._Packages == None:
            self._Packages = []
            RecordList = self._Table.Query(MODEL_META_DATA_PACKAGE, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                Package = self._Db.BuildObject[File, MODEL_FILE_DEC, self._Arch]
                self._Packages.append(Package)
        return self._Packages

    def _GetPcds(self):
        if self._Pcds == None:
            self._Pcds = {}
            self._Pcds.update(self._GetPcd(MODEL_PCD_FIXED_AT_BUILD))
            self._Pcds.update(self._GetPcd(MODEL_PCD_PATCHABLE_IN_MODULE))
            self._Pcds.update(self._GetPcd(MODEL_PCD_FEATURE_FLAG))
            self._Pcds.update(self._GetPcd(MODEL_PCD_DYNAMIC))
            self._Pcds.update(self._GetPcd(MODEL_PCD_DYNAMIC_EX))
        return self._Pcds

    def _GetBuildOptions(self):
        if self._BuildOptions == None:
            self._BuildOptions = sdict()
            RecordList = self._Table.Query(MODEL_META_DATA_BUILD_OPTION, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                ToolChainFamily = Record[0]
                ToolChain = Record[1]
                Option = Record[2]
                if (ToolChainFamily, ToolChain) not in self._BuildOptions:
                    self._BuildOptions[ToolChainFamily, ToolChain] = Option
                else:
                    OptionString = self._BuildOptions[ToolChainFamily, ToolChain]
                    self._BuildOptions[ToolChainFamily, ToolChain] = OptionString + " " + Option
        return self._BuildOptions

    def _GetDepex(self):
        if self._Depex == None:
            self._Depex = ''
            RecordList = self._Table.Query(MODEL_EFI_DEPEX, Arch=self._Arch, Platform=self._Platform)
            for Record in RecordList:
                self._Depex += ' ' + Record[0]
        return self._Depex

    def _GetPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._Table.Query(Type, Arch=self.Arch, Platform=self.Platform)
        for TokenSpaceGuid, PcdCName, Setting, Arch, Platform, Dummy1, Dummy2 in RecordList:
            PcdDict[Arch, Platform, PcdCName, TokenSpaceGuid] = Setting
            PcdSet.add((PcdCName, TokenSpaceGuid))

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '']
            Setting = PcdDict[self.Arch, self.Platform, PcdCName, TokenSpaceGuid]
            if Setting == None:
                continue
            TokenList = Setting.split(TAB_VALUE_SPLIT)
            ValueList[0:len(TokenList)] = TokenList
            DefaultValue = ValueList[0]
            Pcd = PcdClassObject(
                    PcdCName,
                    TokenSpaceGuid,
                    '',
                    '',
                    DefaultValue,
                    '',
                    '',
                    {},
                    True
                    )
            # get necessary info from package declaring this PCD
            for Package in self.Packages:
                # 
                # 'dynamic' in INF means its type is determined by platform;
                # if platform doesn't give its type, use 'lowest' one in the 
                # following order, if any
                # 
                #   "FixedAtBuild", "PatchableInModule", "FeatureFlag", "Dynamic", "DynamicEx"
                # 
                PcdType = self._PCD_TYPE_STRING_[Type]
                if Type in [MODEL_PCD_DYNAMIC, MODEL_PCD_DYNAMIC_EX]:
                    for T in ["FixedAtBuild", "PatchableInModule", "FeatureFlag", "Dynamic", "DynamicEx"]:
                        if (PcdCName, TokenSpaceGuid, T) in Package.Pcds:
                            PcdType = T
                            break

                if (PcdCName, TokenSpaceGuid, PcdType) in Package.Pcds:
                    PcdInPackage = Package.Pcds[PcdCName, TokenSpaceGuid, PcdType]
                    Pcd.Type = PcdType
                    Pcd.TokenValue = PcdInPackage.TokenValue
                    Pcd.DatumType = PcdInPackage.DatumType
                    Pcd.MaxDatumSize = PcdInPackage.MaxDatumSize
                    if Pcd.DefaultValue in [None, '']:
                        Pcd.DefaultValue = PcdInPackage.DefaultValue
                    break
            else:
                EdkLogger.error(
                            'build', 
                            PARSER_ERROR,
                            "PCD [%s.%s] in [%s] is not found in dependent packages:" % (TokenSpaceGuid, PcdCName, self.DescFilePath),
                            ExtraData="\t%s" % '\n\t'.join([str(P) for P in self.Packages])
                            )
            Pcds[PcdCName, TokenSpaceGuid] = Pcd
        return Pcds

    Arch                    = property(_GetArch, _SetArch)
    Platform                = property(_GetPlatform, _SetPlatform)

    AutoGenVersion          = property(_GetInfVersion)
    BaseName                = property(_GetBaseName)
    ModuleType              = property(_GetModuleType)
    ComponentType           = property(_GetComponentType)
    Guid                    = property(_GetFileGuid)
    Version                 = property(_GetVersion)
    PcdIsDriver             = property(_GetPcdIsDriver)
    Shadow                  = property(_GetShadow)
    CustomMakefile          = property(_GetMakefile)
    Specification           = property(_GetSpec)
    LibraryClass            = property(_GetLibraryClass)
    ModuleEntryPointList    = property(_GetEntryPoint)
    ModuleUnloadImageList   = property(_GetUnloadImage)
    ConstructorList         = property(_GetConstructor)
    DestructorList          = property(_GetDestructor)

    Binaries                = property(_GetBinaryFiles)
    Sources                 = property(_GetSourceFiles)
    LibraryClasses          = property(_GetLibraryClassUses, _SetLibraryClassUses)
    Libraries               = property(_GetLibraryInstances)
    Protocols               = property(_GetProtocols)
    Ppis                    = property(_GetPpis)
    Guids                   = property(_GetGuids)
    Includes                = property(_GetIncludes)
    Packages                = property(_GetPackages)
    Pcds                    = property(_GetPcds)
    BuildOptions            = property(_GetBuildOptions)
    Depex                   = property(_GetDepex)


## Database
#
# This class defined the build databse
# During the phase of initialization, the database will create all tables and
# insert all records of table DataModel
# 
# @param object:      Inherited from object class
# @param DbPath:      A string for the path of the ECC database
#
# @var Conn:          Connection of the ECC database
# @var Cur:           Cursor of the connection
# @var TblDataModel:  Local instance for TableDataModel
#
class WorkspaceDatabase(object):
    _FILE_TYPE_ = {
        ".INF"  : MODEL_FILE_INF,
        ".DEC"  : MODEL_FILE_DEC,
        ".DSC"  : MODEL_FILE_DSC,
        ".FDF"  : MODEL_FILE_FDF,
    }

    _FILE_PARSER_ = {
        MODEL_FILE_INF  :   InfParser,
        MODEL_FILE_DEC  :   DecParser,
        MODEL_FILE_DSC  :   DscParser,
        MODEL_FILE_FDF  :   None, #FdfParser,
    }

    _FILE_TABLE_ = {
        MODEL_FILE_INF  :   ModuleTable,
        MODEL_FILE_DEC  :   PackageTable,
        MODEL_FILE_DSC  :   PlatformTable,
    }

    class BuildObjectFactory(object):
        _GENERATOR_ = {
            MODEL_FILE_INF  :   InfBuildData,
            MODEL_FILE_DEC  :   DecBuildData,
            MODEL_FILE_DSC  :   DscBuildData,
            MODEL_FILE_FDF  :   None #FlashDefTable,
        }

        _CACHE_ = {}    # FilePath  : <object>

        def __init__(self, WorkspaceDb):
            self.WorkspaceDb = WorkspaceDb

        # key = (FilePath, FileType, Arch='COMMON', Platform='COMMON')
        def __getitem__(self, Key):
            FilePath = Key[0]
            FileType = Key[1]
            if len(Key) > 2:
                Arch = Key[2]
            else:
                Arch = 'COMMON'
            Key = (FilePath, Arch)
            if Key in self._CACHE_:
                return self._CACHE_[Key]

            self.WorkspaceDb[FilePath] = FileType
            if FileType not in self._GENERATOR_:
                return None

            # create temp table for current file
            Table = self.WorkspaceDb[FilePath]
            BuildObject = self._GENERATOR_[FileType](
                                    FilePath, 
                                    Table, 
                                    self.WorkspaceDb, 
                                    Arch, 
                                    self.WorkspaceDb._GlobalMacros
                                    )
            self._CACHE_[Key] = BuildObject
            return BuildObject

    class TransformObjectFactory:
        def __init__(self, WorkspaceDb):
            self.WorkspaceDb = WorkspaceDb

        # key = FilePath
        def __getitem__(self, Key):
            pass

    def __init__(self, DbPath, GlobalMacros={}):
        self._GlobalMacros = GlobalMacros

        DbDir = os.path.split(DbPath)[0]
        if not os.path.exists(DbDir):
            os.makedirs(DbDir)

        self.Conn = sqlite3.connect(DbPath, isolation_level='DEFERRED')
        self.Conn.execute("PRAGMA synchronous=OFF")
        self.Conn.execute("PRAGMA temp_store=MEMORY")
        self.Conn.execute("PRAGMA count_changes=OFF")
        self.Conn.execute("PRAGMA cache_size=8192")
        #self.Conn.execute("PRAGMA page_size=8192")

        # to avoid non-ascii character conversion issue
        self.Conn.text_factory = str
        self.Cur = self.Conn.cursor()

        self.TblDataModel = TableDataModel(self.Cur)
        self.TblFile = TableFile(self.Cur)

        self.BuildObject = WorkspaceDatabase.BuildObjectFactory(self)
        self.TransformObject = WorkspaceDatabase.TransformObjectFactory(self)
    
    ## Initialize build database
    #
    # 1. Delete all old existing tables
    # 2. Create new tables
    # 3. Initialize table DataModel
    #
    def InitDatabase(self):
        EdkLogger.verbose("\nInitialize ECC database started ...")
        
        #
        # Create new tables
        #
        self.TblDataModel.Create(False)
        self.TblFile.Create(False)
        
        #
        # Initialize table DataModel
        #
        self.TblDataModel.InitTable()
        EdkLogger.verbose("Initialize build database ... DONE!")

    ## Query a table
    #
    # @param Table:  The instance of the table to be queried
    #
    def QueryTable(self, Table):
        Table.Query()
    
    ## Close entire database
    #
    # Commit all first 
    # Close the connection and cursor
    #
    def Close(self):
        self.Conn.commit()
        self.Cur.close()
        self.Conn.close()

    def GetFileId(self, FilePath):
        return self.TblFile.GetFileId(FilePath)

    def GetFileType(self, FileId):
        return self.TblFile.GetFileType(FileId)

    def GetTimeStamp(self, FileId):
        return self.TblFile.GetFileTimeStamp(FileId)

    def SetTimeStamp(self, FileId, TimeStamp):
        return self.TblFile.SetFileTimeStamp(FileId, TimeStamp)

    def CheckIntegrity(self, TableName):
        Result = self.Cur.execute("select min(ID) from %s" % (TableName)).fetchall()
        if Result[0][0] != -1:
            return False
        return True

    def GetTableName(self, FileType, FileId):
        return "_%s_%s" % (FileType, FileId)

    ## TRICK: 
    # Key = FilePath
    # Value = FileType
    def __setitem__(self, FilePath, FileType):
        FileId = self.GetFileId(FilePath)
        if FileId != None:
            TimeStamp = os.stat(FilePath)[8]
            TableName = self.GetTableName(FileType, FileId)
            if TimeStamp != self.GetTimeStamp(FileId):
                self.SetTimeStamp(FileId, TimeStamp)
            else:
                if self.CheckIntegrity(TableName) == True:
                    return
        else:
            FileId = self.TblFile.InsertFile(FilePath, FileType)
            TableName = self.GetTableName(FileType, FileId)

        FileTable = self._FILE_TABLE_[FileType](self.Cur, TableName, FileId)
        FileTable.Create()
        Parser = self._FILE_PARSER_[FileType](FilePath, FileId, FileType, FileTable)
        Parser.Start()

    ## Return a temp table containing all content of the given file
    # 
    def __getitem__(self, FileInfo):
        if type(FileInfo) == type(''):
            FileId = self.GetFileId(FileInfo)
        else:
            FileId = FileInfo
        if FileId == None:
            return None
        FileType = self.GetFileType(FileId)
        if FileType not in self._FILE_TABLE_:
            return None

        TableName = "_%s_%s" % (FileType, FileId)
        FileTable = self._FILE_TABLE_[FileType](self.Cur, TableName, FileId)
        return FileTable

    ## Resolve cross-references between platfor, packages and modules
    def _PostFix(self):
        pass

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.DEBUG_0)
    
    Db = WorkspaceDatabase(DATABASE_PATH)
    Db.InitDatabase()
    Db.QueryTable(Db.TblDataModel)   
    Db.QueryTable(Db.TblFile)
    Db.QueryTable(Db.TblDsc)
    Db.Close()
    