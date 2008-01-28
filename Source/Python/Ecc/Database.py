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
import os, time

import Common.EdkLogger as EdkLogger
import CommonDataClass.DataClass as DataClass

from Table.TableDataModel import TableDataModel
from Table.TableFile import TableFile
from Table.TableFunction import TableFunction
from Table.TablePcd import TablePcd
from Table.TableIdentifier import TableIdentifier

##
# Static definitions
#
DATABASE_PATH = "Database/Ecc.db"

## Database
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
        print time.strftime('%H/%M/%S', time.localtime())
        self.Conn = sqlite3.connect(DbPath, isolation_level = 'DEFERRED')
        #self.Conn = sqlite3.connect(DbPath)
        self.Cur = self.Conn.cursor()
        self.TblDataModel = TableDataModel(self.Cur)
        self.TblFile = TableFile(self.Cur)
        self.TblFunction = TableFunction(self.Cur)
        self.TblIdentifier = TableIdentifier(self.Cur)
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
        self.TblIdentifier.Drop()
        
        #
        # Create new tables
        #
        self.TblDataModel.Create()
        self.TblFile.Create()
        self.TblFunction.Create()
        self.TblPcd.Create()
        self.TblIdentifier.Create()
        
        #
        # Start a Transaction
        #
        #self.Cur.execute("""BEGIN""")
        
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
    
    ## Close entire database
    #
    # Commit all first
    # Close the connection and cursor
    #
    def Close(self):
        #
        # Start a Transaction
        #
        #self.Cur.execute("""END""")
        
        #
        # Commit to file
        #        
        self.Conn.commit()
        
        #
        # Close connection and cursor
        #
        self.Cur.close()
        self.Conn.close()
        print time.strftime('%H/%M/%S', time.localtime())
    
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
        self.TblFile.Insert(FileID, File.Name, File.ExtName, File.Path, File.FullPath, Model = File.Model, TimeStamp = File.TimeStamp)

        #
        # Insert function of file
        #
        for Function in File.FunctionList:
            FunctionID = self.TblFunction.GetCount() + 1
            self.TblFunction.Insert(FunctionID, Function.Header, Function.Modifier, Function.Name, Function.ReturnStatement, \
                                    Function.StartLine, Function.StartColumn, Function.EndLine, Function.EndColumn, \
                                    Function.BodyStartLine, Function.BodyStartColumn, FileID)
            #
            # Insert Identifier of function
            #
            for Identifier in Function.IdentifierList:
                IdentifierID = self.TblIdentifier.GetCount() + 1
                self.TblIdentifier.Insert(IdentifierID, Identifier.Modifier, Identifier.Type, Identifier.Name, Identifier.Value, Identifier.Model, \
                                        FileID, FunctionID, Identifier.StartLine, Identifier.StartColumn, Identifier.EndLine, Identifier.EndColumn)
            #
            # Insert Pcd of function
            #
            for Pcd in Function.PcdList:
                PcdID = self.TblPcd.GetCount() + 1
                self.TblPcd.Insert(PcdID, Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.Token, Pcd.DatumType, Pcd.Model, \
                                   FileID, FunctionID, Pcd.StartLine, Pcd.StartColumn, Pcd.EndLine, Pcd.EndColumn)
        #
        # Insert Identifier of file
        #
        for Identifier in File.IdentifierList:
            IdentifierID = self.TblIdentifier.GetCount() + 1
            self.TblIdentifier.Insert(IdentifierID, Identifier.Modifier, Identifier.Type, Identifier.Name, Identifier.Value, Identifier.Model, \
                                    FileID, -1, Identifier.StartLine, Identifier.StartColumn, Identifier.EndLine, Identifier.EndColumn)
        #
        # Insert Pcd of file
        #
        for Pcd in File.PcdList:
            PcdID = self.TblPcd.GetCount() + 1
            self.TblPcd.Insert(PcdID, Pcd.CName, Pcd.TokenSpaceGuidCName, Pcd.Token, Pcd.DatumType, Pcd.Model, \
                               FileID, -1, Pcd.StartLine, Pcd.StartColumn, Pcd.EndLine, Pcd.EndColumn)
                
        EdkLogger.verbose("Insert information of file %s ... DONE!" % File.FullPath)

    ## UpdateIdentifierBelongsToFunction
    #
    # Update the field "BelongsToFunction" for each Indentifier
    #
    #
    def UpdateIdentifierBelongsToFunction(self):
        EdkLogger.verbose("Update 'BelongsToFunction' for Identifiers started ...")
        
        SqlCommand = """select ID, BelongsToFile, StartLine, EndLine, Model from Identifier"""
        EdkLogger.debug(4, "SqlCommand: %s" %SqlCommand)
        self.Cur.execute(SqlCommand)
        Records = self.Cur.fetchall()
        for Record in Records:
            IdentifierID = Record[0]
            BelongsToFile = Record[1]
            StartLine = Record[2]
            EndLine = Record[3]
            Model = Record[4]

            #
            # Check whether an identifier belongs to a function
            #
            EdkLogger.debug(4, "For common identifiers ... ")
            SqlCommand = """select ID from Function 
                        where StartLine < %s and EndLine > %s
                        and BelongsToFile = %s""" % (StartLine, EndLine, BelongsToFile)
            EdkLogger.debug(4, "SqlCommand: %s" %SqlCommand)
            self.Cur.execute(SqlCommand)
            IDs = self.Cur.fetchall()
            for ID in IDs:
                SqlCommand = """Update Identifier set BelongsToFunction = %s where ID = %s""" % (ID[0], IdentifierID)
                EdkLogger.debug(4, "SqlCommand: %s" %SqlCommand)
                self.Cur.execute(SqlCommand)
            
            #
            # Check whether the identifier is a function header
            #
            EdkLogger.debug(4, "For function headers ... ") 
            if Model == DataClass.MODEL_IDENTIFIER_COMMENT:
                SqlCommand = """select ID from Function 
                        where StartLine = %s + 1
                        and BelongsToFile = %s""" % (EndLine, BelongsToFile)
                EdkLogger.debug(4, "SqlCommand: %s" %SqlCommand)
                self.Cur.execute(SqlCommand)
                IDs = self.Cur.fetchall()
                for ID in IDs:
                    SqlCommand = """Update Identifier set BelongsToFunction = %s, Model = %s where ID = %s""" % (ID[0], DataClass.MODEL_IDENTIFIER_FUNCTION_HEADER, IdentifierID)
                    EdkLogger.debug(4, "SqlCommand: %s" %SqlCommand)
                    self.Cur.execute(SqlCommand)
        
        EdkLogger.verbose("Update 'BelongsToFunction' for Identifiers ... DONE")

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    EdkLogger.Initialize()
    EdkLogger.SetLevel(EdkLogger.VERBOSE)
    
    Db = Database(DATABASE_PATH)
    Db.InitDatabase()
    Db.QueryTable(Db.TblDataModel)
    
    identifier1 = DataClass.IdentifierClass(-1, '', '', "i''1", 'aaa', DataClass.MODEL_IDENTIFIER_COMMENT, 1, -1, 32,  43,  54,  43)
    identifier2 = DataClass.IdentifierClass(-1, '', '', 'i1', 'aaa', DataClass.MODEL_IDENTIFIER_COMMENT, 1, -1, 15,  43,  20,  43)
    identifier3 = DataClass.IdentifierClass(-1, '', '', 'i1', 'aaa', DataClass.MODEL_IDENTIFIER_COMMENT, 1, -1, 55,  43,  58,  43)
    identifier4 = DataClass.IdentifierClass(-1, '', '', "i1'", 'aaa', DataClass.MODEL_IDENTIFIER_COMMENT, 1, -1, 77,  43,  88,  43)
    fun1 = DataClass.FunctionClass(-1, '', '', 'fun1', '', 21, 2, 60,  45, 1, 23, 0, [], [])
    file = DataClass.FileClass(-1, 'F1', 'c', 'C:\\', 'C:\\F1.exe', DataClass.MODEL_FILE_C, '2007-12-28', [fun1], [identifier1, identifier2, identifier3, identifier4], [])
    Db.InsertOneFile(file)
    Db.UpdateIdentifierBelongsToFunction()
        
    Db.QueryTable(Db.TblFile)
    Db.QueryTable(Db.TblFunction)
    Db.QueryTable(Db.TblPcd)
    Db.QueryTable(Db.TblIdentifier)
    
    Db.Close()
    