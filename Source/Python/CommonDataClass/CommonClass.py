# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define common items of class object
#

class CommonClass(object):
    def __init__(self, SupArchList = []):
        self.Usage = []                                   #ALWAYS_CONSUMED | SOMETIMES_CONSUMED | ALWAYS_PRODUCED | SOMETIMES_PRODUCED | TO_START | BY_START | PRIVATE
        self.FeatureFlag = ''
        self.SupArchList = SupArchList                    #EBC | IA32 | X64 | IPF | ARM | PPC
        self.HelpText = ''
        
class CommonHeaderClass(object):
    def __init__(self):
        self.Abstract = ''
        self.Description = ''
        self.Copyright = ''
        self.License = ''
        self.Specification = {}                           #{ SpecificationName : SpecificationValue } 

class DefineClass(object):
    def __init__(self):
        self.Define = {}                                  #{ (DefineName, Arch) : DefineValue, ...}
        
class ClonedRecordClass(object):
    def __init__(self):
        self.Id = 0
        self.FarGuid = ''
        self.PackageGuid = ''
        self.PackageVersion = ''
        self.ModuleGuid = ''
        self.ModuleVersion = ''

class IdentificationClass(object):
    def __init__(self):
        self.Name = ''                                    #ModuleName(BaseName) / PackageName / PlatformName
        self.Guid = ''
        self.Version = ''
        self.FileName = ''
        self.FullPath = ''

class IncludeStatementClass(object):
    def __init__(self):
        self.IncludeFiles = {}                             #{ IncludeFile : [Arch1, Arch2, ...], ...}

class GuidProtocolPpiCommonClass(CommonClass):
    def __init__(self):
        self.Name = ''
        self.CName = ''
        self.Guid = ''
        self.Notify = False
        self.GuidTypeList = []                            #DATA_HUB_RECORD | EFI_EVENT | EFI_SYSTEM_CONFIGURATION_TABLE | EFI_VARIABLE | GUID | HII_PACKAGE_LIST | HOB | TOKEN_SPACE_GUID
        self.SupModuleList = []                           #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
        CommonClass.__init__(self)
        
class LibraryClassClass(CommonClass, DefineClass):
    def __init__(self):
        self.LibraryClass = ''
        self.IncludeHeader = ''
        self.RecommendedInstanceVersion = ''
        self.RecommendedInstanceGuid = ''
        self.RecommendedInstance = ''
        self.SupModuleList = []                           #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
        CommonClass.__init__(self)
        DefineClass.__init__(self)

class GuidClass(GuidProtocolPpiCommonClass):
    def __init__(self):
        GuidProtocolPpiCommonClass.__init__(self)

class ProtocolClass(GuidProtocolPpiCommonClass):
    def __init__(self):
        GuidProtocolPpiCommonClass.__init__(self)
        
class PpiClass(GuidProtocolPpiCommonClass):        
    def __init__(self):
        GuidProtocolPpiCommonClass.__init__(self)
        
class SkuInfoClass(object):
    def __init__(self, SkuIdName = '', SkuId = '', VariableName = '', VariableGuid = '', VariableOffset = '', HiiDefaultValue = '', VpdOffset = '', DefaultValue = ''):
        self.SkuIdName = SkuIdName
        self.SkuId = SkuId
        #Used by Hii
        self.VariableName = VariableName
        self.VariableGuid = VariableGuid
        self.VariableOffset = VariableOffset
        self.HiiDefaultValue = HiiDefaultValue
        
        #Used by Vpd
        self.VpdOffset = VpdOffset
        
        #Used by Default
        self.DefaultValue = DefaultValue
        
    def __str__(self):
        rtn = rtn = str(self.SkuId) + "," + \
                    str(self.VariableName) + "," + \
                    str(self.VariableGuid) + "," + \
                    str(self.VariableOffset) + "," + \
                    str(self.HiiDefaultValue) + "," + \
                    str(self.VpdOffset) + "," + \
                    str(self.DefaultValue) + ","
        return rtn

class PcdClass(CommonClass):
    def __init__(self, CName = '', Token = '', TokenSpaceGuidCName = '', DatumType = '', MaxDatumSize = '', DefaultValue = '', ItemType = '', ValidUsage = [], SkuInfoList = {}, SupModuleList = []):
        self.CName = CName
        self.Token = Token
        self.TokenSpaceGuidCName = TokenSpaceGuidCName
        self.DatumType = DatumType                                 #UINT8 | UINT16 | UINT32 | UINT64 | VOID* | BOOLEAN 
        self.MaxDatumSize = MaxDatumSize
        self.DefaultValue = DefaultValue
        self.ItemType = ItemType                                   #FEATURE_FLAG | FIXED_AT_BUILD | PATCHABLE_IN_MODULE | DYNAMIC | DYNAMIC_EX
        self.ValidUsage = ValidUsage                               #FEATURE_FLAG | FIXED_AT_BUILD | PATCHABLE_IN_MODULE | DYNAMIC | DYNAMIC_EX
        self.SkuInfoList = SkuInfoList                             #{ [SkuIdName] : SkuInfoClass } 
        self.SupModuleList = SupModuleList                         #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED
        CommonClass.__init__(self)

class BuildOptionClass(IncludeStatementClass):
    def __init__(self, ToolChainFamily = '', ToolChain = '', Option = ''):
        IncludeStatementClass.__init__(self)
        self.Statement = ''                               #Family:Target_TagName_Tarch_ToolCode_FLAGS = String 
        self.ToolChainFamily = ToolChainFamily
        self.ToolChain = ToolChain
        self.Option = Option
        self.BuildTarget = ''
        self.TagName = ''
        self.ToolCode = ''
        self.SupArchList = []                             #EBC | IA32 | X64 | IPF | ARM | PPC
        
class IncludeClass(CommonClass):
    def __init__(self):
        self.FilePath = ''
        self.ModuleType = ''
        self.Comment = ''
        CommonClass.__init__(self)        
                
class UserExtensionsClass(object):
    def __init__(self):
        self.UserID = ''
        self.Identifier = 0
        self.Content = ''
