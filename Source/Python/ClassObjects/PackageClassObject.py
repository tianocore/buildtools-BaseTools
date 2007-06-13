# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to define a class object to describe a package
#

from CommonClassObject import *

class PackageHeaderClassObject(IdentificationClassObject, CommonHeaderClassObject):
  def __init__(self):
    IdentificationClassObject.__init__(self)
    CommonHeaderClassObject.__init__(self)
    self.ReadOnly = False
    self.RePackage = False
    self.ClonedFrom = []                               #[ ClonedRecordClassObject, ...]
    
class PackageIndustryStdHeader(CommonClassObject):
  def __init__(self):
    self.Name = ''
    self.IncludeHeader = ''
    CommonClassObject.__init__(self)
    
class PackageIncludePkgHeader(object):
  def __init__(self):
    self.IncludeHeader = ''
    self.ModuleType = []                               #BASE | SEC | PEI_CORE | PEIM | DXE_CORE | DXE_DRIVER | DXE_RUNTIME_DRIVER | DXE_SAL_DRIVER | DXE_SMM_DRIVER | TOOL | UEFI_DRIVER | UEFI_APPLICATION | USER_DEFINED

class PackageClassObject(object):
  def __init__(self):
    self.Header = PackageHeaderClassObject()
    self.LibraryClassDeclarations = []                 #[ LibraryClassClassObject, ...]
    self.IndustryStdHeaders = []                       #[ PackageIndustryStdHeader, ...]
    self.ModuleFiles = []                              #[ '', '', ...] 
    self.PackageIncludePkgHeaders = []                 #[ PackageIncludePkgHeader, ...]
    self.GuidDeclarations = []                         #[ GuidClassObject, ...]
    self.ProtocolDeclarations = []                     #[ ProtocolClassObject, ...]
    self.PpiDeclarations = []                          #[ PpiClassObject, ...]
    self.PcdDeclarations = []                          #[ PcdClassObject, ...]
    self.UserExtensions = []                           #[ UserExtensionsClassObject, ...]
    
if __name__ == '__main__':
  p = PackageClassObject()
