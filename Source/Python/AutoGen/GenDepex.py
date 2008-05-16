## @file
# This file is used to generate DEPEX file for module's dependency expression
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

## Import Modules
#
import sys
import os
import re
import traceback

from StringIO import StringIO
from struct import pack
from Common.BuildToolError import *
from Common.Misc import SaveFileOnChange
from Common import EdkLogger as EdkLogger

import antlr3
from DepexLexer import DepexLexer
from DepexParser import DepexParser

## Mapping between module type and EFI phase
gType2Phase = {
    "BASE"              :   None,
    "SEC"               :   "PEI",
    "PEI_CORE"          :   "PEI",
    "PEIM"              :   "PEI",
    "DXE_CORE"          :   "DXE",
    "DXE_DRIVER"        :   "DXE",
    "DXE_SMM_DRIVER"    :   "DXE",
    "DXE_RUNTIME_DRIVER":   "DXE",
    "DXE_SAL_DRIVER"    :   "DXE",
    "UEFI_DRIVER"       :   "DXE",
    "UEFI_APPLICATION"  :   "DXE",
}

## Convert dependency expression string into EFI internal representation
#
#   DependencyExpression class is used to parse dependency expression string and
# convert it into its binary form.
#
class DependencyExpression:

    OpcodePriority = {
        "AND"   :   1,
        "OR"    :   1,
        "NOT"   :   2,
        # "SOR"   :   9,
        # "BEFORE":   9,
        # "AFTER" :   9,
    }

    Opcode = {
        "PEI"   : {
            "PUSH"  :   0x02,
            "AND"   :   0x03,
            "OR"    :   0x04,
            "NOT"   :   0x05,
            "TRUE"  :   0x06,
            "FALSE" :   0x07,
            "END"   :   0x08
        },

        "DXE"   : {
            "BEFORE":   0x00,
            "AFTER" :   0x01,
            "PUSH"  :   0x02,
            "AND"   :   0x03,
            "OR"    :   0x04,
            "NOT"   :   0x05,
            "TRUE"  :   0x06,
            "FALSE" :   0x07,
            "END"   :   0x08,
            "SOR"   :   0x09
        }
    }

    # all supported op codes and operands
    SupportedOpcode = ["BEFORE", "AFTER", "PUSH", "AND", "OR", "NOT", "END", "SOR"]
    SupportedOperand = ["TRUE", "FALSE"]
    ## Constructor
    #
    #   @param  Expression  The list or string of dependency expression
    #   @param  ModuleType  The type of the module using the dependency expression
    #
    def __init__(self, Expression, ModuleType, Optimize=False, File=''):
        self.Phase = gType2Phase[ModuleType]
        if type(Expression) == type([]):
            self.ExpressionString = " ".join(Expression)
        else:
            self.ExpressionString = Expression

        self.File = File
        self.Tokens = None
        self.Parser = None

        self.PostfixNotation = []
        self.TokenList = []
        self.OpcodeList = []

        self.Parse()
        if Optimize:
            self.Optimize()

    def __str__(self):
        return " ".join(self.PostfixNotation)

    def Parse(self):
        self.Tokens = antlr3.CommonTokenStream(DepexLexer(antlr3.ANTLRStringStream(self.ExpressionString)))
        self.Tokens.fillBuffer()
        self.Parser = DepexParser(self.Tokens)
        self.Parser.start(self.File)

        self.PostfixNotation = self.Parser.PostfixNotation
        self.TokenList = self.Parser.TokenList
        self.OpcodeList = self.Parser.OpcodeList

    ## Simply optimize the dependency expression by removing duplicated operands
    def Optimize(self):
        ValidOpcode = list(set(self.OpcodeList))
        if len(ValidOpcode) != 1 or ValidOpcode[0] not in ['AND', 'OR']:
            return
        Op = ValidOpcode[0]
        NewOperand = []
        AllOperand = set()
        for Token in self.PostfixNotation:
            if Token in self.SupportedOpcode or Token in NewOperand:
                continue
            AllOperand.add(Token)
            if Token == 'TRUE':
                if Op == 'AND':
                    continue
                else:
                    NewOperand.append(Token)
                    break
            elif Token == 'FALSE':
                if Op == 'OR':
                    continue
                else:
                    NewOperand.append(Token)
                    break
            NewOperand.append(Token)

        if len(NewOperand) == 0:
            self.TokenList = list(AllOperand)
        else:
            self.TokenList = []
            while True:
                self.TokenList.append(NewOperand.pop(0))
                if NewOperand == []:
                    break
                self.TokenList.append(Op)
        self.PostfixNotation = []
        self.ExpressionString = ' '.join(self.TokenList)
        self.Parse()

    ## Convert a GUID value in C structure format into its binary form
    #
    #   @param  Guid    The GUID value in C structure format
    #
    #   @retval array   The byte array representing the GUID value
    #
    def GetGuidValue(self, Guid):
        GuidValueString = Guid.replace("{", "").replace("}", "").replace(" ", "")
        GuidValueList = GuidValueString.split(",")
        if len(GuidValueList) != 11:
            EdkLogger.error("GenDepex", PARSER_ERROR, "Invalid GUID value string or opcode: %s" % Guid)
        return pack("1I2H8B", *(int(value, 16) for value in GuidValueList))

    ## Save the binary form of dependency expression in file
    #
    #   @param  File    The path of file. If None is given, put the data on console
    #
    #   @retval True    If the file doesn't exist or file is changed
    #   @retval False   If file exists and is not changed.
    #
    def Generate(self, File=None):
        Buffer = StringIO()
        for Item in self.PostfixNotation:
            if Item in self.Opcode[self.Phase]:
                Buffer.write(pack("B", self.Opcode[self.Phase][Item]))
            elif Item in self.SupportedOpcode:
                EdkLogger.error("GenDepex", FORMAT_INVALID,
                                "Opcode [%s] is not expected in %s phase" % (Item, self.Phase),
                                ExtraData=self.ExpressionString)
            else:
                Buffer.write(self.GetGuidValue(Item))

        FilePath = ""
        FileChangeFlag = True
        if File == None:
            sys.stdout.write(Buffer.getvalue())
            FilePath = "STDOUT"
        else:
            FileChangeFlag = SaveFileOnChange(File, Buffer.getvalue(), True)

        Buffer.close()
        return FileChangeFlag

versionNumber = "0.03"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007-2008, Intel Corporation  All rights reserved."
__usage__ = "%prog [options] [dependency_expression_file]"

## Parse command line options
#
#   @retval OptionParser
#
def GetOptions():
    from optparse import OptionParser

    Parser = OptionParser(description=__copyright__, version=__version__, usage=__usage__)

    Parser.add_option("-o", "--output", dest="OutputFile", default=None, metavar="FILE",
                      help="Specify the name of depex file to be generated")
    Parser.add_option("-t", "--module-type", dest="ModuleType", default=None,
                      help="The type of module for which the dependency expression serves")
    Parser.add_option("-e", "--dependency-expression", dest="Expression", default="",
                      help="The string of dependency expression. If this option presents, the input file will be ignored.")
    Parser.add_option("-m", "--optimize", dest="Optimize", default=False, action="store_true",
                      help="Do some simple optimization on the expression.")
    Parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                      help="build with verbose information")
    Parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
    Parser.add_option("-q", "--quiet", dest="quiet", default=False, action="store_true",
                      help="build with little information")

    return Parser.parse_args()


## Entrance method
#
# @retval 0     Tool was successful
# @retval 1     Tool failed
#
def Main():
    EdkLogger.Initialize()
    Option, Input = GetOptions()

    # Set log level
    if Option.verbose != None:
        EdkLogger.SetLevel(EdkLogger.VERBOSE)
    elif Option.quiet != None:
        EdkLogger.SetLevel(EdkLogger.QUIET)
    elif Option.debug != None:
        EdkLogger.SetLevel(Option.debug + 1)
    else:
        EdkLogger.SetLevel(EdkLogger.INFO)

    try:
        if Option.ModuleType == None or Option.ModuleType not in gType2Phase:
            EdkLogger.error("GenDepex", OPTION_MISSING, "Module type is not specified or supported")

        DxsFile = ''
        if len(Input) > 0 and Option.Expression == "":
            DxsFile = Input[0]
            DxsString = open(DxsFile, 'r').read()
        elif Option.Expression != "":
            if Option.Expression[0] == '"':
                DxsString = Option.Expression[1:-1]
            else:
                DxsString = Option.Expression
        else:
            EdkLogger.error("GenDepex", OPTION_MISSING, "No expression string or file given")

        DxsString += '\n'
        Dpx = DependencyExpression(DxsString, Option.ModuleType, Option.Optimize, DxsFile)

        if Option.OutputFile != None:
            Dpx.Generate(Option.OutputFile)
        else:
            Dpx.Generate()
    except BaseException, X:
        EdkLogger.quiet("")
        if Option != None and Option.debug != None:
            EdkLogger.quiet(traceback.format_exc())
        else:
            EdkLogger.quiet(str(X))
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(Main())

