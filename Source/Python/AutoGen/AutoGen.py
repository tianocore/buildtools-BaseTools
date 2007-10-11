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
from optparse import OptionParser
from optparse import make_option

import Common.EdkLogger
import GenC
import GenMake
import GenDepex

from BuildInfo import *
from StrGather import *
from BuildEngine import *

from Common.BuildToolError import *
from Common.EdkIIWorkspaceBuild import *
from Common.EdkIIWorkspace import *
from Common.DataType import *
from Common.Misc import *
from Common.String import *

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

## AutoGen class for platform
#
#  PlatformAutoGen class will re-organize the original information in platform
#  file in order to generate makefile for platform.
#
class PlatformAutoGen:
    # database to maintain the objects of PlatformAutoGen
    _Database = {}    # (platform file, BuildTarget, ToolChain) : PlatformAutoGen object

    ## The real constructor of PlatformAutoGen
    #
    #  This method is not supposed to be called by users of PlatformAutoGen. It's
    #  only used by factory method New() to do real initialization work for an
    #  object of PlatformAutoGen
    #
    #   @param      Workspace       EdkIIWorkspaceBuild object
    #   @param      PlatformFile    Platform file (DSC file)
    #   @param      Target          Build target (DEBUG, RELEASE)
    #   @param      Toolchain       Name of tool chain
    #   @param      ArchList        List of arch the platform supports
    #
    def _Init(self, Workspace, PlatformFile, Target, Toolchain, ArchList):
        self.PlatformFile = str(PlatformFile)
        self.Workspace = Workspace
        self.WorkspaceDir = Workspace.WorkspaceDir
        self.ToolChain = Toolchain
        self.BuildTarget = Target
        self.ArchList = ArchList

        EdkLogger.verbose("\nAutoGen platform [%s] [%s]" % (self.PlatformFile, " ".join(self.ArchList)))

        # get the original module/package/platform objects
        self.ModuleDatabase = {}
        for a in Workspace.Build:
            self.ModuleDatabase[a] = Workspace.Build[a].ModuleDatabase

        self.PackageDatabase = {}
        for a in Workspace.Build:
            self.PackageDatabase[a] = Workspace.Build[a].PackageDatabase

        self.PlatformDatabase = {}
        for a in Workspace.Build:
            self.PlatformDatabase[a] = Workspace.Build[a].PlatformDatabase

        # flag indicating if the makefile/C-code file has been created or not
        self.IsMakeFileCreated = False
        self.IsCodeFileCreated = False

        #
        # collect build information for the platform
        #
        self.BuildInfo = {}     # arch : PlatformBuildInfo Object
        self.Platform = {}

        for Arch in self.ArchList:
            if Arch not in self.PlatformDatabase or self.PlatformFile not in self.PlatformDatabase[Arch]:
                EdkLogger.error("AutoGen", AUTOGEN_ERROR,
                                "[%s] is not the active platform, or [%s] is not supported by the active platform!"
                                % (PlatformFile, Arch))
            Platform = self.PlatformDatabase[Arch][PlatformFile]
            self.Platform[Arch] = Platform
            self.BuildInfo[Arch] = self.CollectBuildInfo(Platform, Arch)

    ## hash() operator
    #
    #  The file path of platform file will be used to represent hash value of this object
    #
    #   @retval int     Hash value of the file path of platform file
    #
    def __hash__(self):
        return hash(self.PlatformFile)

    ## str() operator
    #
    #  The file path of platform file will be used to represent this object
    #
    #   @retval string  String of platform file path
    #
    def __str__(self):
        return self.PlatformFile

    ## Factory method to create a PlatformAutoGen object
    #
    #   This method will check if an object of PlatformAutoGen has been created
    #   for given platform. And if true, just return it. Otherwise it will create
    #   a new PlatformAutoGen. That means there will be only one PlatformAutoGen
    #   object for the same platform.
    #
    #   @param      Workspace           EdkIIWorkspaceBuild object
    #   @param      Platform            Platform file (DSC file)
    #   @param      Target              Build target (DEBUG, RELEASE)
    #   @param      Toolchain           Name of tool chain
    #   @param      ArchList            List of arch the platform supports
    #   @param      ModuleAutoGenFlag   Flag indicating if creating ModuleAutoGen
    #                                   objects for mdoules in the platform or not
    #
    #   @retval     PlatformAutoGen object
    #
    @staticmethod
    def New(Workspace, Platform, Target, Toolchain, ArchList, ModuleAutoGenFlag=False):
        # check if the object for the platform has been created
        Key = (Platform, Target, Toolchain)
        if Key not in PlatformAutoGen._Database:
            if ArchList == None or ArchList == []:
                return None
            AutoGenObject = PlatformAutoGen()
            AutoGenObject._Init(Workspace, Platform, Target, Toolchain, ArchList)
            PlatformAutoGen._Database[Key] = AutoGenObject
        else:
            AutoGenObject = PlatformAutoGen._Database[Key]

        # create ModuleAutoGen objects for modules in the platform
        if ModuleAutoGenFlag:
            AutoGenObject.CreateModuleAutoGen()

        return AutoGenObject

    ## Collect build information for the platform
    #
    #  Collect build information, such as FDF file path, dynamic pcd list,
    #  package list, tool chain configuration, build rules, etc.
    #
    #   @param      Platform            Platform file (DSC file)
    #   @param      Arch                One of arch the platform supports
    #
    #   @retval     PlatformBuildInfo object
    #
    def CollectBuildInfo(self, Platform, Arch):
        Info = PlatformBuildInfo(Platform)

        Info.Arch = Arch
        Info.ToolChain = self.ToolChain
        Info.BuildTarget = self.BuildTarget

        Info.WorkspaceDir = self.WorkspaceDir
        Info.SourceDir = path.dirname(Platform.DescFilePath)
        Info.OutputDir = Platform.OutputDirectory
        Info.BuildDir = path.join(Info.OutputDir, self.BuildTarget + "_" + self.ToolChain)
        Info.MakeFileDir = Info.BuildDir

        if self.Workspace.Fdf != "":
            Info.FdfFile= path.join(self.WorkspaceDir, self.Workspace.Fdf)

        Info.DynamicPcdList = self.GetDynamicPcdList(Platform, Arch)
        Info.PcdTokenNumber = self.GeneratePcdTokenNumber(Platform, Info.DynamicPcdList)
        Info.PackageList = self.PackageDatabase[Arch].values()

        self.GetToolDefinition(Info)
        Info.BuildRule = self.GetBuildRule()
        Info.FdTargetList = self.Workspace.FdTargetList
        Info.FvTargetList = self.Workspace.FvTargetList

        return Info

    ## Return directory of platform makefile
    #
    #   @retval     string  Makefile directory
    #
    def GetMakeFileDir(self):
        return os.path.join(self.WorkspaceDir, self.BuildInfo[self.ArchList[0]].MakeFileDir)

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def GetBuildCommand(self, Arch=None):
        if Arch != None:
            Arch = [Arch]
        else:
            Arch = self.ArchList
        CommandString = ""
        for A in Arch:
            if A in self.BuildInfo and "MAKE" in self.BuildInfo[A].ToolPath:
                CommandString = self.BuildInfo[A].ToolPath["MAKE"]
                if "MAKE" in self.BuildInfo[A].ToolOption:
                    CommandString = CommandString + " " + self.BuildInfo[A].ToolOption["MAKE"]
                break
        if CommandString == "":
            EdkLogger.error("AutoGen", OPTION_MISSING, "No MAKE command defined. Please check your tools_def.txt!")
        return CommandString

    ## Parse build_rule.txt in $(WORKSPACE)/Conf/build_rule.txt
    #
    #   @retval     BuildRule object
    #
    def GetBuildRule(self):
        return BuildRule(self.Workspace.WorkspaceFile(gBuildRuleFile))

    ## Get tool chain definition
    #
    #  Get each tool defition for given tool chain from tools_def.txt and platform
    #
    #   @param      Info    PlatformBuildInfo object to store the definition
    #
    def GetToolDefinition(self, Info):
        ToolDefinition = self.Workspace.ToolDef.ToolsDefTxtDictionary
        ToolCodeList = self.Workspace.ToolDef.ToolsDefTxtDatabase["COMMAND_TYPE"]
        for Tool in ToolCodeList:
            KeyBaseString = "%s_%s_%s_%s" % (Info.BuildTarget, Info.ToolChain, Info.Arch, Tool)

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

            InputFlag = gIncludeFlag[Family]

            Info.ToolPath[Tool] = Path
            Info.ToolDllPath[Tool] = Dll
            Info.ToolChainFamily[Tool] = Family
            Info.ToolOption[Tool] = Option
            Info.OutputFlag[Tool] = OutputFlag
            Info.IncludeFlag[Tool] = InputFlag

        # get tool options from platform
        BuildOptions = Info.Platform.BuildOptions
        for Key in BuildOptions:
            Family = Key[0]
            Target, Tag, Arch, Tool, Attr = Key[1].split("_")
            if Tool not in Info.ToolPath:
                continue
            if Family != None and Family != "" and Family != Info.ToolChainFamily[Tool]:
                continue
            if Target == "*" or Target == Info.BuildTarget:
                if Tag == "*" or Tag == Info.ToolChain:
                    if Arch == "*" or Arch == Info.Arch:
                        Info.BuildOption[Tool] = BuildOptions[Key]
        for Tool in Info.ToolOption:
            if Tool not in Info.BuildOption:
                Info.BuildOption[Tool] = ""

    ## Collect dynamic PCDs
    #
    #  Gather dynamic PCDs list from each module and their settings from platform
    #
    #   @param      Platform    The object of the platform
    #   @param      Arch        One of the arch the platform supports
    #
    #   @retval     lsit        The list of dynamic PCD
    #
    def GetDynamicPcdList(self, Platform, Arch):
        PcdList = []

        # for gathering error information
        NotFoundPcdList = set()
        NoDatumTypePcdList = set()
        PcdConsumerList = set()

        for F in Platform.Modules:
            M = self.ModuleDatabase[Arch][F]
            for Key in M.Pcds:
                PcdFromModule = M.Pcds[Key]
                # check if the setting of the PCD is found in platform
                if not PcdFromModule.IsOverrided:
                    NotFoundPcdList.add(" | ".join(Key))
                    PcdConsumerList.add(str(M))
                    continue

                if Key not in Platform.Pcds:
                    PcdFromPlatform = PcdFromModule
                else:
                    PcdFromPlatform = Platform.Pcds[Key]

                # make sure that the "VOID*" kind of datum has MaxDatumSize set
                if PcdFromModule.DatumType == "VOID*" and PcdFromPlatform.MaxDatumSize == None:
                    NoDatumTypePcdList.add(" | ".join(Key))
                    PcdConsumerList.add(str(M))

                if PcdFromPlatform.Type in GenC.gDynamicPcd + GenC.gDynamicExPcd:
                    # for autogen code purpose
                    if M.ModuleType in ["PEIM", "PEI_CORE"]:
                        PcdFromPlatform.Phase = "PEI"
                    if PcdFromPlatform not in PcdList:
                        PcdFromPlatform.TokenValue = PcdFromModule.TokenValue
                        PcdFromPlatform.DatumType = PcdFromModule.DatumType
                        PcdList.append(PcdFromPlatform)

        # print out error information and break the build, if error found
        if len(NotFoundPcdList) > 0 or len(NoDatumTypePcdList) > 0:
            NotFoundPcdListString = "\n\t\t".join(NotFoundPcdList)
            NoDatumTypePcdListString = "\n\t\t".join(NoDatumTypePcdList)
            ModuleListString = "\n\t\t".join(PcdConsumerList)
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "PCD setting error",
                            ExtraData="\n\tPCD(s) not found in platform:\n\t\t%s"
                                      "\n\tPCD(s) without MaxDatumSize:\n\t\t%s"
                                      "\n\tUsed by:\n\t\t%s\n"
                                      % (NotFoundPcdListString, NoDatumTypePcdListString, ModuleListString))
        return PcdList

    ## Generate Token Number for all PCD
    #
    #   @param      Platform        The object of the platform
    #   @param      DynamicPcdList  The list of all dynamic PCDs
    #
    #   @retval     dict            A dict object containing the PCD and its token number
    #
    def GeneratePcdTokenNumber(self, Platform, DynamicPcdList):
        PcdTokenNumber = sdict()
        TokenNumber = 1
        for Pcd in DynamicPcdList:
            if Pcd.Phase == "PEI":
                EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Pcd.Phase, TokenNumber))
                PcdTokenNumber[Pcd.TokenCName, Pcd.TokenSpaceGuidCName] = TokenNumber
                TokenNumber += 1

        for Pcd in DynamicPcdList:
            if Pcd.Phase == "DXE":
                EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (Pcd.TokenCName, Pcd.TokenSpaceGuidCName, Pcd.Phase, TokenNumber))
                PcdTokenNumber[Pcd.TokenCName, Pcd.TokenSpaceGuidCName] = TokenNumber
                TokenNumber += 1

        PlatformPcds = Platform.Pcds
        for Key in PlatformPcds:
            Pcd = PlatformPcds[Key]
            if Key not in PcdTokenNumber:
                PcdTokenNumber[Key] = TokenNumber
                TokenNumber += 1
        return PcdTokenNumber

    ## Create autogen object for each module in platform
    #
    def CreateModuleAutoGen(self):
        for Arch in self.BuildInfo:
            Info = self.BuildInfo[Arch]
            for ModuleFile in Info.Platform.Libraries:
                ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                         Info.BuildTarget, Info.ToolChain, Info.Arch)

            for ModuleFile in Info.Platform.Modules:
                ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                         Info.BuildTarget, Info.ToolChain, Info.Arch)

    ## Create makefile for the platform and mdoules in it
    #
    #   @param      CreateLibraryCodeFile   Flag indicating if the makefile for
    #                                       modules will be created as well
    #
    def CreateMakeFile(self, CreateModuleMakeFile=False):
        if CreateModuleMakeFile:
            for Arch in self.BuildInfo:
                Info = self.BuildInfo[Arch]
                for ModuleFile in Info.Platform.Libraries:
                    AutoGenObject = ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                                      Info.BuildTarget, Info.ToolChain, Info.Arch)
                    AutoGenObject.CreateMakeFile(False)

                for ModuleFile in Info.Platform.Modules:
                    AutoGenObject = ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                                      Info.BuildTarget, Info.ToolChain, Info.Arch)
                    AutoGenObject.CreateMakeFile(False)

        # no need to create makefile for the platform more than once
        if self.IsMakeFileCreated:
            return

        # create makefile for platform
        Makefile = GenMake.Makefile(self.BuildInfo)
        if Makefile.Generate():
            EdkLogger.verbose("Generated makefile for platform [%s] [%s]\n" %
                           (self.PlatformFile, " ".join(self.ArchList)))
        else:
            EdkLogger.verbose("Skipped the generation of makefile for platform [%s] [%s]\n" %
                           (self.PlatformFile, " ".join(self.ArchList)))
        self.IsMakeFileCreated = True

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

        for Arch in self.BuildInfo:
            Info = self.BuildInfo[Arch]
            for ModuleFile in Info.Platform.Libraries:
                AutoGenObject = ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                                  Info.BuildTarget, Info.ToolChain, Info.Arch)
                AutoGenObject.CreateCodeFile()

            for ModuleFile in Info.Platform.Modules:
                AutoGenObject = ModuleAutoGen.New(self.Workspace, Info.Platform, ModuleFile,
                                                  Info.BuildTarget, Info.ToolChain, Info.Arch)
                AutoGenObject.CreateCodeFile()
        # don't do this twice
        self.IsCodeFileCreated = True

    ## Test if a module is supported by the platform
    #
    #  An error will be raised directly if the module or its arch is not supported
    #  by the platform or current configuration
    #
    #   @param      Module  The module file
    #   @param      Arch    The arch the module will be built for
    #
    def CheckModule(self, Module, Arch):
        if Arch not in self.Workspace.SupArchList:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "[%s] is not supported by active platform [%s] [%s]!"
                                                      % (Arch, self.PlatformFile, self.Workspace.SupArchList))
        if Arch not in self.ArchList:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "[%s] is not supported by current build configuration!" % Arch)
        if str(Module) not in self.ModuleDatabase[Arch]:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "[%s] [%s] is not supported by active platform [%s]!"
                                                      % (Module, Arch, self.PlatformFile))

    ## Find the package containing the module
    #
    # Find out the package which contains the given module, according to the path
    # of the module and the package.
    #
    # @param  Module            The module to be found for
    #
    # @retval package           Package object if found
    # @retval None              None if not found
    #
    def GetModuleOwnerPackage(self, Module):
        for Arch in self.PackageDatabase:
            Pdb = self.PackageDatabase[Arch]
            for PackagePath in Pdb:
                PackageDir = path.dirname(PackagePath)
                #
                # if package's path is the first part of module's path, bingo!
                #
                if str(Module).find(PackageDir) == 0:
                    return Pdb[PackagePath]
        # nothing found
        return None

    ## Get platform object
    #
    #   @param      PlatformFile    The file path of the platform
    #   @param      Arch            One of the arch the platform supports
    #
    #   @retval     object          The object of the platform
    #
    def GetPlatformObject(self, PlatformFile, Arch):
        if Arch not in self.PlatformDatabase or PlatformFile not in self.PlatformDatabase[Arch]:
            return None
        return self.PlatformDatabase[Arch][PlatformFile]

    ## Get package object
    #
    #   @param      PackageFile     The file path of the package
    #   @param      Arch            One of the arch the package supports
    #
    #   @retval     object          The object of the package
    #
    def GetPackageObject(self, PackageFile, Arch):
        if Arch not in self.PackageDatabase or PackageFile not in self.PackageDatabase[Arch]:
            return None
        return self.PackageDatabase[Arch][PackageFile]

    ## Get module object
    #
    #   @param      ModuleFile      The file path of the module
    #   @param      Arch            One of the arch the module supports
    #
    #   @retval     object          The object of the module
    #
    def GetModuleObject(self, ModuleFile, Arch):
        if Arch not in self.ModuleDatabase or ModuleFile not in self.ModuleDatabase[Arch]:
            return None
        return self.ModuleDatabase[Arch][ModuleFile]

    ## Add ModuleAutoGen object for a module in platform build information
    #
    #   @param      ModuleAutoGen   The ModuleAutoGen object for a module
    #   @param      Arch            The arch of the module
    #
    def AddModuleAutoGen(self, ModuleAutoGen, Arch):
        if ModuleAutoGen not in self.BuildInfo[Arch].ModuleAutoGenList:
            self.BuildInfo[Arch].ModuleAutoGenList.append(ModuleAutoGen)

    ## Add ModuleAutoGen object for a library in platform build information
    #
    #   @param      LibraryAutoGen  The ModuleAutoGen object for a library module
    #   @param      Arch            The arch of the library
    #
    def AddLibraryAutoGen(self, LibraryAutoGen, Arch):
        if LibraryAutoGen not in self.BuildInfo[Arch].LibraryAutoGenList:
            self.BuildInfo[Arch].LibraryAutoGenList.append(LibraryAutoGen)

## AutoGen class
#
# This class encapsules the AutoGen behaviors for the build tools. In addition to
# the generation of AutoGen.h and AutoGen.c, it can generate *.depex file according
# to the [depex] section in module's inf file. The result of parsing unicode file
# has been incorporated either.
#
class ModuleAutoGen(object):
    # The cache for the objects of ModuleAutoGen
    _Database = {}
    # The cache for the object of PlatformAutoGen
    _PlatformAutoGen = None

    ## The real constructor of ModuleAutoGen
    #
    #  This method is not supposed to be called by users of ModuleAutoGen. It's
    #  only used by factory method New() to do real initialization work for an
    #  object of ModuleAutoGen
    #
    #   @param      Workspace           EdkIIWorkspaceBuild object
    #   @param      PlatformAutoGenObj  Platform file (DSC file)
    #   @param      ModuleFile          The path of module file
    #   @param      Target              Build target (DEBUG, RELEASE)
    #   @param      Toolchain           Name of tool chain
    #   @param      Arch                The arch the module supports
    #
    def _Init(self, Workspace, PlatformAutoGenObj, ModuleFile, Target, Toolchain, Arch):
        self.ModuleFile = str(ModuleFile)
        self.PlatformFile = PlatformAutoGenObj.PlatformFile

        self.Workspace = Workspace
        self.WorkspaceDir = Workspace.WorkspaceDir

        self.ToolChain = Toolchain
        self.ToolChainFamily = "MSFT"
        self.BuildTarget = Target
        self.Arch = Arch

        self.IsMakeFileCreated = False
        self.IsCodeFileCreated = False

        self.PlatformAutoGen = PlatformAutoGenObj
        try:
            self.PlatformAutoGen.CheckModule(ModuleFile, self.Arch)
        except:
            return False

        #
        # autogen for module
        #
        EdkLogger.verbose("\nAutoGen module [%s] [%s]" % (ModuleFile, self.Arch))

        self.Platform = self.PlatformAutoGen.GetPlatformObject(self.PlatformFile, self.Arch)
        self.Module = self.PlatformAutoGen.GetModuleObject(self.ModuleFile, self.Arch)

        self.Package = self.PlatformAutoGen.GetModuleOwnerPackage(self.Module)

        self.AutoGenC = TemplateString()
        self.AutoGenH = TemplateString()

        self.BuildInfo = self.GetModuleBuildInfo()
        return True

    ## "==" operator
    #
    #  Use module file path and arch to do the comparison
    #
    #   @retval True    if the file path and arch are equal
    #   @retval False   if the file path or arch are different
    #
    def __eq__(self, Other):
        return Other != None and self.ModuleFile == Other.ModuleFile and self.Arch == Other.Arch

    ## hash() operator
    #
    #  The file path and arch of the module will be used to represent hash value of this object
    #
    #   @retval int     Hash value of the file path and arch name of the module
    #
    def __hash__(self):
        return hash(self.ModuleFile) + hash(self.Arch)

    ## String representation of this object
    #
    #   @retval     string  The string of file path and arch
    #
    def __str__(self):
        return "%s [%s]" % (self.ModuleFile, self.Arch)

    ## Factory method to create a ModuleAutoGen object
    #
    #   This method will check if an object of ModuleAutoGen has been created
    #   for given platform. And if true, just return it. Otherwise it will create
    #   a new ModuleAutoGen. That means there will be only one ModuleAutoGen
    #   object for the same platform.
    #
    #   @param      Workspace           EdkIIWorkspaceBuild object
    #   @param      Platform            Platform file (DSC file)
    #   @param      Module              Module file (INF file)
    #   @param      Target              Build target (DEBUG, RELEASE)
    #   @param      Toolchain           Name of tool chain
    #   @param      Arch                The arch of the module
    #
    #   @retval     ModuleAutoGen object
    #
    @staticmethod
    def New(Workspace, Platform, Module, Target, Toolchain, Arch):
        # creating module autogen needs platform's autogen
        if ModuleAutoGen._PlatformAutoGen == None:
            ModuleAutoGen._PlatformAutoGen = PlatformAutoGen.New(Workspace, Platform, Target, Toolchain, None)
            if ModuleAutoGen._PlatformAutoGen == None:
                EdkLogger.error("AutoGen", AUTOGEN_ERROR, "Please create platform AutoGen first!")

        # check if the autogen for the module has been created or not
        Key = (Module, Target, Toolchain, Arch)
        if Key not in ModuleAutoGen._Database:
            if Arch == None or Arch == "":
                return None
            AutoGenObject = ModuleAutoGen()
            if AutoGenObject._Init(Workspace, ModuleAutoGen._PlatformAutoGen, Module, Target, Toolchain, Arch) == False:
                return None
            ModuleAutoGen._Database[Key] = AutoGenObject

            # for new ModuleAutoGen object, put it in platform's AutoGen
            if AutoGenObject.BuildInfo.IsLibrary:
                ModuleAutoGen._PlatformAutoGen.AddLibraryAutoGen(AutoGenObject, Arch)
            else:
                ModuleAutoGen._PlatformAutoGen.AddModuleAutoGen(AutoGenObject, Arch)
            return AutoGenObject

        return ModuleAutoGen._Database[Key]

    ## Gather module build information
    #
    #   @retval     Info    The object of ModuleBuildInfo
    #
    def GetModuleBuildInfo(self):
        Info = ModuleBuildInfo(self.Module)
        self.BuildInfo = Info
        Info.PlatformInfo = self.PlatformAutoGen.BuildInfo[self.Arch]

        # basic information
        Info.WorkspaceDir = self.WorkspaceDir
        Info.BuildTarget = self.BuildTarget
        Info.ToolChain = self.ToolChain
        Info.Arch = self.Arch
        Info.IsBinary = False
        Info.BaseName = self.Module.BaseName
        Info.FileBase, Info.FileExt = path.splitext(path.basename(self.Module.DescFilePath))
        Info.SourceDir = path.dirname(self.Module.DescFilePath)
        Info.BuildDir = os.path.join(Info.PlatformInfo.BuildDir,
                                     Info.Arch,
                                     Info.SourceDir,
                                     Info.FileBase)
        Info.OutputDir = os.path.join(Info.BuildDir, "OUTPUT")
        Info.DebugDir = os.path.join(Info.BuildDir, "DEBUG")
        Info.MakeFileDir = Info.BuildDir
        if os.path.isabs(Info.BuildDir):
            CreateDirectory(Info.OutputDir)
            CreateDirectory(Info.DebugDir)
        else:
            CreateDirectory(os.path.join(self.WorkspaceDir, Info.OutputDir))
            CreateDirectory(os.path.join(self.WorkspaceDir, Info.DebugDir))

        for Type in self.Module.CustomMakefile:
            MakeType = gMakeTypeMap[Type]
            Info.CustomMakeFile[MakeType] = os.path.join(Info.SourceDir, self.Module.CustomMakefile[Type])

        if self.Module.LibraryClass != None and self.Module.LibraryClass != []:
            Info.IsLibrary = True
            Info.DependentLibraryList = []
        else:
            Info.IsLibrary = False
            Info.DependentLibraryList = self.GetSortedLibraryList()

        Info.DependentPackageList = self.GetDependentPackageList()
        Info.DerivedPackageList = self.GetDerivedPackageList()

        Info.BuildOption = self.GetModuleBuildOption(Info.PlatformInfo)
        if "DLINK" in Info.PlatformInfo.ToolStaticLib:
            Info.SystemLibraryList = Info.PlatformInfo.ToolStaticLib["DLINK"]

        Info.PcdIsDriver = self.Module.PcdIsDriver
        Info.PcdList = self.GetPcdList(Info.DependentLibraryList)
        Info.GuidList = self.GetGuidList()
        Info.ProtocolList = self.GetProtocolGuidList()
        Info.PpiList = self.GetPpiGuidList()
        Info.MacroList = self.GetMacroList()
        Info.DepexList = self.GetDepexTokenList(Info)

        Info.IncludePathList = [Info.SourceDir, Info.DebugDir]
        Info.IncludePathList.extend(self.GetIncludePathList(Info.DependentPackageList))

        Info.SourceFileList = self.GetBuildFileList(Info.PlatformInfo)
        Info.AutoGenFileList = self.GetAutoGenFileList(Info)

        return Info

    ## Return the directory of the makefile
    #
    #   @retval     string  The directory string of module's makefile
    #
    def GetMakeFileDir(self):
        return os.path.join(self.WorkspaceDir, self.BuildInfo.MakeFileDir)

    ## Return build command string
    #
    #   @retval     string  Build command string
    #
    def GetBuildCommand(self):
        return self.PlatformAutoGen.GetBuildCommand(self.Arch)

    ## Get object list of all packages the module and its dependent libraries belong to
    #
    #   @retval     list    The list of package object
    #
    def GetDerivedPackageList(self):
        PackageList = []
        for M in [self.Module] + self.BuildInfo.DependentLibraryList:
            for Package in M.Packages:
                if Package not in PackageList:
                    PackageList.append(self.PlatformAutoGen.GetPackageObject(Package, self.Arch))
        return PackageList

    ## Parse dependency expression
    #
    #   @param      Info    The object of ModuleBuildInfo
    #   @retval     list    The token list of the dependency expression after parsed
    #
    def GetDepexTokenList(self, Info):
        Dxs = self.Module.Depex
        if Dxs == None or Dxs == "":
            return []

        #
        # Append depex from dependent libraries
        #
        for Lib in Info.DependentLibraryList:
            if Lib.Depex != None and Lib.Depex != "":
                Dxs += " AND (" + Lib.Depex + ")"
                EdkLogger.verbose("DEPEX string (+%s) = %s" % (Lib.BaseName, Dxs))
        if Dxs == "":
            return []

        TokenList = gDepexTokenPattern.findall(Dxs)
        EdkLogger.debug(EdkLogger.DEBUG_8, "TokenList(raw) = %s" % (TokenList))
        for I in range(0, len(TokenList)):
            Token = TokenList[I].strip()
            if Token.endswith(".inf"):  # module file name
                ModuleFile = os.path.normpath(Token)
                Token = gModuleDatabase[ModuleFile].Guid
            elif Token.upper() in GenDepex.DependencyExpression.SupportedOpcode: # Opcode name
                Token = Token.upper()
            elif Token not in ['(', ')']:   # GUID C Name
                GuidCName = Token
                for P in Info.DerivedPackageList:
                    if GuidCName in P.Protocols:
                        Token = P.Protocols[GuidCName]
                        break
                    elif GuidCName in P.Ppis:
                        Token = P.Ppis[GuidCName]
                        break
                    elif GuidCName in P.Guids:
                        Token = P.Guids[GuidCName]
                        break
                else:
                    PackageListString = "\n\t".join([str(P) for P in self.BuildInfo.DerivedPackageList])
                    EdkLogger.error("AutoGen", AUTOGEN_ERROR,
                                    "GUID [%s] used in module [%s] cannot be found in dependent packages!"
                                    % (GuidCName, self.Module),
                                    ExtraData=PackageListString)
            TokenList[I] = Token
        EdkLogger.debug(EdkLogger.DEBUG_8, "TokenList(guid) = %s" % " ".join(TokenList))
        return TokenList

    ## Return the list of macro in module
    #
    #   @retval     list    The list of macro defined in module file
    #
    def GetMacroList(self):
        return ["%s %s" % (Name, self.Module.Specification[Name]) for Name in self.Module.Specification]

    ## Tool option for the module build
    #
    #   @param      PlatformInfo    The object of PlatformBuildInfo
    #   @retval     dict            The dict containing valid options
    #
    def GetModuleBuildOption(self, PlatformInfo):
        BuildOption = self.Module.BuildOptions
        OptionList = {}
        for Key in BuildOption:
            Family = Key[0]
            Target, Tag, Arch, Tool, Attr = Key[1].split("_")
            # if no tool defined for the option, skip it
            if Tool not in PlatformInfo.ToolPath:
                continue
            # if tool chain family doesn't match, skip it
            if Family != None and Family != "" and Family != PlatformInfo.ToolChainFamily[Tool]:
                continue
            # expand any wildcard
            if Target == "*" or Target == self.BuildTarget:
                if Tag == "*" or Tag == self.ToolChain:
                    if Arch == "*" or Arch == self.Arch:
                        OptionList[Tool] = BuildOption[Key]
        # for those tools that have no option in module file, give it a empty string
        for Tool in PlatformInfo.ToolOption:
            if Tool not in OptionList:
                OptionList[Tool] = ""

        return OptionList

    ## Return a list of files which can be built
    #
    #  What kind of files can be built is determined by build rules in
    #  $(WORKSPACE)/Conf/build_rule.txt and toolchain family.
    #
    #   @param      PlatformInfo    The object of PlatformBuildInfo
    #   @retval     list            The list of files which can be built later
    #
    def GetBuildFileList(self, PlatformInfo):
        # use toolchain family of CC as the primary toolchain family
        ToolChainFamily = PlatformInfo.ToolChainFamily["CC"]
        BuildRule = PlatformInfo.BuildRule
        BuildFileList = []
        for F in self.Module.Sources:
            SourceFile = F.SourceFile
            # match tool chain
            if F.TagName != "" and F.TagName != self.ToolChain:
                EdkLogger.verbose("The toolchain [%s] for processing file [%s] is found, "
                                  "but [%s] is needed" % (F.TagName, F.SourceFile, self.ToolChain))
                continue
            # match tool chain family
            if F.ToolChainFamily != "" and F.ToolChainFamily != ToolChainFamily:
                EdkLogger.verbose("The file [%s] must be built by tools of [%s], "
                                  "but current toolchain family is [%s]" % (SourceFile, F.ToolChainFamily, ToolChainFamily))
                continue

            # add the file path into search path list for file including
            Dir = path.dirname(SourceFile)
            if Dir != "":
                Dir = path.join(self.BuildInfo.SourceDir, Dir)
                if Dir not in self.BuildInfo.IncludePathList:
                    self.BuildInfo.IncludePathList.insert(0, Dir)

            # skip unknown file
            Base, Ext = path.splitext(SourceFile)

            # skip file which needs a tool having no matching toolchain family
            FileType, RuleObject = BuildRule.Get(Ext, ToolChainFamily)
            if FileType == None:
                EdkLogger.verbose("Don't know how to process file [%s]." % SourceFile)
                continue

            # unicode must be processed by AutoGen
            if FileType == "Unicode-Text-File":
                self.BuildInfo.UnicodeFileList.append(os.path.join(self.WorkspaceDir, self.BuildInfo.SourceDir, SourceFile))
                continue

            # no command, no build
            if RuleObject == None or RuleObject.CommandList == []:
                Buildable = False
                EdkLogger.warn(None, "No rule or command defined for building [%s], ignore file [%s]" % (FileType, SourceFile))
                continue

            BuildFileList.append([SourceFile, FileType, RuleObject])

        return BuildFileList

    ## Get the list of package object the module depends on
    #
    #   @retval     list    The package object list
    #
    def GetDependentPackageList(self):
        PackageList = []
        for PackageFile in self.Module.Packages:
            if PackageFile in PackageList:
                continue
            Package = self.PlatformAutoGen.GetPackageObject(PackageFile, self.Arch)
            if Package == None:
                EdkLogger.error("AutoGen", FILE_NOT_FOUND, ExtraData=PackageFile)
            PackageList.append(Package)
        return PackageList

    ## Return the list of auto-generated code file
    #
    #   @param      BuildInfo   The object ModuleBuildInfo
    #   @retval     list        The list of auto-generated file
    #
    def GetAutoGenFileList(self, BuildInfo):
        GenC.CreateCode(BuildInfo, self.AutoGenC, self.AutoGenH)
        FileList = []
        if self.AutoGenC.String != "":
            FileList.append("AutoGen.c")
        if self.AutoGenH.String != "":
            FileList.append("AutoGen.h")
        return FileList

    ## Get the list of library module object
    #
    #   @retval     list    The list of library module list
    #
    def GetSortedLibraryList(self):
        LibraryList = []
        for Key in self.Module.LibraryClasses:
            Library = self.PlatformAutoGen.GetModuleObject(self.Module.LibraryClasses[Key], self.Arch)
            if Library not in LibraryList:
                LibraryList.append(Library)
        return LibraryList

    ## Get the list of PCD
    #
    #   @param      DependentLibraryList    The list of dependent library
    #   @retval     list                    The list of PCD
    #
    def GetPcdList(self, DependentLibraryList):
        PlatformPcds = self.Platform.Pcds

        PcdList = []
        for PcdKey in self.Module.Pcds:
            Pcd = self.Module.Pcds[PcdKey]
            if (Pcd.Type in GenC.gDynamicPcd + GenC.gDynamicExPcd) and self.Module.ModuleType in ["PEIM", "PEI_CORE"]:
                Pcd.Phase = "PEI"
            PcdList.append(Pcd)
        return PcdList

    ## Get the GUID value mapping
    #
    #   @retval     dict    The mapping between GUID cname and its value
    #
    def GetGuidList(self):
        Guid = {}
        Key = ""
        for Key in self.Module.Guids:
            for P in self.BuildInfo.DerivedPackageList:
                if Key in P.Guids:
                    Guid[Key] = P.Guids[Key]
                    break
                if Key in P.Protocols:
                    Guid[Key] = P.Protocols[Key]
                    break
                if Key in P.Ppis:
                    Guid[Key] = P.Ppis[Key]
                    break
            else:
                PackageListString = "\t" + "\n\t".join([str(P) for P in self.BuildInfo.DerivedPackageList])
                EdkLogger.error("AutoGen", AUTOGEN_ERROR, 'GUID [%s] used by [%s] cannot be found in dependent packages' % (Key, self.Module),
                                ExtraData=PackageListString)
        return Guid

    ## Get the protocol value mapping
    #
    #   @retval     dict    The mapping between protocol cname and its value
    #
    def GetProtocolGuidList(self):
        Guid = {}
        Key = ""
        for Key in self.Module.Protocols:
            for P in self.BuildInfo.DerivedPackageList:
                if Key in P.Guids:
                    Guid[Key] = P.Guids[Key]
                    break
                if Key in P.Protocols:
                    Guid[Key] = P.Protocols[Key]
                    break
                if Key in P.Ppis:
                    Guid[Key] = P.Ppis[Key]
                    break
            else:
                PackageListString = "\t" + "\n\t".join([str(P) for P in self.BuildInfo.DerivedPackageList])
                EdkLogger.error("AutoGen", AUTOGEN_ERROR, 'Protocol [%s] used by [%s] cannot be found in dependent packages' % (Key, self.Module),
                                ExtraData=PackageListString)
        return Guid

    ## Get the PPI value mapping
    #
    #   @retval     dict    The mapping between PPI cname and its value
    #
    def GetPpiGuidList(self):
        Guid = {}
        Key = ""
        for Key in self.Module.Ppis:
            for P in self.BuildInfo.DerivedPackageList:
                if Key in P.Guids:
                    Guid[Key] = P.Guids[Key]
                    break
                if Key in P.Protocols:
                    Guid[Key] = P.Protocols[Key]
                    break
                if Key in P.Ppis:
                    Guid[Key] = P.Ppis[Key]
                    break
            else:
                PackageListString = "\t" + "\n\t".join([str(P) for P in self.BuildInfo.DerivedPackageList])
                EdkLogger.error("AutoGen", AUTOGEN_ERROR, 'PPI [%s] used by [%s] cannot be found in dependent packages' % (Key, self.Module),
                                ExtraData=PackageListString)
        return Guid

    ## Get the list of include search path
    #
    #   @param      DependentPackageList    The list of package object
    #   @retval     list                    The list path
    #
    def GetIncludePathList(self, DependentPackageList):
        IncludePathList = []
        for Inc in self.Module.Includes:
            IncludePathList.append(Inc)

        for Package in DependentPackageList:
            PackageDir = path.dirname(Package.DescFilePath)
            IncludePathList.append(PackageDir)
            for Inc in Package.Includes:
                Inc = os.path.join(PackageDir, Inc)
                if Inc not in IncludePathList:
                    IncludePathList.append(Inc)
        return IncludePathList

    ## Create makefile for the module and its dependent libraries
    #
    #   @param      CreateLibraryMakeFile   Flag indicating if or not the makefiles of
    #                                       dependent libraries will be created
    #
    def CreateMakeFile(self, CreateLibraryMakeFile=True):
        if self.IsMakeFileCreated:
            return

        PlatformInfo = self.BuildInfo.PlatformInfo
        if CreateLibraryMakeFile:
            for Lib in self.BuildInfo.DependentLibraryList:
                EdkLogger.debug(EdkLogger.DEBUG_1, "###" + str(Lib))
                LibraryAutoGen = ModuleAutoGen.New(self.Workspace, self.Platform, Lib,
                                                          self.BuildTarget, self.ToolChain, self.Arch)
                if LibraryAutoGen not in self.BuildInfo.LibraryAutoGenList:
                    self.BuildInfo.LibraryAutoGenList.append(LibraryAutoGen)
                LibraryAutoGen.CreateMakeFile()

        Makefile = GenMake.Makefile(self.BuildInfo)
        if Makefile.Generate():
            EdkLogger.verbose("Generated makefile for module %s [%s]" %
                           (self.BuildInfo.Name, self.BuildInfo.Arch))
        else:
            EdkLogger.verbose("Skipped the generation of makefile for module %s [%s]" %
                           (self.BuildInfo.Name, self.BuildInfo.Arch))

        self.IsMakeFileCreated = True

    ## Create autogen code for the module and its dependent libraries
    #
    #   @param      CreateLibraryCodeFile   Flag indicating if or not the code of
    #                                       dependent libraries will be created
    #
    def CreateCodeFile(self, CreateLibraryCodeFile=True):
        if self.IsCodeFileCreated:
            return

        PlatformInfo = self.BuildInfo.PlatformInfo
        if CreateLibraryCodeFile:
            for Lib in self.BuildInfo.DependentLibraryList:
                LibraryAutoGen = ModuleAutoGen.New(self.Workspace, self.Platform, Lib,
                                                          self.BuildTarget, self.ToolChain, self.Arch)
                if LibraryAutoGen not in self.BuildInfo.LibraryAutoGenList:
                    self.BuildInfo.LibraryAutoGenList.append(LibraryAutoGen)
                LibraryAutoGen.CreateCodeFile()

        AutoGenList = []
        IgoredAutoGenList = []
        if self.AutoGenC.String != "":
            if GenC.Generate(os.path.join(self.BuildInfo.WorkspaceDir, self.BuildInfo.DebugDir, gAutoGenCodeFileName),
                             self.AutoGenC.String):
                AutoGenList.append(gAutoGenCodeFileName)
            else:
                IgoredAutoGenList.append(gAutoGenCodeFileName)

        if self.AutoGenH.String != "":
            if GenC.Generate(os.path.join(self.BuildInfo.WorkspaceDir, self.BuildInfo.DebugDir, gAutoGenHeaderFileName),
                             self.AutoGenH.String):
                AutoGenList.append(gAutoGenHeaderFileName)
            else:
                IgoredAutoGenList.append(gAutoGenHeaderFileName)

        if self.BuildInfo.DepexList != []:
            Dpx = GenDepex.DependencyExpression(self.BuildInfo.DepexList, self.BuildInfo.ModuleType)
            DpxFile = gAutoGenDepexFileName % {"module_name" : self.BuildInfo.Name}
            if Dpx.Generate(os.path.join(self.WorkspaceDir, self.BuildInfo.OutputDir, DpxFile)):
                AutoGenList.append(DpxFile)
            else:
                IgoredAutoGenList.append(DpxFile)

        if IgoredAutoGenList == []:
            EdkLogger.verbose("Generated [%s] files for module %s [%s]" %
                           (" ".join(AutoGenList), self.BuildInfo.Name, self.BuildInfo.Arch))
        elif AutoGenList == []:
            EdkLogger.verbose("Skipped the generation of [%s] files for module %s [%s]" %
                           (" ".join(IgoredAutoGenList), self.BuildInfo.Name, self.BuildInfo.Arch))
        else:
            EdkLogger.verbose("Generated [%s] (skipped %s) files for module %s [%s]" %
                           (" ".join(AutoGenList), " ".join(IgoredAutoGenList), self.BuildInfo.Name, self.BuildInfo.Arch))

        self.IsCodeFileCreated = True
        return AutoGenList

# Version and Copyright
__version_number__ = "0.01"
__version__ = "%prog Version " + __version_number__
__copyright__ = "Copyright (c) 2007, Intel Corporation. All rights reserved."

## Parse command line options
#
# Using standard Python module optparse to parse command line option of this tool.
#
# @retval Options   A optparse.Values object containing the parsed options
# @retval InputFile Path of file to be trimmed
#
def GetOptions():
    OptionList = [
        make_option("-a", "--arch", dest="Arch",
                          help="The input file is preprocessed source code, including C or assembly code"),
        make_option("-p", "--platform", dest="ActivePlatform",
                          help="The input file is preprocessed VFR file"),
        make_option("-m", "--module", dest="ActiveModule",
                          help="Convert standard hex format (0xabcd) to MASM format (abcdh)"),
        make_option("-f", "--FDF-file", dest="FdfFile",
                          help="Convert standard hex format (0xabcd) to MASM format (abcdh)"),
        make_option("-o", "--output", dest="OutputDirectory",
                          help="File to store the trimmed content"),
        make_option("-t", "--toolchain-tag", dest="ToolChain",
                          help=""),
        make_option("-k", "--msft", dest="MakefileType", action="store_const", const="nmake",
                          help=""),
        make_option("-g", "--gcc", dest="MakefileType", action="store_const", const="gmake",
                          help=""),
        make_option("-v", "--verbose", dest="LogLevel", action="store_const", const=EdkLogger.VERBOSE,
                          help="Run verbosely"),
        make_option("-d", "--debug", dest="LogLevel", type="int",
                          help="Run with debug information"),
        make_option("-q", "--quiet", dest="LogLevel", action="store_const", const=EdkLogger.QUIET,
                          help="Run quietly"),
        make_option("-?", action="help", help="show this help message and exit"),
    ]

    # use clearer usage to override default usage message
    UsageString = "%prog [-a ARCH] [-p PLATFORM] [-m MODULE] [-t TOOLCHAIN_TAG] [-k] [-g] [-v|-d <debug_level>|-q] [-o <output_directory>] [GenC|GenMake]"

    Parser = OptionParser(description=__copyright__, version=__version__, option_list=OptionList, usage=UsageString)
    Parser.set_defaults(Arch=[])
    Parser.set_defaults(ActivePlatform=None)
    Parser.set_defaults(ActiveModule=None)
    Parser.set_defaults(OutputDirectory="build")
    Parser.set_defaults(FdfFile=None)
    Parser.set_defaults(ToolChain="MYTOOLS")
    if sys.platform == "win32":
        Parser.set_defaults(MakefileType="nmake")
    else:
        Parser.set_defaults(MakefileType="gmake")
    Parser.set_defaults(LogLevel=EdkLogger.INFO)

    Options, Args = Parser.parse_args()

    # error check
    if len(Args) == 0:
        Options.Target = "genmake"
        sys.argv.append("genmake")
    elif len(Args) == 1:
        Options.Target = Args[0].lower()
        if Options.Target not in ["genc", "genmake"]:
            EdkLogger.error("AutoGen", OPTION_NOT_SUPPORTED, "Not supported target",
                            ExtraData="%s\n\n%s" % (Options.Target, Parser.get_usage()))
    else:
        EdkLogger.error("AutoGen", OPTION_NOT_SUPPORTED, "Too many targets",
                        ExtraData=Parser.get_usage())

    return Options

## Entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
# @retval 0     Tool was successful
# @retval 1     Tool failed
#
def Main():
    from build import build
    try:
        Option = GetOptions()
        build.main()
    except Exception, e:
        print e
        return 1

    return 0

# This acts like the main() function for the script, unless it is 'import'ed into another script.
if __name__ == '__main__':
    sys.exit(Main())
