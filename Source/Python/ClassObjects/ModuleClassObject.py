# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a module
#

from CommonClassObject import *

class ModuleHeaderClassObject(IdentificationClassObject, CommonHeaderClassObject):
  def __init__(self):
    IdentificationClassObject.__init__(self)
    CommonHeaderClassObject.__init__(self)
    self.ModuleType = ''
    self.SupArchList = []                             #EBC | IA32 | X64 | IPF | ARM | PPC
    self.BinaryModule = False
    self.OutputFileBasename = ''
    self.ClonedFrom = []                              #[ ClonedRecordClassObject, ...]
    self.PcdIsDriver = ''                             #PEI_PCD_DRIVER | DXE_PCD_DRIVER
    self.TianoR8FlashMap_h = False
    
class ModuleSourceFileClassObject(CommonClassObject):
  def __init__(self):
    self.SourceFile = ''
    self.TagName = ''
    self.ToolCode = ''
    self.ToolChainFamily = ''
    CommonClassObject.__init__(self)
    
class ModulePackageDependencyClassObject(CommonClassObject):
  def __init__(self):
    self.FilePath = ''
    self.PackageName = ''
    self.PackageVersion = ''
    self.PackageGuid = ''
    CommonClassObject.__init__(self)
    
class ModuleEventClassObject(CommonClassObject):    
  def __init__(self):
    self.CName = ''
    self.GuidCName = ''
    self.Type = ''                                     #CREATE_EVENT | SIGNAL_EVENT
    CommonClassObject.__init__(self)
    
class ModuleHobClassObject(CommonClassObject):
  def __init__(self):
    self.Type = ''                                     #PHIT | MEMORY_ALLOCATION | RESOURCE_DESCRIPTOR | GUID_EXTENSION | FIRMWARE_VOLUME | CPU | POOL | CAPSULE_VOLUME
    self.GuidCName = ''
    CommonClassObject.__init__(self)
    
class ModuleVariableClassObject(CommonClassObject):
  def __init__(self):
    self.Name = ''
    self.GuidCName = ''
    CommonClassObject.__init__(self)

class ModuleBootModeClassObject(CommonClassObject):
  def __init__(self):
    self.Name = ''                                     #FULL | MINIMAL | NO_CHANGE | DIAGNOSTICS | DEFAULT | S2_RESUME | S3_RESUME | S4_RESUME | S5_RESUME | FLASH_UPDATE | RECOVERY_FULL | RECOVERY_MINIMAL | RECOVERY_NO_CHANGE | RECOVERY_DIAGNOSTICS | RECOVERY_DEFAULT | RECOVERY_S2_RESUME | RECOVERY_S3_RESUME | RECOVERY_S4_RESUME | RECOVERY_S5_RESUME | RECOVERY_FLASH_UPDATE 
    CommonClassObject.__init__(self)
    
class ModuleSystemTableClassObject(CommonClassObject):
  def __init__(self):
    self.CName = ''
    CommonClassObject.__init__(self)

class ModuleDataHubClassObject(CommonClassObject):
  def __init__(self):
    self.CName = ''
    CommonClassObject.__init__(self)    

class ModuleHiiPackageClassObject(CommonClassObject):
  def __init__(self):
    self.CName = ''
    CommonClassObject.__init__(self)
    
class ModuleExternImageClassObject(object):
  def __init__(self):
    self.ModuleEntryPoint = ''
    self.ModuleUnloadImage = ''

class ModuleExternLibraryClassObject(object):
  def __init__(self):
    self.Constructor = ''
    self.Destructor = ''

class ModuleExternDriverClassObject(object):
  def __init__(self):
    self.DriverBinding= ''
    self.ComponentName = ''
    self.DriverConfig = ''
    self.DriverDiag = ''

class ModuleExternCallBackClassObject(object):
  def __init__(self):
    self.SetVirtualAddressMapCallBack = ''
    self.ExitBootServicesCallBack = ''
    
class ModuleClassObject(object):
  def __init__(self):
    self.Header = ModuleHeaderClassObject()
    self.LibraryClasses = []                           #[ LibraryClassClassObject, ...]
    self.Sources = []                                  #[ ModuleSourceFileClassObject, ...]
    self.NonProcessedFiles = []                        #[ '', '', ...]
    self.PackageDependencies = []                      #[ PackageDependencyClassObject, ...]
    self.Protocols = []                                #[ ProtocolClassObject, ...]
    self.Ppis = []                                     #[ PpiClassObject, ...]
    self.Events = []                                   #[ ModuleEventClassObject, ...]
    self.Hobs = []                                     #[ ModuleHobClassObject, ...] 
    self.Variables = []                                #[ ModuleVariableClassObject, ...]
    self.BootModes = []                                #[ ModuleBootModeClassObject, ...]
    self.SystemTables = []                             #[ ModuleSystemTableClassObject, ...]
    self.DataHubs = []                                 #[ ModuleDataHubClassObject, ...]
    self.HiiPackages = []                              #[ ModuleHiiPackageClassObject, ...]
    self.Guids = []                                    #[ GuidClassObject, ...]
    self.PcdCodes = []                                 #[ TokenSpaceGuidCName)] : PcdClassObject, ...]
    self.ExternImages = []                             #[ ModuleExternImageClassObject, ...]
    self.ExternLibraries = []                          #[ ModuleExternLibraryClassObject, ...]
    self.ExternDrivers = []                            #[ ModuleExternDriverClassObject, ...]
    self.ExternCallBacks = []                          #[ ModuleExternCallBackClassObject, ...]        
    self.BuildOptions = []                             #[ BuildOptionClassObject, ...]
    self.UserExtensions = []                           #[ UserExtensionsClassObject, ...]

if __name__ == '__main__':
  m = ModuleClassObject()
