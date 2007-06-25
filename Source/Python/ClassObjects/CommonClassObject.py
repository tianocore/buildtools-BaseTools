# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define common items of class object
#

class CommonClassObject(object):
  def __init__(self):
    self.Usage = []                          #ALWAYS_CONSUMED | SOMETIMES_CONSUMED | ALWAYS_PRODUCED | SOMETIMES_PRODUCED | TO_START | BY_START | PRIVATE
    self.FeatureFlag = ''
    self.SupArchList = []                    #EBC | IA32 | X64 | IPF | ARM | PPC
    self.HelpText = ''
    
class CommonHeaderClassObject(object):
  def __init__(self):
    self.Abstract = ''
    self.Description = ''
    self.Copyright = ''
    self.License = ''
    self.Specification = ''
    
class ClonedRecordClassObject(object):
  def __init__(self):
    self.Id = 0
    self.FarGuid = ''
    self.PackageGuid = ''
    self.PackageVersion = ''
    self.ModuleGuid = ''
    self.ModuleVersion = ''

class IdentificationClassObject(object):
  def __init__(self):
    self.Name = ''                                     #ModuleName(BaseName) / PackageName / PlatformName
    self.Guid = ''
    self.Version = ''
    self.FileName = ''
    self.FullPath = ''

class GuidProtocolPpiCommonClassObject(CommonClassObject):
  def __init__(self):
    self.Name = ''
    self.CName = ''
    self.Guid = ''
    self.Notify = False
    self.GuidTypeList = []                             #DATA_HUB_RECORD | EFI_EVENT | EFI_SYSTEM_CONFIGURATION_TABLE | EFI_VARIABLE | GUID | HII_PACKAGE_LIST | HOB | TOKEN_SPACE_GUID
    self.SupModuleList = []                            #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
    CommonClassObject.__init__(self)
    
class LibraryClassClassObject(CommonClassObject):
  def __init__(self):
    self.LibraryClass = ''
    self.IncludeHeader = ''
    self.RecommendedInstanceVersion = ''
    self.RecommendedInstanceGuid = ''
    self.SupModuleList = []                             #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
    CommonClassObject.__init__(self)

class GuidClassObject(GuidProtocolPpiCommonClassObject):
  def __init__(self):
    GuidProtocolPpiCommonClassObject.__init__(self)

class ProtocolClassObject(GuidProtocolPpiCommonClassObject):
  def __init__(self):
    GuidProtocolPpiCommonClassObject.__init__(self)
    
class PpiClassObject(GuidProtocolPpiCommonClassObject):    
  def __init__(self):
    GuidProtocolPpiCommonClassObject.__init__(self)
    
class SkuInfoClassObject(object):
  def __init__(self):
    self.SkuId = ''
    #Used by Hii
    self.VariableName = ''
    self.VariableGuid = ''
    self.VariableOffset = ''
    self.HiiDefaultValue = ''
    
    #Used by Vpd
    self.VpdOffset = ''
    
    #Used by Default
    self.DefaultValue = ''

class PcdClassObject(CommonClassObject):
  def __init__(self):
    self.CName = ''
    self.Token = ''
    self.TokenSpaceGuidCName = ''
    self.DatumType = ''                                 #UINT8 | UINT16 | UINT32 | UINT64 | VOID* | BOOLEAN 
    self.MaxDatumSize = ''
    self.DefaultValue = ''
    self.ItemType = ''                                  #FEATURE_FLAG | FIXED_AT_BUILD | PATCHABLE_IN_MODULE | DYNAMIC | DYNAMIC_EX
    self.ValidUsage = []                                #FEATURE_FLAG | FIXED_AT_BUILD | PATCHABLE_IN_MODULE | DYNAMIC | DYNAMIC_EX
    self.SkuInfoList = {}                               #{ [SkuId] : SkuInfoClassObject } 
    self.SupModuleList = []                             #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
    CommonClassObject.__init__(self)

class BuildOptionClassObject(object):
  def __init__(self):
    self.Option = ''
    self.BuildTarget = ''
    self.ToolChainFamily = ''
    self.TagName = ''
    self.ToolCode = ''
    self.SupArchList = []                               #EBC | IA32 | X64 | IPF | ARM | PPC
    
class UserExtensionsClassObject(object):
  def __init__(self):
    self.UserID = ''
    self.Identifier = 0
    self.Content = ''
