## @file
# This file is used to create/update/query/erase table for ECC reports
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
from Table import Table

## TableDsc
#
# This class defined a table used for data model
# 
# @param object:       Inherited from object class
#
#
class TableDsc(Table):
    def __init__(self, Cursor):
        Table.__init__(self, Cursor)
        self.Table = 'Report'
    
    ## Create table
    #
    # Create table report
    #
    # @param ID:             ID of an Error
    # @param ErrorID:        ID of an Error TypeModel of a Dsc item
    # @param BelongsToItem:  The error belongs to which item
    # @param BelongsToFile:  The error belongs to which file
    # @param Enabled:        If this error enabled
    # @param Corrected:      if this error corrected
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS %s (ID INTEGER PRIMARY KEY,
                                                       ErrorID INTEGER NOT NULL,
                                                       BelongsToItem SINGLE NOT NULL,
                                                       BelongsToFile SINGLE NOT NULL,
                                                       Enabled INTEGER DEFAULT 0,
                                                       Corrected INTEGER DEFAULT -1
                                                      )""" % self.Table
        Table.Create(self, SqlCommand)

    ## Insert table
    #
    # Insert a record into table report
    #
    # @param ID:             ID of an Error
    # @param ErrorID:        ID of an Error TypeModel of a Dsc item
    # @param BelongsToItem:  The error belongs to which item
    # @param BelongsToFile:  The error belongs to which file
    # @param Enabled:        If this error enabled
    # @param Corrected:      if this error corrected
    #
    def Insert(self, ErrorID, BelongsToItem, BelongsToFile, Enabled, Corrected):
        self.ID = self.ID + 1
        SqlCommand = """insert into %s values(%s, %s, %s, %s, %s, %s)""" \
                     % (self.Table, self.ID, ErrorID, BelongsToItem, BelongsToFile, Enabled, Corrected)
        Table.Insert(self, SqlCommand)
        
        return self.ID
    
    ## Query table
    #
    # @retval:       A recordSet of all found records 
    #
    def Query(self):
        SqlCommand = """select ID, ErrorID, BelongsToItem, BelongsToFile, Corrected from %s
                        where Enabled > -1""" % (self.Table)
        EdkLogger.debug(4, "SqlCommand: %s" % SqlCommand)
        self.Cur.execute(SqlCommand)
        return self.Cur.fetchall()

    ## Convert to CSV
    #
    # @param Filename:  To filename to save the report content
    #
    #
    def ToCSV(self, Filename = 'Report.csv'):
        pass