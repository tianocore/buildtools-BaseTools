# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a package
#

from CommonClass import *

class PackageHeaderClass(IdentificationClass, CommonHeaderClass):
    def __init__(self):
        IdentificationClass.__init__(self)
        CommonHeaderClass.__init__(self)
        self.DecSpecification = ''
        self.ReadOnly = False
        self.RePackage = False
        self.ClonedFrom = []                                   #[ ClonedRecordClass, ...]
        
class PackageIndustryStdHeaderClass(CommonClass):
    def __init__(self):
        self.Name = ''
        self.IncludeHeader = ''
        CommonClass.__init__(self)
        
class PackageIncludePkgHeaderClass(object):
    def __init__(self):
        self.IncludeHeader = ''
        self.ModuleType = []                                   #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | TOOL | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED

class PackageClass(object):
    def __init__(self):
        self.Header = PackageHeaderClass()
        self.Includes = []                                     #[ IncludeClass, ...]   
        self.LibraryClassDeclarations = []                     #[ LibraryClassClass, ...]
        self.IndustryStdHeaders = []                           #[ PackageIndustryStdHeader, ...]
        self.ModuleFiles = []                                  #[ '', '', ...] 
        self.PackageIncludePkgHeaders = []                     #[ PackageIncludePkgHeader, ...]
        self.GuidDeclarations = []                             #[ GuidClass, ...]
        self.ProtocolDeclarations = []                         #[ ProtocolClass, ...]
        self.PpiDeclarations = []                              #[ PpiClass, ...]
        self.PcdDeclarations = []                              #[ PcdClass, ...]
        self.UserExtensions = []                               #[ UserExtensionsClass, ...]
        
if __name__ == '__main__':
    p = PackageClass()
