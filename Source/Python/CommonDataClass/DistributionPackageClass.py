## @file
# This file is used to define a class object to describe a distribution package
#
# Copyright (c) 2008, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

##
# Import Modules
#
from CommonClass import *
from Common.Misc import sdict

## DistributionPackageHeaderClass
#
class DistributionPackageHeaderClass(IdentificationClass, CommonHeaderClass):
    def __init__(self):
        IdentificationClass.__init__(self)
        CommonHeaderClass.__init__(self)
        self.ReadOnly = False
        self.RePackage = True
        self.Vendor = ''
        self.Date = ''
        self.Signature = 'Md5Sum'
        self.XmlSpecification = ''

## DistributionPackageClass
#
#
class DistributionPackageClass(object):
    def __init__(self):
        self.Header = DistributionPackageHeaderClass()
        self.PackageSurfaceArea = sdict() # {(Guid, Version, Path) : PackageObj}
        self.ModuleSurfaceArea = sdict()  # {(Guid, Version, Path) : ModuleObj}
        self.Tools = MiscFileClass()
        self.MiscellaneousFiles = MiscFileClass()
        self.UserExtensions = []

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    D = DistributionPackageClass()
