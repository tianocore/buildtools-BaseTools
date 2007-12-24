## @file
# This file is used to create/update/query/erase table for functions
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

## TableFunction
#
# This class defined a table used for function
# 
# @param object:       Inherited from object class
#
class TableFunction(object):
    def __init__(self, Cursor):
        self.Cur = Cursor
    
    ## Create table
    #
    # Create table Function
    #
    # @param ID:               ID of a Function
    # @param Header:           Header of a Function
    # @param Modifier:         Modifier of a Function 
    # @param Name:             Name of a Function
    # @param ReturnStatement:  ReturnStatement of a Funciont
    # @param StartLine:        StartLine of a Function
    # @param StartColumn:      StartColumn of a Function
    # @param EndLine:          EndLine of a Function
    # @param EndColumn:        EndColumn of a Function
    # @param BelongsToFile:    The Function belongs to which file
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS Function(ID SINGLE PRIMARY KEY,
                                                            Header TEXT,
                                                            Modifier VARCHAR,
                                                            Name VARCHAR NOT NULL,
                                                            ReturnStatement VARCHAR,
                                                            StartLine INTEGER NOT NULL,
                                                            StartColumn INTEGER NOT NULL,
                                                            EndLine INTEGER NOT NULL,
                                                            EndColumn INTEGER NOT NULL,
                                                            BelongsToFile SINGLE NOT NULL
                                                           )"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Create table Function ... DONE!")

    ## Insert table
    #
    # Insert a record into table Function
    #
    # @param ID:               ID of a Function
    # @param Header:           Header of a Function
    # @param Modifier:         Modifier of a Function 
    # @param Name:             Name of a Function
    # @param ReturnStatement:  ReturnStatement of a Funciont
    # @param StartLine:        StartLine of a Function
    # @param StartColumn:      StartColumn of a Function
    # @param EndLine:          EndLine of a Function
    # @param EndColumn:        EndColumn of a Function
    # @param BelongsToFile:    The Function belongs to which file
    #
    def Insert(self, ID, Header, Modifier, Name, ReturnStatement, StartLine, StartColumn, EndLine, EndColumn, BelongsToFile):
        SqlCommand = """insert into Function values(%s, '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s)""" \
                                                 % (ID, Header, Modifier, Name, ReturnStatement, StartLine, StartColumn, EndLine, EndColumn, BelongsToFile)
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose(SqlCommand + " ... DONE!")
    
    ## Query table
    #
    # Query all records of table Function
    #  
    def Query(self):
        EdkLogger.verbose("\nQuery tabel Function started ...")
        SqlCommand = """select * from Function"""
        self.Cur.execute(SqlCommand)
        for Rs in self.Cur:
            EdkLogger.verbose(Rs)
        SqlCommand = """select count(*) as Count from Function"""
        self.Cur.execute(SqlCommand)
        for Item in self.Cur:
            EdkLogger.verbose("***Total %s records in table Function***" % Item)
        EdkLogger.verbose("Query tabel Function DONE!")

    ## Drop a table
    #
    # Drop the table Function
    #
    def Drop(self):
        SqlCommand = """drop table IF EXISTS Function"""
        self.Cur.execute(SqlCommand)
        EdkLogger.verbose("Drop tabel Function ... DONE!")

