## @file
# This file is used to create a database used by ECC tool
#
# Copyright (c) 2007, Intel Corporation
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
from TableDataModel import TableDataModel
from TableFile import TableFile
from TableFunction import TableFunction
from TablePcd import TablePcd
from TableVariable import TableVariable
import Common.EdkLogger as EdkLogger

##
# Static definitions
#
DATABASE_PATH = "Database/Ecc.db"

## TableDataModel
#
# This class defined the ECC databse
# During the phase of initialization, the database will create all tables and
# insert all records of table DataModel
# 
# @param object:    Inherited from object class
# @param DbPath:    A string for the path of the ECC database
#
# @var Conn:        Connection of the ECC database
# @var Cur:         Cursor of the connection
# @var TblDataModel:  Local instance for TableDataModel
#
class Database(object):
    def __init__(self, DbPath):
        EdkLogger.SetLevel(EdkLogger.VERBOSE)
        self.Conn = sqlite3.connect(DbPath)
        self.Cur = self.Conn.cursor()
        self.TblDataModel = TableDataModel(self.Cur)
        self.TblFile = TableFile(self.Cur)
        self.TblFunction = TableFunction(self.Cur)
        self.TblVariable = TableVariable(self.Cur)
        self.TblPcd = TablePcd(self.Cur)
    
    ## Initialize ECC database
    #
    # 1. Delete all old existing tables
    # 2. Create new tables
    # 3. Initialize table DataModel
    #
    def InitDatabase(self):
        EdkLogger.verbose("\nInitialize ECC database started ...")
        #
        # Drop all old existing tables
        #
        self.TblDataModel.Drop()
        self.TblFile.Drop()
        self.TblFunction.Drop()
        self.TblPcd.Drop()
        self.TblVariable.Drop()
        
        #
        # Create new tables
        #
        self.TblDataModel.Create()
        self.TblFile.Create()
        self.TblFunction.Create()
        self.TblPcd.Create()
        self.TblVariable.Create()
        
        #
        # Initialize table DataModel
        #
        self.TblDataModel.InitTable()
        EdkLogger.verbose("Initialize ECC database ... DONE!")

    ## Query a table
    #
    # @param Table:  The instance of the table to be queried
    #
    def QueryTable(self, Table):
        Table.Query()

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    Db = Database(DATABASE_PATH)
    Db.InitDatabase()
    Db.QueryTable(Db.TblDataModel)
    Db.QueryTable(Db.TblFile)
    Db.QueryTable(Db.TblFunction)
    Db.QueryTable(Db.TblPcd)
    Db.QueryTable(Db.TblVariable)
    
    