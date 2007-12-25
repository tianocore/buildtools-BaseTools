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
import DataClass

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
        EdkLogger.SetLevel(EdkLogger.DEBUG_0)
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
    
    ## Insert one file information
    #
    # Insert one file's information to the database
    # 1. Create a record in TableFile
    # 2. Create functions one by one
    #    2.1 Create variables of function one by one
    #    2.2 Create pcds of function one by one
    # 3. Create variables one by one
    # 4. Create pcds one by one
    #
    def InsertOneFile(self, File):
        #
        # Insert a record for file
        #
        FileID = self.TblFile.GetCount() + 1
        self.TblFile.Insert(FileID, File.Name, File.ExtName, File.Path, File.FullPath, Model = File.Model)

        #
        # Insert function of file
        #
        for Function in File.FunctionList:
            FunctionID = self.TblFunction.GetCount() + 1
            self.TblFunction.Insert(FunctionID, Function.Header, Function.Modifier, Function.Name, Function.ReturnStatement, \
                                    Function.StartLine, Function.StartColumn, Function.EndLine, Function.EndColumn, FileID)
            #
            # Insert Variable of function
            #
            for Variable in Function.VariableList:
                VariableID = self.TblVariable.GetCount() + 1
                self.TblVariable.Insert(VariableID, Variable.Modifier, Variable.Type, Variable.Name, Variable.Value, Variable.Model, \
                                        FileID, FunctionID, Variable.StartLine, Variable.StartColumn, Variable.EndLine, Variable.EndColumn)
            #
            # Insert Pcd of function
            #
            for Pcd in Function.PcdList:
                PcdID = self.TblPcd.GetCount() + 1
                self.TblPcd.Insert(PcdID, Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.Token, Pcd.DatumType, Pcd.Model, \
                                   FileID, FunctionID, Pcd.StartLine, Pcd.StartColumn, Pcd.EndLine, Pcd.EndColumn)
        #
        # Insert Variable of file
        #
        for Variable in File.VariableList:
            VariableID = self.TblVariable.GetCount() + 1
            self.TblVariable.Insert(VariableID, Variable.Modifier, Variable.Type, Variable.Name, Variable.Value, Variable.Model, \
                                    FileID, -1, Variable.StartLine, Variable.StartColumn, Variable.EndLine, Variable.EndColumn)
        #
        # Insert Pcd of file
        #
        for Pcd in File.PcdList:
            PcdID = self.TblPcd.GetCount() + 1
            self.TblPcd.Insert(PcdID, Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.Token, Pcd.DatumType, Pcd.Model, \
                               FileID, -1, Pcd.StartLine, Pcd.StartColumn, Pcd.EndLine, Pcd.EndColumn)
                
        EdkLogger.verbose("Insert information of file %s ... DONE!" % File.FullPath)

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
