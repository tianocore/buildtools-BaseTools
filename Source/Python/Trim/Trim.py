## @file
# Trim files preprocessed by compiler
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
import os
import sys
import re

from optparse import OptionParser
from optparse import make_option

from Common.BuildToolError import *
from Common.Misc import *

## Version and Copyright
__version_number__ = "0.01"
__version__ = "%prog Version " + __version_number__
__copyright__ = "Copyright (c) 2007, Intel Corporation. All rights reserved."

## Global variables
gTypedefPattern = re.compile("^\s*typedef\s+struct\s+[{]*$", re.MULTILINE)
gPragmaPattern = re.compile("^\s*#pragma\s+pack", re.MULTILINE)
gHexNumberPattern = re.compile("0[xX]([0-9a-fA-F]+)", re.MULTILINE)

## Trim preprocessed source code
#
# Remove extra content made by preprocessor. The preprocessor must enable the
# line number generation option when preprocessing.
#
# @param  foo  A parameter
#
# @retval EFI_OK  Function was successful
# @retval Other   Function failed
#
def TrimPreprocessedFile (Source, Target, Convert):
    f = open (Source, 'r')
    Lines = f.readlines()
    f.close()

    for Index in range (len(Lines) - 1, -1, -1):
        Line = Lines[Index].strip()
        if Line.find('#line') == 0 or Line.find('# ') == 0:
            EndOfCode = Index + 1
            break
    else:
        Index = 0
        EndOfCode = len(Lines) - 1

    if Convert:
        ConvertHex(Lines, EndOfCode, len(Lines))

    f = open (Target, 'w')
    f.writelines(Lines[EndOfCode:])
    f.close()

## brief dsce
#
# Detailed description of what the function does
# and how it does it.
#
# @param  foo  A parameter
#
# @retval EFI_OK  Function was successful
# @retval Other   Function failed
#
def TrimPreprocessedVfr(Source, Target):
    f = open (Source,'r')
    Lines = f.readlines()
    f.close()

    FoundTypedef = False
    Brace = 0
    TypedefStart = 0
    TypedefEnd = 0
    for Index in range (len(Lines)):
        Line = Lines[Index]
        if Line.strip() == 'formset':
            break

        if FoundTypedef == False and (Line.find('#line') == 0 or Line.find('# ') == 0):
            Lines[Index] = "\n"
            continue

        if FoundTypedef == False and gTypedefPattern.search(Line) == None:
            if gPragmaPattern.search(Line) == None:
                Lines[Index] = "\n"
            continue
        elif FoundTypedef == False:
            FoundTypedef = True
            TypedefStart = Index

        if Line.find("{") >= 0:
            Brace += 1
        elif Line.find("}") >= 0:
            Brace -= 1

        if Brace == 0 and Line.find(";") >= 0:
            FoundTypedef = False
            TypedefEnd = Index
            if Line.strip("} ;\r\n") in ["GUID", "EFI_PLABEL", "PAL_CALL_RETURN"]:
                for i in range(TypedefStart, TypedefEnd+1):
                    Lines[i] = "\n"

    f = open (Target,'w')
    f.writelines(Lines)
    f.close()

## brief dsce
#
# Detailed description of what the function does
# and how it does it.
#
# @param  foo  A parameter
#
# @retval EFI_OK  Function was successful
# @retval Other   Function failed
#
def ConvertHex(Lines, start, end):
    for Index in range (start, end):
        Lines[Index] = gHexNumberPattern.sub(r"\1h", Lines[Index])

## brief dsce
#
# Detailed description of what the function does
# and how it does it.
#
# @param  foo  A parameter
#
# @retval EFI_OK  Function was successful
# @retval Other   Function failed
#
def Options():
    OptionList = [
        make_option("-s", "--source-code", dest="FileType", const="SourceCode", action="store_const",
                          help="The input file is preprocessed source code, including C or assembly code"),
        make_option("-v", "--vfr-file", dest="FileType", const="Vfr", action="store_const",
                          help="The input file is preprocessed VFR file"),
        make_option("-c", "--convert-hex", dest="ConvertHex", action="store_true",
                          help="Convert standard hex format (0xabcd) to MASM format (abcdh)"),
        make_option("-o", "--output", dest="OutputFile",
                          help="File to store the trimmed content"),
        make_option("-?", action="help", help="show this help message and exit"),
    ]
    
    UsageString = "%prog [-s|-v] [-c] [-o <output_file>] <input_file>"

    Parser = OptionParser(description=__copyright__, version=__version__, option_list=OptionList, usage=UsageString)
    Parser.set_defaults(FileType="SourceCode")
    Parser.set_defaults(ConvertHex=False)

    Options, Args = Parser.parse_args()

    if len(Args) == 0:
        raise BuildToolError(OPTION_MISSING, name="Input file", usage=Parser.get_usage())
    if len(Args) > 1:
        raise BuildToolError(OPTION_NOT_SUPPORTED, name="Too many input files", usage=Parser.get_usage())

    InputFile = Args[0]
    if Options.OutputFile == None:
        Options.OutputFile = os.path.splitext(InputFile)[0] + '.iii'

    return Options, InputFile

## brief dsce
#
# Detailed description of what the function does
# and how it does it.
#
# @param  foo  A parameter
#
# @retval EFI_OK  Function was successful
# @retval Other   Function failed
#
def Main():
    try:
        CommandOptions, InputFile = Options()

        if CommandOptions.FileType == "Vfr":
            TrimPreprocessedVfr(InputFile, CommandOptions.OutputFile)
        else :
            TrimPreprocessedFile(InputFile, CommandOptions.OutputFile, CommandOptions.ConvertHex)
    except Exception, e:
        print e
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(Main())
