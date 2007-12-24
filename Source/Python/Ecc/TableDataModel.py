## @file
# This file is used to create/update/query/erase table for data models
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
import Common.EdkLogger as EdkLogger
import DataClass

## TableDataModel
#
# This class defined a table used for data model
# 
# @param object:       Inherited from object class
#
#
class TableDataModel(object):
    def __init__(self, Cursor):
        self.Cur = Cursor
    
    ## Create table
    #
    # Create table DataModel
    #
    # @param ID:           ID of a ModelType
    # @param CrossIndex:   CrossIndex of a ModelType
    # @param Name:         Name of a ModelType
    # @param Description:  Description of a ModelType
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS DataModel(ID SINGLE PRIMARY KEY,
                                                              CrossIndex INTEGER NOT NULL,
                                                              Name VARCHAR NOT NULL,
                                                              Description VARCHAR
                                                             )"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Create table DataModel ... DONE!")

    ## Insert table
    #
    # Insert a record into table DataModel
    #
    # @param ID:           ID of a ModelType
    # @param CrossIndex:   CrossIndex of a ModelType
    # @param Name:         Name of a ModelType
    # @param Description:  Description of a ModelType
    #
    def Insert(self, ID, CrossIndex, Name, Description):
        SqlCommand = """insert into DataModel values(%s, %s, '%s', '%s')""" % (ID, CrossIndex, Name, Description)
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose(SqlCommand + " ... DONE!")
    
    ## Query table
    #
    # Query all records of table DataModel
    #  
    def Query(self):
        EdkLogger.verbose("\nQuery tabel DataModel started ...")
        SqlCommand = """select * from DataModel"""
        self.Cur.execute(SqlCommand)
        for Rs in self.Cur:
            EdkLogger.verbose(Rs)
        SqlCommand = """select count(*) as Count from DataModel"""
        self.Cur.execute(SqlCommand)
        for Item in self.Cur:
            EdkLogger.verbose("***Total %s records in table DataModel***" % Item)
        EdkLogger.verbose("Query tabel DataModel DONE!")

    ## Drop a table
    #
    # Drop the table DataModel
    #
    def Drop(self):
        SqlCommand = """drop table IF EXISTS DataModel"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Drop tabel DataModel ... DONE!")
    
    ## Init table
    #
    # Create all default records of table DataModel
    #  
    def InitTable(self):
        EdkLogger.verbose("\nInitialize table DataModel started ...")
        ID = 0
        for Item in DataClass.MODEL_LIST:
            ID = ID + 1
            CrossIndex = Item[1]
            Name = Item[0]
            Description = Item[0]
            self.Insert(ID, CrossIndex, Name, Description)
        EdkLogger.verbose("Initialize table DataModel ... DONE!")
