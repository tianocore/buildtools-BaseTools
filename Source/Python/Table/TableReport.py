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
import EccToolError

## TableReport
#
# This class defined a table used for data model
# 
# @param object:       Inherited from object class
#
#
class TableReport(Table):
    def __init__(self, Cursor):
        Table.__init__(self, Cursor)
        self.Table = 'Report'
    
    ## Create table
    #
    # Create table report
    #
    # @param ID:             ID of an Error
    # @param ErrorID:        ID of an Error TypeModel of a Report item
    # @param BelongsToItem:  The error belongs to which item
    # @param BelongsToFile:  The error belongs to which file
    # @param Enabled:        If this error enabled
    # @param Corrected:      if this error corrected
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS %s (ID INTEGER PRIMARY KEY,
                                                       ErrorID INTEGER NOT NULL,
                                                       BelongsToTable TEXT NOT NULL,
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
    # @param ErrorID:        ID of an Error TypeModel of a report item
    # @param BelongsToTable: The error item belongs to which table
    # @param BelongsToItem:  The error belongs to which item
    # @param BelongsToFile:  The error belongs to which file
    # @param Enabled:        If this error enabled
    # @param Corrected:      if this error corrected
    #
    def Insert(self, ErrorID, BelongsToTable, BelongsToItem = -1, BelongsToFile = -1, Enabled = 0, Corrected = -1):
        self.ID = self.ID + 1
        SqlCommand = """insert into %s values(%s, %s, '%s', %s, %s, %s, %s)""" \
                     % (self.Table, self.ID, ErrorID, BelongsToTable, BelongsToItem, BelongsToFile, Enabled, Corrected)
        Table.Insert(self, SqlCommand)
        
        return self.ID
    
    ## Query table
    #
    # @retval:       A recordSet of all found records 
    #
    def Query(self):
        SqlCommand = """select ID, ErrorID, BelongsToTable, BelongsToItem, BelongsToFile, Corrected from %s
                        where Enabled > -1 order by ErrorID""" % (self.Table)
        return self.Exec(SqlCommand)

    ## Convert to CSV
    #
    # Get all enabled records from table report and save them to a .csv file
    #
    # @param Filename:  To filename to save the report content
    #
    def ToCSV(self, Filename = 'Report.csv'):
        File = open(Filename, 'w+')
        File.write("""No, File, LineNo, Error Code, Error Message\r\n""")
        RecordSet = self.Query()
        Index = 0
        for Record in RecordSet:
            Index = Index + 1
            ErrorID = Record[1]
            BelongsToTable = Record[2]
            BelongsToItem = Record[3]
            BelongsToFile = Record[4]
            IsCorrected = Record[5]
            SqlCommand = """select A.StartLine, B.FullPath from %s as A, File as B
                            where A.ID = %s and B.ID = %s
                         """ % (BelongsToTable, BelongsToItem, BelongsToFile)
            NewRecord = self.Exec(SqlCommand)
            if NewRecord != []:
                File.write("""%s, %s, %s, %s, %s\r\n""" % (Index, NewRecord[0][0], NewRecord[0][1], ErrorID, EccToolError.gEccErrorMessage[ErrorID])) 
        
        File.close()

