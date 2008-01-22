## @file
# This file is used to create/update/query/erase table for data models
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

##
# Import Modules
#
import Common.EdkLogger as EdkLogger
import CommonDataClass.DataClass as DataClass
from Table import Table
from Common.String import ConvertToSqlString

## TableDataModel
#
# This class defined a table used for data model
# 
# @param object:       Inherited from object class
#
#
class TableDataModel(Table):
    def __init__(self, Cursor):
        self.Cur = Cursor
        self.Table = 'DataModel'
    
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
        SqlCommand = """create table IF NOT EXISTS %s (ID SINGLE PRIMARY KEY,
                                                       CrossIndex INTEGER NOT NULL,
                                                       Name VARCHAR NOT NULL,
                                                       Description VARCHAR
                                                      )""" % self.Table
        Table.Create(self, SqlCommand)

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
        ID = self.GenerateID(ID)
        (Name, Description) = ConvertToSqlString((Name, Description))
        SqlCommand = """insert into %s values(%s, %s, '%s', '%s')""" % (self.Table, ID, CrossIndex, Name, Description)
        Table.Insert(self, SqlCommand)
    
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
    
    ## Get CrossIndex
    #
    # Get a model's cross index from its name
    #
    # @param ModelName:    Name of the model
    # @retval CrossIndex:  CrossIndex of the model
    #
    def GetCrossIndex(self, ModelName):
        CrossIndex = -1
        SqlCommand = """select CrossIndex from DataModel where name = '""" + ModelName + """'"""
        self.Cur.execute(SqlCommand)
        for Item in self.Cur:
            CrossIndex = Item[0]
        
        return CrossIndex
