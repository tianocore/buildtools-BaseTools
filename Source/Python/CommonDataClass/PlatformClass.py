# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a platform
#

from CommonClass import *

class SkuInfoListClass(IncludeStatementClass):
    def __init__(self):
        IncludeStatementClass.__init__(self)
        self.SkuInfoList = {}                                       #{ SkuName : SkuId }

class PlatformHeaderClass(IdentificationClass, CommonHeaderClass, DefineClass):
    def __init__(self):
        IdentificationClass.__init__(self)
        CommonHeaderClass.__init__(self)
        DefineClass.__init__(self)
        self.DscSpecification = ''
        self.SupArchList = []                                        #EBC | IA32 | X64 | IPF | ARM | PPC
        self.BuildTargets = []                                       #RELEASE | DEBUG
        self.IntermediateDirectories = ''                            #MODULE | UNIFIED
        self.OutputDirectory = ''                                                    
        self.ForceDebugTarget = ''
        self.SkuId = ''
        self.BuildNumber = ''
        self.MakefileName = ''
        self.ClonedFrom = []                                         #[ ClonedRecordClass, ...]

class PlatformFlashDefinitionFileClass(object):
    def __init__(self):
        self.Id = ''
        self.UiName = ''
        self.Preferred = False
        self.FilePath = ''

class PlatformFvImageOption(object):
    def __init__(self):
        self.FvImageOptionName = ''
        self.FvImageOptionValues = []
        
class PlatformFvImageClass(object):
    def __init__(self):
        self.Name = ''
        self.Value = ''
        self.Type = ''                                               #Attributes | Options | Components | ImageName 
        self.FvImageNames = []
        self.FvImageOptions = []                                     #[ PlatformFvImageOption, ...]

class PlatformFvImageNameClass(object):
    def __init__(self):
        self.Name = ''
        self.Type = ''                                               #FV_MAIN | FV_MAIN_COMPACT | NV_STORAGE | FV_RECOVERY | FV_RECOVERY_FLOPPY | FV_FILE | CAPSULE_CARGO | NULL | USER_DEFINED 
        self.FvImageOptions = []                                     #[ PlatformFvImageOption, ...]
        
class PlatformFvImagesClass(object):
    def __init__(self):
        self.FvImages1 = []                                          #[ PlatformFvImageClass, ...]
        self.FvImages2 = []                                          #[ PlatformFvImageNameClass, ...]

class PlatformAntTaskClass(object):
    def __init__(self):
        self.Id = ''
        self.AntCmdOptions = ''
        self.FilePath = ''

class PlatformFfsSectionClass(CommonClass):
    def __init__(self):
        CommonClass.__init__(self)
        self.BindingOrder                = ''
        self.Compressible                = ''
        self.SectionType                 = ''
        self.EncapsulationType     = ''
        self.ToolName                        = ''
        self.Filenames = []
        self.Args                                = ''
        self.OutFile                         = ''
        self.OutputFileExtension = ''
        self.ToolNameElement         = ''
        
class PlatformFfsSectionsClass(CommonClass):
    def __init__(self):
        CommonClass.__init__(self)        
        self.BindingOrder            = ''
        self.Compressible            = ''
        self.SectionType             = ''
        self.EncapsulationType = ''
        self.ToolName                    = ''
        self.Section = []                                            #[ PlatformFfsSectionClass, ... ]
        self.Sections = []                                           #[ PlatformFfsSectionsClass, ...]
        
class PlatformFfsClass(object):
    def __init__(self):
        self.Attribute = {}                                          #{ [(Name, PlatformFfsSectionsClass)] : Value}
        self.Sections = []                                           #[ PlatformFfsSectionsClass]

class PlatformBuildOptionClass(object):
    def __init__(self):
        self.UserDefinedAntTasks = {}                                #{ [Id] : PlatformAntTaskClass, ...}
        self.Options = []                                            #[ BuildOptionClass, ...]
        self.UserExtensions = {}                                     #{ [(UserID, Identifier)] : UserExtensionsClass, ...}
        self.FfsKeyList = {}                                         #{ [FfsKey]: PlatformFfsClass, ...} 

class PlatformLibraryInstanceClass(DefineClass):
    def __init__(self):
        DefineClass.__init__(self)
        self.Name = ''
        self.FilePath = ''
        self.ModuleGuid = ''
        self.ModuleVersion = ''
        self.PackageGuid = ''
        self.PackageVersion = ''

class PlatformModuleSaBuildOptionClass(DefineClass):
    def __init__(self):
        self.FvBinding = ''
        self.FfsFileNameGuid = ''
        self.FfsFormatKey = ''
        self.Options = []                                            #[ BuildOptionClass, ...]
                
class PlatformModuleClass(CommonClass, DefineClass, IncludeStatementClass):
    def __init__(self):
        CommonClass.__init__(self)
        DefineClass.__init__(self)
        IncludeStatementClass.__init__(self)
        self.Name = ''                                               #Library name or libraryclass name or module name
        self.FilePath = ''
        self.Type = ''                                               #LIBRARY | LIBRARY_CLASS | MODULE, used by dsc
        self.ModuleType = ''
        self.LibraryClasses = []                                     #[ PlatformLibraryInstanceClass, ...]
        self.PcdBuildDefinitions = []                                #[ PcdClass, ...]
        self.ModuleSaBuildOption = PlatformModuleSaBuildOptionClass()
        self.Specifications = []                                     #[ '', '', ...]
    
class PlatformClass(object):
    def __init__(self):
        self.Header = PlatformHeaderClass()
        self.SkuInfoList = SkuInfoListClass()
        self.Modules = []                                            #[ PlatformModuleClass, ...]
        self.FlashDefinitionFile = None                              #PlatformFlashDefinitionFileClass()
        self.FvImages = []                                           #[ PlatformFvImagesClass, ...]
        self.BuildOptions = []                                       #[ PlatformBuildOptionClass, ...]
        self.DynamicPcdBuildDefinitions = []                         #[ PcdClass, ...] 
        self.Fdf = []                                                #[ FdfClass, ...]
        self.UserExtensions = []                                     #[ UserExtensionsClass, ...]

if __name__ == '__main__':
    p = PlatformClass()
