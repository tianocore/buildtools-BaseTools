## @file
# This file is used to define checkpoints used by ECC tool
#
# Copyright (c) 2008, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

## Check
#
# This class is to define checkpoints used by ECC tool
#
# @param object:          Inherited from object class
#
class Check(object):
    def __init__(self):
        pass
     
    #
    # Check all required checkpoints
    #   
    def Check(self):
        pass
    
    #
    # Meta-Data File Processing Checking
    #
    def MetaDataFileCheck(self):
        self.MetaDataFileCheckPathName()
        self.MetaDataFileCheckGenerateFileList()
        self.MetaDataFileCheckLibraryInstance()
        self.MetaDataFileCheckLibraryInstanceDependent()
        self.MetaDataFileCheckLibraryInstanceOrder()
        self.MetaDataFileCheckLibraryNoUse()
        self.MetaDataFileCheckBinaryInfInFdf()
        self.MetaDataFileCheckPcdDuplicate()
        self.MetaDataFileCheckPcdFlash()
        self.MetaDataFileCheckPcdNoUse()

    #
    # Check whether each file defined in meta-data exists
    #
    def MetaDataFileCheckPathName(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPathName == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass
    
    #
    # Generate a list for all files defined in meta-data files
    #
    def MetaDataFileCheckGenerateFileList(self):
        if EccGlobalData.gConfig.MetaDataFileCheckGenerateFileList == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            File = EccGlobalData.gConfig.MetaDataFileCheckPathOfGenerateFileList
            pass
    
    #
    # Check whether all Library Instances defined for a given module (or dependent library instance) match the module's type.  
    # Each Library Instance must specify the Supported Module Types in its INF file, 
    # and any module specifying the library instance must be one of the supported types.
    #
    def MetaDataFileCheckLibraryInstance(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstance == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Check whether a Library Instance has been defined for all dependent library classes
    #
    def MetaDataFileCheckLibraryInstanceDependent(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceDependent == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Check whether the Library Instances specified by the LibraryClasses sections are listed in order of dependencies
    #
    def MetaDataFileCheckLibraryInstanceOrder(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceOrder == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Check whether the unnecessary inclusion of library classes in the INF file
    #
    def MetaDataFileCheckLibraryNoUse(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryNoUse == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Check whether an INF file is specified in the FDF file, but not in the DSC file, then the INF file must be for a Binary module only
    #
    def MetaDataFileCheckBinaryInfInFdf(self):
        if EccGlobalData.gConfig.MetaDataFileCheckBinaryInfInFdf == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Not to report error and warning related OS include file such as "windows.h" and "stdio.h"
    # Check whether a PCD is set in a DSC file or the FDF file, but not in both.
    #
    def MetaDataFileCheckPcdDuplicate(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdDuplicate == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass

    #
    # Check whether PCD settings in the FDF file can only be related to flash.
    #
    def MetaDataFileCheckPcdFlash(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdFlash == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass
        
    #
    # Check whether PCDs used in INF files but not specified in DSC or FDF files
    #
    def MetaDataFileCheckPcdNoUse(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdNoUse == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass
        
    #
    # Check whether having duplicate guids defined for Guid/Protocol/Ppi
    #
    def MetaDataFileCheckGuidDuplicate(self):
        if EccGlobalData.gConfig.MetaDataFileCheckGuidDuplicate == 1 or EccGlobalData.gConfig.MetaDataFileCheckAll == 1:
            pass
