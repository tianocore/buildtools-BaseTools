## @file
# This file is used to create a database used by build tool
#
# Copyright (c) 2008, Intel Corporation
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
from Common.Misc import *

from MetaDataTable import *
from MetaFileTable import *
from MetaFileParser import *
from BuildClassObject import *

## Platform build information from DSC file
#
#  This class is used to retrieve information stored in database and convert them
# into PlatformBuildClassObject form for easier use for AutoGen.
#
class DscBuildData(PlatformBuildClassObject):
    # dict used to convert PCD type in database to string used by build tool
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
        TAB_DSC_DEFINES_PLATFORM_NAME           :   "_PlatformName",
        TAB_DSC_DEFINES_PLATFORM_GUID           :   "_Guid",
        TAB_DSC_DEFINES_PLATFORM_VERSION        :   "_Version",
        TAB_DSC_DEFINES_DSC_SPECIFICATION       :   "_DscSpecification",
        #TAB_DSC_DEFINES_OUTPUT_DIRECTORY        :   "_OutputDirectory",
        #TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES :   "_SupArchList",
        #TAB_DSC_DEFINES_BUILD_TARGETS           :   "_BuildTargets",
        #TAB_DSC_DEFINES_SKUID_IDENTIFIER        :   "_SkuName",
        #TAB_DSC_DEFINES_FLASH_DEFINITION        :   "_FlashDefinition",
        TAB_DSC_DEFINES_BUILD_NUMBER            :   "_BuildNumber",
        TAB_DSC_DEFINES_MAKEFILE_NAME           :   "_MakefileName",
        TAB_DSC_DEFINES_BS_BASE_ADDRESS         :   "_BsBaseAddress",
        TAB_DSC_DEFINES_RT_BASE_ADDRESS         :   "_RtBaseAddress",
    }

    # used to compose dummy library class name for those forced library instances
    _NullLibraryNumber = 0

    def __init__(self, FilePath, RawData, BuildDataBase, Arch='COMMON', Platform='DUMMY', Macros={}):
        self.DescFilePath = FilePath
        self._RawData = RawData
        self._Bdb = BuildDataBase
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
    def __setitem__(self, key, value):
        self.__dict__[self._PROPERTY_[key]] = value
    ## value = XXX[key]
    def __getitem__(self, key):
        return self.__dict__[self._PROPERTY_[key]]
    ## "in" test support
    def __contains__(self, key):
        return key in self._PROPERTY_

    def _Clear(self):
        self._Header            = None
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
        self._Pcds              = None
        self._BuildOptions      = None

    def _GetArch(self):
        return self._Arch

    def _SetArch(self, Value):
        if self._Arch == Value:
            return
        self._Arch = Value
        self._Clear()

    def _GetHeaderInfo(self):
        RecordList = self._RawData[MODEL_META_DATA_HEADER, self._Arch]
        for Record in RecordList:
            Name = Record[0]
            if Name in self:
                self[Name] = Record[1]
            elif Name == TAB_DSC_DEFINES_OUTPUT_DIRECTORY:
                self._OutputDirectory = NormPath(Record[1], self._Macros)
            elif Name == TAB_DSC_DEFINES_FLASH_DEFINITION:
                self._FlashDefinition = NormPath(Record[1], self._Macros)
            elif Name == TAB_DSC_DEFINES_SUPPORTED_ARCHITECTURES:
                self._SupArchList = GetSplitValueList(Record[1], TAB_VALUE_SPLIT)
            elif Name == TAB_DSC_DEFINES_BUILD_TARGETS:
                self._BuildTargets = GetSplitValueList(Record[1])
            elif Name == TAB_DSC_DEFINES_SKUID_IDENTIFIER:
                if self._SkuName == None:
                    self._SkuName = Record[1]
        self._Header = 'DUMMY'

    def _GetPlatformName(self):
        if self._PlatformName == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._PlatformName == None:
                EdkLogger.error('build', ATTRIBUTE_NOT_AVAILABLE, "No PLATFORM_NAME", File=self.DescFilePath)
        return self._PlatformName

    def _GetFileGuid(self):
        if self._Guid == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._Guid == None:
                EdkLogger.error('build', ATTRIBUTE_NOT_AVAILABLE, "No FILE_GUID", File=self.DescFilePath)
        return self._Guid

    def _GetVersion(self):
        if self._Version == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._Version == None:
                self._Version = ''
        return self._Version

    def _GetDscSpec(self):
        if self._DscSpecification == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._DscSpecification == None:
                self._DscSpecification = ''
        return self._DscSpecification

    def _GetOutpuDir(self):
        if self._OutputDirectory == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._OutputDirectory == None:
                self._OutputDirectory = os.path.join("Build", self._PlatformName)
        return self._OutputDirectory

    def _GetSupArch(self):
        if self._SupArchList == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._SupArchList == None:
                self._SupArchList = ARCH_LIST
        return self._SupArchList

    def _GetBuildTarget(self):
        if self._BuildTargets == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._BuildTargets == None:
                self._BuildTargets = ['DEBUG', 'RELEASE']
        return self._BuildTargets

    def _GetSkuName(self):
        if self._SkuName == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._SkuName == None or self._SkuName not in self.SkuIds:
                self._SkuName = 'DEFAULT'
        return self._SkuName

    def _SetSkuName(self, Value):
        if Value in self.SkuIds:
            self._SkuName = Value

    def _GetFdfFile(self):
        if self._FlashDefinition == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._FlashDefinition == None:
                self._FlashDefinition = ''
        return self._FlashDefinition

    def _GetBuildNumber(self):
        if self._BuildNumber == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._BuildNumber == None:
                self._BuildNumber = ''
        return self._BuildNumber

    def _GetMakefileName(self):
        if self._MakefileName == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._MakefileName == None:
                self._MakefileName = ''
        return self._MakefileName

    def _GetBsBaseAddress(self):
        if self._BsBaseAddress == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._BsBaseAddress == None:
                self._BsBaseAddress = ''
        return self._BsBaseAddress

    def _GetRtBaseAddress(self):
        if self._RtBaseAddress == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._RtBaseAddress == None:
                self._RtBaseAddress = ''
        return self._RtBaseAddress

    def _GetSkuIds(self):
        if self._SkuIds == None:
            self._SkuIds = {}
            RecordList = self._RawData[MODEL_EFI_SKU_ID]
            for Record in RecordList:
                if Record[0] in [None, '']:
                    EdkLogger.error('build', FORMAT_INVALID, 'No Sku ID number',
                                    File=self.DescFilePath, Line=Record[-1])
                if Record[1] in [None, '']:
                    EdkLogger.error('build', FORMAT_INVALID, 'No Sku ID name',
                                    File=self.DescFilePath, Line=Record[-1])
                self._SkuIds[Record[1]] = Record[0]
            if 'DEFAULT' not in self._SkuIds:
                self._SkuIds['DEFAULT'] = 0
        return self._SkuIds

    def _GetModules(self):
        if self._Modules != None:
            return self._Modules

        self._Modules = sdict()
        RecordList = self._RawData[MODEL_META_DATA_COMPONENT, self._Arch]
        for Record in RecordList:
            ModuleFile = NormPath(Record[0], self._Macros)
            ModuleId = Record[5]
            LineNo = Record[6]
            if not ValidFile(ModuleFile):
                EdkLogger.error('build', FILE_NOT_FOUND, File=self.DescFilePath, 
                                ExtraData=ModuleFile, Line=LineNo)
            if ModuleFile in self._Modules:
                continue
            Module = ModuleBuildClassObject()
            Module.DescFilePath = ModuleFile

            # get module private library instance
            RecordList = self._RawData[MODEL_EFI_LIBRARY_CLASS, self._Arch, None, ModuleId]
            for Record in RecordList:
                LibraryClass = Record[0]
                LibraryPath = NormPath(Record[1], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(LibraryPath):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=LibraryPath,
                                    File=self.DescFilePath, Line=LineNo)
                if LibraryClass == '' or LibraryClass == 'NULL':
                    self._NullLibraryNumber += 1
                    LibraryClass = 'NULL%d' % self._NullLibraryNumber
                    EdkLogger.verbose("Found forced library for %s\n\t%s [%s]" % (ModuleFile, LibraryPath, LibraryClass))
                Module.LibraryClasses[LibraryClass] = LibraryPath
                if LibraryPath not in self.LibraryInstances:
                    self.LibraryInstances.append(LibraryPath)

            # get module private PCD setting
            for Type in [MODEL_PCD_FIXED_AT_BUILD, MODEL_PCD_PATCHABLE_IN_MODULE, \
                         MODEL_PCD_FEATURE_FLAG, MODEL_PCD_DYNAMIC, MODEL_PCD_DYNAMIC_EX]:
                RecordList = self._RawData[Type, self._Arch, None, ModuleId]
                for TokenSpaceGuid, PcdCName, Setting, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
                    TokenList = GetSplitValueList(Setting)
                    DefaultValue = TokenList[0]
                    if len(TokenList) > 1:
                        MaxDatumSize = TokenList[1]
                    else:
                        MaxDatumSize = ''
                    Type = self._PCD_TYPE_STRING_[MODEL_PCD_FIXED_AT_BUILD]
                    Pcd = PcdClassObject(
                            PcdCName,
                            TokenSpaceGuid,
                            Type,
                            '',
                            DefaultValue,
                            '',
                            MaxDatumSize,
                            {},
                            None
                            )
                    Module.Pcds[PcdCName, TokenSpaceGuid] = Pcd

            RecordList = self._RawData[MODEL_META_DATA_BUILD_OPTION, self._Arch, None, ModuleId]
            for ToolChainFamily, ToolChain, Option, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
                if (ToolChainFamily, ToolChain) not in Module.BuildOptions:
                    Module.BuildOptions[ToolChainFamily, ToolChain] = Option
                else:
                    OptionString = Module.BuildOptions[ToolChainFamily, ToolChain]
                    Module.BuildOptions[ToolChainFamily, ToolChain] = OptionString + " " + Option

            self._Modules[ModuleFile] = Module
        return self._Modules

    def _GetLibraryInstances(self):
        if self._LibraryInstances == None:
            self._GetLibraryClasses()
        return self._LibraryInstances

    def _GetLibraryClasses(self):
        if self._LibraryClasses == None:
            self._LibraryInstances = []
            LibraryClassDict = tdict(True, 3)
            LibraryClassSet = set()
            RecordList = self._RawData[MODEL_EFI_LIBRARY_CLASS, self._Arch]
            for LibraryClass, LibraryInstance, Dummy, Arch, ModuleType, Dummy, LineNo in RecordList:
                LibraryClassSet.add(LibraryClass)
                LibraryInstance = NormPath(LibraryInstance, self._Macros)
                if not ValidFile(LibraryInstance):
                    EdkLogger.error('build', FILE_NOT_FOUND, File=self.DescFilePath, 
                                    ExtraData=LibraryInstance, Line=LineNo)
                LibraryClassDict[Arch, ModuleType, LibraryClass] = LibraryInstance
                if LibraryInstance not in self._LibraryInstances:
                    self._LibraryInstances.append(LibraryInstance)

            # resolve the specific library instance for each class and each module type 
            self._LibraryClasses = tdict(True)
            for LibraryClass in LibraryClassSet:
                for ModuleType in SUP_MODULE_LIST:
                    LibraryInstance = LibraryClassDict[self._Arch, ModuleType, LibraryClass]
                    if LibraryInstance == None:
                        continue
                    self._LibraryClasses[LibraryClass, ModuleType] = LibraryInstance

            # for R8 style library instances
            RecordList = self._RawData[MODEL_EFI_LIBRARY_INSTANCE, self._Arch]
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                if File not in self._LibraryInstances:
                    self._LibraryInstances.append(File)
                # 
                # we need the module name as the library class name, so we have
                # to parse it here
                # 
                Library = self._Bdb[File, self._Arch]
                self._LibraryClasses[Library.BaseName, ':dummy:'] = Library
        return self._LibraryClasses

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
            RecordList = self._RawData[MODEL_META_DATA_BUILD_OPTION]
            for ToolChainFamily, ToolChain, Option, Dummy1, Dummy2, Dummy3, Dummy4 in RecordList:
                self._BuildOptions[ToolChainFamily, ToolChain] = Option
        return self._BuildOptions

    def _GetPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 3)
        PcdSet = set()
        # Find out all possible PCD candidates for self._Arch
        RecordList = self._RawData[Type, self._Arch]
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, PcdCName, TokenSpaceGuid] = Setting
        # Remove redundant PCD candidates
        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self._Arch, PcdCName, TokenSpaceGuid]
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
                                                None
                                                )
        return Pcds

    def _GetDynamicPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._RawData[Type, self._Arch]
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self._Arch, self.SkuName, PcdCName, TokenSpaceGuid]
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
                                                None
                                                )
        return Pcds

    def _GetDynamicHiiPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._RawData[Type, self._Arch]
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '', '']
            Setting = PcdDict[self._Arch, self.SkuName, PcdCName, TokenSpaceGuid]
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
                                                None
                                                )
        return Pcds

    def _GetDynamicVpdPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._RawData[Type, self._Arch]
        for TokenSpaceGuid, PcdCName, Setting, Arch, SkuName, Dummy3, Dummy4 in RecordList:
            PcdSet.add((PcdCName, TokenSpaceGuid))
            PcdDict[Arch, SkuName, PcdCName, TokenSpaceGuid] = Setting

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '']
            Setting = PcdDict[self._Arch, self.SkuName, PcdCName, TokenSpaceGuid]
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
                                                None
                                                )
        return Pcds

    def AddModule(self, FilePath):
        FilePath = NormPath(FilePath)
        if FilePath not in self.Modules:
            Module = ModuleBuildClassObject()
            Module.DescFilePath = FilePath
            self.Modules.append(Module)

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
                                        None
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
    SkuName             = property(_GetSkuName, _SetSkuName)
    FlashDefinition     = property(_GetFdfFile)
    BuildNumber         = property(_GetBuildNumber)
    MakefileName        = property(_GetMakefileName)
    BsBaseAddress       = property(_GetBsBaseAddress)
    RtBaseAddress       = property(_GetRtBaseAddress)

    SkuIds              = property(_GetSkuIds)
    Modules             = property(_GetModules)
    LibraryInstances    = property(_GetLibraryInstances)
    LibraryClasses      = property(_GetLibraryClasses)
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

    _PROPERTY_ = {
        #
        # Required Fields
        #
        TAB_DEC_DEFINES_PACKAGE_NAME                : "_PackageName",
        TAB_DEC_DEFINES_PACKAGE_GUID                : "_Guid",
        TAB_DEC_DEFINES_PACKAGE_VERSION             : "_Version",
    }


    def __init__(self, FilePath, RawData, BuildDataBase, Arch='COMMON', Platform='COMMON', Macros={}):
        self.DescFilePath = FilePath
        self._PackageDir = os.path.dirname(FilePath)
        self._RawData = RawData
        self._Bdb = BuildDataBase
        self._Arch = Arch
        self._Platform = Platform
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
        self._Header            = None
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

    def _GetHeaderInfo(self):
        RecordList = self._RawData[MODEL_META_DATA_HEADER]
        for Record in RecordList:
            Name = Record[0]
            if Name in self:
                self[Name] = Record[1]
        self._Header = 'DUMMY'

    def _GetPackageName(self):
        if self._PackageName == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._PackageName == None:
                EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "No PACKAGE_NAME", File=self.DescFilePath)
        return self._PackageName

    def _GetFileGuid(self):
        if self._Guid == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._Guid == None:
                EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "No PACKAGE_GUID", File=self.DescFilePath)
        return self._Guid

    def _GetVersion(self):
        if self._Version == None:
            if self._Header == None:
                self._GetHeaderInfo()
            if self._Version == None:
                self._Version = ''
        return self._Version

    def _GetProtocol(self):
        if self._Protocols == None:
            ProtocolDict = tdict(True)
            NameList = []
            RecordList = self._RawData[MODEL_EFI_PROTOCOL, self._Arch]
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                if Name not in NameList:
                    NameList.append(Name)
                ProtocolDict[Arch, Name] = Guid
            self._Protocols = sdict()
            for Name in NameList:
                self._Protocols[Name] = ProtocolDict[self._Arch, Name]
        return self._Protocols

    def _GetPpi(self):
        if self._Ppis == None:
            PpiDict = tdict(True)
            NameList = []
            RecordList = self._RawData[MODEL_EFI_PPI, self._Arch]
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                if Name not in NameList:
                    NameList.append(Name)
                PpiDict[Arch, Name] = Guid
            self._Ppis = sdict()
            for Name in NameList:
                self._Ppis[Name] = PpiDict[self._Arch, Name]
        return self._Ppis

    def _GetGuid(self):
        if self._Guids == None:
            GuidDict = tdict(True)
            NameList = []
            RecordList = self._RawData[MODEL_EFI_GUID, self._Arch]
            for Name, Guid, Dummy, Arch, ID, LineNo in RecordList:
                if Name not in NameList:
                    NameList.append(Name)
                GuidDict[Arch, Name] = Guid
            self._Guids = sdict()
            for Name in NameList:
                self._Guids[Name] = GuidDict[self._Arch, Name]
        return self._Guids

    def _GetInclude(self):
        if self._Includes == None:
            self._Includes = []
            RecordList = self._RawData[MODEL_EFI_INCLUDE, self._Arch]
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File, self._PackageDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                if File not in self._Includes:
                    self._Includes.append(File)
        return self._Includes

    def _GetLibraryClass(self):
        if self._LibraryClasses == None:
            LibraryClassDict = tdict(True)
            LibraryClassSet = set()
            RecordList = self._RawData[MODEL_EFI_LIBRARY_CLASS, self._Arch]
            for LibraryClass, File, Dummy, Arch, ID, LineNo in RecordList:
                File = NormPath(File, self._Macros)
                if not ValidFile(File, self._PackageDir):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                LibraryClassSet.add(LibraryClass)
                LibraryClassDict[Arch, LibraryClass] = File
            self._LibraryClasses = sdict()
            for LibraryClass in LibraryClassSet:
                self._LibraryClasses[LibraryClass] = LibraryClassDict[self._Arch, LibraryClass]
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
        RecordList = self._RawData[Type, self._Arch]
        for TokenSpaceGuid, PcdCName, Setting, Arch, Dummy1, Dummy2 in RecordList:
            PcdDict[Arch, PcdCName, TokenSpaceGuid] = Setting
            PcdSet.add((PcdCName, TokenSpaceGuid))

        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '', '']
            Setting = PcdDict[self._Arch, PcdCName, TokenSpaceGuid]
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
                                                                            None
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
        TAB_INF_DEFINES_MAKEFILE_NAME               : "_MakefileName",
        #TAB_INF_DEFINES_CUSTOM_MAKEFILE             : "_CustomMakefile",
        TAB_INF_DEFINES_VERSION_NUMBER              : "_Version",
        TAB_INF_DEFINES_VERSION_STRING              : "_Version",
        TAB_INF_DEFINES_VERSION                     : "_Version",
        TAB_INF_DEFINES_PCD_IS_DRIVER               : "_PcdIsDriver",
        TAB_INF_DEFINES_SHADOW                      : "_Shadow",
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
    

    def __init__(self, FilePath, RawData, BuildDatabase, Arch='COMMON', Platform='COMMON', Macros={}):
        self.DescFilePath = FilePath
        self._ModuleDir = os.path.dirname(FilePath)
        self._RawData = RawData
        self._Bdb = BuildDatabase
        self._Arch = Arch
        self._Platform = 'COMMON'
        self._Macros = Macros
        self._Clear()

    def Print(self):
        S = '[%s.%s]\n' % (self.DescFilePath, self._Arch)
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
        self._MakefileName          = None
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
        RecordList = self._RawData[MODEL_META_DATA_HEADER, self._Arch, self._Platform]
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
            elif Name == TAB_INF_DEFINES_CUSTOM_MAKEFILE:
                TokenList = GetSplitValueList(Record[1])
                if self._CustomMakefile == None:
                    self._CustomMakefile = {}
                if len(TokenList) < 2:
                    self._CustomMakefile['MSFT'] = TokenList[0]
                    self._CustomMakefile['GCC'] = TokenList[0]
                else:
                    if TokenList[0] not in ['MSFT', 'GCC']:
                        EdkLogger.error("build", FORMAT_NOT_SUPPORTED,
                                        "No supported family [%s]" % TokenList[0], 
                                        File=self.DescFilePath, Line=Record[-1])
                    self._CustomMakefile[TokenList[0]] = TokenList[1]

        # 
        # R8.x modules
        # 
        if self._AutoGenVersion < 0x00010005:   # _AutoGenVersion may be None, which is less than anything
            if self._ComponentType in self._MODULE_TYPE_:
                self._ModuleType = self._MODULE_TYPE_[self._ComponentType]
            if self._ComponentType == 'LIBRARY':
                self._LibraryClass = [LibraryClassObject(self._BaseName, SUP_MODULE_LIST)]
            # make use some [nmake] section macros
            RecordList = self._RawData[MODEL_META_DATA_NMAKE, self._Arch, self._Platform]
            for Name,Value,Dummy,Arch,Platform,ID,LineNo in RecordList:
                if Name == "IMAGE_ENTRY_POINT":
                    if self._ModuleEntryPointList == None:
                        self._ModuleEntryPointList = []
                    self._ModuleEntryPointList.append(Value)
                elif Name == "DPX_SOURCE":
                    File = NormPath(Value, self._Macros)
                    if not ValidFile(File, self._ModuleDir):
                        EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                        File=self.DescFilePath, Line=LineNo)
                    if self.Sources == None:
                        self._Sources = []
                    self._Sources.append(ModuleSourceFileClass(File, "", "", "", ""))
                else:
                    ToolList = self._NMAKE_FLAG_PATTERN_.findall(Name)
                    if len(ToolList) == 0 or len(ToolList) != 1:
                        EdkLogger.warn("build", "Don't know how to do with macro [%s]" % Name, 
                                       File=self.DescFilePath, Line=LineNo)
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
                EdkLogger.error('build', ATTRIBUTE_NOT_AVAILABLE, "No BASE_NAME name", File=self.DescFilePath)
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
                self._CustomMakefile = {}
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
            RecordList = self._RawData[MODEL_EFI_BINARY_FILE, self._Arch, self._Platform]
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
            RecordList = self._RawData[MODEL_EFI_SOURCE_FILE, self._Arch, self._Platform]
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
            RecordList = self._RawData[MODEL_EFI_LIBRARY_CLASS, self._Arch, self._Platform]
            for Record in RecordList:
                Lib = Record[0]
                Instance = Record[1]
                if Instance != None and Instance != '':
                    Instance = NormPath(Instance, self._Macros)
                self._LibraryClasses[Lib] = Instance
        return self._LibraryClasses

    def _SetLibraryClassUses(self, Value):
        self._LibraryClasses = Value

    def _GetLibraryNames(self):
        if self._Libraries == None:
            self._Libraries = []
            RecordList = self._RawData[MODEL_EFI_LIBRARY_INSTANCE, self._Arch, self._Platform]
            for Record in RecordList:
                # in case of name with '.lib' extension, which is unusual in R8.x inf
                LibraryName = os.path.splitext(Record[0])[0]
                if LibraryName not in self._Libraries:
                    self._Libraries.append(LibraryName)
        return self._Libraries

    def _GetProtocols(self):
        if self._Protocols == None:
            self._Protocols = sdict()
            RecordList = self._RawData[MODEL_EFI_PROTOCOL, self._Arch, self._Platform]
            for Record in RecordList:
                CName = Record[0]
                Value = GuidValue(CName, self.Packages)
                if Value == None:
                    PackageList = '\t' + "\n\t".join([str(P) for P in self.Packages])
                    EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "Value of [%s] is not found in" % CName,
                                    ExtraData=PackageList, File=self.DescFilePath, Line=Record[-1])
                self._Protocols[CName] = Value
        return self._Protocols

    def _GetPpis(self):
        if self._Ppis == None:
            self._Ppis = sdict()
            RecordList = self._RawData[MODEL_EFI_PPI, self._Arch, self._Platform]
            for Record in RecordList:
                CName = Record[0]
                Value = GuidValue(CName, self.Packages)
                if Value == None:
                    PackageList = '\t' + "\n\t".join([str(P) for P in self.Packages])
                    EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "Value of [%s] is not found in " % CName,
                                    ExtraData=PackageList, File=self.DescFilePath, Line=Record[-1])
                self._Ppis[CName] = Value
        return self._Ppis

    def _GetGuids(self):
        if self._Guids == None:
            self._Guids = sdict()
            RecordList = self._RawData[MODEL_EFI_GUID, self._Arch, self._Platform]
            for Record in RecordList:
                CName = Record[0]
                Value = GuidValue(CName, self.Packages)
                if Value == None:
                    PackageList = '\t' + "\n\t".join([str(P) for P in self.Packages])
                    EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "Value of [%s] is not found in" % CName,
                                    ExtraData=PackageList, File=self.DescFilePath, Line=Record[-1])
                self._Guids[CName] = Value
        return self._Guids

    def _GetIncludes(self):
        if self._Includes == None:
            self._Includes = []
            RecordList = self._RawData[MODEL_EFI_INCLUDE, self._Arch, self._Platform]
            # [includes] section must be used only in old (R8.x) inf file
            if self.AutoGenVersion >= 0x00010005 and len(RecordList) > 0:
                EdkLogger.error('build', FORMAT_NOT_SUPPORTED, "No [include] section allowed",
                                File=self.DescFilePath, Line=RecordList[0][-1]-1)
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
                if File in self._Includes:
                    continue
                self._Includes.append(File)
        return self._Includes

    def _GetPackages(self):
        if self._Packages == None:
            self._Packages = []
            RecordList = self._RawData[MODEL_META_DATA_PACKAGE, self._Arch, self._Platform]
            for Record in RecordList:
                File = NormPath(Record[0], self._Macros)
                LineNo = Record[-1]
                if not ValidFile(File):
                    EdkLogger.error('build', FILE_NOT_FOUND, ExtraData=File,
                                    File=self.DescFilePath, Line=LineNo)
                Package = self._Bdb[File, self._Arch]
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
            RecordList = self._RawData[MODEL_META_DATA_BUILD_OPTION, self._Arch, self._Platform]
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
            self._Depex = []
            RecordList = self._RawData[MODEL_EFI_DEPEX, self._Arch, self._Platform]
            for Record in RecordList:
                TokenList = Record[0].split()
                for Token in TokenList:
                    if Token in DEPEX_SUPPORTED_OPCODE or Token.endswith(".inf"):
                        self._Depex.append(Token)
                    else:
                        Value = GuidValue(Token, self.Packages)
                        if Value == None:
                            PackageList = '\t' + "\n\t".join([str(P) for P in self.Packages])
                            EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "Value of [%s] is not found in" % Token,
                                            ExtraData=PackageList, File=self.DescFilePath, Line=Record[-1])
                        self._Depex.append(Value)
        return self._Depex

    def _GetPcd(self, Type):
        Pcds = {}
        PcdDict = tdict(True, 4)
        PcdSet = set()
        RecordList = self._RawData[Type, self._Arch, self._Platform]
        for TokenSpaceGuid, PcdCName, Setting, Arch, Platform, Dummy1, LineNo in RecordList:
            PcdDict[Arch, Platform, PcdCName, TokenSpaceGuid] = (Setting, LineNo)
            PcdSet.add((PcdCName, TokenSpaceGuid))
            if TokenSpaceGuid not in self.Guids:
                Value = GuidValue(TokenSpaceGuid, self.Packages)
                if Value == None:
                    PackageList = '\t' + "\n\t".join([str(P) for P in self.Packages])
                    EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "Value of [%s] is not found in" % PcdCName,
                                    ExtraData=PackageList, File=self.DescFilePath, Line=LineNo)
                self.Guids[TokenSpaceGuid] = Value

        # resolve PCD type, value, datum info, etc. by getting its definition from package
        for PcdCName, TokenSpaceGuid in PcdSet:
            ValueList = ['', '']
            Setting, LineNo = PcdDict[self._Arch, self.Platform, PcdCName, TokenSpaceGuid]
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
                    self.Guids[TokenSpaceGuid]
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
                            File =self.DescFilePath, Line=LineNo,
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
    Libraries               = property(_GetLibraryNames)
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
    _FILE_PARSER_ = {
        MODEL_FILE_INF  :   InfParser,
        MODEL_FILE_DEC  :   DecParser,
        MODEL_FILE_DSC  :   DscParser,
        MODEL_FILE_FDF  :   None, #FdfParser,
        MODEL_FILE_CIF  :   None
    }

    _FILE_TABLE_ = {
        MODEL_FILE_INF  :   ModuleTable,
        MODEL_FILE_DEC  :   PackageTable,
        MODEL_FILE_DSC  :   PlatformTable,
    }

    _DB_PATH_ = "Conf/.cache/build.db"

    class BuildObjectFactory(object):
        _FILE_TYPE_ = {
            ".INF"  : MODEL_FILE_INF,
            ".DEC"  : MODEL_FILE_DEC,
            ".DSC"  : MODEL_FILE_DSC,
            ".FDF"  : MODEL_FILE_FDF,
            ".CIF"  : MODEL_FILE_CIF,
        }
    
        _GENERATOR_ = {
            MODEL_FILE_INF  :   InfBuildData,
            MODEL_FILE_DEC  :   DecBuildData,
            MODEL_FILE_DSC  :   DscBuildData,
            MODEL_FILE_FDF  :   None #FlashDefTable,
        }

        _CACHE_ = {}    # FilePath  : <object>

        def __init__(self, WorkspaceDb):
            self.WorkspaceDb = WorkspaceDb

        # key = (FilePath, Arch='COMMON')
        def __contains__(self, Key):
            FilePath = Key[0]
            Arch = 'COMMON'
            if len(Key) > 1:
                Arch = Key[1]
            return (FilePath, Arch) in self._CACHE_

        # key = (FilePath, Arch='COMMON', Platform='COMMON')
        def __getitem__(self, Key):
            FilePath = Key[0]
            Arch = 'COMMON'
            Platform = 'COMMON'
            if len(Key) > 1:
                Arch = Key[1]
            if len(Key) > 2:
                Platform = Key[2]

            # if it's generated before, just return the cached one
            Key = (FilePath, Arch)
            if Key in self._CACHE_:
                return self._CACHE_[Key]

            # check file type
            FileExt = os.path.splitext(FilePath)[1].upper()
            if FileExt not in self._FILE_TYPE_:
                return None
            FileType = self._FILE_TYPE_[FileExt]
            if FileType not in self._GENERATOR_:
                return None

            # get table for current file
            MetaFile = self.WorkspaceDb[FilePath, FileType]
            BuildObject = self._GENERATOR_[FileType](
                                    FilePath, 
                                    MetaFile, 
                                    self,
                                    Arch,
                                    Platform,
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

    def __init__(self, DbPath, GlobalMacros={}, RenewDb=False):
        self._GlobalMacros = GlobalMacros

        if DbPath == None or DbPath == '':
            DbPath = self._DB_PATH_

        if DbPath != ':memory:':
            DbDir = os.path.split(DbPath)[0]
            if not os.path.exists(DbDir):
                os.makedirs(DbDir)

        if RenewDb and os.path.exists(DbPath):
            os.remove(DbPath)

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
        EdkLogger.verbose("\nInitialize build database started ...")
        
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
    #def __setitem__(self, FilePath, FileType):
    #    FileId = self.GetFileId(FilePath)
    #    if FileId != None:
    #        TimeStamp = os.stat(FilePath)[8]
    #        TableName = self.GetTableName(FileType, FileId)
    #        if TimeStamp != self.GetTimeStamp(FileId):
    #            self.SetTimeStamp(FileId, TimeStamp)
    #        else:
    #            if self.CheckIntegrity(TableName) == True:
    #                return
    #    else:
    #        FileId = self.TblFile.InsertFile(FilePath, FileType)
    #        TableName = self.GetTableName(FileType, FileId)
    #
    #    FileTable = self._FILE_TABLE_[FileType](self.Cur, TableName, FileId)
    #    FileTable.Create()
    #    Parser = self._FILE_PARSER_[FileType](FilePath, FileId, FileType, FileTable)
    #    Parser.Start()

    ## Return a temp table containing all content of the given file
    # 
    def __getitem__(self, FileInfo):
        FilePath, FileType = FileInfo
        if FileType not in self._FILE_TABLE_:
            return None

        Parsed = False
        FileId = self.GetFileId(FilePath)
        if FileId != None:
            TimeStamp = os.stat(FilePath)[8]
            TableName = self.GetTableName(FileType, FileId)
            if TimeStamp != self.GetTimeStamp(FileId):
                # update the timestamp in database
                self.SetTimeStamp(FileId, TimeStamp)
            else:
                # if the table exists and is integrity, don't parse it
                Parsed = self.CheckIntegrity(TableName)
        else:
            FileId = self.TblFile.InsertFile(FilePath, FileType)
            TableName = self.GetTableName(FileType, FileId)

        FileTable = self._FILE_TABLE_[FileType](self.Cur, TableName, FileId)
        FileTable.Create(not Parsed)
        Parser = self._FILE_PARSER_[FileType](FilePath, FileId, FileType, FileTable)
        Parser.Finished = Parsed

        return Parser

    def _GetPackageList(self):
        PackageList = []
        for Module in self.ModuleList:
            for Package in Module.Packages:
                if Package not in PackageList:
                    PackageList.append(Package)
        return PackageList

    def _GetPlatformList(self):
        PlatformList = []
        for PlatformFile in self.TblFile.GetFileList(MODEL_FILE_DSC):
            try:
                Platform = self.BuildObject[PlatformFile, 'COMMON']
            except:
                Platform = None
            if Platform != None:
                PlatformList.append(Platform)
        return PlatformList

    def _GetModuleList(self):
        ModuleList = []
        for ModuleFile in self.TblFile.GetFileList(MODEL_FILE_INF):
            try:
                Module = self.BuildObject[ModuleFile, 'COMMON']
            except:
                Module = None
            if Module != None:
                ModuleList.append(Module)
        return ModuleList

    PlatformList = property(_GetPlatformList)
    PackageList = property(_GetPackageList)
    ModuleList = property(_GetModuleList)

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    pass
