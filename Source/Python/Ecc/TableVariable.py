## @file
# This file is used to create/update/query/erase table for variables
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
from Table import Table

## TableVariable
#
# This class defined a table used for variable
# 
# @param object:       Inherited from object class
#
#
class TableVariable(Table):
    def __init__(self, Cursor):
        self.Cur = Cursor
        self.Table = 'Variable'
    
    ## Create table
    #
    # Create table Variable
    #
    # @param ID:                 ID of a Variable
    # @param Modifier:           Modifier of a Variable
    # @param Type:               Type of a Variable
    # @param Name:               Name of a Variable
    # @param Value:              Value of a Variable
    # @param Model:              Model of a Variable
    # @param BelongsToFile:      The Variable belongs to which file
    # @param BelongsToFunction:  The Variable belongs to which function
    # @param StartLine:          StartLine of a Variable
    # @param StartColumn:        StartColumn of a Variable
    # @param EndLine:            EndLine of a Variable
    # @param EndColumn:          EndColumn of a Variable
    #
    def Create(self):
        SqlCommand = """create table IF NOT EXISTS %s(ID SINGLE PRIMARY KEY,
                                                      Modifier VARCHAR,
                                                      Type VARCHAR,
                                                      Name VARCHAR NOT NULL,
                                                      Value VARCHAR NOT NULL,
                                                      Model INTEGER NOT NULL,
                                                      BelongsToFile SINGLE NOT NULL,
                                                      BelongsToFunction SINGLE DEFAULT -1,
                                                      StartLine INTEGER NOT NULL,
                                                      StartColumn INTEGER NOT NULL,
                                                      EndLine INTEGER NOT NULL,
                                                      EndColumn INTEGER NOT NULL
                                                     )""" % self.Table
        Table.Create(self, SqlCommand)

    ## Insert table
    #
    # Insert a record into table Variable
    #
    # @param ID:                 ID of a Variable
    # @param Modifier:           Modifier of a Variable
    # @param Type:               Type of a Variable
    # @param Name:               Name of a Variable
    # @param Value:              Value of a Variable
    # @param Model:              Model of a Variable
    # @param BelongsToFile:      The Variable belongs to which file
    # @param BelongsToFunction:  The Variable belongs to which function
    # @param StartLine:          StartLine of a Variable
    # @param StartColumn:        StartColumn of a Variable
    # @param EndLine:            EndLine of a Variable
    # @param EndColumn:          EndColumn of a Variable
    #
    def Insert(self, ID, Modifier, Type, Name, Value, Model, BelongsToFile, BelongsToFunction, StartLine, StartColumn, EndLine, EndColumn):
        SqlCommand = """insert into %s values(%s, '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s)""" \
                                           % (self.Table, ID, Modifier, Type, Name, Value, Model, BelongsToFile, BelongsToFunction, StartLine, StartColumn, EndLine, EndColumn)
        Table.Insert(self, SqlCommand)
