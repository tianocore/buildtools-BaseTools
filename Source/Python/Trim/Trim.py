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

import Common.EdkLogger as EdkLogger

# Version and Copyright
__version_number__ = "0.01"
__version__ = "%prog Version " + __version_number__
__copyright__ = "Copyright (c) 2007, Intel Corporation. All rights reserved."

## Regular expression for matching "#line xxx"/"# xxx"
gLineControlDirective = re.compile("^\s*#line\s+[0-9]+\s+(.+)$")
## Regular expression for matching "typedef struct"
gTypedefPattern = re.compile("^\s*typedef\s+struct\s+[{]*$", re.MULTILINE)
## Regular expression for matching "#pragma pack"
gPragmaPattern = re.compile("^\s*#pragma\s+pack", re.MULTILINE)
## Regular expression for matching HEX number
gHexNumberPattern = re.compile("0[xX]([0-9a-fA-F]+)", re.MULTILINE)

## Get the name of file in the Line Control directive line
#
# Extract the name of file whose content was injected by preprocessor from the
# Line Control directive line
#
# @param  Line     The string may contain the line control directive
#
# @retval "string" The name of the file
#
def GetInjectedFile(Line):
    FileList = gLineControlDirective.findall(Line)
    if len(FileList) != 1:
        return ""
    return FileList[0]
    
    
## Trim preprocessed source code
#
# Remove extra content made by preprocessor. The preprocessor must enable the
# line number generation option when preprocessing.
#
# @param  Source    File to be trimmed
# @param  Target    File to store the trimmed content
# @param  Convert   If True, convert standard HEX format to MASM format
#
def TrimPreprocessedFile (Source, Target, Convert):
    f = open (Source, 'r')
    # read whole file
    Lines = f.readlines()
    f.close()

    # skip empty lines, if any(necessary?)
    FirstLine = ""
    for Line in Lines:
        FirstLine = Line.strip()
        if FirstLine != "":
            break

    PreprocessedFile = GetInjectedFile(FirstLine)
    if PreprocessedFile != "":
        # find "#line" from the end of file to the top of file
        for Index in range (len(Lines) - 1, -1, -1):
            Line = Lines[Index].strip()
            InjectedFile = GetInjectedFile(Line)
            
            # skip lines without "#line"
            if InjectedFile == "":
                continue
            
            # empty embedded line control lines
            if InjectedFile == PreprocessedFile:
                Lines[Index] = "\n"
                EdkLogger.verbose("Found embedded line control directive at line%d: %s" % (Index + 1, Line))
                continue
            else:
                # remove the lines between the top of file and the last "#line"
                StartOfCode = Index + 1
                EdkLogger.verbose("Found last non-embedded line control directive at line%d: %s" % (Index, Line))
                break
    else:
        # no "#line" found, keep all lines
        StartOfCode = 0

    # convert HEX number format if indicated
    if Convert:
        ConvertHex(Lines, StartOfCode, len(Lines))

    # save to file
    f = open (Target, 'w')
    f.writelines(Lines[StartOfCode:])
    f.close()

## Trim preprocessed VFR file
#
# Remove extra content made by preprocessor. The preprocessor doesn't need to
# enable line number generation option when preprocessing.
#
# @param  Source    File to be trimmed
# @param  Target    File to store the trimmed content
#
def TrimPreprocessedVfr(Source, Target):
    f = open (Source,'r')
    # read whole file
    Lines = f.readlines()
    f.close()

    FoundTypedef = False
    Brace = 0
    TypedefStart = 0
    TypedefEnd = 0
    for Index in range (len(Lines)):
        Line = Lines[Index]
        # don't trim the lines from "formset" definition to the end of file
        if Line.strip() == 'formset':
            break

        if FoundTypedef == False and (Line.find('#line') == 0 or Line.find('# ') == 0):
            # empty the line number directive if it's not aomong "typedef struct"
            Lines[Index] = "\n"
            continue

        if FoundTypedef == False and gTypedefPattern.search(Line) == None:
            # keep "#pragram pack" directive
            if gPragmaPattern.search(Line) == None:
                Lines[Index] = "\n"
            continue
        elif FoundTypedef == False:
            # found "typedef struct", keept its position and set a flag
            FoundTypedef = True
            TypedefStart = Index

        # match { and } to find the end of typedef definition
        if Line.find("{") >= 0:
            Brace += 1
        elif Line.find("}") >= 0:
            Brace -= 1

        # "typedef struct" must end with a ";"
        if Brace == 0 and Line.find(";") >= 0:
            FoundTypedef = False
            TypedefEnd = Index
            # keep all "typedef struct" except to GUID, EFI_PLABEL and PAL_CALL_RETURN
            if Line.strip("} ;\r\n") in ["GUID", "EFI_PLABEL", "PAL_CALL_RETURN"]:
                for i in range(TypedefStart, TypedefEnd+1):
                    Lines[i] = "\n"

    # save all lines trimmed
    f = open (Target,'w')
    f.writelines(Lines)
    f.close()

## Convert HEX format
#
# Convert HEX format like 0xabcd to MASM format like abcdh.
#
# @param  Lines     List containg the string which may have hex number
# @param  Start     The line number to start the conversion
# @param  End       The line number to end the conversion
#
def ConvertHex(Lines, Start, End):
    for Index in range (Start, End):
        #
        # HEX number starting with [abcdef] must be prefixed with a '0'
        # otherwise assembler will take it as symbol
        #
        Lines[Index] = gHexNumberPattern.sub(r"0\1h", Lines[Index])

## Parse command line options
#
# Using standard Python module optparse to parse command line option of this tool.
#
# @retval Options   A optparse.Values object containing the parsed options
# @retval InputFile Path of file to be trimmed
#
def Options():
    OptionList = [
        make_option("-s", "--source-code", dest="FileType", const="SourceCode", action="store_const",
                          help="The input file is preprocessed source code, including C or assembly code"),
        make_option("-r", "--vfr-file", dest="FileType", const="Vfr", action="store_const",
                          help="The input file is preprocessed VFR file"),
        make_option("-c", "--convert-hex", dest="ConvertHex", action="store_true",
                          help="Convert standard hex format (0xabcd) to MASM format (abcdh)"),
        make_option("-o", "--output", dest="OutputFile",
                          help="File to store the trimmed content"),
        make_option("-v", "--verbose", dest="LogLevel", action="store_const", const=EdkLogger.VERBOSE,
                          help="Run verbosely"),
        make_option("-d", "--debug", dest="LogLevel", type="int",
                          help="Run with debug information"),
        make_option("-q", "--quiet", dest="LogLevel", action="store_const", const=EdkLogger.QUIET,
                          help="Run quietly"),
        make_option("-?", action="help", help="show this help message and exit"),
    ]

    # use clearer usage to override default usage message
    UsageString = "%prog [-s|-r] [-c] [-v|-d <debug_level>|-q] [-o <output_file>] <input_file>"

    Parser = OptionParser(description=__copyright__, version=__version__, option_list=OptionList, usage=UsageString)
    Parser.set_defaults(FileType="Vfr")
    Parser.set_defaults(ConvertHex=False)
    Parser.set_defaults(LogLevel=EdkLogger.INFO)

    Options, Args = Parser.parse_args()

    # error check
    if len(Args) == 0:
        raise BuildToolError(OPTION_MISSING, name="Input file", usage=Parser.get_usage())
    if len(Args) > 1:
        raise BuildToolError(OPTION_NOT_SUPPORTED, name="Too many input files", usage=Parser.get_usage())

    InputFile = Args[0]
    if Options.OutputFile == None:
        Options.OutputFile = os.path.splitext(InputFile)[0] + '.iii'

    return Options, InputFile

## Entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
# @retval 0     Tool was successful
# @retval 1     Tool failed
#
def Main():
    try:
        CommandOptions, InputFile = Options()
        if CommandOptions.LogLevel < EdkLogger.DEBUG_9:
            EdkLogger.setLevel(CommandOptions.LogLevel + 1)
        else:
            EdkLogger.setLevel(CommandOptions.LogLevel)

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
