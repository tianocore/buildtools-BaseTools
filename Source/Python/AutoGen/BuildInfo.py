## @file
# Class definitions for storing build information
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

## Base class of build information
# 
#   BuildInfo defines basic operations which are needed for it to be used as KEY
# in dictionary. This should be used for derivation only.
# 
class BuildInfo(object):
    ## Constructor
    #
    #   @param  MetaInfo    The raw information the build information will be 
    #                       extracted from
    # 
    def __init__(self, MetaInfo):
        self._Key = str(MetaInfo)

    ## str() operator
    def __str__(self):
        return self._Key

    ## "==" operator
    def __eq__(self, other):
        return self._Key == str(other)

    ## hash() operator
    def __hash__(self):
        return hash(self._Key)

## Build information of a module
# 
#   ModuleBuildInfo class is intended to gather build information for a module.
# The input "Module" ojbect must support str() operation.
# 
class ModuleBuildInfo(BuildInfo):
    ## Constructor
    #
    #   @param  Module  The ModuleBuildClassObject object
    # 
    def __init__(self, Module):
        BuildInfo.__init__(self, Module)
        self.Module     = Module

        self.Name       = Module.BaseName
        self.Guid       = Module.Guid
        self.Version    = Module.Version
        self.ModuleType = Module.ModuleType

        self.PlatformInfo = None
        self.PackageInfo = None
        self.Arch = ""
        self.ToolChain = ""
        self.BuildTarget = ""
        self.PcdIsDriver = ""

        self.IsLibrary = False
        self.IsBinary = False

        self.BaseName = ""
        self.FileBase = ""
        self.FileExt = ""

        self.WorkspaceDir = ""
        self.SourceDir = ""
        self.BuildDir = ""
        self.OutputDir = ""
        self.DebugDir = ""
        self.MakeFileDir = ""
        self.CustomMakefile = {}

        self.IncludePathList = []
        self.AutoGenFileList = []
        self.UnicodeFileList = []
        self.SourceFileList = []
        self.ObjectFileList = []

        self.DependentPackageList = []
        self.DependentLibraryList = []
        self.LibraryAutoGenList = []
        self.DerivedPackageList = []

        self.FileDependency = {}
        self.BuildOption = {}

        self.PcdList = []
        self.GuidList = []
        self.ProtocolList = []
        self.PpiList = []

        self.MacroList = []
        self.DepexList = []

## Build information of a package
# 
#   PackageBuildInfo class is intended to gather build information for a package.
# The input "Package" ojbect must support str() operation.
# 
class PackageBuildInfo(BuildInfo):
    ## Constructor
    #
    #   @param  Package     The PackageBuildClassObject object
    # 
    def __init__(self, Package):
        BuildInfo.__init__(self, Package)
        self.Package    = Package
        self.Name       = Package.PackageName
        self.Guid       = Package.Guid
        self.Version    = Package.Version

        self.SourceDir = ""
        self.IncludePathList = []

## Build information of a platform
# 
#   PlatformBuildInfo class is intended to gather build information for a platform.
# The input "Platform" ojbect must support str() operation.
# 
class PlatformBuildInfo(BuildInfo):
    ## Constructor
    #
    #   @param  Platform    The PlatformBuildClassObject object
    # 
    def __init__(self, Platform):
        BuildInfo.__init__(self, Platform)
        self.Platform   = Platform
        self.Name       = Platform.PlatformName
        self.Guid       = Platform.Guid
        self.Version    = Platform.Version

        self.ArchList = []
        self.ToolChain = ""
        self.BuildTarget = ""
        self.BuildRule = ""

        self.WorkspaceDir = ""
        self.SourceDir = ""
        self.BuildDir = ""
        self.OutputDir = ""
        self.DebugDir = ""
        self.LibraryDir = ""
        self.FvDir = ""
        self.MakeFileDir = ""
        self.FdfFile = ""

        self.ModuleAutoGenList = []
        self.LibraryAutoGenList = []
        self.PackageList = []

        self.PcdTokenNumber = {}    # (TokenCName, TokenSpaceGuidCName) : GeneratedTokenNumber
        self.DynamicPcdList = []    # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]
        self.NonDynamicPcdList = [] # [(TokenCName1, TokenSpaceGuidCName1), (TokenCName2, TokenSpaceGuidCName2), ...]

        self.ToolPath = {}          # toolcode : tool path
        self.ToolDllPath = {}       # toolcode : lib path
        self.ToolStaticLib = {}     # toolcode : lib path
        self.ToolChainFamily = {}   # toolcode : tool chain family
        self.BuildOption = {}       # toolcode : option
        self.OutputFlag = {}        # toolcode : output flag
        self.IncludeFlag = {}       # toolcode : include flag
        self.ToolOption = {}        # toolcode : tool option string

