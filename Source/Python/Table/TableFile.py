## @file
# This file is used to create/update/query/erase table for files
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

## TableFile
#
# This class defined a table used for file
# 
# @param object:       Inherited from object class
#
class TableFile(Table):
    def __init__(self, Cursor):
        self.Cur = Cursor
        self.Table = 'File'
    
    ## Create table
    #
    # Create table File
    #
    # @param ID:        ID of a File
    # @param Name:      Name of a File
    # @param ExtName:   ExtName of a File
    # @param Path:      Path of a File
    # @param FullPath:  FullPath of a File
    # @param Model:     Model of a File
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS %s (ID SINGLE PRIMARY KEY,
                                                       Name VARCHAR NOT NULL,
                                                       ExtName VARCHAR,
                                                       Path VARCHAR,
                                                       FullPath VARCHAR NOT NULL,
                                                       Model INTEGER DEFAULT 0
                                                      )""" % self.Table
        Table.Create(self, SqlCommand)

    ## Insert table
    #
    # Insert a record into table File
    #
    # @param ID:        ID of a File
    # @param Name:      Name of a File
    # @param ExtName:   ExtName of a File
    # @param Path:      Path of a File
    # @param FullPath:  FullPath of a File
    # @param Model:     Model of a File
    #
    def Insert(self, ID, Name, ExtName, Path, FullPath, Model):
        SqlCommand = """insert into %s values(%s, '%s', '%s', '%s', '%s', %s)""" \
                                           % (self.Table, ID, Name, ExtName, Path, FullPath, Model)
        Table.Insert(self, SqlCommand)
