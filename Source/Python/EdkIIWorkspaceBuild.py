# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
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
from EdkIIWorkspace import *
from TargetTxtClassObject import *
from ToolDefClassObject import *
from InfClassObject import *
from DecClassObject import *
from DscClassObject import *
from String import *

class ModuleSourceFilesClassObject(object):
  def __init__(self, Item):
    self.SourceFile            = Item
    self.TagName               = ''
    self.ToolCode              = ''
    self.ToolChainFamily       = ''
    
class PcdClassObject(object):
  def __init__(self, Name = None, Guid = None, Type = None, DatumType = None, Value = None, Token = None, MaxDatumSize = None):
    self.TokenCName = Name
    self.TokenSpaceGuidCName = Guid
    self.Type = Type
    self.DatumType = DatumType
    self.DefaultValue = Value
    self.TokenValue = Token
    self.MaxDatumSize = MaxDatumSize

class LibraryClassObject(object):
  def __init__(self, Name = None, Type = None):
    self.LibraryClass = Name
    self.SupModList = []
    if Type != None:
      self.SupModList = CleanString(Type).split(DataType.TAB_SPACE_SPLIT)
    
class ModuleBuildClassObject(object):
  def __init__(self):
    self.DescFilePath          = ''
    self.BaseName              = ''
    self.ModuleType            = ''
    self.Guid                  = ''
    self.Version               = ''
    self.Specification         = ''
    self.LibraryClass          = None      # LibraryClassObject
    self.ModuleEntryPointList  = []
    self.ModuleUnloadImageList = []
    self.ConstructorList       = []
    self.DestructorList        = []
    
    self.Sources               = []        #[ SourcesClassObject, ... ]
    self.LibraryClasses        = {}        #{ [LibraryClassName, ModuleType] : LibraryClassInfFile }
    self.Protocols             = []        #[ ProtocolName, ... ]
    self.Ppis                  = []        #[ PpiName, ... ]
    self.Guids                 = []        #[ GuidName, ... ]
    self.Includes              = []        #[ IncludePath, ... ]
    self.Packages              = []        #[ DecFileName, ... ]
    self.Pcds                  = {}        #{ [(PcdCName, PcdGuidCName)] : PcdClassObject}
    self.BuildOptions          = {}        #{ [BuildOptionKey] : BuildOptionValue}

  def __str__(self):
    return self.DescFilePath

  def __eq__(self, other):
    return self.DescFilePath == other.DescFilePath

  def __hash__(self):
    return hash(self.DescFilePath)

class PackageBuildClassObject(object):
  def __init__(self):
    self.DescFilePath          = ''
    self.PackageName           = ''
    self.Guid                  = ''
    self.Version               = ''
    
    self.Protocols             = {}        #{ [ProtocolName] : Protocol Guid, ... }
    self.Ppis                  = {}        #{ [PpiName] : Ppi Guid, ... }
    self.Guids                 = {}        #{ [GuidName] : Guid, ... }
    self.Includes              = []        #[ IncludePath, ... ]    
    self.LibraryClasses        = {}        #{ [LibraryClassName] : LibraryClassInfFile }
    self.Pcds                  = {}        #{ [(PcdCName, PcdGuidCName)] : PcdClassObject}
    
  def __str__(self):
    return self.DescFilePath

  def __eq__(self, other):
    return self.DescFilePath == other.DescFilePath

  def __hash__(self):
    return hash(self.DescFilePath)

class PlatformBuildClassObject(object):
  def __init__(self):
    self.DescFilePath          = ''
    self.PlatformName          = ''
    self.Guid                  = ''
    self.Version               = ''
    self.OutputDirectory       = ''
    
    self.Modules               = []        #[ InfFileName, ... ]
    self.LibraryClasses        = {}        #{ (LibraryClassName, ModuleType) : LibraryClassInfFile }
    self.Pcds                  = {}        #{ [(PcdCName, PcdGuidCName)] : PcdClassObject }
    self.BuildOptions          = {}        #{ [BuildOptionKey] : BuildOptionValue }  

  def __str__(self):
    return self.DescFilePath

  def __eq__(self, other):
    return self.DescFilePath == other.DescFilePath

  def __hash__(self):
    return hash(self.DescFilePath)

class ItemBuild(object):
  def __init__(self, arch, platform = None, package = None, module = None):
    self.Arch                  = arch
    self.PlatformDatabase      = {}        #{ [DscFileName] : PlatformBuildClassObject, ...}
    self.PackageDatabase       = {}        #{ [DecFileName] : PacakgeBuildClassObject, ...}
    self.ModuleDatabase        = {}        #{ [InfFileName] : ModuleBuildClassObject, ...}
    
class WorkspaceBuild(object):
  def __init__(self):
    self.Workspace              = EdkIIWorkspace()
    self.PrintRunTime           = True
    self.PlatformBuild          = True
    self.TargetTxt              = TargetTxtClassObject()
    self.ToolDef                = ToolDefClassObject()
    self.InfDatabase            = {}       #{ [InfFileName] : InfClassObject}    
    self.DecDatabase            = {}       #{ [DecFileName] : DecClassObject}
    self.DscDatabase            = {}       #{ [DscFileName] : DscClassObject}
    
    self.Build                  = {}
    for key in DataType.ARCH_LIST:
      self.Build[key] = ItemBuild(key)
    
    self.TargetTxt.LoadTargetTxtFile(self.Workspace.WorkspaceFile('Tools/Conf/target.txt'))
    self.ToolDef.LoadToolDefFile(self.Workspace.WorkspaceFile('Tools/Conf/tools_def.txt'))
    
    #get active platform
    dscFileName = NormPath(self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM][0])
    file = self.Workspace.WorkspaceFile(dscFileName)
    if os.path.exists(file) and os.path.isfile(file):
      self.DscDatabase[dscFileName] = Dsc(file, True)
    else:
      EdkLogger.error('No Active Platform')
      return
    
    #parse platform to get module
    for dsc in self.DscDatabase.keys():
      dscObj = self.DscDatabase[dsc]
      #Get all inf
      for key in DataType.ARCH_LIST:
        for index in range(len(dscObj.Contents[key].LibraryClasses)):
          self.AddToInfDatabase(dscObj.Contents[key].LibraryClasses[index][0].split(DataType.TAB_VALUE_SPLIT, 1)[1])
        for index in range(len(dscObj.Contents[key].Components)):
          self.AddToInfDatabase(dscObj.Contents[key].Components[index][0])
        
    #End For of Dsc
    
    #parse module to get package
    for inf in self.InfDatabase.keys():
      infObj = self.InfDatabase[inf]
      #Get all dec
      for key in DataType.ARCH_LIST:
        for index in range(len(infObj.Contents[key].Packages)):
          self.AddToDecDatabase(infObj.Contents[key].Packages[index])
    
    #Build databases
    #Build PlatformDatabase
    for dsc in self.DscDatabase.keys():
      dscObj = self.DscDatabase[dsc]
      
      for key in DataType.ARCH_LIST:
        pb = PlatformBuildClassObject()
        pb.DescFilePath = dsc
        pb.PlatformName = dscObj.Defines.DefinesDictionary[DataType.TAB_DSC_DEFINES_PLATFORM_NAME]
        pb.Guid = dscObj.Defines.DefinesDictionary[DataType.TAB_DSC_DEFINES_PLATFORM_GUID]
        pb.Version = dscObj.Defines.DefinesDictionary[DataType.TAB_DSC_DEFINES_PLATFORM_VERSION]
        pb.OutputDirectory = NormPath(dscObj.Defines.DefinesDictionary[DataType.TAB_DSC_DEFINES_OUTPUT_DIRECTORY])
      
        #Module
        for index in range(len(dscObj.Contents[key].Components)):
          pb.Modules.append(NormPath(dscObj.Contents[key].Components[index][0]))
        
        #BuildOptions
        for index in range(len(dscObj.Contents[key].BuildOptions)):
          b = desObj.Contents[key].BuildOptions[index]
          pb.BuildOptions[CleanString(b.split(DataType.TAB_EQUAL_SPLIT)[0])] = CleanString(b.split(DataType.TAB_EQUAL_SPLIT)[1])
          
        #LibraryClass
        for index in range(len(dscObj.Contents[key].LibraryClasses)):
          #['DebugLib|MdePkg/Library/PeiDxeDebugLibReportStatusCode/PeiDxeDebugLibReportStatusCode.inf', 'DXE_CORE']
          list = dscObj.Contents[key].LibraryClasses[index][0].split(DataType.TAB_VALUE_SPLIT, 1)
          type = dscObj.Contents[key].LibraryClasses[index][1]
          pb.LibraryClasses[(list[0], type)] = NormPath(list[1])

        #Pcds
        for index in range(len(dscObj.Contents[key].PcdsFixedAtBuild)):
          pcd = dscObj.Contents[key].PcdsFixedAtBuild[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_FIXED_AT_BUILD, None, pcd[2], None, None)
        for index in range(len(dscObj.Contents[key].PcdsPatchableInModule)):
          pcd = dscObj.Contents[key].PcdsPatchableInModule[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_PATCHABLE_IN_MODULE, None, pcd[2], None, None)
        for index in range(len(dscObj.Contents[key].PcdsFeatureFlag)):
          pcd = dscObj.Contents[key].PcdsFeatureFlag[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_FEATURE_FLAG, None, pcd[2], None, None)
        for index in range(len(dscObj.Contents[key].PcdsDynamic)):
          pcd = dscObj.Contents[key].PcdsDynamic[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC, None, pcd[2], None, None)
        for index in range(len(dscObj.Contents[key].PcdsDynamicEx)):
          pcd = dscObj.Contents[key].PcdsDynamicEx[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC_EX, None, pcd[2], None, None)
        
        self.Build[key].PlatformDatabase[dsc] = pb
        pb = None  
      #End of Arch List Go Through  
        
    #End of Dsc Go Through
    
    #End of build PlatformDatabase
    
    #Build PackageDatabase
    for dec in self.DecDatabase.keys():
      decObj = self.DecDatabase[dec]

      for key in DataType.ARCH_LIST:
        pb = PackageBuildClassObject()
        #Defines
        pb.DescFilePath = dec
        pb.PackageName = decObj.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_NAME]
        pb.Guid = decObj.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_GUID]
        pb.Version = decObj.Defines.DefinesDictionary[TAB_DEC_DEFINES_PACKAGE_VERSION]
        
        #Protocols
        for index in range(len(decObj.Contents[key].Protocols)):
          list = decObj.Contents[key].Protocols[index].split(DataType.TAB_EQUAL_SPLIT)
          pb.Protocols[CleanString(list[0])] = CleanString(list[1])

        #Ppis
        for index in range(len(decObj.Contents[key].Ppis)):
          list = decObj.Contents[key].Ppis[index].split(DataType.TAB_EQUAL_SPLIT)
          pb.Ppis[CleanString(list[0])] = CleanString(list[1])      

        #Guids
        for index in range(len(decObj.Contents[key].Guids)):
          list = decObj.Contents[key].Guids[index].split(DataType.TAB_EQUAL_SPLIT)
          pb.Guids[CleanString(list[0])] = CleanString(list[1])    
        
        #Includes
        for index in range(len(decObj.Contents[key].Includes)):
          pb.Includes.append(NormPath(decObj.Contents[key].Includes[index]))
      
        #LibraryClasses
        for index in range(len(decObj.Contents[key].LibraryClasses)):
          list = decObj.Contents[key].LibraryClasses[index].split(DataType.TAB_VALUE_SPLIT)
          pb.LibraryClasses[CleanString(list[0])] = NormPath(CleanString(list[1]))
                        
        #Pcds
        for index in range(len(decObj.Contents[key].PcdsFixedAtBuild)):
          pcd = decObj.Contents[key].PcdsFixedAtBuild[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[2])] = PcdClassObject(pcd[0], pcd[2], DataType.TAB_PCDS_FIXED_AT_BUILD, pcd[3], pcd[4], pcd[1], None)
        for index in range(len(decObj.Contents[key].PcdsPatchableInModule)):
          pcd = decObj.Contents[key].PcdsPatchableInModule[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[2])] = PcdClassObject(pcd[0], pcd[2], DataType.TAB_PCDS_PATCHABLE_IN_MODULE, pcd[3], pcd[4], pcd[1], None)
        for index in range(len(decObj.Contents[key].PcdsFeatureFlag)):
          pcd = decObj.Contents[key].PcdsFeatureFlag[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[2])] = PcdClassObject(pcd[0], pcd[2], DataType.TAB_PCDS_FEATURE_FLAG, pcd[3], pcd[4], pcd[1], None)
        for index in range(len(decObj.Contents[key].PcdsDynamic)):
          pcd = decObj.Contents[key].PcdsDynamic[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[2])] = PcdClassObject(pcd[0], pcd[2], DataType.TAB_PCDS_DYNAMIC, pcd[3], pcd[4], pcd[1], None)
        for index in range(len(decObj.Contents[key].PcdsDynamicEx)):
          pcd = decObj.Contents[key].PcdsDynamicEx[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[2])] = PcdClassObject(pcd[0], pcd[2], DataType.TAB_PCDS_DYNAMIC_EX, pcd[3], pcd[4], pcd[1], None)
      
        #Add to database
        self.Build[key].PackageDatabase[dec] = pb
        pb = None  
      #End of Arch List Go Through
    
    #End of Dec Go Through  
    
    #End of build PackageDatabase
  
    #Build ModuleDatabase
    for inf in self.InfDatabase.keys():
      infObj = self.InfDatabase[inf]
      
      for key in DataType.ARCH_LIST:
        #Defines
        pb = ModuleBuildClassObject()
        pb.DescFilePath = inf
        pb.BaseName = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_BASE_NAME]
        pb.Guid = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_FILE_GUID]
        pb.Version = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_VERSION_STRING]
        pb.ModuleType = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_MODULE_TYPE]
        pb.Specification = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_EFI_SPECIFICATION_VERSION]
        
        LibraryClass = infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_LIBRARY_CLASS]
        if LibraryClass != '':
          l = LibraryClass.split(DataType.TAB_VALUE_SPLIT)
          if len(l) == 2:
            pb.LibraryClass = LibraryClassObject(l[0], l[1])
          elif len(l) == 1:
            pb.LibraryClass = LibraryClassObject(l[0], DataType.SUP_MODULE_LIST_STRING)

        pb.ModuleEntryPointList.extend(infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_ENTRY_POINT])
        pb.ModuleUnloadImageList.extend(infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_UNLOAD_IMAGE])
        pb.ConstructorList.extend(infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_CONSTRUCTOR])
        pb.DestructorList.extend(infObj.Defines.DefinesDictionary[TAB_INF_DEFINES_DESTRUCTOR])

        #Sources
        for index in range(len(infObj.Contents[key].Sources)):
          pb.Sources.append(ModuleSourceFilesClassObject(NormPath(infObj.Contents[key].Sources[index])))

        #Protocols
        for index in range(len(infObj.Contents[key].Protocols)):
          pb.Protocols.append(infObj.Contents[key].Protocols[index])
      
        #Ppis
        for index in range(len(infObj.Contents[key].Ppis)):
          pb.Ppis.append(infObj.Contents[key].Ppis[index])
                
        #Guids
        for index in range(len(infObj.Contents[key].Guids)):
          pb.Guids.append(infObj.Contents[key].Guids[index])
      
        #Includes
        for index in range(len(infObj.Contents[key].Includes)):
          pb.Includes.append(NormPath(infObj.Contents[key].Includes[index]))
      
        #Packages
        for index in range(len(infObj.Contents[key].Packages)):
          pb.Packages.append(NormPath(infObj.Contents[key].Packages[index]))
          
        #BuildOptions
        for index in range(len(infObj.Contents[key].BuildOptions)):
          b = infObj.Contents[key].BuildOptions[index]
          pb.BuildOptions[CleanString(b.split(DataType.TAB_EQUAL_SPLIT)[0])] = CleanString(b.split(DataType.TAB_EQUAL_SPLIT)[1])
        self.FindBuildOptions(key, inf, pb.BuildOptions)
        
        #LibraryClasses
        for index in range(len(infObj.Contents[key].LibraryClasses)):
          #Get LibraryClass name and default instance if existing
          list = infObj.Contents[key].LibraryClasses[index].split(DataType.TAB_VALUE_SPLIT)
          if len(list) < 2:
            v = ''
          else:
            v = list[1]
          
          if pb.LibraryClass != None:
            #For Library
            for type in pb.LibraryClass.SupModList:
              instance = self.FindLibraryClassInstanceOfLibrary(CleanString(list[0]), key, type)
              if instance != None:
                v = instance
                pb.LibraryClasses[(CleanString(list[0]), type)] = NormPath(CleanString(v))
          else:
            #For Module            
            instance = self.FindLibraryClassInstanceOfModule(CleanString(list[0]), key, pb.ModuleType, inf) 
            if instance != None:
              v = instance
              pb.LibraryClasses[(CleanString(list[0]), pb.ModuleType)] = NormPath(CleanString(v))

        #Pcds
        for index in range(len(infObj.Contents[key].PcdsFixedAtBuild)):
          pcd = infObj.Contents[key].PcdsFixedAtBuild[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = self.FindPcd(key, pcd[0], pcd[1], DataType.TAB_PCDS_FIXED_AT_BUILD)
        for index in range(len(infObj.Contents[key].PcdsPatchableInModule)):
          pcd = infObj.Contents[key].PcdsPatchableInModule[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = self.FindPcd(key, pcd[0], pcd[1], DataType.TAB_PCDS_PATCHABLE_IN_MODULE)
          #pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_PATCHABLE_IN_MODULE, None, None, None, None)          
        for index in range(len(infObj.Contents[key].PcdsFeatureFlag)):
          pcd = infObj.Contents[key].PcdsFeatureFlag[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = self.FindPcd(key, pcd[0], pcd[1], DataType.TAB_PCDS_FEATURE_FLAG)
          #pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_FEATURE_FLAG, None, None, None, None)          
        for index in range(len(infObj.Contents[key].PcdsDynamic)):
          pcd = infObj.Contents[key].PcdsDynamic[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = self.FindPcd(key, pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC)
          #pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC, None, None, None, None)
        for index in range(len(infObj.Contents[key].PcdsDynamicEx)):
          pcd = infObj.Contents[key].PcdsDynamicEx[index].split(DataType.TAB_VALUE_SPLIT)
          pb.Pcds[(pcd[0], pcd[1])] = self.FindPcd(key, pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC_EX)
          #pb.Pcds[(pcd[0], pcd[1])] = PcdClassObject(pcd[0], pcd[1], DataType.TAB_PCDS_DYNAMIC_EX, None, None, None, None)
                    
        #Add to database
        self.Build[key].ModuleDatabase[inf] = pb
        pb = None  
      #End of Arch List Go Through
    
    #End of Inf Go Through
    
    #End of build ModuleDatabase  
  
  #End of self.Init
  
  def AddToInfDatabase(self, infFileName):
    infFileName = NormPath(infFileName)
    file = self.Workspace.WorkspaceFile(infFileName)
    if os.path.exists(file) and os.path.isfile(file):
      if infFileName not in self.InfDatabase:
        self.InfDatabase[infFileName] = Inf(file, True)
        
  def AddToDecDatabase(self, decFileName):
    decFileName = NormPath(decFileName)
    file = self.Workspace.WorkspaceFile(decFileName)
    if os.path.exists(file) and os.path.isfile(file):
      if decFileName not in self.DecDatabase:
        self.DecDatabase[decFileName] = Dec(file, True)
        
  def FindLibraryClassInstanceOfModule(self, lib, arch, moduleType, moduleName):
    for dsc in self.DscDatabase.keys():
      #First find if exist in <LibraryClass> of <Components> from dsc file      
      dscObj = self.DscDatabase[dsc]
      for index in range(len(dscObj.Contents[arch].Components)):
        if NormPath(dscObj.Contents[arch].Components[index][0]) == moduleName and len(dscObj.Contents[arch].Components[index][1]) > 0:
          #Search each library class
          LibList = dscObj.Contents[arch].Components[index][1]
          for indexOfLib in range(len(LibList)):
            if LibList[indexOfLib].split(DataType.TAB_VALUE_SPLIT)[0] == lib:
              return LibList[indexOfLib].split(DataType.TAB_VALUE_SPLIT)[1]
      
      #Second find if exist in <LibraryClass> of <LibraryClasses> from dsc file      
      if (lib, moduleType) in self.Build[arch].PlatformDatabase[dsc].LibraryClasses:
        return self.Build[arch].PlatformDatabase[dsc].LibraryClasses[(lib, moduleType)]
      elif (lib, None) in self.Build[arch].PlatformDatabase[dsc].LibraryClasses:
        return self.Build[arch].PlatformDatabase[dsc].LibraryClasses[(lib, None)]
      
  def FindLibraryClassInstanceOfLibrary(self, lib, arch, type):
    for dsc in self.DscDatabase.keys():
      dscObj = self.DscDatabase[dsc]
      if (lib, type) in self.Build[arch].PlatformDatabase[dsc].LibraryClasses:
        return self.Build[arch].PlatformDatabase[dsc].LibraryClasses[(lib, type)]
      elif (lib, None) in self.Build[arch].PlatformDatabase[dsc].LibraryClasses:
        return self.Build[arch].PlatformDatabase[dsc].LibraryClasses[(lib, None)]
      
  def FindBuildOptions(self, arch, moduleName, BuildOptions):
    for dsc in self.DscDatabase.keys():
      #First find if exist in <BuildOptions> of <Components> from dsc file
      dscObj = self.DscDatabase[dsc]
      for index in range(len(dscObj.Contents[arch].Components)):
        if NormPath(dscObj.Contents[arch].Components[index][0]) == moduleName and len(dscObj.Contents[arch].Components[index][2]) > 0:
          list = dscObj.Contents[arch].Components[index][2]
          for l in list:
            BuildOptions[CleanString(l.split(DataType.TAB_EQUAL_SPLIT)[0])] = CleanString(l.split(DataType.TAB_EQUAL_SPLIT)[1])
            
  def FindPcd(self, arch, CName, GuidCName, Type):
    DatumType = ''
    DefaultValue = ''
    TokenValue = ''
    MaxDatumSize = ''
    for dsc in self.Build[arch].PlatformDatabase.keys():
      platform = self.Build[arch].PlatformDatabase[dsc]
      pcds = platform.Pcds
      if (CName, GuidCName) in pcds:
        DatumType = pcds[(CName, GuidCName)].DatumType
        DefaultValue = pcds[(CName, GuidCName)].DefaultValue
        TokenValue = pcds[(CName, GuidCName)].TokenValue
        MaxDatumSize = pcds[(CName, GuidCName)].MaxDatumSize
        break

    for dec in self.Build[arch].PackageDatabase.keys():
      package = self.Build[arch].PackageDatabase[dec]
      pcds = package.Pcds
      if (CName, GuidCName) in pcds:
        DatumType = pcds[(CName, GuidCName)].DatumType
        #DefaultValue = pcds[(CName, GuidCName)].DefaultValue
        TokenValue = pcds[(CName, GuidCName)].TokenValue
        #MaxDatumSize = pcds[(CName, GuidCName)].MaxDatumSize
        break
    
    return PcdClassObject(CName, GuidCName, Type, DatumType, DefaultValue, TokenValue, MaxDatumSize)
        
        
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':

  # Nothing to do here. Could do some unit tests.
  ewb = WorkspaceBuild()
  #printDict(ewb.TargetTxt.TargetTxtDictionary)
  #printDict(ewb.ToolDef.ToolsDefTxtDictionary)
#  print ewb.DscDatabase
#  print ewb.InfDatabase
#  print ewb.DecDatabase
  
  #
  for arch in DataType.ARCH_LIST:
    print arch
    print 'Platform'
    for platform in ewb.Build[arch].PlatformDatabase.keys():
      p = ewb.Build[arch].PlatformDatabase[platform]
      print p.DescFilePath   
      print p.PlatformName   
      print p.Guid           
      print p.Version
      print p.OutputDirectory        
      print p.Modules        
      print p.LibraryClasses 
      print p.Pcds           
      print p.BuildOptions   
    #End of Platform
  
    print 'package'
    for package in ewb.Build[arch].PackageDatabase.keys():
      p = ewb.Build[arch].PackageDatabase[package]
      print p.DescFilePath  
      print p.PackageName   
      print p.Guid          
      print p.Version       
      print p.Protocols     
      print p.Ppis          
      print p.Guids         
      print p.Includes      
      print p.LibraryClasses
      print p.Pcds          
    #End of Package
    
    print 'module'
    for module in ewb.Build[arch].ModuleDatabase.keys():
      p = ewb.Build[arch].ModuleDatabase[module]
      print p.DescFilePath          
      print p.BaseName             
      print p.ModuleType           
      print p.Guid                 
      print p.Version
      print p.Specification
      if p.LibraryClass != None:
        print p.LibraryClass.LibraryClass
        print p.LibraryClass.SupModList
      print p.ModuleEntryPointList 
      print p.ModuleUnloadImageList
      print p.ConstructorList      
      print p.DestructorList       
                                   
      print p.Sources              
      print p.LibraryClasses       
      print p.Protocols            
      print p.Ppis                 
      print p.Guids                
      print p.Includes             
      print p.Packages             
      print p.Pcds                 
      print p.BuildOptions
    #End of Module  
      
  #End of Arch List
