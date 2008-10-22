## @file
# Generate AutoGen.h, AutoGen.c and *.depex files
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

## Import Modules
#
import sys
import os
import re
import os.path as path
import imp
import copy
from optparse import OptionParser
from optparse import make_option

import Common.EdkLogger
import GenC
import GenMake
import GenDepex

from StrGather import *
from BuildEngine import *

from Common.BuildToolError import *
from Common.EdkIIWorkspaceBuild import *
from Common.EdkIIWorkspace import *
from Common.DataType import *
from Common.Misc import *
from Common.String import *
import Common.GlobalData as GlobalData
from GenFds.FdfParser import *

## Regular expression for splitting Dependency Expression stirng into tokens
gDepexTokenPattern = re.compile("(\(|\)|\w+| \S+\.inf)")

## Mapping Makefile type
gMakeTypeMap = {"MSFT":"nmake", "GCC":"gmake"}

## Default output flag for all tools
gDefaultOutputFlag = "-o "

## Output flags for specific tools
gOutputFlag = {
    ("MSFT", "CC", "OUTPUT")      :   "/Fo",
    ("MSFT", "SLINK", "OUTPUT")   :   "/OUT:",
    ("MSFT", "DLINK", "OUTPUT")   :   "/OUT:",
    ("MSFT", "ASMLINK", "OUTPUT") :   "/OUT:",
    ("MSFT", "PCH", "OUTPUT")     :   "/Fp",
    ("MSFT", "ASM", "OUTPUT")     :   "/Fo",

    ("INTEL", "CC", "OUTPUT")          :   "/Fo",
    ("INTEL", "SLINK", "OUTPUT")       :   "/OUT:",
    ("INTEL", "DLINK", "OUTPUT")       :   "/OUT:",
    ("INTEL", "ASMLINK", "OUTPUT")     :   "/OUT:",
    ("INTEL", "PCH", "OUTPUT")         :   "/Fp",
    ("INTEL", "ASM", "OUTPUT")         :   "/Fo",

    ("GCC", "CC", "OUTPUT")        :   "-o ",
    ("GCC", "SLINK", "OUTPUT")     :   "-cr ",
    ("GCC", "DLINK", "OUTPUT")     :   "-o ",
    ("GCC", "ASMLINK", "OUTPUT")   :   "-o ",
    ("GCC", "PCH", "OUTPUT")       :   "-o ",
    ("GCC", "ASM", "OUTPUT")       :   "-o ",
}

## Flag for include file search path
gIncludeFlag = {"MSFT" : "/I", "GCC" : "-I", "INTEL" : "-I"}

## Build rule configuration file
gBuildRuleFile = 'Conf/build_rule.txt'

## default file name for AutoGen
gAutoGenCodeFileName = "AutoGen.c"
gAutoGenHeaderFileName = "AutoGen.h"
gAutoGenDepexFileName = "%(module_name)s.depex"

## Base class for AutoGen
#
#   This class just implements the cache mechanism of AutoGen objects.
#
class AutoGen(object):
    # database to maintain the objects of xxxAutoGen
    _CACHE_ = {}    # (BuildTarget, ToolChain) : {ARCH : {platform file: AutoGen object}}}

    ## Factory method
    #
    #   @param  Class           class object of real AutoGen class
    #                           (WorkspaceAutoGen, ModuleAutoGen or PlatformAutoGen)
    #   @param  Workspace       Workspace directory or WorkspaceAutoGen object
    #   @param  MetaFile        The path of meta file
    #   @param  Target          Build target
    #   @param  Toolchain       Tool chain name
    #   @param  Arch            Target arch
    #   @param  *args           The specific class related parameters
    #   @param  **kwargs        The specific class related dict parameters
    #
    def __new__(Class, Workspace, MetaFile, Target, Toolchain, Arch, *args, **kwargs):
        # check if the object has been created
        Key = (Target, Toolchain)
        if Key not in Class._CACHE_ or Arch not in Class._CACHE_[Key] \
           or MetaFile not in Class._CACHE_[Key][Arch]:
            AutoGenObject = super(AutoGen, Class).__new__(Class)
            # call real constructor
            if not AutoGenObject._Init(Workspace, MetaFile, Target, Toolchain, Arch, *args, **kwargs):
                return None
            if Key not in Class._CACHE_:
                Class._CACHE_[Key] = {}
            if Arch not in Class._CACHE_[Key]:
                Class._CACHE_[Key][Arch] = {}
            Class._CACHE_[Key][Arch][MetaFile] = AutoGenObject
        else:
            AutoGenObject = Class._CACHE_[Key][Arch][MetaFile]

        return AutoGenObject

    ## hash() operator
    #
    #  The file path of platform file will be used to represent hash value of this object
    #
    #   @retval int     Hash value of the file path of platform file
    #
    def __hash__(self):
        return hash(self._MetaFile)

    ## str() operator
    #
    #  The file path of platform file will be used to represent this object
    #
    #   @retval string  String of platform file path
    #
    def __str__(self):
        return self._MetaFile

    ## "==" operator
    def __eq__(self, Other):
        return Other != None and self._MetaFile == str(Other)

## Workspace AutoGen class
#
#   This class is used mainly to control the whole platform build for different
# architecture. This class will generate top level makefile.
#
class WorkspaceAutoGen(AutoGen):
    ## Real constructor of WorkspaceAutoGen
    #
    # This method behaves the same as __init__ except that it needs explict invoke
    # (in super class's __new__ method)
    #
    #   @param  WorkspaceDir            Root directory of workspace
    #   @param  ActivePlatform          Meta-file of active platform
    #   @param  Target                  Build target
    #   @param  Toolchain               Tool chain name
    #   @param  ArchList                List of architecture of current build
    #   @param  MetaFileDb              Database containing meta-files
    #   @param  BuildConfig             Configuration of build
    #   @param  ToolDefinition          Tool chain definitions
    #   @param  FlashDefinitionFile     File of flash definition
    #   @param  Fds                     FD list to be generated
    #   @param  Fvs                     FV list to be generated
    #   @param  SkuId                   SKU id from command line
    #
    def _Init(self, WorkspaceDir, ActivePlatform, Target, Toolchain, ArchList, MetaFileDb,
              BuildConfig, ToolDefinition, FlashDefinitionFile='', Fds=[], Fvs=[], SkuId=''):
        self._MetaFile      = str(ActivePlatform)
        self.WorkspaceDir   = WorkspaceDir
        self.Platform       = ActivePlatform
        self.BuildTarget    = Target
        self.ToolChain      = Toolchain
        self.ArchList       = ArchList
        self.SkuId          = SkuId

        self.BuildDatabase  = MetaFileDb
        self.TargetTxt      = BuildConfig
        self.ToolDef        = ToolDefinition
        self.FdfFile        = FlashDefinitionFile
        self.FdTargetList   = Fds
        self.FvTargetList   = Fvs
        self.AutoGenObjectList = []

        # there's many relative directory operations, so ...
        os.chdir(self.WorkspaceDir)

        # parse FDF file to get PCDs in it, if any
        if self.FdfFile != None and self.FdfFile != '':
            Fdf = FdfParser(os.path.join(self.WorkspaceDir, self.FdfFile))
            Fdf.ParseFile()
            PcdSet = Fdf.Profile.PcdDict
            ModuleList = Fdf.Profile.InfList
        else:
            PcdSet = {}
            ModuleList = []

        # apply SKU and inject PCDs from Flash Definition file
        for Arch in self.ArchList:
            Platform = self.BuildDatabase[self._MetaFile, Arch]
            Platform.SkuName = self.SkuId
            for Name, Guid in PcdSet:
                Platform.AddPcd(Name, Guid, PcdSet[Name, Guid])

            Pa = PlatformAutoGen(self, self._MetaFile, Target, Toolchain, Arch)
            self.AutoGenObjectList.append(Pa)

        self._BuildDir = None
        self._FvDir = None
        self._MakeFileDir = None
        self._BuildCommand = None

        return True

    ## Return the directory to store FV files
    def _GetFvDir(self):
        if self._FvDir == None:
            self._FvDir = path.join(self.BuildDir, 'FV')
        return self._FvDir

    ## Return the directory to store all intermediate and final files built
    def _GetBuildDir(self):
        return self.AutoGenObjectList[0].BuildDir

    ## Return the build output directory platform specifies
    def _GetOutputDir(self):
        return self.Platform.OutputDirectory

    ## Return platform name
    def _GetName(self):
        return self.Platform.PlatformName

    ## Return meta-file GUID
    def _GetGuid(self):
        return self.Platform.Guid

    ## Return platform version
    def _GetVersion(self):
        return self.Platform.Version

    ## Return paths of tools
    def _GetToolPaths(self):
        return self.AutoGenObjectList[0].ToolPath

    ## Return options of tools
    def _GetToolOptions(self):
        return self.AutoGenObjectList[0].ToolOption

    ## Return directory of platform makefile
    #
    #   @retval     string  Makefile directory
    #
    def _GetMakeFileDir(self):
        if self._MakeFileDir == None:
            self._MakeFileDir = self.BuildDir
        return self._MakeFileDir

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def _GetBuildCommand(self):
        if self._BuildCommand == None:
            # BuildCommand should be all the same. So just get one from platform AutoGen
            self._BuildCommand = self.AutoGenObjectList[0].BuildCommand
        return self._BuildCommand

    ## Create makefile for the platform and mdoules in it
    #
    #   @param      CreateDepsMakeFile      Flag indicating if the makefile for
    #                                       modules will be created as well
    #
    def CreateMakeFile(self, CreateDepsMakeFile=False):
        # create makefile for platform
        Makefile = GenMake.TopLevelMakefile(self)
        if Makefile.Generate():
            EdkLogger.verbose("Generated makefile for platform [%s] %s\n" %
                           (self._MetaFile, self.ArchList))
        else:
            EdkLogger.verbose("Skipped the generation of makefile for platform [%s] %s\n" %
                           (self._MetaFile, self.ArchList))

        if CreateDepsMakeFile:
            for Pa in self.AutoGenObjectList:
                Pa.CreateMakeFile(CreateDepsMakeFile)

    ## Create autogen code for platform and modules
    #
    #  Since there's no autogen code for platform, this method will do nothing
    #  if CreateModuleCodeFile is set to False.
    #
    #   @param      CreateDepsCodeFile      Flag indicating if creating module's
    #                                       autogen code file or not
    #
    def CreateCodeFile(self, CreateDepsCodeFile=False):
        if not CreateDepsCodeFile:
            return
        for Pa in self.AutoGenObjectList:
            Pa.CreateCodeFile(CreateDepsCodeFile)

    Name                = property(_GetName)
    Guid                = property(_GetGuid)
    Version             = property(_GetVersion)
    OutputDir           = property(_GetOutputDir)

    ToolPath            = property(_GetToolPaths)       # toolcode : tool path
    ToolOption          = property(_GetToolOptions)     # toolcode : tool option string

    BuildDir            = property(_GetBuildDir)
    FvDir               = property(_GetFvDir)
    MakeFileDir         = property(_GetMakeFileDir)
    BuildCommand        = property(_GetBuildCommand)

## AutoGen class for platform
#
#  PlatformAutoGen class will process the original information in platform
#  file in order to generate makefile for platform.
#
class PlatformAutoGen(AutoGen):
    ## The real constructor of PlatformAutoGen
    #
    #  This method is not supposed to be called by users of PlatformAutoGen. It's
    #  only used by factory method __new__() to do real initialization work for an
    #  object of PlatformAutoGen
    #
    #   @param      Workspace       EdkIIWorkspaceBuild object
    #   @param      PlatformFile    Platform file (DSC file)
    #   @param      Target          Build target (DEBUG, RELEASE)
    #   @param      Toolchain       Name of tool chain
    #   @param      Arch            arch of the platform supports
    #
    def _Init(self, Workspace, PlatformFile, Target, Toolchain, Arch):
        EdkLogger.verbose("\nAutoGen platform [%s] [%s]" % (PlatformFile, Arch))
        GlobalData.gProcessingFile = "%s [%s, %s, %s]" % (PlatformFile, Arch, Toolchain, Target)

        self._MetaFile = str(PlatformFile)
        self.Workspace = Workspace
        self.WorkspaceDir = Workspace.WorkspaceDir
        self.ToolChain = Toolchain
        self.BuildTarget = Target
        self.Arch = Arch
        self.SourceDir = path.dirname(PlatformFile)
        self.SourceOverrideDir = None
        self.FdTargetList = self.Workspace.FdTargetList
        self.FvTargetList = self.Workspace.FvTargetList

        # flag indicating if the makefile/C-code file has been created or not
        self.IsMakeFileCreated  = False
        self.IsCodeFileCreated  = False

        self._Platform   = None
        self._Name       = None
        self._Guid       = None
        self._Version    = None

        self._BuildRule = None
        self._SourceDir = None
        self._BuildDir = None
        self._OutputDir = None
        self._FvDir = None
        self._MakeFileDir = None
        self._FdfFile = None

        self._PcdTokenNumber = None    # (TokenCName, TokenSpaceGuidCName) : GeneratedTokenNumber
        self._DynamicPcdList = None    # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]
        self._NonDynamicPcdList = None # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]

        self._ToolPath = None          # toolcode : tool path
        self._ToolDllPath = None       # toolcode : lib path
        self._ToolStaticLib = None     # toolcode : lib path
        self._ToolChainFamily = None   # toolcode : tool chain family
        self._BuildOption = None       # toolcode : option
        self._OutputFlag = None        # toolcode : output flag
        self._IncludeFlag = None       # toolcode : include flag
        self._ToolOption = None        # toolcode : tool option string
        self._PackageList = None
        self._ModuleAutoGenList  = None
        self._LibraryAutoGenList = None
        self._BuildCommand = None

        # get the original module/package/platform objects
        self.BuildDatabase = Workspace.BuildDatabase
        return True

    ## Create autogen code for platform and modules
    #
    #  Since there's no autogen code for platform, this method will do nothing
    #  if CreateModuleCodeFile is set to False.
    #
    #   @param      CreateModuleCodeFile    Flag indicating if creating module's
    #                                       autogen code file or not
    #
    def CreateCodeFile(self, CreateModuleCodeFile=False):
        # only module has code to be greated, so do nothing if CreateModuleCodeFile is False
        if self.IsCodeFileCreated or not CreateModuleCodeFile:
            return

        for Ma in self.ModuleAutoGenList:
            Ma.CreateCodeFile(True)

        # don't do this twice
        self.IsCodeFileCreated = True

    ## Create makefile for the platform and mdoules in it
    #
    #   @param      CreateModuleMakeFile    Flag indicating if the makefile for
    #                                       modules will be created as well
    #
    def CreateMakeFile(self, CreateModuleMakeFile=False):
        if CreateModuleMakeFile:
            for ModuleFile in self.Platform.Modules:
                Ma = ModuleAutoGen(self.Workspace, ModuleFile,
                                              self.BuildTarget, self.ToolChain,
                                              self.Arch, self._MetaFile)
                Ma.CreateMakeFile(True)

        # no need to create makefile for the platform more than once
        if self.IsMakeFileCreated:
            return

        # create makefile for platform
        Makefile = GenMake.PlatformMakefile(self)
        if Makefile.Generate():
            EdkLogger.verbose("Generated makefile for platform [%s] [%s]\n" %
                           (self._MetaFile, self.Arch))
        else:
            EdkLogger.verbose("Skipped the generation of makefile for platform [%s] [%s]\n" %
                           (self._MetaFile, self.Arch))
        self.IsMakeFileCreated = True

    ## Return the platform build data object
    def _GetPlatform(self):
        if self._Platform == None:
            self._Platform = self.BuildDatabase[self._MetaFile, self.Arch]
        return self._Platform

    ## Return platform name
    def _GetName(self):
        return self.Platform.PlatformName

    ## Return the meta file GUID
    def _GetGuid(self):
        return self.Platform.Guid

    ## Return the platform version
    def _GetVersion(self):
        return self.Platform.Version

    ## Return the FDF file name
    def _GetFdfFile(self):
        if self._FdfFile == None:
            if self.Workspace.FdfFile != "":
                self._FdfFile= path.join(self.WorkspaceDir, self.Workspace.FdfFile)
            else:
                self._FdfFile = ''
        return self._FdfFile

    ## Return the build output directory platform specifies
    def _GetOutputDir(self):
        return self.Platform.OutputDirectory

    ## Return the directory to store all intermediate and final files built
    def _GetBuildDir(self):
        if self._BuildDir == None:
            if os.path.isabs(self.OutputDir):
                self._BuildDir = path.join(
                                            path.abspath(self.OutputDir),
                                            self.BuildTarget + "_" + self.ToolChain,
                                            )
            else:
                self._BuildDir = path.join(
                                            self.WorkspaceDir,
                                            self.OutputDir,
                                            self.BuildTarget + "_" + self.ToolChain,
                                            )
        return self._BuildDir

    ## Return directory of platform makefile
    #
    #   @retval     string  Makefile directory
    #
    def _GetMakeFileDir(self):
        if self._MakeFileDir == None:
            self._MakeFileDir = path.join(self.BuildDir, self.Arch)
        return self._MakeFileDir

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def _GetBuildCommand(self):
        if self._BuildCommand == None:
            self._BuildCommand = tuple()
            if "MAKE" in self.ToolPath:
                self._BuildCommand += (self.ToolPath["MAKE"],)
                if "MAKE" in self.ToolOption:
                    NewOption = self.ToolOption["MAKE"].strip()
                    if NewOption != '':
                      self._BuildCommand += (NewOption,)
        return self._BuildCommand

    ## Get tool chain definition
    #
    #  Get each tool defition for given tool chain from tools_def.txt and platform
    #
    def _GetToolDefinition(self):
        ToolDefinition = self.Workspace.ToolDef.ToolsDefTxtDictionary
        if "COMMAND_TYPE" not in self.Workspace.ToolDef.ToolsDefTxtDatabase:
            EdkLogger.error('build', RESOURCE_NOT_AVAILABLE, "No tools found in configuration",
                            ExtraData="[%s]" % self._MetaFile)
        ToolCodeList = self.Workspace.ToolDef.ToolsDefTxtDatabase["COMMAND_TYPE"]
        self._ToolPath = {}
        self._ToolDllPath = {}
        self._ToolChainFamily = {}
        self._ToolOption = {}
        self._OutputFlag = {}
        self._IncludeFlag = {}
        for Tool in ToolCodeList:
            KeyBaseString = "%s_%s_%s_%s" % (self.BuildTarget, self.ToolChain, self.Arch, Tool)

            Key = "%s_PATH" % KeyBaseString
            if Key not in ToolDefinition:
                continue
            Path = ToolDefinition[Key]

            Key = "%s_FAMILY" % KeyBaseString
            if Key in ToolDefinition:
                Family = ToolDefinition[Key]
            else:
                Family = ""

            Key = "%s_FLAGS" % KeyBaseString
            if Key in ToolDefinition:
                Option = ToolDefinition[Key]
            else:
                Option = ""

            Key = "%s_DLL" % KeyBaseString
            if Key in ToolDefinition:
                Dll = ToolDefinition[Key]
                # set the DLL path in system's PATH environment
                os.environ["PATH"] = Dll + os.pathsep + os.environ["PATH"]
            else:
                Dll = ""

            Key = KeyBaseString + "_OUTPUT"
            if Key in ToolDefinition:
                OutputFlag = ToolDefinition[Key]
            elif (Family, Tool, "OUTPUT") in gOutputFlag:
                OutputFlag = gOutputFlag[Family, Tool, "OUTPUT"]
                if OutputFlag[0] == '"' and OutputFlag[-1] == '"':
                    OutputFlag = OutputFlag[1:-1]
            else:
                OutputFlag = gDefaultOutputFlag

            if Family in gIncludeFlag:
                InputFlag = gIncludeFlag[Family]
            else:
                InputFlag = '-I'

            self._ToolPath[Tool] = Path
            self._ToolDllPath[Tool] = Dll
            self._ToolChainFamily[Tool] = Family
            self._ToolOption[Tool] = Option
            self._OutputFlag[Tool] = OutputFlag
            self._IncludeFlag[Tool] = InputFlag

    ## Return the paths of tools
    def _GetToolPaths(self):
        if self._ToolPath == None:
            self._GetToolDefinition()
        return self._ToolPath

    ## Return the dll paths of tools
    def _GetToolDllPaths(self):
        if self._ToolDllPath == None:
            self._GetToolDefinition()
        return self._ToolDllPath

    ## Return the static libraries of tools
    def _GetToolStaticLibs(self):
        if self._ToolStaticLib == None:
            self._GetToolDefinition()
        return self._ToolStaticLib

    ## Return the families of tools
    def _GetToolChainFamilies(self):
        if self._ToolChainFamily == None:
            self._GetToolDefinition()
        return self._ToolChainFamily

    ## Return the build options specific to this platform
    def _GetBuildOptions(self):
        if self._BuildOption == None:
            self._BuildOption = self._ExpandBuildOption(self.Platform.BuildOptions)
        return self._BuildOption

    ## Return the output flag of tools
    def _GetOuputFlags(self):
        if self._OutputFlag == None:
            self._GetToolDefinition()
        return self._OutputFlag

    ## Return the include flags of tools
    def _GetIncludeFlags(self):
        if self._IncludeFlag == None:
            self._GetToolDefinition()
        return self._IncludeFlag

    ## Return the default options of tools
    def _GetToolOptions(self):
        if self._ToolOption == None:
            self._GetToolDefinition()
        return self._ToolOption

    ## Parse build_rule.txt in $(WORKSPACE)/Conf/build_rule.txt
    #
    #   @retval     BuildRule object
    #
    def _GetBuildRule(self):
        if self._BuildRule == None:
            BuildRuleFile = None
            if TAB_TAT_DEFINES_BUILD_RULE_CONF in self.Workspace.TargetTxt.TargetTxtDictionary:
                BuildRuleFile = self.Workspace.TargetTxt.TargetTxtDictionary[TAB_TAT_DEFINES_BUILD_RULE_CONF]
            if BuildRuleFile in [None, '']:
                BuildRuleFile = gBuildRuleFile
            self._BuildRule = BuildRule(BuildRuleFile)
        return self._BuildRule

    ## Summarize the packages used by modules in this platform
    def _GetPackageList(self):
        if self._PackageList == None:
            self._PackageList = set()
            for La in self.LibraryAutoGenList:
                self._PackageList.update(La.DependentPackageList)
            for Ma in self.ModuleAutoGenList:
                self._PackageList.update(Ma.DependentPackageList)
        return self._PackageList

    ## Collect dynamic PCDs
    #
    #  Gather dynamic PCDs list from each module and their settings from platform
    #
    def _GetPcdList(self):
        self._NonDynamicPcdList = []
        self._DynamicPcdList = []

        # for gathering error information
        NotFoundPcdList = set()
        NoDatumTypePcdList = set()

        self._GuidValue = {}
        for F in self.Platform.Modules:
            M = ModuleAutoGen(self.Workspace, F, self.BuildTarget, self.ToolChain, self.Arch, self._MetaFile)
            #GuidValue.update(M.Guids)
            for PcdFromModule in M.PcdList:
                # check if the setting of the PCD is found in platform
                #if not PcdFromModule.IsOverrided:
                #    NotFoundPcdList.add("%s [%s]" % (" | ".join(Key), F))
                #    continue

                # make sure that the "VOID*" kind of datum has MaxDatumSize set
                if PcdFromModule.DatumType == "VOID*" and PcdFromModule.MaxDatumSize == None:
                    NoDatumTypePcdList.add("%s [%s]" % (" | ".join(Key), F))

                if PcdFromModule.Type in GenC.gDynamicPcd or PcdFromModule.Type in GenC.gDynamicExPcd:
                    # for autogen code purpose
                    if M.ModuleType in ["PEIM", "PEI_CORE"]:
                        PcdFromModule.Phase = "PEI"
                    if PcdFromModule not in self._DynamicPcdList:
                        self._DynamicPcdList.append(PcdFromModule)
                elif PcdFromModule not in self._NonDynamicPcdList:
                    self._NonDynamicPcdList.append(PcdFromModule)

        # print out error information and break the build, if error found
        if len(NoDatumTypePcdList) > 0:
            NoDatumTypePcdListString = "\n\t\t".join(NoDatumTypePcdList)
            EdkLogger.error("build", AUTOGEN_ERROR, "PCD setting error",
                            File=self._MetaFile,
                            ExtraData="\n\tPCD(s) without MaxDatumSize:\n\t\t%s\n"
                                      % NoDatumTypePcdListString)

    ## Get list of non-dynamic PCDs
    def _GetNonDynamicPcdList(self):
        if self._NonDynamicPcdList == None:
            self._GetPcdList()
        return self._NonDynamicPcdList

    ## Get list of dynamic PCDs
    def _GetDynamicPcdList(self):
        if self._DynamicPcdList == None:
            self._GetPcdList()
        return self._DynamicPcdList

    ## Generate Token Number for all PCD
    def _GetPcdTokenNumbers(self):
        if self._PcdTokenNumber == None:
            self._PcdTokenNumber = sdict()
            TokenNumber = 1
            for Pcd in self.DynamicPcdList:
                if Pcd.Phase == "PEI":
                    EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Pcd.Phase, TokenNumber))
                    self._PcdTokenNumber[Pcd.TokenCName, Pcd.TokenSpaceGuidCName] = TokenNumber
                    TokenNumber += 1

            for Pcd in self.DynamicPcdList:
                if Pcd.Phase == "DXE":
                    EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Pcd.Phase, TokenNumber))
                    self._PcdTokenNumber[Pcd.TokenCName, Pcd.TokenSpaceGuidCName] = TokenNumber
                    TokenNumber += 1

            for Pcd in self.NonDynamicPcdList:
                self._PcdTokenNumber[Pcd.TokenCName, Pcd.TokenSpaceGuidCName] = TokenNumber
                TokenNumber += 1
        return self._PcdTokenNumber

    ## Summarize ModuleAutoGen objects of all modules/libraries to be built for this platform
    def _GetAutoGenObjectList(self):
        self._ModuleAutoGenList = []
        self._LibraryAutoGenList = []
        for ModuleFile in self.Platform.Modules:
            Ma = ModuleAutoGen(
                    self.Workspace,
                    ModuleFile,
                    self.BuildTarget,
                    self.ToolChain,
                    self.Arch,
                    self._MetaFile
                    )
            if Ma not in self._ModuleAutoGenList:
                self._ModuleAutoGenList.append(Ma)
            for La in Ma.LibraryAutoGenList:
                if La not in self._LibraryAutoGenList:
                    self._LibraryAutoGenList.append(La)

    ## Summarize ModuleAutoGen objects of all modules to be built for this platform
    def _GetModuleAutoGenList(self):
        if self._ModuleAutoGenList == None:
            self._GetAutoGenObjectList()
        return self._ModuleAutoGenList

    ## Summarize ModuleAutoGen objects of all libraries to be built for this platform
    def _GetLibraryAutoGenList(self):
        if self._LibraryAutoGenList == None:
            self._GetAutoGenObjectList()
        return self._LibraryAutoGenList

    ## Test if a module is supported by the platform
    #
    #  An error will be raised directly if the module or its arch is not supported
    #  by the platform or current configuration
    #
    def ValidModule(self, Module):
        return Module in self.Platform.Modules or Module in self.Platform.LibraryInstances

    ## Resolve the library classes in a module to library instances
    #
    # This method will not only resolve library classes but also sort the library
    # instances according to the dependency-ship.
    #
    #   @param  Module      The module from which the library classes will be resolved
    #
    #   @retval library_list    List of library instances sorted
    #
    def ApplyLibraryInstance(self, Module):
        ModuleType = Module.ModuleType

        # for overridding library instances with module specific setting
        PlatformModule = self.Platform.Modules[str(Module)]

        # add forced library instance
        for LibraryClass in PlatformModule.LibraryClasses:
            if LibraryClass.startswith("NULL"):
                Module.LibraryClasses[LibraryClass] = PlatformModule.LibraryClasses[LibraryClass]

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
                if LibraryClassName not in LibraryInstance:
                    # override library instance for this module
                    if LibraryClassName in PlatformModule.LibraryClasses:
                        LibraryPath = PlatformModule.LibraryClasses[LibraryClassName]
                    else:
                        LibraryPath = self.Platform.LibraryClasses[LibraryClassName, ModuleType]
                    if LibraryPath == None or LibraryPath == "":
                        LibraryPath = M.LibraryClasses[LibraryClassName]
                        if LibraryPath == None or LibraryPath == "":
                            EdkLogger.error("build", RESOURCE_NOT_AVAILABLE,
                                            "Instance of library class [%s] is not found" % LibraryClassName,
                                            File=self._MetaFile,
                                            ExtraData="in [%s] [%s]\n\tconsumed by module [%s]" % (str(M), self.Arch, str(Module)))

                    LibraryModule = self.BuildDatabase[LibraryPath, self.Arch]
                    # for those forced library instance (NULL library), add a fake library class
                    if LibraryClassName.startswith("NULL"):
                        LibraryModule.LibraryClass.append(LibraryClassObject(LibraryClassName, [ModuleType]))
                    elif LibraryModule.LibraryClass == None or len(LibraryModule.LibraryClass) == 0 \
                         or ModuleType not in LibraryModule.LibraryClass[0].SupModList:
                        EdkLogger.error("build", OPTION_MISSING,
                                        "Module type [%s] is not supported by library instance [%s]" \
                                        % (ModuleType, LibraryPath), File=self._MetaFile,
                                        ExtraData="consumed by [%s]" % str(Module))

                    LibraryInstance[LibraryClassName] = LibraryModule
                    LibraryConsumerList.append(LibraryModule)
                    EdkLogger.verbose("\t" + str(LibraryClassName) + " : " + str(LibraryModule))
                else:
                    LibraryModule = LibraryInstance[LibraryClassName]

                if LibraryModule == None:
                    continue

                if LibraryModule.ConstructorList != [] and LibraryModule not in Constructor:
                    Constructor.append(LibraryModule)

                if LibraryModule not in ConsumedByList:
                    ConsumedByList[LibraryModule] = []
                # don't add current module itself to consumer list
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
            LibraryList.append(M)
            if ConsumedByList[M] == []:
                Q.insert(0, M)

        #
        # start the  DAG algorithm
        #
        while True:
            EdgeRemoved = True
            while Q == [] and EdgeRemoved:
                EdgeRemoved = False
                # for each node Item with a Constructor
                for Item in LibraryList:
                    if Item not in Constructor:
                        continue
                    # for each Node without a constructor with an edge e from Item to Node
                    for Node in ConsumedByList[Item]:
                        if Node in Constructor:
                            continue
                        # remove edge e from the graph if Node has no constructor
                        ConsumedByList[Item].remove(Node)
                        EdgeRemoved = True
                        if ConsumedByList[Item] == []:
                            # insert Item into Q
                            Q.insert(0, Item)
                            break
                    if Q != []:
                        break
            # DAG is done if there's no more incoming edge for all nodes
            if Q == []:
                break

            # remove node from Q
            Node = Q.pop()
            # output Node
            SortedLibraryList.append(Node)

            # for each node Item with an edge e from Node to Item do
            for Item in LibraryList:
                if Node not in ConsumedByList[Item]:
                    continue
                # remove edge e from the graph
                ConsumedByList[Item].remove(Node)

                if ConsumedByList[Item] != []:
                    continue
                # insert Item into Q, if Item has no other incoming edges
                Q.insert(0, Item)

        #
        # if any remaining node Item in the graph has a constructor and an incoming edge, then the graph has a cycle
        #
        for Item in LibraryList:
            if ConsumedByList[Item] != [] and Item in Constructor and len(Constructor) > 1:
                ErrorMessage = "\tconsumed by " + "\n\tconsumed by ".join([str(L) for L in ConsumedByList[Item]])
                EdkLogger.error("build", BUILD_ERROR, 'Library [%s] with constructors has a cycle' % str(Item),
                                ExtraData=ErrorMessage, File=self._MetaFile)
            if Item not in SortedLibraryList:
                SortedLibraryList.append(Item)

        #
        # Build the list of constructor and destructir names
        # The DAG Topo sort produces the destructor order, so the list of constructors must generated in the reverse order
        #
        SortedLibraryList.reverse()
        return SortedLibraryList


    ## Override PCD setting (type, value, ...)
    #
    #   @param  ToPcd       The PCD to be overrided
    #   @param  FromPcd     The PCD overrideing from
    #
    def _OverridePcd(self, ToPcd, FromPcd, Module=""):
        #
        # in case there's PCDs coming from FDF file, which have no type given.
        # at this point, ToPcd.Type has the type found from dependent
        # package
        #
        if FromPcd != None:
            if ToPcd.Pending and FromPcd.Type not in [None, '']:
                ToPcd.Type = FromPcd.Type
            elif ToPcd.Type not in [None, ''] and FromPcd.Type not in [None, ''] \
                and ToPcd.Type != FromPcd.Type:
                EdkLogger.error("build", OPTION_CONFLICT, "Mismatched PCD type",
                                ExtraData="%s.%s is defined as [%s] in module %s, but as [%s] in platform."\
                                          % (ToPcd.TokenSpaceGuidCName, ToPcd.TokenCName,
                                             ToPcd.Type, Module, FromPcd.Type),
                                          File=self._MetaFile)

            if FromPcd.MaxDatumSize not in [None, '']:
                ToPcd.MaxDatumSize = FromPcd.MaxDatumSize
            if FromPcd.DefaultValue not in [None, '']:
                ToPcd.DefaultValue = FromPcd.DefaultValue
            if FromPcd.TokenValue not in [None, '']:
                ToPcd.TokenValue = FromPcd.TokenValue
            if FromPcd.MaxDatumSize not in [None, '']:
                ToPcd.MaxDatumSize = FromPcd.MaxDatumSize
            if FromPcd.DatumType not in [None, '']:
                ToPcd.DatumType = FromPcd.DatumType
            if FromPcd.SkuInfoList not in [None, '', []]:
                ToPcd.SkuInfoList = FromPcd.SkuInfoList

        if ToPcd.DatumType == "VOID*" and ToPcd.MaxDatumSize in ['', None]:
            EdkLogger.verbose("No MaxDatumSize specified for PCD %s.%s" \
                              % (ToPcd.TokenSpaceGuidCName, ToPcd.TokenCName))
            Value = ToPcd.DefaultValue
            if Value in [None, '']:
                ToPcd.MaxDatumSize = 1
            elif Value[0] == 'L':
                ToPcd.MaxDatumSize = str(len(Value) * 2)
            elif Value[0] == '{':
                ToPcd.MaxDatumSize = str(len(Value.split(',')))
            else:
                ToPcd.MaxDatumSize = str(len(Value))

        # apply default SKU for dynamic PCDS if specified one is not available
        if (ToPcd.Type in PCD_DYNAMIC_TYPE_LIST or ToPcd.Type in PCD_DYNAMIC_EX_TYPE_LIST) \
            and ToPcd.SkuInfoList in [None, {}, '']:
            if self.Platform.SkuName in self.Platform.SkuIds:
                SkuName = self.Platform.SkuName
            else:
                SkuName = 'DEFAULT'
            ToPcd.SkuInfoList = {
                SkuName : SkuInfoClass(SkuName, self.Platform.SkuIds[SkuName], '', '', '', '', '', ToPcd.DefaultValue)
            }

    ## Apply PCD setting defined platform to a module
    #
    #   @param  Module  The module from which the PCD setting will be overrided
    #
    #   @retval PCD_list    The list PCDs with settings from platform
    #
    def ApplyPcdSetting(self, Module):
        # for each PCD in module
        for Name,Guid in Module.Pcds:
            PcdInModule = Module.Pcds[Name,Guid]
            # find out the PCD setting in platform
            if (Name,Guid) in self.Platform.Pcds:
                PcdInPlatform = self.Platform.Pcds[Name,Guid]
            else:
                PcdInPlatform = None
            # then override the settings if any
            self._OverridePcd(PcdInModule, PcdInPlatform, Module)
            # resolve the VariableGuid value
            for SkuId in PcdInModule.SkuInfoList:
                Sku = PcdInModule.SkuInfoList[SkuId]
                if Sku.VariableGuid == '': continue
                Sku.VariableGuidValue = GuidValue(Sku.VariableGuid, self.PackageList)
                if Sku.VariableGuidValue == None:
                    PackageList = '\t' + "\n\t".join([str(P) for P in Module.Packages])
                    EdkLogger.error(
                                'build',
                                RESOURCE_NOT_AVAILABLE,
                                "Value of GUID [%s] is not found in" % Sku.VariableGuid,
                                ExtraData=PackageList + "\n\t(used with %s.%s from module %s)" \
                                                        % (Guid, Name, str(Module)),
                                File=self._MetaFile
                                )

        # override PCD settings with module specific setting
        if Module in self.Platform.Modules:
            PlatformModule = self.Platform.Modules[str(Module)]
            for Key  in PlatformModule.Pcds:
                if Key in Module.Pcds:
                    self._OverridePcd(Module.Pcds[Key], PlatformModule.Pcds[Key], Module)
        return Module.Pcds.values()

    ## Resolve library names to library modules
    #
    # (for R8.x modules)
    #
    #   @param  Module  The module from which the library names will be resolved
    #
    #   @retval library_list    The list of library modules
    #
    def ResolveLibraryReference(self, Module):
        EdkLogger.verbose("")
        EdkLogger.verbose("Library instances of module [%s] [%s]:" % (str(Module), self.Arch))
        LibraryConsumerList = [Module]

        # "CompilerStub" is a must for R8 modules
        Module.Libraries.append("CompilerStub")
        LibraryList = []
        while len(LibraryConsumerList) > 0:
            M = LibraryConsumerList.pop()
            for LibraryName in M.Libraries:
                Library = self.Platform.LibraryClasses[LibraryName, ':dummy:']
                if Library == None:
                    for Key in self.Platform.LibraryClasses.data.keys():
                        if LibraryName.upper() == Key.upper():
                            Library = self.Platform.LibraryClasses[Key, ':dummy:']
                            break
                    if Library == None:
                        EdkLogger.warn("build", "Library [%s] is not found" % LibraryName, File=str(M),
                            ExtraData="\t%s [%s]" % (str(Module), self.Arch))
                        continue

                if Library not in LibraryList:
                    LibraryList.append(Library)
                    LibraryConsumerList.append(Library)
                    EdkLogger.verbose("\t" + LibraryName + " : " + str(Library) + ' ' + str(type(Library)))
        return LibraryList

    ## Expand * in build option key
    #
    #   @param  Options     Options to be expanded
    #
    #   @retval options     Options expanded
    #
    def _ExpandBuildOption(self, Options):
        BuildOptions = {}
        for Key in Options:
            Family = Key[0]
            Target, Tag, Arch, Tool, Attr = Key[1].split("_")
            # if no tool defined for the option, skip it
            if Tool not in self.ToolPath:
                continue
            # if tool chain family doesn't match, skip it
            if Family != None and Family != "" and Family != self.ToolChainFamily[Tool]:
                continue
            # expand any wildcard
            if Target == "*" or Target == self.BuildTarget:
                if Tag == "*" or Tag == self.ToolChain:
                    if Arch == "*" or Arch == self.Arch:
                        if Tool not in BuildOptions:
                            BuildOptions[Tool] = Options[Key]
                        else:
                            # append options for the same tool
                            BuildOptions[Tool] += " " + Options[Key]
        return BuildOptions

    ## Append build options in platform to a module
    #
    #   @param  Module  The module to which the build options will be appened
    #
    #   @retval options     The options appended with build options in platform
    #
    def ApplyBuildOption(self, Module):
        PlatformOptions = self.BuildOption
        ModuleOptions = self._ExpandBuildOption(Module.BuildOptions)
        if Module in self.Platform.Modules:
            PlatformModule = self.Platform.Modules[str(Module)]
            PlatformModuleOptions = self._ExpandBuildOption(PlatformModule.BuildOptions)
        else:
            PlatformModuleOptions = {}

        BuildOptions = {}
        # for those tools that have no option in module file, give it a empty string
        for Tool in self.Workspace.ToolPath:
            if Tool in self.ToolOption and Module.ModuleType != 'USER_DEFINED':
                BuildOptions[Tool] = self.ToolOption[Tool]
            else:
                BuildOptions[Tool] = ''
            if Tool in ModuleOptions:
                BuildOptions[Tool] += " " + ModuleOptions[Tool]
            if Tool in PlatformOptions:
                BuildOptions[Tool] += " " + PlatformOptions[Tool]
            if Tool in PlatformModuleOptions:
                BuildOptions[Tool] += " " + PlatformModuleOptions[Tool]
        return BuildOptions

    Platform            = property(_GetPlatform)
    Name                = property(_GetName)
    Guid                = property(_GetGuid)
    Version             = property(_GetVersion)

    OutputDir           = property(_GetOutputDir)
    BuildDir            = property(_GetBuildDir)
    MakeFileDir         = property(_GetMakeFileDir)
    FdfFile             = property(_GetFdfFile)

    PcdTokenNumber      = property(_GetPcdTokenNumbers)    # (TokenCName, TokenSpaceGuidCName) : GeneratedTokenNumber
    DynamicPcdList      = property(_GetDynamicPcdList)    # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]
    NonDynamicPcdList   = property(_GetNonDynamicPcdList)    # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]
    PackageList         = property(_GetPackageList)

    ToolPath            = property(_GetToolPaths)    # toolcode : tool path
    ToolDllPath         = property(_GetToolDllPaths)    # toolcode : lib path
    ToolStaticLib       = property(_GetToolStaticLibs)    # toolcode : lib path
    ToolChainFamily     = property(_GetToolChainFamilies)    # toolcode : tool chain family
    BuildOption         = property(_GetBuildOptions)    # toolcode : option
    OutputFlag          = property(_GetOuputFlags)    # toolcode : output flag
    IncludeFlag         = property(_GetIncludeFlags)    # toolcode : include flag
    ToolOption          = property(_GetToolOptions)    # toolcode : tool option string

    BuildCommand        = property(_GetBuildCommand)
    BuildRule           = property(_GetBuildRule)
    ModuleAutoGenList   = property(_GetModuleAutoGenList)
    LibraryAutoGenList  = property(_GetLibraryAutoGenList)

## ModuleAutoGen class
#
# This class encapsules the AutoGen behaviors for the build tools. In addition to
# the generation of AutoGen.h and AutoGen.c, it will generate *.depex file according
# to the [depex] section in module's inf file.
#
class ModuleAutoGen(AutoGen):
    ## The real constructor of ModuleAutoGen
    #
    #  This method is not supposed to be called by users of ModuleAutoGen. It's
    #  only used by factory method __new__() to do real initialization work for an
    #  object of ModuleAutoGen
    #
    #   @param      Workspace           EdkIIWorkspaceBuild object
    #   @param      ModuleFile          The path of module file
    #   @param      Target              Build target (DEBUG, RELEASE)
    #   @param      Toolchain           Name of tool chain
    #   @param      Arch                The arch the module supports
    #   @param      PlatformFile        Platform meta-file
    #
    def _Init(self, Workspace, ModuleFile, Target, Toolchain, Arch, PlatformFile):
        EdkLogger.verbose("\nAutoGen module [%s] [%s]" % (ModuleFile, Arch))
        GlobalData.gProcessingFile = "%s [%s, %s, %s]" % (ModuleFile, Arch, Toolchain, Target)

        self.Workspace = Workspace
        self.WorkspaceDir = Workspace.WorkspaceDir

        self._MetaFile = str(ModuleFile)
        self.PlatformInfo = PlatformAutoGen(Workspace, PlatformFile, Target, Toolchain, Arch)
        # check if this module is employed by active platform
        if not self.PlatformInfo.ValidModule(self._MetaFile):
            EdkLogger.verbose("Module [%s] for [%s] is not employed by active platform\n" \
                              % (self._MetaFile, Arch))
            return False

        self.SourceDir = path.dirname(self._MetaFile)
        self.SourceOverrideDir = None
        # use overrided path defined in DSC file
        if self._MetaFile.upper() in GlobalData.gOverrideDir:
            self.SourceOverrideDir = GlobalData.gOverrideDir[self._MetaFile.upper()]

        self.FileBase, self.FileExt = path.splitext(path.basename(self._MetaFile))

        self.ToolChain = Toolchain
        self.ToolChainFamily = "MSFT"
        self.BuildTarget = Target
        self.Arch = Arch

        self.IsMakeFileCreated = False
        self.IsCodeFileCreated = False

        self.BuildDatabase = self.Workspace.BuildDatabase

        self._Module          = None
        self._Name            = None
        self._Guid            = None
        self._Version         = None
        self._ModuleType      = None
        self._ComponentType   = None
        self._PcdIsDriver     = None
        self._AutoGenVersion  = None
        self._LibraryFlag     = None
        self._CustomMakefile  = None
        self._Macro           = None

        self._BuildDir        = None
        self._OutputDir       = None
        self._DebugDir        = None
        self._MakeFileDir     = None

        self._IncludePathList = None
        self._AutoGenFileList = None
        self._UnicodeFileList = None
        self._SourceFileList  = None
        self._ObjectFileList  = None
        self._BinaryFileDict  = None

        self._DependentPackageList    = None
        self._DependentLibraryList    = None
        self._LibraryAutoGenList      = None
        self._DerivedPackageList      = None
        self._PcdList                 = None
        self._GuidList                = None
        self._ProtocolList            = None
        self._PpiList                 = None
        self._DepexList               = None
        self._BuildOption             = None

        return True


    ## Return the module build data object
    def _GetModule(self):
        if self._Module == None:
            self._Module = self.Workspace.BuildDatabase[self._MetaFile, self.Arch]
        return self._Module

    ## Return the module name
    def _GetBaseName(self):
        return self.Module.BaseName

    ## Return the module SourceOverridePath
    def _GetSourceOverridePath(self):
        return self.Module.SourceOverridePath

    ## Return the module meta-file GUID
    def _GetGuid(self):
        return self.Module.Guid

    ## Return the module version
    def _GetVersion(self):
        return self.Module.Version

    ## Return the module type
    def _GetModuleType(self):
        return self.Module.ModuleType

    ## Return the component type (for R8.x style of module)
    def _GetComponentType(self):
        return self.Module.ComponentType

    ## Return the build type
    def _GetBuildType(self):
        return self.Module.BuildType

    ## Return the PCD_IS_DRIVER setting
    def _GetPcdIsDriver(self):
        return self.Module.PcdIsDriver

    ## Return the autogen version, i.e. module meta-file version
    def _GetAutoGenVersion(self):
        return self.Module.AutoGenVersion

    ## Check if the module is library or not
    def _IsLibrary(self):
        if self._LibraryFlag == None:
            if self.Module.LibraryClass != None and self.Module.LibraryClass != []:
                self._LibraryFlag = True
            else:
                self._LibraryFlag = False
        return self._LibraryFlag

    ## Return the directory to store intermediate files of the module
    def _GetBuildDir(self):
        if self._BuildDir == None:
            self._BuildDir = path.join(
                                    self.PlatformInfo.BuildDir,
                                    self.Arch,
                                    self.SourceDir,
                                    self.FileBase
                                    )
        return self._BuildDir

    ## Return the directory to store the intermediate object files of the mdoule
    def _GetOutputDir(self):
        if self._OutputDir == None:
            self._OutputDir = path.join(self.BuildDir, "OUTPUT")
        return self._OutputDir

    ## Return the directory to store auto-gened source files of the mdoule
    def _GetDebugDir(self):
        if self._DebugDir == None:
            self._DebugDir = path.join(self.BuildDir, "DEBUG")
        return self._DebugDir

    ## Return the path of custom file
    def _GetCustomMakefile(self):
        if self._CustomMakefile == None:
            self._CustomMakefile = {}
            for Type in self.Module.CustomMakefile:
                if Type in gMakeTypeMap:
                    MakeType = gMakeTypeMap[Type]
                else:
                    MakeType = 'nmake'
                if self.SourceOverrideDir != None:
                    File = os.path.join(self.SourceOverrideDir, self.Module.CustomMakefile[Type])
                    if not os.path.exists(File):
                        File = os.path.join(self.SourceDir, self.Module.CustomMakefile[Type])
                else:
                    File = os.path.join(self.SourceDir, self.Module.CustomMakefile[Type])
                self._CustomMakefile[MakeType] = File
        return self._CustomMakefile

    ## Return the directory of the makefile
    #
    #   @retval     string  The directory string of module's makefile
    #
    def _GetMakeFileDir(self):
        return self.BuildDir

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def _GetBuildCommand(self):
        return self.PlatformInfo.BuildCommand

    ## Get object list of all packages the module and its dependent libraries belong to
    #
    #   @retval     list    The list of package object
    #
    def _GetDerivedPackageList(self):
        PackageList = []
        for M in [self.Module] + self.DependentLibraryList:
            for Package in M.Packages:
                if Package in PackageList:
                    continue
                PackageList.append(Package)
        return PackageList

    ## Merge dependency expression
    #
    #   @retval     list    The token list of the dependency expression after parsed
    #
    def _GetDepexTokenList(self):
        if self._DepexList == None:
            if self.IsLibrary:
                self._DepexList = []
                return self._DepexList
            else:
                self._DepexList = self.Module.Depex
            EdkLogger.verbose("DEPEX (%s) = %s" % (self.Name, self._DepexList))
            if len(self._DepexList) == 0 or self._DepexList[0] not in ['BEFORE', 'AFTER']:
                #
                # Append depex from dependent libraries, if not "BEFORE", "AFTER" expresion
                #
                for Lib in self.DependentLibraryList:
                    if Lib.Depex != None and Lib.Depex != []:
                        if self._DepexList != []:
                            self._DepexList.append('AND')
                        self._DepexList.append('(')
                        self._DepexList.extend(Lib.Depex)
                        self._DepexList.append(')')
                        EdkLogger.verbose("DEPEX (+%s) = %s" % (Lib.BaseName, self._DepexList))

            for I in range(0, len(self._DepexList)):
                Token = self._DepexList[I]
                if Token.endswith(".inf"):  # module file name
                    ModuleFile = os.path.normpath(Token)
                    self._DepexList[I] = self.BuildDatabase[ModuleFile].Guid
        return self._DepexList

    ## Return the list of macro in module
    #
    #   @retval     list    The list of macro defined in module file
    #
    def _GetMacroList(self):
        return self.Module.Specification

    ## Tool option for the module build
    #
    #   @param      PlatformInfo    The object of PlatformBuildInfo
    #   @retval     dict            The dict containing valid options
    #
    def _GetModuleBuildOption(self):
        if self._BuildOption == None:
            self._BuildOption = self.PlatformInfo.ApplyBuildOption(self.Module)
        return self._BuildOption

    ## Return a list of files which can be built from source
    #
    #  What kind of files can be built is determined by build rules in
    #  $(WORKSPACE)/Conf/build_rule.txt and toolchain family.
    #
    def _GetSourceFileList(self):
        if self._SourceFileList != None:
            return self._SourceFileList

        self._SourceFileList = []
        self._UnicodeFileList = []
        # use toolchain family of CC as the primary toolchain family
        if "CC" not in self.PlatformInfo.ToolChainFamily:
            EdkLogger.error("build", AUTOGEN_ERROR, "Tool [CC] is not defined for %s [%s, %s]" \
                             % (self.ToolChain, self.BuildTarget, self.Arch),
                            ExtraData="[%s]" % self._MetaFile)
        ToolChainFamily = self.PlatformInfo.ToolChainFamily["CC"]
        BuildRule = self.PlatformInfo.BuildRule

        # Add source override path to include
        if self.SourceOverrideDir != '' and self.SourceOverrideDir != None:
            Status, FullPath = ValidFile2(GlobalData.gAllFiles,
                                          '',
                                          Ext=None,
                                          Workspace=GlobalData.gWorkspace,
                                          EfiSource=GlobalData.gEfiSource,
                                          EdkSource=GlobalData.gEdkSource,
                                          Dir=self.SourceDir,
                                          OverrideDir=self.SourceOverrideDir
                                         )
            if Status and FullPath not in self.IncludePathList:
                    self.IncludePathList.insert(0, FullPath)

        for F in self.Module.Sources:
            SourceFile = F.SourceFile
            # match tool chain
            if F.TagName != "" and F.TagName != self.ToolChain:
                EdkLogger.verbose("The toolchain [%s] for processing file [%s] is found, "
                                  "but [%s] is needed" % (F.TagName, F.SourceFile, self.ToolChain))
                continue
            # match tool chain family
            if F.ToolChainFamily != "" and F.ToolChainFamily != ToolChainFamily:
                EdkLogger.debug(EdkLogger.DEBUG_0, "The file [%s] must be built by tools of [%s], "
                                "but current toolchain family is [%s]" % (SourceFile, F.ToolChainFamily, ToolChainFamily))
                continue

            # add the file path into search path list for file including
            Dir = path.dirname(SourceFile)
            if Dir != "":
                Dir = path.join(self.WorkspaceDir, self.SourceDir, Dir)
                if Dir not in self.IncludePathList and self.AutoGenVersion >= 0x00010005:
                    self.IncludePathList.insert(0, Dir)

            # skip unknown file
            Base, Ext = path.splitext(SourceFile)

            # skip file which needs a tool having no matching toolchain family
            FileType, RuleObject = BuildRule[Ext, self.BuildType, self.Arch, ToolChainFamily]
            # unicode must be processed by AutoGen
            if FileType == "UNICODE-TEXT-FILE":
                Status, FullPath = ValidFile2(GlobalData.gAllFiles,
                                          SourceFile,
                                          Ext=None,
                                          Workspace=GlobalData.gWorkspace,
                                          EfiSource=GlobalData.gEfiSource,
                                          EdkSource=GlobalData.gEdkSource,
                                          Dir=self.SourceDir,
                                          OverrideDir=self.SourceOverrideDir
                                         )
                if Status:
                    self._UnicodeFileList.append(FullPath)

            # if there's dxs file, don't use content in [depex] section to generate .depex file
            if FileType == "DEPENDENCY-EXPRESSION-FILE":
                self._DepexList = []

            # no command, no build
            if RuleObject != None and len(RuleObject.CommandList) == 0:
                RuleObject = None
            if [SourceFile, FileType, RuleObject] not in self._SourceFileList:
                self._SourceFileList.append([SourceFile, FileType, RuleObject])

        return self._SourceFileList

    ## Return the list of unicode files
    def _GetUnicodeFileList(self):
        if self._UnicodeFileList == None:
            self._GetSourceFileList()
        return self._UnicodeFileList

    ## Return a list of files which can be built from binary
    #
    #  "Build" binary files are just to copy them to build directory.
    #
    #   @retval     list            The list of files which can be built later
    #
    def _GetBinaryFiles(self):
        if self._BinaryFileDict == None:
            self._BinaryFileDict = sdict()
            for F in self.Module.Binaries:
                if F.Target != '*' and F.Target != self.BuildTarget:
                    continue
                if F.FileType not in self._BinaryFileDict:
                    self._BinaryFileDict[F.FileType] = []
                self._BinaryFileDict[F.FileType].append(F.BinaryFile)
        return self._BinaryFileDict

    ## Get the list of package object the module depends on
    #
    #   @retval     list    The package object list
    #
    def _GetDependentPackageList(self):
        return self.Module.Packages

    ## Return the list of auto-generated code file
    #
    #   @retval     list        The list of auto-generated file
    #
    def _GetAutoGenFileList(self):
        if self._AutoGenFileList == None:
            self._AutoGenFileList = {}
            AutoGenC = TemplateString()
            AutoGenH = TemplateString()
            GenC.CreateCode(self, AutoGenC, AutoGenH)
            if str(AutoGenC) != "":
                self._AutoGenFileList[gAutoGenCodeFileName] = AutoGenC
            if str(AutoGenH) != "":
                self._AutoGenFileList[gAutoGenHeaderFileName] = AutoGenH
        return self._AutoGenFileList

    ## Return the list of library modules explicitly or implicityly used by this module
    def _GetLibraryList(self):
        if self._DependentLibraryList == None:
            # only merge library classes and PCD for non-library module
            if self.IsLibrary:
                self._DependentLibraryList = []
            else:
                if self.AutoGenVersion < 0x00010005:
                    self._DependentLibraryList = self.PlatformInfo.ResolveLibraryReference(self.Module)
                else:
                    self._DependentLibraryList = self.PlatformInfo.ApplyLibraryInstance(self.Module)
        return self._DependentLibraryList

    ## Get the list of PCD
    #
    #   @retval     list                    The list of PCD
    #
    def _GetPcdList(self):
        if self._PcdList == None:
            if not self.IsLibrary:
                # derive PCDs from libraries first
                for Library in self.DependentLibraryList:
                    for Key in Library.Pcds:
                        if Key in self.Module.Pcds:
                            continue
                        self.Module.Pcds[Key] = copy.copy(Library.Pcds[Key])
                # apply PCD settings from platform
            self._PcdList = self.PlatformInfo.ApplyPcdSetting(self.Module)
        return self._PcdList

    ## Get the GUID value mapping
    #
    #   @retval     dict    The mapping between GUID cname and its value
    #
    def _GetGuidList(self):
        if self._GuidList == None:
            self._GuidList = self.Module.Guids
            for Library in self.DependentLibraryList:
                self._GuidList.update(Library.Guids)
        return self._GuidList

    ## Get the protocol value mapping
    #
    #   @retval     dict    The mapping between protocol cname and its value
    #
    def _GetProtocolList(self):
        if self._ProtocolList == None:
            self._ProtocolList = self.Module.Protocols
            for Library in self.DependentLibraryList:
                self._ProtocolList.update(Library.Protocols)
        return self._ProtocolList

    ## Get the PPI value mapping
    #
    #   @retval     dict    The mapping between PPI cname and its value
    #
    def _GetPpiList(self):
        if self._PpiList == None:
            self._PpiList = self.Module.Ppis
            for Library in self.DependentLibraryList:
                self._PpiList.update(Library.Ppis)
        return self._PpiList

    ## Get the list of include search path
    #
    #   @retval     list                    The list path
    #
    def _GetIncludePathList(self):
        if self._IncludePathList == None:
            self._IncludePathList = []
            if self.AutoGenVersion < 0x00010005:
                for Inc in self.Module.Includes:
                    # '.' means "relative to module directory".
                    if Inc == '':
                        Inc = path.join(self.WorkspaceDir, Inc)
                    elif Inc[0] == ".":
                        Inc = path.join(self.WorkspaceDir, self.SourceDir, Inc)
                    else:
                        Inc = path.join(self.WorkspaceDir, Inc)
                    if not os.path.exists(Inc) or Inc in self._IncludePathList:
                        continue
                    self._IncludePathList.append(Inc)
                    # for r8 modules
                    Inc = path.join(Inc, self.Arch.capitalize())
                    if not os.path.exists(Inc) or Inc in self._IncludePathList:
                        continue 
                    self._IncludePathList.append(Inc)
                # r8 module needs to put DEBUG_DIR at the end of search path and not to use SOURCE_DIR all the time
                self._IncludePathList.append(self.DebugDir)
            else:
                self._IncludePathList.append(os.path.join(self.WorkspaceDir, self.SourceDir))
                self._IncludePathList.append(self.DebugDir)

            for Package in self.Module.Packages:
                PackageDir = path.join(self.WorkspaceDir, path.dirname(str(Package)))
                if PackageDir not in self._IncludePathList:
                    self._IncludePathList.append(PackageDir)
                for Inc in Package.Includes:
                    Inc = path.join(PackageDir, Inc)
                    if Inc not in self._IncludePathList:
                        self._IncludePathList.append(Inc)
        return self._IncludePathList

    ## Create makefile for the module and its dependent libraries
    #
    #   @param      CreateLibraryMakeFile   Flag indicating if or not the makefiles of
    #                                       dependent libraries will be created
    #
    def CreateMakeFile(self, CreateLibraryMakeFile=True):
        if self.IsMakeFileCreated:
            return

        PlatformInfo = self.PlatformInfo
        if not self.IsLibrary and CreateLibraryMakeFile:
            for LibraryAutoGen in self.LibraryAutoGenList:
                LibraryAutoGen.CreateMakeFile()

        if len(self.CustomMakefile) == 0:
            Makefile = GenMake.ModuleMakefile(self)
        else:
            Makefile = GenMake.CustomMakefile(self)
        if Makefile.Generate():
            EdkLogger.verbose("Generated makefile for module %s [%s]" %
                           (self.Name, self.Arch))
        else:
            EdkLogger.verbose("Skipped the generation of makefile for module %s [%s]" %
                              (self.Name, self.Arch))

        self.IsMakeFileCreated = True

    ## Create autogen code for the module and its dependent libraries
    #
    #   @param      CreateLibraryCodeFile   Flag indicating if or not the code of
    #                                       dependent libraries will be created
    #
    def CreateCodeFile(self, CreateLibraryCodeFile=True):
        if self.IsCodeFileCreated:
            return

        PlatformInfo = self.PlatformInfo
        if not self.IsLibrary and CreateLibraryCodeFile:
            for LibraryAutoGen in self.LibraryAutoGenList:
                LibraryAutoGen.CreateCodeFile()

        AutoGenList = []
        IgoredAutoGenList = []

        for File in self.AutoGenFileList:
            if GenC.Generate(path.join(self.DebugDir, File), str(self.AutoGenFileList[File])):
                #Ignore R8 AutoGen.c
                if self.AutoGenVersion < 0x00010005 and File.find('AutoGen.c') > -1:
                        continue

                AutoGenList.append(File)
            else:
                IgoredAutoGenList.append(File)

        if self.DepexList != []:
            Dpx = GenDepex.DependencyExpression(self.DepexList, self.ModuleType, True)
            DpxFile = gAutoGenDepexFileName % {"module_name" : self.Name}

            if Dpx.Generate(path.join(self.OutputDir, DpxFile)):
                AutoGenList.append(DpxFile)
            else:
                IgoredAutoGenList.append(DpxFile)

        if IgoredAutoGenList == []:
            EdkLogger.verbose("Generated [%s] files for module %s [%s]" %
                           (" ".join(AutoGenList), self.Name, self.Arch))
        elif AutoGenList == []:
            EdkLogger.verbose("Skipped the generation of [%s] files for module %s [%s]" %
                           (" ".join(IgoredAutoGenList), self.Name, self.Arch))
        else:
            EdkLogger.verbose("Generated [%s] (skipped %s) files for module %s [%s]" %
                           (" ".join(AutoGenList), " ".join(IgoredAutoGenList), self.Name, self.Arch))

        self.IsCodeFileCreated = True
        return AutoGenList

    ## Summarize the ModuleAutoGen objects of all libraries used by this module
    def _GetLibraryAutoGenList(self):
        if self._LibraryAutoGenList == None:
            self._LibraryAutoGenList = []
            for Library in self.DependentLibraryList:
                La = ModuleAutoGen(
                        self.Workspace,
                        str(Library),
                        self.BuildTarget,
                        self.ToolChain,
                        self.Arch,
                        str(self.PlatformInfo)
                        )
                if La not in self._LibraryAutoGenList:
                    self._LibraryAutoGenList.append(La)
        return self._LibraryAutoGenList

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def _GetBuildCommand(self):
        return self.PlatformInfo.BuildCommand


    Module          = property(_GetModule)
    Name            = property(_GetBaseName)
    Guid            = property(_GetGuid)
    Version         = property(_GetVersion)
    ModuleType      = property(_GetModuleType)
    ComponentType   = property(_GetComponentType)
    BuildType       = property(_GetBuildType)
    PcdIsDriver     = property(_GetPcdIsDriver)
    AutoGenVersion  = property(_GetAutoGenVersion)
    Macro           = property(_GetMacroList)

    IsLibrary       = property(_IsLibrary)

    BuildDir        = property(_GetBuildDir)
    OutputDir       = property(_GetOutputDir)
    DebugDir        = property(_GetDebugDir)
    MakeFileDir     = property(_GetMakeFileDir)
    CustomMakefile  = property(_GetCustomMakefile)

    IncludePathList = property(_GetIncludePathList)
    AutoGenFileList = property(_GetAutoGenFileList)
    UnicodeFileList = property(_GetUnicodeFileList)
    SourceFileList  = property(_GetSourceFileList)
    BinaryFileDict  = property(_GetBinaryFiles) # FileType : [File List]

    DependentPackageList    = property(_GetDependentPackageList)
    DependentLibraryList    = property(_GetLibraryList)
    LibraryAutoGenList      = property(_GetLibraryAutoGenList)
    DerivedPackageList      = property(_GetDerivedPackageList)

    PcdList                 = property(_GetPcdList)
    GuidList                = property(_GetGuidList)
    ProtocolList            = property(_GetProtocolList)
    PpiList                 = property(_GetPpiList)
    DepexList               = property(_GetDepexTokenList)
    BuildOption             = property(_GetModuleBuildOption)
    BuildCommand            = property(_GetBuildCommand)

# This acts like the main() function for the script, unless it is 'import'ed into another script.
if __name__ == '__main__':
    pass

