# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
# This file is used to generate DEPEX file for module's dependency expression
#

import sys
import os
import re
from StringIO import StringIO
from struct import pack
from EdkIIWorkspace import CreateDirectory
#from AutoGen import gModuleDatabase

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

class DependencyExpression:

    OpcodePriority = {
        "AND"   :   1,
        "OR"    :   1,
        "NOT"   :   2,
        "SOR"   :   9,
        "BEFORE":   9,
        "AFTER" :   9,
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

    SupportedOpcode = ["BEFORE", "AFTER", "PUSH", "AND", "OR", "NOT", "TRUE", "FALSE", "END", "SOR"]
    
    NonEndingOpcode = ["AND", "OR"]

    ExclusiveOpcode = ["BEFORE", "AFTER"]
    
    AboveAllOpcode = ["SOR"]

    #
    # open and close brace must be taken as individual tokens
    #
    TokenPattern = re.compile("(\(|\)|\{[^{}]+\{[^{}]+\}[ ]*\}|\w+)")
    
    def __init__(self, expression, mtype):
        self.Phase = gType2Phase[mtype]
        if type(expression) == type([]):
            self.ExpressionString = " ".join(expression)
            self.TokenList = expression
        else:
            self.ExpressionString = expression
            self.GetExpressionTokenList()

        self.PostfixNotation = []
        self.OpcodeList = []

        self.GetPostfixNotation()
        self.ValidateOpcode()

    def GetExpressionTokenList(self):
        self.TokenList = self.TokenPattern.findall(self.ExpressionString)

    def GetPostfixNotation(self):
        stack = []
        for token in self.TokenList:
            if token == "(":
                stack.append(token)
            elif token == ")":
                while len(stack) > 0:
                    if stack[-1] == '(':
                        stack.pop()
                        break
                    self.PostfixNotation.append(stack.pop())
            elif token in self.OpcodePriority:
                while len(stack) > 0:
                    if stack[-1] == "(" or self.OpcodePriority[token] > self.OpcodePriority[stack[-1]]:
                        break
                    self.PostfixNotation.append(stack.pop())
                stack.append(token)
                self.OpcodeList.append(token)
            else:
                if token not in self.Opcode[self.Phase]:
                    self.PostfixNotation.append("PUSH")
                else:
                    self.OpcodeList.append(token)
                self.PostfixNotation.append(token)
        while len(stack) > 0:
            self.PostfixNotation.append(stack.pop())
        self.PostfixNotation.append("END")
        #print "  ","\n   ".join(self.PostfixNotation)

    def ValidateOpcode(self):
        for op in self.AboveAllOpcode:
            if op in self.OpcodeList and op != self.OpcodeList[0]:
                raise Exception("Opcode=%s should be the first one in expression", op)
        for op in self.ExclusiveOpcode:
            if op in self.OpcodeList and len(self.OpcodeList) > 1:
                raise Exception("Opcode=%s should be only opcode in expression", op)
        # print "######", self.ExpressionString
        if self.TokenList[-1] in self.NonEndingOpcode:
            raise Exception("Extra %s at the end of dependency expression" % self.TokenList[-1])

    def GetGuidValue(self, guid):
        guidValueString = guid.replace("{", "").replace("}", "").replace(" ", "")
        guidValueList = guidValueString.split(",")
        if len(guidValueList) != 11:
            raise Exception("Invalid GUID value string or opcode: %s" % guid)
        return pack("1I2H8B", *(int(value, 16) for value in guidValueList))

    def SaveFile(self, file, content):
        CreateDirectory(os.path.dirname(file))
        f = None
        if os.path.exists(file):
            f = open(file, 'rb')
            if content == f.read():
                f.close()
                return
            f.close()
        f = open(file, "wb")
        f.write(content)
        f.close()

    def Generate(self, file=None):
        buffer = StringIO()
        for item in self.PostfixNotation:
            if item in self.Opcode[self.Phase]:
                buffer.write(pack("B", self.Opcode[self.Phase][item]))
            else:
                buffer.write(self.GetGuidValue(item))

        filePath = ""
        if file == None:
            sys.stdout.write(buffer.getvalue())
            filePath = "STDOUT"
        else:
            self.SaveFile(file, buffer.getvalue())
            filePath = file

        buffer.close()
        return filePath

versionNumber = "0.01"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."
__usage__ = "%prog [options] [dependency_expression_file]"

def GetOptions():
    from optparse import OptionParser

    parser = OptionParser(description=__copyright__, version=__version__, usage=__usage__)

    parser.add_option("-o", "--output", dest="OutputFile", default=None, metavar="FILE",
                      help="Specify the name of depex file to be generated")
    parser.add_option("-t", "--module-type", dest="ModuleType", default=None,
                      help="The type of module for which the dependency expression serves")
    parser.add_option("-e", "--dependency-expression", dest="Expression", default="",
                      help="The string of dependency expression. If this option presents, the input file will be ignored.")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                      help="build with verbose information")
    parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true",
                      help="build with debug information")
    parser.add_option("-q", "--quiet", dest="quiet", default=False, action="store_true",
                      help="build with little information")

    return parser.parse_args()


def Main():
    option, input = GetOptions()
    if option.ModuleType == None or option.ModuleType not in gType2Phase:
        print "Module type is not specified or supported"
        return -1

    try:
        if len(input) > 0 and option.Expression == "":
            dxsFile = input[0]
            dxsString = open(dxsFile, 'r').read().replace("\n", " ").replace("\r", " ")
            dxsString = re.compile("DEPENDENCY_START(.+)DEPENDENCY_END").findall(dxsString)[0]
        elif option.Expression != "":
            dxsString = option.Expression
        else:
            print "No expression string or file given"
            return -1

        dpx = DependencyExpression(dxsString, option.ModuleType)

        if option.OutputFile != None:
            dpx.Generate(option.OutputFile)
        else:
            dpx.Generate()
    except Exception, e:
        return -1

    return 0

if __name__ == '__main__':
    sys.exit(Main())
