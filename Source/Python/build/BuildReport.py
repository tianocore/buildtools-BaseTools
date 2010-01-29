## @file
# Routines for generating build report.
# 
# This module contains the functionality to generate build report after
# build all target completes successfully. 
#
# Copyright (c) 2010, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

## Import Modules
#
import os
import re
import platform
import textwrap
from datetime import datetime
from Common import EdkLogger
from Common.Misc import GuidStructureByteArrayToGuidString
from Common.InfClassObject import gComponentType2ModuleType
from Common.BuildToolError import FILE_OPEN_FAILURE
from Common.BuildToolError import FILE_WRITE_FAILURE


## Pattern to extract contents in EDK DXS files
gDxsDependencyPattern = re.compile(r"DEPENDENCY_START(.+)DEPENDENCY_END", re.DOTALL)

## Pattern to find total FV total size, occupied size in flash report intermediate file
gFvTotalSizePattern = re.compile(r"EFI_FV_TOTAL_SIZE = (0x[0-9a-fA-F]+)")
gFvTakenSizePattern = re.compile(r"EFI_FV_TAKEN_SIZE = (0x[0-9a-fA-F]+)")

## Pattern to find module size and time stamp in module summary report intermediate file  
gModuleSizePattern = re.compile(r"MODULE_SIZE = (\d+)")
gTimeStampPattern  = re.compile(r"TIME_STAMP = (\d+)") 

## Pattern to find GUID value in flash description files
gPcdGuidPattern = re.compile(r"PCD\((\w+)[.](\w+)\)")

## Pattern to collect offset, GUID value pair in the flash report intermediate file 
gOffsetGuidPattern = re.compile(r"(0x[0-9A-Fa-f]+) ([-A-Fa-f0-9]+)")

## Tags for section start, end and separator
gSectionStart = ">" + "=" * 118 + "<"
gSectionEnd = "<" + "=" * 118 + ">" + "\n"
gSectionSep = "=" * 120

## Tags for subsection start, end and separator
gSubSectionStart = ">" + "-" * 118 + "<"
gSubSectionEnd = "<" + "-" * 118 + ">"
gSubSectionSep = "-" * 120

## The look up table to map PCD type to pair of report display type and DEC type
gPcdTypeMap = {
  'FixedAtBuild'     : ('FIXED',  'FixedAtBuild'),
  'PatchableInModule': ('PATCH',  'PatchableInModule'),
  'FeatureFlag'      : ('FLAG',   'FeatureFlag'),
  'Dynamic'          : ('DYN',    'Dynamic'),
  'DynamicHii'       : ('DYNHII', 'Dynamic'),
  'DynamicVpd'       : ('DYNVPD', 'Dynamic'),
  'DynamicEx'        : ('DEX',    'Dynamic'),
  'DynamicExHii'     : ('DEXHII', 'Dynamic'),
  'DynamicExVpd'     : ('DEXVPD', 'Dynamic'),
  }

## The look up table to map module type to driver type
gDriverTypeMap = {
  'SEC'               : '0x3 (SECURITY_CORE)',
  'PEI_CORE'          : '0x4 (PEI_CORE)',
  'PEIM'              : '0x6 (PEIM)',
  'DXE_CORE'          : '0x5 (DXE_CORE)',
  'DXE_DRIVER'        : '0x7 (DRIVER)',
  'DXE_SAL_DRIVER'    : '0x7 (DRIVER)',
  'DXE_SMM_DRIVER'    : '0x7 (DRIVER)',
  'DXE_RUNTIME_DRIVER': '0x7 (DRIVER)',
  'UEFI_DRIVER'       : '0x7 (DRIVER)',
  'UEFI_APPLICATION'  : '0x9 (APPLICATION)',
  'SMM_CORE'          : '0xD (SMM_CORE)',
  }

##
# Writes a string to the file object.
# 
# This function writes a string to the file object and a new line is appended 
# afterwards. It may optionally wraps the string for better readability.   
#
# @File                      The file object to write
# @String                    The string to be written to the file
# @Wrapper                   Indicates whether to wrap the string
#
def FileWrite(File, String, Wrapper=False):
    if Wrapper:
        String = textwrap.fill(String, 120)
    File.write(String + "\n")


##
# Reports library information
#
# This class reports the module library subsection in the build report file.
#     
class LibraryReport(object):
    ##
    # Constructor function for class LibraryReport
    #
    # This constructor function generates LibraryReport object for 
    # a module.
    #
    # @param self            The object pointer
    # @param M               Module context information
    #
    def __init__(self, M):
        self.LibraryList = []
        if int(str(M.AutoGenVersion), 0) >= 0x00010005:
            self._EdkIIModule = True
        else:
            self._EdkIIModule = False
               
        for Lib in M.DependentLibraryList:
            LibInfPath = str(Lib)
            LibClassList = Lib.LibraryClass[0].LibraryClass
            LibConstructorList = Lib.ConstructorList
            LibDesstructorList = Lib.DestructorList
            LibDepexList = Lib.DepexExpression[M.Arch, M.ModuleType]
            self.LibraryList.append((LibInfPath, LibClassList, LibConstructorList, LibDesstructorList, LibDepexList))
    
    ##
    # Generate report for module library information
    #
    # This function generates report for the module library.
    # If the module is EDKII style one, the additional library class, library
    # constructor/destructor and dependency expression may also be reported.  
    #
    # @param self            The object pointer
    # @param File            The file object for report
    #
    def GenerateReport(self, File):
        FileWrite(File, gSubSectionStart)
        FileWrite(File, "Library")
        if len(self.LibraryList) > 0:
            FileWrite(File, gSubSectionSep)
            for LibraryItem in self.LibraryList:
                LibInfPath = LibraryItem[0]
                FileWrite(File, LibInfPath)
                
                #
                # Report library class, library constructor and destructor for
                # EDKII style module.
                #
                if self._EdkIIModule:
                    LibClass = LibraryItem[1]
                    EdkIILibInfo = ""
                    LibConstructor = " ".join(LibraryItem[2])
                    if LibConstructor:
                        EdkIILibInfo += " C = " + LibConstructor
                    LibDestructor = " ".join(LibraryItem[3])
                    if LibDestructor:
                        EdkIILibInfo += " D = " + LibConstructor
                    LibDepex = " ".join(LibraryItem[3])
                    if LibDepex:
                        EdkIILibInfo += " Depex = " + LibDepex
                    if EdkIILibInfo:
                        FileWrite(File, "{%s: %s}" % (LibClass, EdkIILibInfo))
                    else:
                        FileWrite(File, "{%s}" % LibClass)
        
        FileWrite(File, gSubSectionEnd)

##
# Reports dependency expression information
#
# This class reports the module dependency expression subsection in the build report file.
#             
class DepexReport(object):
    ##
    # Constructor function for class DepexReport
    #
    # This constructor function generates DepexReport object for 
    # a module. If the module source contains the DXS file (usually EDK
    # style module), it uses the dependency in DXS file; otherwise,
    # it uses the dependency expression from its own INF [Depex] section
    # and then merges with the ones from its dependent library INF.
    #
    # @param self            The object pointer
    # @param M               Module context information
    #
    def __init__(self, M):
        for Source in M.SourceFileList:
            if os.path.splitext(Source.Path)[1].lower() == ".dxs":
                Match = gDxsDependencyPattern.search(open(Source.Path).read())
                if Match:
                    self.Depex = Match.group(1).strip()
                    self.Source = "DXS"
                    break
        else:
            self.Depex = M.DepexExpressionList[M.ModuleType]
            self.ModuleDepex = " ".join(M.Module.DepexExpression[M.Arch, M.ModuleType])
            if not self.ModuleDepex:
                self.ModuleDepex = "TRUE"
            
            LibDepexList = []
            for Lib in M.DependentLibraryList:
                LibDepex = " ".join(Lib.DepexExpression[M.Arch, M.ModuleType]).strip()
                if LibDepex != "":                         
                    if " " in LibDepex:
                        LibDepex = "(" + LibDepex + ")"
                    LibDepexList.append(LibDepex)
            self.LibraryDepex = " AND ".join(LibDepexList)
            if not self.LibraryDepex:
                self.LibraryDepex = "(None)"
            self.Source = "INF"
    
    ##
    # Generate report for module dependency expression information
    #
    # This function generates report for the module dependency expression.
    #
    # @param self            The object pointer
    # @param File            The file object for report
    #
    def GenerateReport(self, File):
        FileWrite(File, gSubSectionStart)
        FileWrite(File, "Dependency Expression (DEPEX) from %s" % self.Source)
        
        if self.Source == "INF":
            FileWrite(File, "%s" % self.Depex, True)
            FileWrite(File, gSubSectionSep)
            FileWrite(File, "From Module INF:  %s" % self.ModuleDepex, True)
            FileWrite(File, "From Library INF: %s" % self.LibraryDepex, True)
        else:
            FileWrite(File, "%s" % self.Depex)
        FileWrite(File, gSubSectionEnd)

##
# Reports dependency expression information
#
# This class reports the module build flags subsection in the build report file.
#                     
class BuildFlagsReport(object):
    ##
    # Constructor function for class BuildFlagsReport
    #
    # This constructor function generates BuildFlagsReport object for 
    # a module. It reports the build tool chain tag and all relevant 
    # build flags to build the module.
    #
    # @param self            The object pointer
    # @param M               Module context information
    #
    def __init__(self, M):
        BuildOptions = {}
        #
        # Add build flags according to source file extension so that
        # irrelevant ones can be filtered out. 
        #
        for Source in M.SourceFileList:
            Ext = os.path.splitext(Source.File)[1].lower()
            if Ext in [".c", ".cc", ".cpp"]:
                BuildOptions["CC"] = 1
            elif Ext in [".s", ".asm"]:
                BuildOptions["PP"] = 1
                BuildOptions["ASM"] = 1
            elif Ext in [".vfr"]:
                BuildOptions["VFRPP"] = 1
                BuildOptions["VFR"] = 1
            elif Ext in [".dxs"]:
                BuildOptions["APP"] = 1
                BuildOptions["CC"] = 1
            elif Ext in [".asl"]:
                BuildOptions["ASLPP"] = 1
                BuildOptions["ASL"] = 1
            elif Ext in [".aslc"]:
                BuildOptions["ASLCC"] = 1
                BuildOptions["ASLDLINK"] = 1
                BuildOptions["CC"] = 1
            elif Ext in [".asm16"]:
                BuildOptions["ASMLINK"] = 1
            BuildOptions["SLINK"] = 1
            BuildOptions["DLINK"] = 1
        
        #
        # Save module build flags.
        #
        self.ToolChainTag = M.ToolChain
        self.BuildFlags = {}
        for Tool in BuildOptions:
            self.BuildFlags[Tool + "_FLAGS"] = M.BuildOption.get(Tool, {}).get("FLAGS", "")

    ##
    # Generate report for module build flags information
    #
    # This function generates report for the module build flags expression.
    #
    # @param self            The object pointer
    # @param File            The file object for report
    #
    def GenerateReport(self, File):
        FileWrite(File, gSubSectionStart)
        FileWrite(File, "Build Flags")
        FileWrite(File, "Tool Chain Tag: %s" % self.ToolChainTag)
        for Tool in self.BuildFlags:
            FileWrite(File, gSubSectionSep)
            FileWrite(File, "%s = %s" % (Tool, self.BuildFlags[Tool]), True)
        
        FileWrite(File, gSubSectionEnd)


##
# Reports individual module information
#
# This class reports the module section in the build report file. 
# It comprises of module summary, module PCD, library, dependency expression,
# build flags sections.  
#        
class ModuleReport(object):
    ##
    # Constructor function for class ModuleReport
    #
    # This constructor function generates ModuleReport object for 
    # a separate module in a platform build.  
    #
    # @param self            The object pointer
    # @param M               Module context information
    # @param DscOverridePcds Module DSC override PCD information
    # @param ReportType      The kind of report items in the final report file
    #
    def __init__(self, M, DscOverridePcds, ReportType):
        self.ModuleName = M.Module.BaseName
        self.ModuleInfPath = M.MetaFile.File
        self.FileGuid = M.Guid
        self.Size = 0
        self.BuildTimeStamp = None
        self.DriverType = ""
        ModuleType = M.ModuleType
        if not ModuleType:
            ModuleType = gComponentType2ModuleType.get(M.ComponentType, "")
        self.DriverType = gDriverTypeMap.get(ModuleType, "")
        self.UefiSpecVersion = M.Module.Specification.get("UEFI_SPECIFICATION_VERSION", "")
        self.PiSpecVersion = M.Module.Specification.get("PI_SPECIFICATION_VERSION", "")
        self.PciDeviceId = M.Module.Defines.get("PCI_DEVICE_ID", "")
        self.PciVendorId = M.Module.Defines.get("PCI_VENDOR_ID", "")
        self.PciClassCode = M.Module.Defines.get("PCI_CLASS_CODE", "")
  
        self._BuildDir = M.BuildDir
        self.ModulePcdSet = {}
        self.ModuleDscOverridePcds = {}
        if "PCD" in ReportType:
            #
            # Collect all module used PCD set: module INF referenced directly or indirectly.
            # It also saves module INF default values of them in case they exist.
            #
            for Pcd in M.ModulePcdList + M.LibraryPcdList:
                self.ModulePcdSet.setdefault((Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Pcd.Type), Pcd.InfDefaultValue)
            
            #
            # Collect module DSC override PCD set for report
            #
            for (PcdTokenCName, PcdTokenSpaceGuidCName) in DscOverridePcds:
                Pcd = DscOverridePcds[(PcdTokenCName, PcdTokenSpaceGuidCName)]
                self.ModuleDscOverridePcds.setdefault((PcdTokenCName, PcdTokenSpaceGuidCName), Pcd.DefaultValue)
        
        self.LibraryReport = None
        if "LIBRARY" in ReportType:
            self.LibraryReport = LibraryReport(M)
        
        self.DepexReport = None
        if "DEPEX" in ReportType:
            self.DepexReport = DepexReport(M)
        
        if "BUILD_FLAGS" in ReportType:
            self.BuildFlagsReport = BuildFlagsReport(M)
        
    
    ##
    # Generate report for module information
    #
    # This function generates report for separate module expression
    # in a platform build.
    #
    # @param self            The object pointer
    # @param File            The file object for report
    # @param GlobalPcdReport The platform global PCD class object
    # @param ReportType      The kind of report items in the final report file
    #
    def GenerateReport(self, File, GlobalPcdReport, ReportType):
        FileWrite(File, gSectionStart)
        
        FwReportFileName = os.path.join(self._BuildDir, "DEBUG", self.ModuleName + ".txt")
        if os.path.isfile(FwReportFileName):
            try:
                FileContents = open(FwReportFileName).read()
                Match = gModuleSizePattern.search(FileContents)
                if Match:
                    self.Size = int(Match.group(1))
                
                Match = gTimeStampPattern.search(FileContents)
                if Match:
                    self.BuildTimeStamp = datetime.utcfromtimestamp(int(Match.group(1)))
            except IOError:
                EdkLogger.warn(None, "Fail to read report file", FwReportFileName)
            
        FileWrite(File, "Module Summary")
        FileWrite(File, "Module Name:          %s" % self.ModuleName)
        FileWrite(File, "Module INF Path:      %s" % self.ModuleInfPath)
        FileWrite(File, "File GUID:            %s" % self.FileGuid)
        if self.Size:
            FileWrite(File, "Size:                 0x%X (%.2fK)" % (self.Size, self.Size / 1024.0))
        if self.BuildTimeStamp:
            FileWrite(File, "Build Time Stamp:     %s" % self.BuildTimeStamp)
        if self.DriverType:
            FileWrite(File, "Driver Type:          %s" % self.DriverType)
        if self.UefiSpecVersion:
            FileWrite(File, "UEFI Spec Version:    %s" % self.DriverType)
        if self.PiSpecVersion:
            FileWrite(File, "PI Spec Version:      %s" % self.PiSpecVersion)
        if self.PciDeviceId:
            FileWrite(File, "PCI Device ID:        %s" % self.PciDeviceId)
        if self.PciVendorId:
            FileWrite(File, "PCI Vendor ID:        %s" % self.PciVendorId)
        if self.PciClassCode:
            FileWrite(File, "PCI Class Code:       %s" % self.PciClassCode)
        
        FileWrite(File, gSectionSep)   
        
        if "PCD" in ReportType:
            GlobalPcdReport.GenerateReport(File, self.ModulePcdSet, self.ModuleDscOverridePcds)
        
        if "LIBRARY" in ReportType:
            self.LibraryReport.GenerateReport(File)
        
        if "DEPEX" in ReportType:
            self.DepexReport.GenerateReport(File)
        
        if "BUILD_FLAGS" in ReportType:
            self.BuildFlagsReport.GenerateReport(File)
        
        FileWrite(File, gSectionEnd)

##
# Reports platform and module PCD information
#
# This class reports the platform PCD section and module PCD subsection
# in the build report file.
#     
class PcdReport(object):
    ##
    # Constructor function for class PcdReport
    #
    # This constructor function generates PcdReport object a platform build.
    # It collects the whole PCD database from platform DSC files, platform
    # flash description file and package DEC files.
    #
    # @param self            The object pointer
    # @param Wa              Workspace context information
    #
    def __init__(self, Wa):
        self.AllPcds = {}
        self.MaxLen = 0
        self.FdfPcdSet = Wa.FdfProfile.PcdDict

        self.DecPcdDefault = {}
        self.ModulePcdOverride = {}
        for Pa in Wa.AutoGenObjectList:
            #
            # Collect all platform referenced PCDs and grouped them by PCD token space
            # GUID C Names
            #
            for Pcd in Pa.AllPcdList:
                PcdList = self.AllPcds.setdefault(Pcd.TokenSpaceGuidCName, {}).setdefault(Pcd.Type, [])
                if Pcd not in PcdList:
                    PcdList.append(Pcd)
                if len(Pcd.TokenCName) > self.MaxLen:
                    self.MaxLen = len(Pcd.TokenCName)
            
            for ModuleKey in Pa.Platform.Modules:
                #
                # Collect PCD DEC default value.
                #   
                Module = Pa.Platform.Modules[ModuleKey]
                for Package in Module.M.Module.Packages:
                    for (TokenCName, TokenSpaceGuidCName, DecType) in Package.Pcds:
                        DecDefaultValue = Package.Pcds[TokenCName, TokenSpaceGuidCName, DecType].DefaultValue
                        self.DecPcdDefault.setdefault((TokenCName, TokenSpaceGuidCName, DecType), DecDefaultValue)
                #
                # Collect module override PCDs
                #
                for ModulePcd in Module.M.ModulePcdList + Module.M.LibraryPcdList:
                    TokenCName = ModulePcd.TokenCName
                    TokenSpaceGuid = ModulePcd.TokenSpaceGuidCName
                    ModuleDefault = ModulePcd.DefaultValue
                    ModulePath = os.path.basename(Module.M.MetaFile.File)
                    self.ModulePcdOverride.setdefault((TokenCName, TokenSpaceGuid), []).append((ModuleDefault, ModulePath))

        #
        # Collect PCDs defined in DSC common section
        #
        self.DscPcdDefault = {}
        for Platform in Wa.BuildDatabase.WorkspaceDb.PlatformList:
            for (TokenCName, TokenSpaceGuidCName) in Platform.Pcds:
                DscDefaultValue = Platform.Pcds[(TokenCName, TokenSpaceGuidCName)].DefaultValue
                self.DscPcdDefault[(TokenCName, TokenSpaceGuidCName)] = DscDefaultValue
    
    ##
    # Generate report for PCD information
    #
    # This function generates report for separate module expression
    # in a platform build.
    #
    # @param self            The object pointer
    # @param File            The file object for report
    # @param ModulePcdSet    Set of all PCDs referenced by module or None for
    #                        platform PCD report
    # @param DscOverridePcds Module DSC override PCDs set
    #
    def GenerateReport(self, File, ModulePcdSet, DscOverridePcds):
        if ModulePcdSet == None:
            #
            # For platform global PCD section
            #
            FileWrite(File, gSectionStart)
            FileWrite(File, "Platform Configuration Database Report")
            FileWrite(File, "  *P  - Platform scoped PCD override in DSC file")
            FileWrite(File, "  *F  - Platform scoped PCD override in FDF file")
            FileWrite(File, "  *M  - Module scoped PCD override in DSC file")
            FileWrite(File, gSectionSep)
        else:
            #
            # For module PCD sub-section
            #
            FileWrite(File, gSubSectionStart)
            FileWrite(File, "PCD")
            FileWrite(File, gSubSectionSep)

        for Key in self.AllPcds:
            #
            # Group PCD by their token space GUID C Name
            #
            First = True
            for Type in self.AllPcds[Key]:
                #
                # Group PCD by their usage type
                #
                TypeName, DecType = gPcdTypeMap.get(Type, ("", Type))
                for Pcd in self.AllPcds[Key][Type]:
                    #
                    # Get PCD default value and their override relationship
                    #
                    InfDefaultValue = None
                    if ModulePcdSet != None:
                        if (Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Type) not in ModulePcdSet:
                            continue
                        InfDefault = ModulePcdSet[Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Type]
                        if InfDefault == "":
                            InfDefault = None
                    if First:
                        if ModulePcdSet == None:
                            FileWrite(File, "")
                        FileWrite(File, Key)
                        First = False
                    DecDefaultValue = self.DecPcdDefault.get((Pcd.TokenCName, Pcd.TokenSpaceGuidCName, DecType))
                    DscDefaultValue = self.DscPcdDefault.get((Pcd.TokenCName, Pcd.TokenSpaceGuidCName))
                    DscModuleOverrideValue = DscOverridePcds.get((Pcd.TokenCName, Pcd.TokenSpaceGuidCName))
                          
                    if Pcd.DatumType in ('UINT8', 'UINT16', 'UINT32', 'UINT64'):
                        PcdDefaultValueNumber = int(Pcd.DefaultValue.strip(), 0)
                        if DecDefaultValue == None:
                            DecMatch = True
                        else:
                            DecDefaultValueNumber = int(DecDefaultValue.strip(), 0)
                            DecMatch = (DecDefaultValueNumber == PcdDefaultValueNumber)
                  
                        if InfDefaultValue == None:
                            InfMatch = True
                        else:
                            InfDefaultValueNumber = int(InfDefaultValue.strip(), 0)
                            InfMatch = (InfDefaultValueNumber == PcdDefaultValueNumber)
                                
                        if DscDefaultValue == None:
                            DscMatch = True
                        else:
                            DscDefaultValueNumber = int(DscDefaultValue.strip(), 0)
                            DscMatch = (DscDefaultValueNumber == PcdDefaultValueNumber)
                    else:
                        if DecDefaultValue == None:
                            DecMatch = True
                        else:
                            DecMatch = (DecDefaultValue == Pcd.DefaultValue)
                  
                        if InfDefaultValue == None:
                            InfMatch = True
                        else:
                            InfMatch = (InfDefaultValue == Pcd.DefaultValue)
                            
                        if DscDefaultValue == None:
                            DscMatch = True
                        else:
                            DscMatch = (DscDefaultValue == Pcd.DefaultValue)
                    
                    #
                    # Report PCD item according to their override relationship
                    #        
                    if DecMatch and InfMatch:
                        FileWrite(File, '    %-*s: %6s %10s = %-22s' % (self.MaxLen, Pcd.TokenCName, TypeName, '('+Pcd.DatumType+')', Pcd.DefaultValue))
                    else:
                        if DscMatch and DscModuleOverrideValue == None:
                            if (Pcd.TokenCName, Key) in self.FdfPcdSet:
                                FileWrite(File, ' *F %-*s: %6s %10s = %-22s' % (self.MaxLen, Pcd.TokenCName, TypeName, '('+Pcd.DatumType+')', Pcd.DefaultValue))
                            else:
                                FileWrite(File, ' *P %-*s: %6s %10s = %-22s' % (self.MaxLen, Pcd.TokenCName, TypeName, '('+Pcd.DatumType+')', Pcd.DefaultValue))
                        else:
                            FileWrite(File, ' *M %-*s: %6s %10s = %-22s' % (self.MaxLen, Pcd.TokenCName, TypeName, '('+Pcd.DatumType+')', Pcd.DefaultValue))
                            if DscDefaultValue != None:
                                FileWrite(File, '    %*s = %s' % (self.MaxLen + 19, 'DSC DEFAULT', DscDefaultValue))
                        
                        if InfDefaultValue != None:
                            FileWrite(File, '    %*s = %s' % (self.MaxLen + 19, 'INF DEFAULT', InfDefaultValue))
                        
                        if DecDefaultValue != None and not DecMatch:
                            FileWrite(File, '    %*s = %s' % (self.MaxLen + 19, 'DEC DEFAULT', DecDefaultValue))

                    if ModulePcdSet == None:
                        for (ModuleDefault, ModulePath) in self.ModulePcdOverride.get((Pcd.TokenCName, Pcd.TokenSpaceGuidCName), []):
                            if Pcd.DatumType in ('UINT8', 'UINT16', 'UINT32', 'UINT64'):
                                ModulePcdDefaultValueNumber = int(ModuleDefault.strip(), 0)
                                Match = (ModulePcdDefaultValueNumber == PcdDefaultValueNumber)
                            else:
                                Match = (ModuleDefault == Pcd.DefaultValue)
                            if Match:
                                continue
                            FileWrite(File, ' *M %-*s = %s' % (self.MaxLen + 19, ModulePath, ModuleDefault))
        
        if ModulePcdSet == None:
            FileWrite(File, gSectionEnd)
        else:
            FileWrite(File, gSubSectionEnd)     


##
# Reports FD region information
#
# This class reports the FD subsection in the build report file.
# It collects region information of platform flash device. 
# If the region is a firmware volume, it lists the set of modules
# and its space information; otherwise, it only lists its region name,
# base address and size in its sub-section header.
# If there are nesting FVs, the nested FVs will list immediate after
# this FD region subsection
#
class FdRegionReport(object):
    ##
    # Discover all the nested FV name list.
    #
    # This is an internal worker function to discover the all the nested FV information
    # in the parent firmware volume. It uses deep first search algorithm recursively to
    # find all the FV list name and append them to the list.
    #
    # @param self            The object pointer
    # @param FvName          The name of current firmware file system
    # @param Wa              Workspace context information
    #
    def _DiscoverNestedFvList(self, FvName, Wa):
        for Ffs in Wa.FdfProfile.FvDict[FvName.upper()].FfsList:
            for Section in Ffs.SectionList:
                try:
                    for FvSection in Section.SectionList:
                        if FvSection.FvName in self.FvList:
                            continue
                        self._GuidsDb[Ffs.NameGuid.upper()] = FvSection.FvName
                        self.FvList.append(FvSection.FvName)
                        self.FvInfo[FvSection.FvName] = ("Nested FV", 0, 0)
                        self._DiscoverNestedFvList(FvSection.FvName, Wa)
                except AttributeError:
                    pass
    
    ##
    # Constructor function for class FdRegionReport
    #
    # This constructor function generates FdRegionReport object for a specified FdRegion. 
    # If the FdRegion is a firmware volume, it will recursively find all its nested Firmware
    # volume list. This function also collects GUID map in order to dump module identification
    # in the final report.
    #
    # @param self:           The object pointer
    # @param FdRegion        The current FdRegion object
    # @param Wa              Workspace context information
    #
    def __init__(self, FdRegion, Wa):
        self.Type = FdRegion.RegionType
        self.BaseAddress = FdRegion.Offset
        self.Size = FdRegion.Size
        self.FvList = []
        self.FvInfo = {}
        self._GuidsDb = {}
        self._FvDir = Wa.FvDir

        #
        # If the input FdRegion is not a firmware volume,
        # we are done. 
        #
        if self.Type != "FV":
            return
        
        #
        # Find all nested FVs in the FdRegion
        #
        for FvName in FdRegion.RegionDataList:
            if FvName in self.FvList:
                continue
            self.FvList.append(FvName)
            self.FvInfo[FvName] = ("Fd Region", self.BaseAddress, self.Size)
            self._DiscoverNestedFvList(FvName, Wa)

        PlatformPcds = {}
        for Pa in Wa.AutoGenObjectList:
            PackageList = []
            for ModuleKey in Pa.Platform.Modules:
                #
                # Collect PCD DEC default value.
                #   
                Module = Pa.Platform.Modules[ModuleKey]
                for Package in Module.M.Module.Packages:
                    if Package not in PackageList:
                        PackageList.append(Package)
                
            for Package in PackageList:
                for (TokenCName, TokenSpaceGuidCName, DecType) in Package.Pcds:
                    DecDefaultValue = Package.Pcds[TokenCName, TokenSpaceGuidCName, DecType].DefaultValue
                    PlatformPcds[(TokenCName, TokenSpaceGuidCName)] = DecDefaultValue
        
        #
        # Collect PCDs defined in DSC common section
        #
        for Platform in Wa.BuildDatabase.WorkspaceDb.PlatformList:
            for (TokenCName, TokenSpaceGuidCName) in Platform.Pcds:
                DscDefaultValue = Platform.Pcds[(TokenCName, TokenSpaceGuidCName)].DefaultValue
                PlatformPcds[(TokenCName, TokenSpaceGuidCName)] = DscDefaultValue
        
        #
        # Add PEI and DXE a priori files GUIDs defined in PI specification.
        #
        self._GuidsDb["1B45CC0A-156A-428A-AF62-49864DA0E6E6"] = "PEI Apriori"
        self._GuidsDb["FC510EE7-FFDC-11D4-BD41-0080C73C8881"] = "DXE Apriori" 
        #
        # Add ACPI table storage file
        #
        self._GuidsDb["7E374E25-8E01-4FEE-87F2-390C23C606CD"] = "ACPI table storage"
        #
        # Collect the GUID map in the FV firmware volume
        #
        for FvName in self.FvList:
            for Ffs in Wa.FdfProfile.FvDict[FvName.upper()].FfsList:
                try:
                    #
                    # Collect GUID, module mapping from INF file
                    #
                    InfFileName = Ffs.InfFileName
                    try:
                        FileGuid = ""
                        ModuleName = ""
                        InfPath = os.path.join(Wa.WorkspaceDir, InfFileName)
                        for Line in open(InfPath):
                            ItemList = Line.split("#")[0].split("=")
                            if len(ItemList) == 2:
                                Key   = ItemList[0].strip().upper()
                                Value = ItemList[1].strip()
                                if Key == "FILE_GUID":
                                    FileGuid = Value.upper()
                                if Key == "BASE_NAME":
                                    ModuleName = Value
                        if FileGuid:
                            self._GuidsDb[FileGuid] = "%s (%s)" % (ModuleName, InfPath)
                    except IOError:
                        EdkLogger.warn(None, "Cannot open file to read", InfPath)
                except AttributeError:
                    try:
                        #
                        # collect GUID map for binary EFI file in FDF file.
                        #
                        Guid = Ffs.NameGuid.upper()
                        Match = gPcdGuidPattern.match(Ffs.NameGuid)
                        if Match:
                            PcdTokenspace = Match.group(1)
                            PcdToken = Match.group(2)
                            if (PcdToken, PcdTokenspace) in PlatformPcds:
                                GuidValue = PlatformPcds[(PcdToken, PcdTokenspace)]
                                Guid = GuidStructureByteArrayToGuidString(GuidValue).upper()

                        for Section in Ffs.SectionList:
                            try:
                                ModuleSectFile = os.path.join(Wa.WorkspaceDir, Section.SectFileName)
                                self._GuidsDb[Guid] = ModuleSectFile
                            except AttributeError:
                                pass
                    except AttributeError:
                        pass
        
    
    ##
    # Internal worker function to generate report for the FD region
    #
    # This internal worker function to generate report for the FD region.
    # It the type is firmware volume, it lists offset and module identification. 
    #
    # @param self            The object pointer
    # @param File            The file object for report
    # @param Title           The title for the FD subsection 
    # @param BaseAddress     The base address for the FD region
    # @param Size            The size of the FD region
    # @param FvName          The FV name if the FD region is a firmware volume
    #
    def _GenerateReport(self, File, Title, Type, BaseAddress, Size=0, FvName=None):
        FileWrite(File, gSubSectionStart)
        FileWrite(File, Title)
        FileWrite(File, "Type:               %s" % Type)
        FileWrite(File, "Base Address:       0x%X" % BaseAddress)
        
        if self.Type == "FV":
            FvTotalSize = 0
            FvTakenSize = 0
            FvFreeSize  = 0
            FvReportFileName = os.path.join(self._FvDir, FvName + ".fv.txt")
            try:
                #
                # Collect size info in the firmware volume.
                #
                FvReport = open(FvReportFileName).read()
                Match = gFvTotalSizePattern.search(FvReport)
                if Match:
                    FvTotalSize = int(Match.group(1), 16)
                Match = gFvTakenSizePattern.search(FvReport)
                if Match:
                    FvTakenSize = int(Match.group(1), 16)
                FvFreeSize = FvTotalSize - FvTakenSize 
                #
                # Write size information to the report file.
                #
                FileWrite(File, "Size:               0x%X (%.0fK)" % (FvTotalSize, FvTotalSize / 1024.0))
                FileWrite(File, "Fv Name:            %s (%.1f%% Full)" % (FvName, FvTakenSize * 100.0 / FvTotalSize))
                FileWrite(File, "Occupied Size:      0x%X (%.0fK)" % (FvTakenSize, FvTakenSize / 1024.0))
                FileWrite(File, "Free Size:          0x%X (%.0fK)" % (FvFreeSize, FvFreeSize / 1024.0))
                FileWrite(File, "Offset     Module")
                FileWrite(File, gSubSectionSep)
                #
                # Write module offset and module identification to the report file.
                #
                for Match in gOffsetGuidPattern.finditer(FvReport):
                    Guid = Match.group(2).upper()
                    Offset = int(Match.group(1), 16)
                    FileWrite (File, "0x%07X %s" % (Offset, self._GuidsDb.get(Guid, Guid)))
            except IOError:
                EdkLogger.warn(None, "Fail to read report file", FvReportFileName)
        else:
            FileWrite(File, "Size:               0x%X (%.0fK)" % (Size, Size / 1024.0))
        FileWrite(File, gSubSectionEnd)

    ##
    # Generate report for the FD region
    #
    # This function generates report for the FD region. 
    #
    # @param self            The object pointer
    # @param File            The file object for report
    #
    def GenerateReport(self, File):
        if (len(self.FvList) > 0):
            for FvItem in self.FvList:
                Info = self.FvInfo[FvItem]
                self._GenerateReport(File, Info[0], "FV", Info[1], Info[2], FvItem)
        else:
            self._GenerateReport(File, "FD Region", self.Type, self.BaseAddress, self.Size)    
            
##
# Reports FD information
#
# This class reports the FD section in the build report file.
# It collects flash device information for a platform. 
#
class FdReport(object):
    ##
    # Constructor function for class FdReport
    #
    # This constructor function generates FdReport object for a specified
    # firmware device. 
    #
    # @param self            The object pointer
    # @param Fd              The current Firmware device object
    # @param Wa              Workspace context information
    #
    def __init__(self, Fd, Wa):
        self.FdName = Fd.FdUiName
        self.BaseAddress = Fd.BaseAddress
        self.Size = Fd.Size
        self.FdRegionList = [FdRegionReport(FdRegion, Wa) for FdRegion in Fd.RegionList]

    ##
    # Generate report for the firmware device.
    #
    # This function generates report for the firmware device. 
    #
    # @param self            The object pointer
    # @param File            The file object for report
    #
    def GenerateReport(self, File):
        FileWrite(File, gSectionStart)
        FileWrite(File, "Firmware Device (FD)")
        FileWrite(File, "FD Name:            %s" % self.FdName)
        FileWrite(File, "Base Address:       0x%s" % self.BaseAddress)
        FileWrite(File, "Size:               0x%X (%.0fK)" % (self.Size, self.Size / 1024.0))
        if len(self.FdRegionList) > 0:
            FileWrite(File, gSectionSep)
            for FdRegionItem in self.FdRegionList:
                FdRegionItem.GenerateReport(File)
        
        FileWrite(File, gSectionEnd)

    
##
# Reports platform information
#
# This class reports the whole platform information 
#     
class PlatformReport(object):
    ##
    # Constructor function for class PlatformReport
    #
    # This constructor function generates PlatformReport object a platform build.
    # It generates report for platform summary, flash, global PCDs and detailed
    # module information for modules involved in platform build.
    #
    # @param self            The object pointer
    # @param Wa              Workspace context information
    #
    def __init__(self, Wa, ReportType):
        self._WorkspaceDir = Wa.WorkspaceDir
        self.PlatformName = Wa.Name
        self.PlatformDscPath = Wa.Platform
        self.Architectures = " ".join(Wa.ArchList)
        self.ToolChain = Wa.ToolChain
        self.Target = Wa.BuildTarget
        self.OutputPath = os.path.join(Wa.WorkspaceDir, Wa.OutputDir)
        self.BuildEnvironment = platform.platform()
        
        self.PcdReport = None
        if "PCD" in ReportType:
            self.PcdReport = PcdReport(Wa)

        self.FdReportList = []
        if "FLASH" in ReportType and Wa.FdfProfile:
            for Fd in Wa.FdfProfile.FdDict:
                self.FdReportList.append(FdReport(Wa.FdfProfile.FdDict[Fd], Wa))
                
        self.ModuleReportList = []
        for Pa in Wa.AutoGenObjectList:
            for ModuleKey in Pa.Platform.Modules:
                for Platform in Wa.BuildDatabase.WorkspaceDb.PlatformList:
                    if ModuleKey in Platform.Modules:
                        DscOverridePcds = Platform.Modules[ModuleKey].Pcds
                        break
                else:
                    DscOverridePcds = {}
                self.ModuleReportList.append(ModuleReport(Pa.Platform.Modules[ModuleKey].M, DscOverridePcds, ReportType))
 
    ##
    # Generate report for the whole platform.
    #
    # This function generates report for platform information.
    # It comprises of platform summary, global PCD, flash and 
    # module list sections.
    #
    # @param self            The object pointer
    # @param File            The file object for report
    # @param BuildDuration   The total time to build the modules
    # @param ReportType      The kind of report items in the final report file
    #
    def GenerateReport(self, File, BuildDuration, ReportType):
        FileWrite(File, "Platform Summary")
        FileWrite(File, "Platform Name:        %s" % self.PlatformName)
        FileWrite(File, "Platform DSC Path:    %s" % self.PlatformDscPath)
        FileWrite(File, "Platform DSC Path:    %s" % self.Architectures)
        FileWrite(File, "Tool Chain:           %s" % self.ToolChain)
        FileWrite(File, "Target:               %s" % self.Target)
        FileWrite(File, "Output Path:          %s" % self.OutputPath)
        FileWrite(File, "Build Environment:    %s" % self.BuildEnvironment)
        FileWrite(File, "Build Duration:       %s" % BuildDuration)
        FileWrite(File, "Report Content:       %s" % ", ".join(ReportType))
 
        if "PCD" in ReportType:
            self.PcdReport.GenerateReport(File, None, {})
            
        if "FLASH" in ReportType:
            for FdReportListItem in self.FdReportList:
                FdReportListItem.GenerateReport(File)
        
        for ModuleReportItem in self.ModuleReportList:
            ModuleReportItem.GenerateReport(File, self.PcdReport, ReportType)
        

## BuildReport class
#
#  This base class contain the routines to collect data and then
#  applies certain format to the output report 
#
class BuildReport(object):
    ##
    # Constructor function for class BuildReport
    #
    # This constructor function generates BuildReport object a platform build.
    # It generates report for platform summary, flash, global PCDs and detailed
    # module information for modules involved in platform build.
    #
    # @param self            The object pointer
    # @param ReportFile      The file name to save report file
    # @param ReportType      The kind of report items in the final report file
    #
    def __init__(self, ReportFile, ReportType):
        self.ReportFile = ReportFile
        if ReportFile:
            self.ReportType = []
            if ReportType == None or "ALL" in ReportType:
                self.ReportType = ["PCD", "LIBRARY", "BUILD_FLAGS", "DEPEX", "FLASH", "PREDICTION"]
            else:
                for ReportTypeItem in ReportType:
                    if ReportTypeItem not in self.ReportType:
                        self.ReportType.append(ReportTypeItem)
    
    ##
    # Adds platform report to the list
    #
    # This function adds a platform report to the final report list.
    #
    # @param self            The object pointer
    # @param Wa              Workspace context information
    #           
    def AddPlatformReport(self, Wa):
        if self.ReportFile:
            self.ReportList.append(PlatformReport(Wa, self.ReportType))

    ##
    # Generates the final report.
    #
    # This function generates platform build report. It invokes GenerateReport()
    # method for every platform report in the list.
    #
    # @param self            The object pointer
    # @param BuildDuration   The total time to build the modules
    # 
    def GenerateReport(self, BuildDuration):
        if self.ReportFile:
            try:
                File = open(self.ReportFile, "w+")
            except IOError:
                EdkLogger.error(None, FILE_OPEN_FAILURE, ExtraData=self.ReportFile)
            try:
                for Report in self.ReportList:
                    Report.GenerateReport(File, BuildDuration, self.ReportType) 
            except IOError:
                EdkLogger.error(None, FILE_WRITE_FAILURE, ExtraData=self.ReportFile)
            File.close()
        
# This acts like the main() function for the script, unless it is 'import'ed into another script.
if __name__ == '__main__':
    pass

