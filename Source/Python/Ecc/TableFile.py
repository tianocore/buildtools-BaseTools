## @file
# This file is used to create/update/query/erase table for files
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

## TableFile
#
# This class defined a table used for file
# 
# @param object:       Inherited from object class
#
class TableFile(object):
    def __init__(self, Cursor):
        self.Cur = Cursor
    
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
        SqlCommand = """create table IF NOT EXISTS File(ID SINGLE PRIMARY KEY,
                                                        Name VARCHAR NOT NULL,
                                                        ExtName VARCHAR,
                                                        Path VARCHAR,
                                                        FullPath VARCHAR NOT NULL,
                                                        Model INTEGER DEFAULT 0
                                                       )"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Create table File ... DONE!")

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
        SqlCommand = """insert into File values(%s, '%s', '%s', '%s', '%s', %s)""" \
                                             % (ID, Name, ExtName, Path, FullPath, Model)
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose(SqlCommand + " ... DONE!")
    
    ## Query table
    #
    # Query all records of table File
    #  
    def Query(self):
        EdkLogger.verbose("\nQuery tabel File started ...")
        SqlCommand = """select * from File"""
        self.Cur.execute(SqlCommand)
        for Rs in self.Cur:
            EdkLogger.verbose(Rs)
        SqlCommand = """select count(*) as Count from File"""
        self.Cur.execute(SqlCommand)
        for Item in self.Cur:
            EdkLogger.verbose("***Total %s records in table File***" % Item)
        EdkLogger.verbose("Query tabel File DONE!")

    ## Drop a table
    #
    # Drop the table File
    #
    def Drop(self):
        SqlCommand = """drop table IF EXISTS File"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Drop tabel File ... DONE!")

