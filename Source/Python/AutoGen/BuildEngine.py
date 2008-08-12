## @file
# The engine for building files
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
import re
import string

from Common.BuildToolError import *
from Common.Misc import tdict
import Common.EdkLogger as EdkLogger

## Convert file type to makefile macro name
#
#   @param      FileType    The name of file type
#
#   @retval     string      The name of macro
#
def FileType2Macro(FileType):
    return "$(%s_LIST)" % FileType.replace("-", "_").upper()

## Class for one build rule
#
# This represents a build rule which can give out corresponding command list for
# building the given source file(s). The result can be used for generating the
# target for makefile.
#
class FileBuildRule:
    ## constructor
    #
    #   @param  Input       The dictionary represeting input file(s) for a rule
    #   @param  Output      The list represeting output file(s) for a rule
    #   @param  Command     The list containing commands to generate the output from input
    #
    def __init__(self, Type, Input, Output, Command, ExtraDependency=None):
        # The Input should not be empty
        if Input == None or len(Input) == 0:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "No input files for a build rule")
        if Output == None:
            Output = []

        self.SourceFileType = [Type]
        self.SourceFileExtList = []
        # source files listed not in "*" or "?" pattern format
        if ExtraDependency == None:
            self.ExtraSourceFileList = []
        else:
            self.ExtraSourceFileList = ExtraDependency
        self.IsMultipleInput = False
        for File in Input:
            Base, Ext = os.path.splitext(File)
            if Base.find("*") >= 0:
                # There's "*" in the file name
                self.IsMultipleInput = True
            elif Base.find("?") < 0:
                # There's no "*" and "?" in file name
                self.ExtraSourceFileList.append(File)
                continue
            if Ext not in self.SourceFileExtList:
                self.SourceFileExtList.append(Ext)

        if len(self.SourceFileType) > 1:
            self.IsMultipleInput = True

        if len(Command) == 0:
            self.IsMultipleInput = False

        self.DestFileList = Output
        self.DestFile = ""
        if len(Output) > 0:
            self.DestFileExt = os.path.splitext(Output[0])[1]
        else:
            self.DestFileExt = ''
        self.DestPath = ""
        self.DestFileName = ""
        self.DestFileBase = ""
        self.CommandList = Command

    ## str() function support
    #
    #   @retval     string
    #
    def __str__(self):
        SourceString = ""
        SourceString += " %s %s %s" % (self.SourceFileType, " ".join(self.SourceFileExtList), self.ExtraSourceFileList)
        DestString = ", ".join(self.DestFileList)
        CommandString = "\n\t".join(self.CommandList)
        return "%s : %s\n\t%s" % (DestString, SourceString, CommandString)

    ## Check if given file extension is supported by this rule
    #
    #   @param  FileExt     The extension of a file
    #
    #   @retval True        If the extension is supported
    #   @retval False       If the extension is not supported
    #
    def IsSupported(self, FileExt):
        return FileExt in self.SourceFileExtList

    ## Apply the rule to given source file(s)
    #
    #   @param  SourceFile      One file or a list of files to be built
    #   @param  RelativeToDir   The relative path of the source file
    #   @param  PathSeparator   Path separator
    #
    #   @retval     tuple       (Source file in full path, List of individual sourcefiles, Destionation file, List of build commands)
    #
    def Apply(self, SourceFile, RelativeToDir, PathSeparator):
        # source file
        if not self.IsMultipleInput:
            SrcFileName = os.path.basename(SourceFile)
            SrcFileBase, SrcFileExt = os.path.splitext(SrcFileName)
            if RelativeToDir != None:
                SrcFileDir = os.path.dirname(SourceFile)
                if SrcFileDir == "":
                    SrcFileDir = "."

                SrcFile = PathSeparator.join([RelativeToDir, SourceFile])
            else:
                SrcFileDir = "."
                SrcFile = SourceFile
            SrcPath = os.path.dirname(SrcFile)
        else:
            SrcFileName = ""
            SrcFileBase = ""
            SrcFileExt = ""
            SrcFileDir = ""
            SrcPath = ""
            # SourceFile must be a list
            SrcFileList = []
            for FileType in self.SourceFileType:
                Macro = FileType2Macro(FileType)
                SrcFileList.append(Macro)
            SrcFile = " ".join(SrcFileList)

        # destination file
        for Index in range(len(self.DestFileList)):
            self.DestFileList[Index] = self.DestFileList[Index].replace("(+)", PathSeparator)
        for Index in range(len(self.CommandList)):
            self.CommandList[Index] = self.CommandList[Index].replace("(+)", PathSeparator)

        if self.DestFile == "" and len(self.DestFileList) > 0:
            self.DestFile = self.DestFileList[0]
        if self.DestPath == "":
            self.DestPath = os.path.dirname(self.DestFile)
        if self.DestFileName == "":
            self.DestFileName = os.path.basename(self.DestFile)
        if self.DestFileBase == "":
            self.DestFileBase = os.path.splitext(self.DestFileName)[0]

        BuildRulePlaceholderDict = {
            # source file
            "src"       :   SrcFile,
            "s_path"    :   SrcPath,
            "s_dir"     :   SrcFileDir,
            "s_name"    :   SrcFileName,
            "s_base"    :   SrcFileBase,
            "s_ext"     :   SrcFileExt,
            # destination file
            "dst"       :   self.DestFile,
            "d_path"    :   self.DestPath,
            "d_name"    :   self.DestFileName,
            "d_base"    :   self.DestFileBase,
            "d_ext"     :   self.DestFileExt,
        }

        DstFile = ''
        if len(self.DestFileList) > 0:
            DstFile = self.DestFileList[0]
            DstFile = string.Template(DstFile).safe_substitute(BuildRulePlaceholderDict)
            DstFile = string.Template(DstFile).safe_substitute(BuildRulePlaceholderDict)
        CommandList = []
        for CommandString in self.CommandList:
            CommandString = string.Template(CommandString).safe_substitute(BuildRulePlaceholderDict)
            CommandString = string.Template(CommandString).safe_substitute(BuildRulePlaceholderDict)
            CommandList.append(CommandString)

        return SrcFile, self.ExtraSourceFileList, DstFile, CommandList

## Class for build rules
#
# BuildRule class parses rules defined in a file or passed by caller, and converts
# the rule into FileBuildRule object.
#
class BuildRule:
    _SectionHeader = "SECTIONHEADER"
    _Section = "SECTION"
    _SubSectionHeader = "SUBSECTIONHEADER"
    _SubSection = "SUBSECTION"
    _InputFile = "INPUTFILE"
    _OutputFile = "OUTPUTFILE"
    _ExtraDependency = "EXTRADEPENDENCY"
    _Command = "COMMAND"
    _UnknownSection = "UNKNOWNSECTION"

    _SubSectionList = [_InputFile, _OutputFile, _Command]

    _FileTypePattern = re.compile("^[_a-zA-Z][_\-0-9a-zA-Z]*$")

    ## Constructor
    #
    #   @param  File                The file containing build rules in a well defined format
    #   @param  Content             The string list of build rules in a well defined format
    #   @param  LineIndex           The line number from which the parsing will begin
    #   @param  SupportedFamily     The list of supported tool chain families
    #
    def __init__(self, File=None, Content=None, LineIndex=0, SupportedFamily=["MSFT", "INTEL", "GCC"]):
        self.RuleFile = File
        # Read build rules from file if it's not none
        if File != None:
            try:
                self.RuleContent = open(File, 'r').readlines()
            except:
                EdkLogger.error("build", FILE_OPEN_FAILURE, ExtraData=File)
        elif Content != None:
            self.RuleContent = Content
        else:
            EdkLogger.error("build", PARAMETER_MISSING, ExtraData="No rule file or string given")

        self.SupportedToolChainFamilyList = SupportedFamily
        self.RuleDatabase = tdict(True, 4)  # {FileExt, ModuleType, Arch, Family : FileBuildRule object}
        self.FileTypeDict = {}  # {ext : file-type}

        self._LineIndex = LineIndex
        self._State = ""
        self._RuleInfo = tdict(True, 2)     # {toolchain family : {"InputFile": {}, "OutputFile" : [], "Command" : []}}
        self._FileType = ''
        self._BuildTypeList = []
        self._ArchList = []
        self._FamilyList = []
        self._TotalToolChainFamilySet = set()
        self._RuleObjectList = [] # FileBuildRule object list

        self.Parse()

    ## Parse the build rule strings
    def Parse(self):
        self._State = self._Section
        for Index in range(self._LineIndex, len(self.RuleContent)):
            Line = self.RuleContent[Index].strip()
            self.RuleContent[Index] = Line

            # skip empty or comment line
            if Line == "" or Line[0] == "#":
                continue

            # find out section header, enclosed by []
            if Line[0] == '[' and Line[-1] == ']':
                # merge last section information into rule database
                self.EndOfSection()
                self._State = self._SectionHeader
            # find out sub-section header, enclosed by <>
            elif Line[0] == '<' and Line[-1] == '>':
                if self._State != self._UnknownSection:
                    self._State = self._SubSectionHeader
            # call section handler to parse each (sub)section
            self._StateHandler[self._State](self, Index)
        # merge last section information into rule database
        self.EndOfSection()

        # setup the relationship between file extension and file type
        for RuleObject in self._RuleObjectList:
            for FileType in RuleObject.SourceFileType:
                for FileExt in RuleObject.SourceFileType[FileType]:
                    self.FileTypeDict[FileExt] = FileType

    ## Parse definitions under a section
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseSection(self, LineIndex):
        pass

    ## Parse definitions under a subsection
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseSubSection(self, LineIndex):
        # currenly nothing here
        pass

    ## Placeholder for not supported sections
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def SkipSection(self, LineIndex):
        pass

    ## Merge section information just got into rule database
    def EndOfSection(self):
        Database = self.RuleDatabase
        # if there's specific toochain family, 'COMMON' doesnt make any sense any more
        if len(self._TotalToolChainFamilySet) > 1 and 'COMMON' in self._TotalToolChainFamilySet:
            self._TotalToolChainFamilySet.remove('COMMON')
        for Family in self._TotalToolChainFamilySet:
            Input = self._RuleInfo[Family, self._InputFile]
            if Input == None or len(Input) == 0:
                EdkLogger.error("build", FORMAT_INVALID, File=self.RuleFile,
                                ExtraData="No input files found for rule %s" % self._FileType)

            Output = self._RuleInfo[Family, self._OutputFile]
            if Output == None:
                Output = []

            Command = self._RuleInfo[Family, self._Command]
            if Command == None:
                Command = []

            ExtraDependency = self._RuleInfo[Family, self._ExtraDependency]
            if ExtraDependency == None:
                ExtraDependency = []

            BuildRule = FileBuildRule(self._FileType, Input, Output, Command, ExtraDependency)
            for BuildType in self._BuildTypeList:
                for Arch in self._ArchList:
                    for FileExt in BuildRule.SourceFileExtList:
                        Database[FileExt, BuildType, Arch, Family] = BuildRule

    ## Parse section header
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseSectionHeader(self, LineIndex):
        self._RuleInfo = tdict(True, 2)
        self._BuildTypeList = []
        self._ArchList = []
        self._FamilyList = []
        self._TotalToolChainFamilySet = set()
        FileType = ''
        RuleNameList = self.RuleContent[LineIndex][1:-1].split(',')
        for RuleName in RuleNameList:
            Arch = 'COMMON'
            BuildType = 'COMMON'
            TokenList = [Token.strip().upper() for Token in RuleName.split('.')]
            # old format: Build.File-Type
            if TokenList[0] == "BUILD":
                if len(TokenList) == 1:
                    EdkLogger.error("build", FORMAT_INVALID, "Invalid rule section",
                                    File=self.RuleFile, Line=LineIndex+1,
                                    ExtraData=self.RuleContent[LineIndex])

                FileType = TokenList[1]
                if FileType == '':
                    EdkLogger.error("build", FORMAT_INVALID, File=self.RuleFile, Line=LineIndex+1,
                                    ExtraData="No file type given: " + Line)
                if self._FileTypePattern.match(FileType) == None:
                    EdkLogger.error("build", FORMAT_INVALID, File=self.RuleFile, Line=LineIndex+1,
                                    ExtraData="Only character, number (non-first character), '_' and '-' are allowed in file type")
            # new format: File-Type.Build-Type.Arch
            else:
                if FileType == '':
                    FileType = TokenList[0]
                elif FileType != TokenList[0]:
                    EdkLogger.error("build", FORMAT_INVALID,
                                    "Different file types are not allowed in the same rule section",
                                    File=self.RuleFile, Line=LineIndex+1,
                                    ExtraData=self.RuleContent[LineIndex])
                if len(TokenList) > 1:
                    BuildType = TokenList[1]
                if len(TokenList) > 2:
                    Arch = TokenList[2]
            if BuildType not in self._BuildTypeList:
                self._BuildTypeList.append(BuildType)
            if Arch not in self._ArchList:
                self._ArchList.append(Arch)

        if 'COMMON' in self._BuildTypeList and len(self._BuildTypeList) > 1:
            EdkLogger.error("build", FORMAT_INVALID,
                            "Specific build types must not be mixed with common one",
                            File=self.RuleFile, Line=LineIndex+1,
                            ExtraData=self.RuleContent[LineIndex])
        if 'COMMON' in self._ArchList and len(self._ArchList) > 1:
            EdkLogger.error("build", FORMAT_INVALID,
                            "Specific ARCH must not be mixed with common one",
                            File=self.RuleFile, Line=LineIndex+1,
                            ExtraData=self.RuleContent[LineIndex])

        self._FileType = FileType
        self._State = self._Section

    ## Parse sub-section header
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseSubSectionHeader(self, LineIndex):
        SectionType = ""
        List = self.RuleContent[LineIndex][1:-1].split(',')
        FamilyList = []
        for Section in List:
            TokenList = Section.split('.')
            Type = TokenList[0].strip().upper()

            if SectionType == "":
                SectionType = Type
            elif SectionType != Type:
                EdkLogger.error("build", FORMAT_INVALID,
                                "Two different section types are not allowed in the same sub-section",
                                File=self.RuleFile, Line=LineIndex+1,
                                ExtraData=self.RuleContent[LineIndex])

            if len(TokenList) > 1:
                Family = TokenList[1].strip().upper()
            else:
                Family = "COMMON"

            if Family not in FamilyList:
                FamilyList.append(Family)

        self._FamilyList = FamilyList
        self._TotalToolChainFamilySet.update(FamilyList)
        self._State = SectionType.upper()
        if 'COMMON' in FamilyList and len(FamilyList) > 1:
            EdkLogger.error("build", FORMAT_INVALID,
                            "Specific tool chain family should not be mixed with general one",
                            File=self.RuleFile, Line=LineIndex+1,
                            ExtraData=self.RuleContent[LineIndex])
        if self._State not in self._StateHandler:
            EdkLogger.error("build", FORMAT_INVALID, File=self.RuleFile, Line=LineIndex+1,
                            ExtraData="Unknown subsection: %s" % self.RuleContent[LineIndex])
    ## Parse <InputFile> sub-section
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseInputFile(self, LineIndex):
        FileList = [File.strip() for File in self.RuleContent[LineIndex].split(",")]
        for ToolChainFamily in self._FamilyList:
            InputFiles = self._RuleInfo[ToolChainFamily, self._State]
            if InputFiles == None:
                InputFiles = []
                self._RuleInfo[ToolChainFamily, self._State] = InputFiles
            InputFiles.extend(FileList)

    ## Parse <ExtraDependency> sub-section
    #
    #   @param  LineIndex   The line index of build rule text
    #
    def ParseCommon(self, LineIndex):
        for ToolChainFamily in self._FamilyList:
            Items = self._RuleInfo[ToolChainFamily, self._State]
            if Items == None:
                Items = []
                self._RuleInfo[ToolChainFamily, self._State] = Items
            Items.append(self.RuleContent[LineIndex])

    ## Get a build rule via [] operator
    #
    #   @param  FileExt             The extension of a file
    #   @param  ToolChainFamily     The tool chain family name
    #   @param  BuildVersion        The build version number. "*" means any rule
    #                               is applicalbe.
    #
    #   @retval FileType        The file type string
    #   @retval FileBuildRule   The object of FileBuildRule
    #
    # Key = (FileExt, ModuleType, Arch, ToolChainFamily)
    def __getitem__(self, Key):
        RuleObj = self.RuleDatabase[Key]
        if RuleObj == None:
            return None, None
        return RuleObj.SourceFileType[0], RuleObj

    _StateHandler = {
        _SectionHeader     : ParseSectionHeader,
        _Section           : ParseSection,
        _SubSectionHeader  : ParseSubSectionHeader,
        _SubSection        : ParseSubSection,
        _InputFile         : ParseInputFile,
        _OutputFile        : ParseCommon,
        _ExtraDependency   : ParseCommon,
        _Command           : ParseCommon,
        _UnknownSection    : SkipSection,
    }

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    import sys
    EdkLogger.Initialize()
    if len(sys.argv) > 1:
        Br = BuildRule(sys.argv[1])
        print str(Br[".c", "DXE_DRIVER", "IA32", "MSFT"][1])
        print
        print str(Br[".c", "DXE_DRIVER", "IA32", "INTEL"][1])
        print
        print str(Br[".c", "DXE_DRIVER", "IA32", "GCC"][1])
        print
        print str(Br[".ac", "ACPI_TABLE", "IA32", "MSFT"][1])
        print
        print str(Br[".h", "ACPI_TABLE", "IA32", "INTEL"][1])
        print
        print str(Br[".ac", "ACPI_TABLE", "IA32", "MSFT"][1])
        print
        print str(Br[".s", "SEC", "IPF", "COMMON"][1])
        print
        print str(Br[".s", "SEC"][1])

