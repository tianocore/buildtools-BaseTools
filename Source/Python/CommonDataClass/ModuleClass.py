# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a module
#

from CommonClass import *

class ModuleHeaderClass(IdentificationClass, CommonHeaderClass, DefineClass):
    def __init__(self):
        IdentificationClass.__init__(self)
        CommonHeaderClass.__init__(self)
        DefineClass.__init__(self)
        self.ModuleType = ''
        self.SupArchList = []                       #EBC | IA32 | X64 | IPF | ARM | PPC
        self.BinaryModule = False
        self.OutputFileBasename = ''
        self.ClonedFrom = []                        #[ ClonedRecordClass, ...]
        self.PcdIsDriver = ''                       #PEI_PCD_DRIVER | DXE_PCD_DRIVER
        self.TianoR8FlashMap_h = False
        self.InfVersion = ''
        self.EfiSpecificationVersion = ''
        self.EdkReleaseVersion = ''
        self.LibraryClass = []                      #[ LibraryClass, ...]
        self.ComponentType = ''                     #LIBRARY | SECURITY_CORE | PEI_CORE | COMBINED_PEIM_DRIVER | PIC_PEIM | RELOCATABLE_PEIM | BS_DRIVER | RT_DRIVER | SAL_RT_DRIVER | APPLICATION
        self.MakefileName = ''
        self.BuildNumber = ''
        self.BuildType = ''
        self.FfsExt = ''
        self.FvExt = ''
        self.SourceFv = ''
        self.CustomMakefile = ''
        
class ModuleSourceFileClass(CommonClass):
    def __init__(self):
        self.SourceFile = ''
        self.TagName = ''
        self.ToolCode = ''
        self.ToolChainFamily = ''
        CommonClass.__init__(self)

class ModuleBinaryFileClass(CommonClass):
    def __init__(self):
        self.BinaryFile = ''
        self.FileType = ''                          #FW | GUID | PREEFORM | UEFI_APP | UNI_UI | UNI_VER | LIB | PE32 | PIC | PEI_DEPEX | DXE_DEPEX | TE | VER | UI | BIN | FV
        self.Target = ''
        CommonClass.__init__(self)
        
class ModulePackageDependencyClass(CommonClass, DefineClass):
    def __init__(self):
        self.FilePath = ''
        self.PackageName = ''
        self.PackageVersion = ''
        self.PackageGuid = ''
        CommonClass.__init__(self)
        DefineClass.__init__(self)       
        
class ModuleLibraryClass(CommonClass):
    def __init__(self):
        self.Library = ''
        CommonClass.__init__(self)
        
class ModuleEventClass(CommonClass):        
    def __init__(self):
        self.CName = ''
        self.GuidCName = ''
        self.Type = ''                              #CREATE_EVENT | SIGNAL_EVENT
        CommonClass.__init__(self)
        
class ModuleHobClass(CommonClass):
    def __init__(self):
        self.Type = ''                              #PHIT | MEMORY_ALLOCATION | RESOURCE_DESCRIPTOR | GUID_EXTENSION | FIRMWARE_VOLUME | CPU | POOL | CAPSULE_VOLUME
        self.GuidCName = ''
        CommonClass.__init__(self)
        
class ModuleVariableClass(CommonClass):
    def __init__(self):
        self.Name = ''
        self.GuidCName = ''
        CommonClass.__init__(self)

class ModuleBootModeClass(CommonClass):
    def __init__(self):
        self.Name = ''                              #FULL | MINIMAL | NO_CHANGE | DIAGNOSTICS | DEFAULT | S2_RESUME | S3_RESUME | S4_RESUME | S5_RESUME | FLASH_UPDATE | RECOVERY_FULL | RECOVERY_MINIMAL | RECOVERY_NO_CHANGE | RECOVERY_DIAGNOSTICS | RECOVERY_DEFAULT | RECOVERY_S2_RESUME | RECOVERY_S3_RESUME | RECOVERY_S4_RESUME | RECOVERY_S5_RESUME | RECOVERY_FLASH_UPDATE 
        CommonClass.__init__(self)
        
class ModuleSystemTableClass(CommonClass):
    def __init__(self):
        self.CName = ''
        CommonClass.__init__(self)

class ModuleDataHubClass(CommonClass):
    def __init__(self):
        self.CName = ''
        CommonClass.__init__(self)        

class ModuleHiiPackageClass(CommonClass):
    def __init__(self):
        self.CName = ''
        CommonClass.__init__(self)
        
class ModuleExternImageClass(object):
    def __init__(self):
        self.ModuleEntryPoint = ''
        self.ModuleUnloadImage = ''

class ModuleExternLibraryClass(object):
    def __init__(self):
        self.Constructor = ''
        self.Destructor = ''

class ModuleExternDriverClass(object):
    def __init__(self):
        self.DriverBinding= ''
        self.ComponentName = ''
        self.DriverConfig = ''
        self.DriverDiag = ''

class ModuleExternCallBackClass(object):
    def __init__(self):
        self.SetVirtualAddressMapCallBack = ''
        self.ExitBootServicesCallBack = ''
        
class ModuleClass(object):
    def __init__(self):
        self.Header = ModuleHeaderClass()
        self.LibraryClasses = []                    #[ LibraryClassClass, ...]
        self.Libraries = []                         #[ ModuleLibraryClass, ...]
        self.Sources = []                           #[ ModuleSourceFilesClass, ...]
        self.Binaries = []                          #[ ModuleBinaryFilesClass, ...]
        self.NonProcessedFiles = []                 #[ '', '', ...]
        self.PackageDependencies = []               #[ ModulePackageDependencyClass, ... ] 
        self.Nmake = {}                             #{ Name : Value, ... }
        self.Depex = []                             #[ '', '', ... ]
        self.Includes = []                          #[ IncludeClass, ...]
        self.Protocols = []                         #[ ProtocolClass, ...]
        self.Ppis = []                              #[ PpiClass, ...]
        self.Events = []                            #[ ModuleEventClass, ...]
        self.Hobs = []                              #[ ModuleHobClass, ...] 
        self.Variables = []                         #[ ModuleVariableClass, ...]
        self.BootModes = []                         #[ ModuleBootModeClass, ...]
        self.SystemTables = []                      #[ ModuleSystemTableClass, ...]
        self.DataHubs = []                          #[ ModuleDataHubClass, ...]
        self.HiiPackages = []                       #[ ModuleHiiPackageClass, ...]
        self.Guids = []                             #[ GuidClass, ...]
        self.PcdCodes = []                          #[ TokenSpaceGuidCName)] : PcdClass, ...]
        self.ExternImages = []                      #[ ModuleExternImageClass, ...]
        self.ExternLibraries = []                   #[ ModuleExternLibraryClass, ...]
        self.ExternDrivers = []                     #[ ModuleExternDriverClass, ...]
        self.ExternCallBacks = []                   #[ ModuleExternCallBackClass, ...]                
        self.BuildOptions = []                      #[ BuildOptionClass, ...]
        self.UserExtensions = []                    #[ UserExtensionsClass, ...]

if __name__ == '__main__':
    m = ModuleClass()
