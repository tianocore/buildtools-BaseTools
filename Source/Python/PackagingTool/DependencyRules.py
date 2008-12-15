## @file
# This file is for installed package information database operations
#
# Copyright (c) 2007 ~ 2008, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import sqlite3
import os

import EdkLogger as EdkLogger
import IpiDb

(DEPEX_CHECK_SUCCESS, DEPEX_CHECK_MODULE_NOT_FOUND, \
DEPEX_CHECK_PACKAGE_NOT_FOUND, DEPEX_CHECK_DP_NOT_FOUND) = (0, 1, 2, 3)

## IpiDb
#
# This class represents the installed package information databse
# Add/Remove/Get installed distribution package information here.
# 
# 
# @param object:      Inherited from object class
# @param DbPath:      A string for the path of the database
#
# @var Conn:          Connection of the database
# @var Cur:           Cursor of the connection
#
class DependencyRules(object):
    def __init__(self, Db):
        self.IpiDb = Db
    
    ## Check whether a module exists in current workspace.
    #
    # @param Guid:  
    # @param Version:
    #
    def CheckModuleExists(self, Guid, Version, ReturnCode = DEPEX_CHECK_SUCCESS):
        EdkLogger.verbose("\nCheck module exists in workspace started ...")
        ModuleList = []
        ModuleList = self.IpiDb.GetModInPackage(self.IpiDb, Guid, Version)
        ModuleList.extend(self.IpiDb.GetStandaloneModule(self.IpiDb, Guid, Version))
        EdkLogger.verbose("Check module exists in workspace ... DONE!")
        if len(ModuleList) > 0:
            return True
        else:
            ReturnCode = DEPEX_CHECK_MODULE_NOT_FOUND
            return False
        

    ## Check whether a module depex satified by current workspace.
    #
    # @param Guid:  
    # @param Version:
    #
    def CheckModuleDepexSatisfied(self, GuidVersionList, ReturnCode = DEPEX_CHECK_SUCCESS):
        EdkLogger.verbose("\nCheck module depex met by workspace started ...")
        for GuidVerPair in GuidVersionList:
            Exist = self.CheckPackageExists(GuidVerPair[0], GuidVerPair[1], ReturnCode)
            if not Exist:
                return False
            
        return True
        
        EdkLogger.verbose("Check module depex met by workspace ... DONE!")
    
    ## Check whether a package exists in current workspace.
    #
    # @param Guid:  
    # @param Version:
    #
    def CheckPackageExists(self, Guid, Version, ReturnCode = DEPEX_CHECK_SUCCESS):
        EdkLogger.verbose("\nCheck package exists in workspace started ...")
        PkgList = []
        PkgList = self.IpiDb.GetPackage(self.IpiDb, Guid, Version)
        if len(PkgList) > 0:
            return True
        else:
            ReturnCode = DEPEX_CHECK_PACKAGE_NOT_FOUND
            return False
        
        EdkLogger.verbose("Check package exists in workspace ... DONE!")
        
    ## Check whether a DP exists in current workspace.
    #
    # @param Guid:  
    # @param Version:
    #
    def CheckDpExists(self, Guid, Version, ReturnCode = DEPEX_CHECK_SUCCESS):
        EdkLogger.verbose("\nCheck DP exists in workspace started ...")
        DpList = []
        DpList = self.IpiDb.GetDp(self.IpiDb, Guid, Version)
        if len(DpList) > 0:
            return True
        else:
            ReturnCode = DEPEX_CHECK_DP_NOT_FOUND
            return False
        
        EdkLogger.verbose("Check DP exists in workspace ... DONE!")
##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.DEBUG_0)


    