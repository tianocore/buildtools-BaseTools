# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define each component of the build database
#

#
# Import Modules
#
import os, string, copy, pdb
import EdkLogger
import DataType
from InfClassObject import *
from DecClassObject import *
from DscClassObject import *
from String import *
from BuildToolError import *
from CommonDataClass.CommonClass import *

#
# This Class is used for PcdObject 
#
class PcdClassObject(object):
    def __init__(self, Name = None, Guid = None, Type = None, DatumType = None, Value = None, Token = None, MaxDatumSize = None, SkuInfoList = {}):
        self.TokenCName = Name
        self.TokenSpaceGuidCName = Guid
        self.Type = Type
        self.DatumType = DatumType
        self.DefaultValue = Value
        self.TokenValue = Token
        self.MaxDatumSize = MaxDatumSize
        self.SkuInfoList = SkuInfoList
        self.Phase = "DXE"
        
    def __str__(self):
        rtn = str(self.TokenCName) + DataType.TAB_VALUE_SPLIT + \
              str(self.TokenSpaceGuidCName) + DataType.TAB_VALUE_SPLIT + \
              str(self.Type) + DataType.TAB_VALUE_SPLIT + \
              str(self.DatumType) + DataType.TAB_VALUE_SPLIT + \
              str(self.DefaultValue) + DataType.TAB_VALUE_SPLIT + \
              str(self.TokenValue) + DataType.TAB_VALUE_SPLIT + \
              str(self.MaxDatumSize) + DataType.TAB_VALUE_SPLIT
        for Item in self.SkuInfoList.values():
            rtn = rtn + Item.SkuId + DataType.TAB_VALUE_SPLIT + Item.SkuIdName
        return rtn

    def __eq__(self, other):
        return other != None and self.TokenCName == other.TokenCName and self.TokenSpaceGuidCName == other.TokenSpaceGuidCName

    def __hash__(self):
        return hash((self.TokenCName, self.TokenSpaceGuidCName))

#
# This Class is used for LibraryClassObject
#
class LibraryClassObject(object):
    def __init__(self, Name = None, SupModList = [], Type = None):
        self.LibraryClass = Name
        self.SupModList = SupModList
        if Type != None:
            self.SupModList = CleanString(Type).split(DataType.TAB_SPACE_SPLIT)
        
class ModuleBuildClassObject(object):
    def __init__(self):
        self.DescFilePath            = ''
        self.BaseName                = ''
        self.ModuleType              = ''
        self.Guid                    = ''
        self.Version                 = ''
        self.PcdIsDriver             = ''
        self.BinaryModule            = ''
        self.CustomMakefile          = {}
        self.Specification           = {}
        self.LibraryClass            = None      # LibraryClassObject
        self.ModuleEntryPointList    = []
        self.ModuleUnloadImageList   = []
        self.ConstructorList         = []
        self.DestructorList          = []
        
        self.Binaries                = []        #[ ModuleBinaryClassObject, ...]
        self.Sources                 = []        #[ ModuleSourceFilesClassObject, ... ]
        self.LibraryClasses          = {}        #{ [LibraryClassName, ModuleType] : LibraryClassInfFile }
        self.Protocols               = []        #[ ProtocolName, ... ]
        self.Ppis                    = []        #[ PpiName, ... ]
        self.Guids                   = []        #[ GuidName, ... ]
        self.Includes                = []        #[ IncludePath, ... ]
        self.Packages                = []        #[ DecFileName, ... ]
        self.Pcds                    = {}        #{ [(PcdCName, PcdGuidCName)] : PcdClassObject}
        self.BuildOptions            = {}        #{ [BuildOptionKey] : BuildOptionValue}
        self.Depex                   = ''

    def __str__(self):
        return self.DescFilePath

    def __eq__(self, other):
        return self.DescFilePath == str(other)

    def __hash__(self):
        return hash(self.DescFilePath)

class PackageBuildClassObject(object):
    def __init__(self):
        self.DescFilePath            = ''
        self.PackageName             = ''
        self.Guid                    = ''
        self.Version                 = ''
        
        self.Protocols               = {}       #{ [ProtocolName] : Protocol Guid, ... }
        self.Ppis                    = {}       #{ [PpiName] : Ppi Guid, ... }
        self.Guids                   = {}       #{ [GuidName] : Guid, ... }
        self.Includes                = []       #[ IncludePath, ... ]        
        self.LibraryClasses          = {}       #{ [LibraryClassName] : LibraryClassInfFile }
        self.Pcds                    = {}       #{ [(PcdCName, PcdGuidCName)] : PcdClassObject}
        
    def __str__(self):
        return self.DescFilePath

    def __eq__(self, other):
        return self.DescFilePath == str(other)

    def __hash__(self):
        return hash(self.DescFilePath)

class PlatformBuildClassObject(object):
    def __init__(self):
        self.DescFilePath            = ''
        self.PlatformName            = ''
        self.Guid                    = ''
        self.Version                 = ''
        self.DscSpecification        = ''
        self.OutputDirectory         = ''
        self.FlashDefinition         = ''
        self.BuildNumber             = ''
        self.MakefileName            = ''
                
        self.SkuIds                  = {}       #{ 'SkuName' : SkuId, '!include' : includefilename, ...}
        self.Modules                 = []       #[ InfFileName, ... ]
        self.Libraries               = []       #[ InfFileName, ... ]
        self.LibraryClasses          = {}       #{ (LibraryClassName, ModuleType) : LibraryClassInfFile }
        self.Pcds                    = {}       #{ [(PcdCName, PcdGuidCName)] : PcdClassObject }
        self.BuildOptions            = {}       #{ [BuildOptionKey] : BuildOptionValue }    

    def __str__(self):
        return self.DescFilePath

    def __eq__(self, other):
        return self.DescFilePath == str(other)

    def __hash__(self):
        return hash(self.DescFilePath)

class ItemBuild(object):
    def __init__(self, Arch, Platform = None, Package = None, Module = None):
        self.Arch                    = Arch
        self.PlatformDatabase        = {}        #{ [DscFileName] : PlatformBuildClassObject, ...}
        self.PackageDatabase         = {}        #{ [DecFileName] : PacakgeBuildClassObject, ...}
        self.ModuleDatabase          = {}        #{ [InfFileName] : ModuleBuildClassObject, ...}
        
#
# This class is used to parse active platform to init all inf/dec/dsc files
# Generate module/package/platform databases for build
#
class WorkspaceBuild(object):
    def __init__(self, ActivePlatform, WorkspaceDir):
        self.WorkspaceDir            = NormPath(WorkspaceDir)
        self.SupArchList             = []        #[ 'IA32', 'X64', ...]
        self.BuildTarget             = []        #[ 'RELEASE', 'DEBUG']
        self.SkuId                   = ''
        self.Fdf                     = ''
        self.TargetTxt               = None
        self.ToolDef                 = None
        
        self.InfDatabase             = {}        #{ [InfFileName] : InfClassObject}
        self.DecDatabase             = {}        #{ [DecFileName] : DecClassObject}
        self.DscDatabase             = {}        #{ [DscFileName] : DscClassObject}
        
        #
        # Init build for all arches
        #
        self.Build                   = {}
        for Arch in DataType.ARCH_LIST:
            self.Build[Arch] = ItemBuild(Arch)
        
        #
        # Get active platform
        #
        DscFileName = ActivePlatform
        File = self.WorkspaceFile(NormPath(DscFileName))
        if os.path.exists(File) and os.path.isfile(File):
            self.DscDatabase[DscFileName] = Dsc(File, True, True)
        else:
            raise ParserError(FILE_NOT_FOUND, name = File)
        
        #
        # Parse platform to get module
        #
        for DscFile in self.DscDatabase.keys():
            Platform = self.DscDatabase[DscFile].Platform
            
            #
            # Get global information
            #
            self.SupArchList = Platform.Header.SupArchList
            self.BuildTarget = Platform.Header.BuildTargets
            self.SkuId = Platform.Header.SkuIdName
            self.Fdf = Platform.FlashDefinitionFile.FilePath
            
            #
            # Get all inf files
            #
            for Item in Platform.LibraryClasses.LibraryList:
                for Arch in Item.SupArchList:
                    self.AddToInfDatabase(Item.FilePath)
            
            for Item in Platform.Modules.ModuleList:
                for Arch in Item.SupArchList:
                    #
                    # Add modules
                    #
                    Module = Item.FilePath
                    self.AddToInfDatabase(Module)
                    #
                    # Add library used in modules
                    #
                    for Lib in Item.LibraryClasses.LibraryList:
                        self.AddToInfDatabase(Lib.FilePath)
                        self.UpdateLibraryClassOfModule(Module, Lib.Name, Arch)
        
        #
        # Parse module to get package
        #
        for InfFile in self.InfDatabase.keys():
            Module = self.InfDatabase[InfFile].Module
            #
            # Get all dec
            #
            for Item in Module.PackageDependencies:
                for Arch in Item.SupArchList:
                    self.AddToDecDatabase(Item.FilePath)
    # End of self.Init()
    
    #
    # Generate PlatformDatabase
    #
    def GenPlatformDatabase(self):
        for Dsc in self.DscDatabase.keys():
            Platform = self.DscDatabase[Dsc].Platform
            
            for Arch in self.SupArchList:
                pb = PlatformBuildClassObject()
                
                # Defines
                pb.DescFilePath = Dsc
                pb.PlatformName = Platform.Header.Name
                pb.Guid = Platform.Header.Guid
                pb.Version = Platform.Header.Version
                pb.DscSpecification = Platform.Header.DscSpecification
                pb.OutputDirectory = NormPath(Platform.Header.OutputDirectory)
                pb.FlashDefinition = NormPath(Platform.FlashDefinitionFile.FilePath)
                pb.BuildNumber = Platform.Header.BuildNumber
            
                # SkuId
                for Key in Platform.SkuInfos.SkuInfoList.keys():
                    pb.SkuIds[Key] = Platform.SkuInfos.SkuInfoList[Key]
                
                # Module
                for Item in Platform.Modules.ModuleList:
                    if Arch in Item.SupArchList:
                        pb.Modules.append(NormPath(Item.FilePath))
                    
                # BuildOptions
                for Item in Platform.BuildOptions.BuildOptionList:
                    if Arch in Item.SupArchList:
                        pb.BuildOptions[(Item.ToolChainFamily, Item.ToolChain)] = Item.Option
                  
                # LibraryClass
                for Item in Platform.LibraryClasses.LibraryList:
                    if Arch in Item.SupArchList:
                        for ModuleType in Item.ModuleType:
                            pb.LibraryClasses[(Item.Name, ModuleType)] = NormPath(Item.FilePath)
                    
                # Pcds
                for Item in Platform.DynamicPcdBuildDefinitions:
                    if Arch in Item.SupArchList:
                        Name = Item.CName
                        Guid = Item.TokenSpaceGuidCName
                        Type = Item.ItemType
                        DatumType = ''
                        Value = Item.DefaultValue
                        Token = Item.Token
                        MaxDatumSize = Item.MaxDatumSize
                        SkuInfoList = Item.SkuInfoList
                        pb.Pcds[(Name, Guid)] = PcdClassObject(Name, Guid, Type, DatumType, Value, Token, MaxDatumSize, SkuInfoList)
                
                # Add to database
                self.Build[Arch].PlatformDatabase[Dsc] = pb
                pb = None
    
    #
    # Generate PackageDatabase
    #    
    def GenPackageDatabase(self):
        for Dec in self.DecDatabase.keys():
            Package = self.DecDatabase[Dec].Package
        
            for Arch in self.SupArchList:
                pb = PackageBuildClassObject()
                
                # Defines
                pb.DescFilePath = Dec
                pb.PackageName = Package.Header.Name
                pb.Guid = Package.Header.Guid
                pb.Version = Package.Header.Version
                
                # Protocols
                for Item in Package.ProtocolDeclarations:
                    if Arch in Item.SupArchList:
                        pb.Protocols[Item.CName] = Item.Guid
                        
                # Ppis
                for Item in Package.PpiDeclarations:
                    if Arch in Item.SupArchList:
                        pb.Ppis[Item.CName] = Item.Guid
                
                # Guids
                for Item in Package.GuidDeclarations:
                    if Arch in Item.SupArchList:
                        pb.Ppis[Item.CName] = Item.Guid
                
                # Includes
                for Item in Package.Includes:
                    if Arch in Item.SupArchList:
                        pb.Includes.append(NormPath(Item.FilePath))
                        
                # LibraryClasses
                for Item in Package.LibraryClassDeclarations:
                    if Arch in Item.SupArchList:
                        pb.LibraryClasses[Item.LibraryClass] = NormPath(Item.RecommendedInstance)
                
                # Pcds
                for Item in Package.PcdDeclarations:
                    if Arch in Item.SupArchList:
                        Name = Item.CName
                        Guid = Item.TokenSpaceGuidCName
                        Type = Item.ItemType
                        DatumType = ''
                        Value = Item.DefaultValue
                        Token = Item.Token
                        MaxDatumSize = Item.MaxDatumSize
                        SkuInfoList = Item.SkuInfoList
                        pb.Pcds[(Name, Guid)] = PcdClassObject(Name, Guid, Type, DatumType, Value, Token, MaxDatumSize, SkuInfoList)
                
                # Add to database
                self.Build[Arch].PackageDatabase[Dec] = pb
                pb = None
    
    #
    # Generate ModuleDatabase
    #
    def GenModuleDatabase(self, PcdsSet = {}):
        for Inf in self.InfDatabase.keys():
            Module = self.InfDatabase[Inf].Module
            
            for Arch in self.SupArchList:
                pb = ModuleBuildClassObject()
                
                # Defines
                pb.DescFilePath = Inf
                pb.BaseName = Module.Header.Name
                pb.Guid = Module.Header.Guid
                pb.Version = Module.Header.Version
                pb.ModuleType = Module.Header.ModuleType
                pb.PcdIsDriver = Module.Header.PcdIsDriver
                pb.BinaryModule = Module.Header.BinaryModule
                pb.CustomMakefile = Module.Header.CustomMakefile
                
                # Specs os Defines
                pb.Specification = Module.Header.Specification
                pb.Specification[TAB_INF_DEFINES_EDK_RELEASE_VERSION] = Module.Header.EdkReleaseVersion
                pb.Specification[TAB_INF_DEFINES_EFI_SPECIFICATION_VERSION] = Module.Header.EfiSpecificationVersion
                
                # LibraryClass of Defines
                for Item in Module.Header.LibraryClass:
                    pb.LibraryClass = LibraryClassObject(Item.LibraryClass, Item.SupModuleList, None)

                # Module image and library of Defines
                for Item in Module.ExternImages:
                    if Item.ModuleEntryPoint != '':
                        pb.ModuleEntryPointList.append(Item.ModuleEntryPoint)
                    if Item.ModuleUnloadImage != '':
                        pb.ModuleUnloadImageList.append(Item.ModuleUnloadImage)
                for Item in Module.ExternLibraries:
                    if Item.Constructor != '':
                        pb.ConstructorList.append(Item.Constructor)
                    if Item.Destructor != '':
                        pb.DestructorList.append(Item.Destructor)
                
                # Binaries
                for Item in Module.Binaries:
                    if Arch in Item.SupArchList:
                        FileName = NormPath(Item.BinaryFile)
                        FileType = Item.FileType
                        Target = Item.Target
                        FeatureFlag = Item.FeatureFlag
                        pb.Binaries.append(ModuleBinaryFileClass(FileName, FileType, Target, FeatureFlag))
                
                #Sources
                for Item in Module.Sources:
                    if Arch in Item.SupArchList:
                        SourceFile = NormPath(Item.SourceFile)
                        TagName = Item.TagName
                        ToolCode = Item.ToolCode
                        ToolChainFamily = Item.ToolChainFamily
                        FeatureFlag = Item.FeatureFlag
                        pb.Sources.append(ModuleSourceFileClass(SourceFile, TagName, ToolCode, ToolChainFamily, FeatureFlag))
                
                # Protocols
                for Item in Module.Protocols:
                    if Arch in Item.SupArchList:
                        pb.Protocols.append(Item.CName)
                        
                # Ppis
                for Item in Module.Ppis:
                    if Arch in Item.SupArchList:
                        pb.Ppis.append(Item.CName)
                
                # Guids
                for Item in Module.Guids:
                    if Arch in Item.SupArchList:
                        pb.Ppis.append(Item.CName)
                
                # Includes
                for Item in Module.Includes:
                    if Arch in Item.SupArchList:
                        pb.Includes.append(NormPath(Item.FilePath))                
                
                # Packages
                for Item in Module.PackageDependencies:
                    if Arch in Item.SupArchList:
                        pb.Packages.append(NormPath(Item.FilePath))                        

                # BuildOptions
                for Item in Module.BuildOptions:
                    if Arch in Item.SupArchList:
                        pb.BuildOptions[(Item.ToolChainFamily, Item.ToolChain)] = Item.Option
                self.FindBuildOptions(Arch, Inf, pb.BuildOptions)
                
                # Depex
                for Item in Module.Depex:
                    if Arch in Item.SupArchList:
                        pb.Depex = pb.Depex + Item.Depex + ' '
                pb.Depex = pb.Depex.strip()
                
                # LibraryClasses
                for Item in Module.LibraryClasses:
                    if Arch in Item.SupArchList:
                        Lib = Item.LibraryClass
                        RecommendedInstance = Item.RecommendedInstance
                        if pb.LibraryClass != None:
                            # For Library
                            for Type in pb.LibraryClass.SupModList:
                                Instance = self.FindLibraryClassInstanceOfLibrary(Lib, Arch, Type)
                                if Instance == None:
                                    Instance = RecommendedInstance
                                    pb.LibraryClasses[(Lib, Type)] = NormPath(Instance)
                        else:
                            # For Module
                            Instance = self.FindLibraryClassInstanceOfModule(Lib, Arch, pb.ModuleType, Inf) 
                            if Instance == None:
                                Instance = RecommendedInstance
                            pb.LibraryClasses[(Lib, pb.ModuleType)] = NormPath(Instance)
                
                # Pcds
                for Item in Module.PcdCodes:
                    if Arch in Item.SupArchList:
                        Name = Item.CName
                        Guid = Item.TokenSpaceGuidCName
                        Type = Item.ItemType
                        pb.Pcds[(Name, Guid)] = self.FindPcd(Arch, Inf, Name, Guid, Type, PcdsSet)
                
                # Add to database
                self.Build[Arch].ModuleDatabase[Inf] = pb
                pb = None
    
    #
    # Update Libraries Of Platform Database
    #
    def UpdateLibrariesOfPlatform(self):
        for Arch in self.SupArchList:
            PlatformDatabase = self.Build[Arch].PlatformDatabase
            for Dsc in PlatformDatabase:
                Platform = PlatformDatabase[Dsc]
                for Inf in Platform.Modules:
                    Module = self.Build[Arch].ModuleDatabase[NormPath(Inf)]
                    Stack = [NormPath(str(Module))]
                    while len(Stack) > 0:
                        M = self.Build[Arch].ModuleDatabase[Stack.pop()]
                        if M != Module:
                            Platform.Libraries.append(M)
                        for Lib in M.LibraryClasses.values():
                            if Lib not in Platform.Libraries and Lib != '':
                                Platform.Libraries.append(NormPath(Lib))
                                Stack.append(NormPath(Lib))
    
    #
    # Generate build database for all arches
    #
    def GenBuildDatabase(self, PcdsSet = {}):
        self.GenPlatformDatabase()
        self.GenPackageDatabase()
        self.GenModuleDatabase(PcdsSet)
        #self.UpdateLibrariesOfPlatform()

    #
    # Return a full path with workspace dir
    #
    def WorkspaceFile(self, Filename):
        return os.path.join(os.path.normpath(self.WorkspaceDir), os.path.normpath(Filename))
    
    #
    # If a module of a platform has its own override libraryclass but the libraryclass not defined in the module
    # Add this libraryclass to the module
    #
    def UpdateLibraryClassOfModule(self, InfFileName, LibraryClass, Arch):
        LibList = self.InfDatabase[NormPath(InfFileName)].Module.LibraryClasses
        NotFound = True
        for Lib in LibList:
            #
            # Find this LibraryClass
            #
            if Lib.LibraryClass == LibraryClass:
                if Arch in Lib.SupArchList:
                    return
                else:
                    Lib.SupArchList.append(Arch)
                    return
        if NotFound:
            Lib = LibraryClassClass()
            Lib.LibraryClass = LibraryClass
            Lib.SupArchList = [Arch]
            self.InfDatabase[NormPath(InfFileName)].Module.LibraryClasses.append(Lib)
            
    #
    # Create a Inf instance for input inf file and add it to InfDatabase
    #
    def AddToInfDatabase(self, InfFileName):
        InfFileName = NormPath(InfFileName)
        File = self.WorkspaceFile(InfFileName)
        if os.path.exists(File) and os.path.isfile(File):
            if InfFileName not in self.InfDatabase:
                self.InfDatabase[InfFileName] = Inf(File, True, True)
        else:
            raise ParserError(FILE_NOT_FOUND, name = File)
    
    #
    # Create a Dec instance for input dec file and add it to DecDatabase
    #                
    def AddToDecDatabase(self, DecFileName):
        DecFileName = NormPath(DecFileName)
        File = self.WorkspaceFile(DecFileName)
        if os.path.exists(File) and os.path.isfile(File):
            if DecFileName not in self.DecDatabase:
                self.DecDatabase[DecFileName] = Dec(File, True, True)
        else:
            raise ParserError(FILE_NOT_FOUND, name = File)
                
    #
    # Search PlatformBuildDatabase to find LibraryClass Instance for Module
    # Return the instance if found
    #
    def FindLibraryClassInstanceOfModule(self, Lib, Arch, ModuleType, ModuleName):
        #
        # First find if exist in <LibraryClass> of <Components> from dsc file
        #
        for Dsc in self.DscDatabase.keys():
            Platform = self.DscDatabase[Dsc].Platform
            for Module in Platform.Modules.ModuleList:
                if Arch in Module.SupArchList:
                    if NormPath(Module.FilePath) == ModuleName:
                        for LibraryClass in Module.LibraryClasses.LibraryList:
                            if LibraryClass.Name == Lib:
                                return NormPath(LibraryClass.FilePath)
        #
        #Second find if exist in <LibraryClass> of <LibraryClasses> from dsc file            
        #
        return self.FindLibraryClassInstanceOfLibrary(Lib, Arch, ModuleType)
            
    #
    # Search PlatformBuildDatabase to find LibraryClass Instance for Library
    # Return the instance if found
    #
    def FindLibraryClassInstanceOfLibrary(self, Lib, Arch, Type):
        for Dsc in self.DscDatabase.keys():
            Platform  = self.DscDatabase[Dsc].Platform
            if (Lib, Type) in self.Build[Arch].PlatformDatabase[Dsc].LibraryClasses:
                return self.Build[Arch].PlatformDatabase[Dsc].LibraryClasses[(Lib, Type)]
            elif (Lib, '') in self.Build[Arch].PlatformDatabase[Dsc].LibraryClasses:
                return self.Build[Arch].PlatformDatabase[Dsc].LibraryClasses[(Lib, '')]
        return None
            
    #
    # Search DscDatabase to find component definition of ModuleName
    # Override BuildOption if it is defined in component
    #
    def FindBuildOptions(self, Arch, ModuleName, BuildOptions):
        for Dsc in self.DscDatabase.keys():
            #
            # First find if exist in <BuildOptions> of <Components> from dsc file
            # if find, use that override the one defined in inf file
            #
            Platform = self.DscDatabase[Dsc].Platform
            for Module in Platform.Modules.ModuleList:
                if Arch in Module.SupArchList:
                    if NormPath(Module.FilePath) == ModuleName:
                        for BuildOption in Module.ModuleSaBuildOption.BuildOptionList:
                            BuildOptions[(BuildOption.ToolChainFamily, BuildOption.ToolChain)] = BuildOption.Option
                        
    #
    # Search platform database, package database, module database and PcdsSet from Fdf
    # Return found Pcd
    #
    def FindPcd(self, Arch, ModuleName, Name, Guid, Type, PcdsSet):
        DatumType = ''
        Value = ''
        Token = ''
        MaxDatumSize = ''
        SkuInfoList = {}
        #
        # First get information from platform database
        #
        for Dsc in self.Build[Arch].PlatformDatabase.keys():
            Pcds = self.Build[Arch].PlatformDatabase[Dsc].Pcds
            if (Name, Guid) in Pcds:
                Type = Pcds[(Name, Guid)].Type
                DatumType = Pcds[(Name, Guid)].DatumType
                Value = Pcds[(Name, Guid)].DefaultValue
                Token = Pcds[(Name, Guid)].TokenValue
                MaxDatumSize = Pcds[(Name, Guid)].MaxDatumSize
                SkuInfoList =  Pcds[(Name, Guid)].SkuInfoList
                break

        #
        # Second get information from package database
        #
        for Dec in self.Build[Arch].PackageDatabase.keys():
            Pcds = self.Build[Arch].PackageDatabase[Dec].Pcds
            if (Name, Guid) in Pcds:
                DatumType = Pcds[(Name, Guid)].DatumType
                Token = Pcds[(Name, Guid)].TokenValue
                break
        
        #
        # Third get information from <Pcd> of <Compontents> from module database
        #
        for Dsc in self.DscDatabase.keys():
            for Module in self.DscDatabase[Dsc].Platform.Modules.ModuleList:
                if Arch in Module.SupArchList:
                    if NormPath(Module.FilePath) == ModuleName:
                        for Pcd in Module.PcdBuildDefinitions:
                            if (Name, Guid) == (Pcd.CName, Pcd.TokenSpaceGuidCName):
                                if Pcd.DefaultValue != '':
                                    Value = Pcd.DefaultValue
                                if Pcd.MaxDatumSize != '':
                                    MaxDatumSize = Pcd.MaxDatumSize
        
        #
        # Last get information from PcdsSet defined by FDF
        #
        if Guid in PcdsSet.keys():
            Value = PcdsSet[Guid]
        
        return PcdClassObject(Name, Guid, Type, DatumType, Value, Token, MaxDatumSize, SkuInfoList)   

    #
    # Show all content of the workspacebuild
    #
    def ShowWorkspaceBuild(self):
        print ewb.DscDatabase
        print ewb.InfDatabase
        print ewb.DecDatabase
        print 'SupArchList', ewb.SupArchList
        print 'BuildTarget', ewb.BuildTarget
        print 'SkuId', ewb.SkuId
        
        for arch in ewb.SupArchList:
            print arch
            print 'Platform'
            for platform in ewb.Build[arch].PlatformDatabase.keys():
                p = ewb.Build[arch].PlatformDatabase[platform]
                print 'DescFilePath = ', p.DescFilePath     
                print 'PlatformName = ', p.PlatformName     
                print 'Guid = ', p.Guid                     
                print 'Version = ', p.Version
                print 'OutputDirectory = ', p.OutputDirectory                
                print 'FlashDefinition = ', p.FlashDefinition
                print 'SkuIds = ', p.SkuIds
                print 'Modules = ', p.Modules
                print 'LibraryClasses = ', p.LibraryClasses 
                print 'Pcds = ', p.Pcds
                for item in p.Pcds.keys():
                    print p.Pcds[item]
                print 'BuildOptions = ', p.BuildOptions
                print ''   
            # End of Platform
        
            print 'package'
            for package in ewb.Build[arch].PackageDatabase.keys():
                p = ewb.Build[arch].PackageDatabase[package]
                print 'DescFilePath = ', p.DescFilePath    
                print 'PackageName = ', p.PackageName     
                print 'Guid = ', p.Guid                    
                print 'Version = ', p.Version             
                print 'Protocols = ', p.Protocols         
                print 'Ppis = ', p.Ppis                    
                print 'Guids = ', p.Guids                 
                print 'Includes = ', p.Includes            
                print 'LibraryClasses = ', p.LibraryClasses
                print 'Pcds = ', p.Pcds
                for item in p.Pcds.keys():
                    print p.Pcds[item]
                print ''                    
            # End of Package
            
            print 'module'
            for module in ewb.Build[arch].ModuleDatabase.keys():
                p = ewb.Build[arch].ModuleDatabase[module]
                print 'DescFilePath = ', p.DescFilePath                    
                print 'BaseName = ', p.BaseName                         
                print 'ModuleType = ', p.ModuleType                     
                print 'Guid = ', p.Guid                                 
                print 'Version = ', p.Version
                print 'CustomMakefile = ', p.CustomMakefile
                print 'Specification = ', p.Specification
                print 'PcdIsDriver = ', p.PcdIsDriver
                if p.LibraryClass != None:
                    print 'LibraryClass = ', p.LibraryClass.LibraryClass, 'SupModList = ', p.LibraryClass.SupModList
                print 'ModuleEntryPointList = ', p.ModuleEntryPointList 
                print 'ModuleUnloadImageList = ', p.ModuleUnloadImageList
                print 'ConstructorList = ', p.ConstructorList            
                print 'DestructorList = ', p.DestructorList             
                                                                         
                print 'Binaries = '
                for item in p.Binaries:
                    print item.BinaryFile, item.FeatureFlag
                print 'Sources = '
                for item in p.Sources:
                    print item.SourceFile
                print 'LibraryClasses = ', p.LibraryClasses             
                print 'Protocols = ', p.Protocols                        
                print 'Ppis = ', p.Ppis                                 
                print 'Guids = ', p.Guids                                
                print 'Includes = ', p.Includes                         
                print 'Packages = ', p.Packages                         
                print 'Pcds = ', p.Pcds
                for item in p.Pcds.keys():
                    print p.Pcds[item]
                print 'BuildOptions = ', p.BuildOptions
                print 'Depex = ', p.Depex
                print ''
            # End of Module    

#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    # Nothing to do here. Could do some unit tests.
    w = os.getenv('WORKSPACE')
    ewb = WorkspaceBuild('Nt32Pkg/Nt32Pkg.dsc', w)
    ewb.GenBuildDatabase({'gEfiMdeModulePkgTokenSpaceGuid' : 'KKKKKKKKKKKKKKKKKKKKK'})
    ewb.ShowWorkspaceBuild()
