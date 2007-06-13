# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a platform
#

from CommonClassObject import *

class PlatformSkuInfoClassObject(object):
  def __init__(self):
    self.SkuId = ''
    self.String = ''

class PlatformHeaderClassObject(IdentificationClassObject, CommonHeaderClassObject):
  def __init__(self):
    IdentificationClassObject.__init__(self)
    CommonHeaderClassObject.__init__(self)
    self.SupArchList = []                              #EBC | IA32 | X64 | IPF | ARM | PPC
    self.BuildTargets = []                             #RELEASE | DEBUG
    self.IntermediateDirectories = ''                  #MODULE | UNIFIED
    self.OutputDirectory = ''                          
    self.ForceDebugTarget = ''
    self.ClonedFrom = []                               #[ ClonedRecordClassObject, ...]

class PlatformFlashDefinitionFileClassObject(object):
  def __init__(self):
    self.Id = ''
    self.UiName = ''
    self.Preferred = False
    self.FilePath = ''

class PlatformFvImageOption(object):
  def __init__(self):
    self.FvImageOptionName = ''
    self.FvImageOptionValues = []
    
class PlatformFvImageClassObject(object):
  def __init__(self):
    self.Name = ''
    self.Value = ''
    self.Type = ''                                     #Attributes | Options | Components | ImageName 
    self.FvImageNames = []
    self.FvImageOptions = []                           #[ PlatformFvImageOption, ...]

class PlatformFvImageNameClassObject(object):
  def __init__(self):
    self.Name = ''
    self.Type = ''                                     #FV_MAIN | FV_MAIN_COMPACT | NV_STORAGE | FV_RECOVERY | FV_RECOVERY_FLOPPY | FV_FILE | CAPSULE_CARGO | NULL | USER_DEFINED 
    self.FvImageOptions = []                           #[ PlatformFvImageOption, ...]
    
class PlatformFvImagesClassObject(object):
  def __init__(self):
    self.FvImages1 = []                                #[ PlatformFvImageClassObject, ...]
    self.FvImages2 = []                                #[ PlatformFvImageNameClassObject, ...]

class PlatformAntTaskClassObject(object):
  def __init__(self):
    self.Id = ''
    self.AntCmdOptions = ''
    self.FilePath = ''

class PlatformFfsSectionClassObject(CommonClassObject):
  def __init__(self):
    CommonClassObject.__init__(self)
    self.BindingOrder        = ''
    self.Compressible        = ''
    self.SectionType         = ''
    self.EncapsulationType   = ''
    self.ToolName            = ''
    self.Filenames = []
    self.Args                = ''
    self.OutFile             = ''
    self.OutputFileExtension = ''
    self.ToolNameElement     = ''
    
class PlatformFfsSectionsClassObject(CommonClassObject):
  def __init__(self):
    CommonClassObject.__init__(self)    
    self.BindingOrder      = ''
    self.Compressible      = ''
    self.SectionType       = ''
    self.EncapsulationType = ''
    self.ToolName          = ''
    self.Section = []                                  #[ PlatformFfsSectionClassObject, ... ]
    self.Sections = []                                 #[ PlatformFfsSectionsClassObject, ...]
    
class PlatformFfsClassObject(object):
  def __init__(self):
    self.Attribute = {}                                #{ [(Name, PlatformFfsSectionsClassObject)] : Value}
    self.Sections = []                                 #[ PlatformFfsSectionsClassObject]

class PlatformBuildOptionClassObject(object):
  def __init__(self):
    self.UserDefinedAntTasks = {}                      #{ [Id] : PlatformAntTaskClassObject, ...}
    self.Options = []                                  #[ BuildOptionClassObject, ...]
    self.UserExtensions = {}                           #{ [(UserID, Identifier)] : UserExtensionsClassObject, ...}
    self.FfsKeyList = {}                               #{ [FfsKey]: PlatformFfsClassObject, ...} 

class PlatformLibraryInstanceClassObject(object):
  def __init__(self):
    self.Name = ''
    self.ModuleGuid = ''
    self.ModuleVersion = ''
    self.PackageGuid = ''
    self.PackageVersion = ''

class PlatformModuleSaBuildOptionClassObject(object):
  def __init__(self):
    self.FvBinding = ''
    self.FfsFileNameGuid = ''
    self.FfsFormatKey = ''
    self.Options = []                                  #[ BuildOptionClassObject, ...]
        
class PlatformModuleClassObject(object):
  def __init__(self):
    self.Name = ''
    self.FilePath = ''
    self.LibraryInstances = []                         #[ PlatformLibraryInstanceClassObject, ...]
    self.Specifications = []                           #[ '', '', ...]
    self.PcdBuildDefinitions = []                      #[ PcdClassObject, ...]
    self.ModuleSaBuildOption = PlatformModuleSaBuildOptionClassObject()
    
class PlatformClassObject(object):
  def __init__(self):
    self.Header = PlatformHeaderClassObject()
    self.SkuInfoList = {}                              #[ PlatformSkuInfoClassObject ]
    self.FlashDefinitionFile = None                    #PlatformFlashDefinitionFileClassObject()
    self.FvImages = []                                 #[ PlatformFvImagesClassObject, ...]
    self.Modules = []                                  #[ PlatformModuleClassObject, ...]
    self.BuildOptions = []                             #[ PlatformBuildOptionClassObject, ...]
    self.DynamicPcdBuildDefinitions = []               #[ PcdClassObject, ...] 
    self.UserExtensions = []                           #[ UserExtensionsClassObject, ...]

if __name__ == '__main__':
  p = PlatformClassObject()
