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
import string

from Common.BuildToolError import *
import Common.EdkLogger as EdkLogger

## Convert file type to makefile macro name
#
#   @param      FileType    The name of file type
#
#   @retval     string      The name of macro
#
def FileType2Macro(FileType):
    return "$(%s_LIST)" % FileType.replace("-", "_").upper()

class FileBuildRule:
    def __init__(self, Input, Output, Command):
        if Input == {}:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "No input files for a build rule")
        if Output == []:
            EdkLogger.error("AutoGen", AUTOGEN_ERROR, "No output files for a build rule")

        self.SourceFileType = {}
        self.SourceFileExtList = []
        self.ExtraSourceFileList = []
        self.IsMultipleInput = False
        for FileType in Input:
            if FileType not in self.SourceFileType:
                self.SourceFileType[FileType] = []
            for File in Input[FileType]:
                Base, Ext = os.path.splitext(File)
                if Base.find("*") >= 0:
                    # There's "*" in the file name
                    self.IsMultipleInput = True
                elif Base.find("?") < 0:
                    # There's no "*" and "?" in file name
                    self.ExtraSourceFileList.append(File)
                    continue
                self.SourceFileType[FileType].append(Ext)
                self.SourceFileExtList.append(Ext)

        if len(self.SourceFileType) > 1:
            self.IsMultipleInput = True

        self.DestFileList = Output
        self.DestFile = ""
        self.DestFileExt = os.path.splitext(Output[0])[1]
        self.DestPath = ""
        self.DestFileName = ""
        self.DestFileBase = ""
        self.CommandList = Command

    def __str__(self):
        SourceString = ""
        for FileType in self.SourceFileType:
            SourceString += " %s(%s)" % (FileType, " ".join(self.SourceFileType[FileType]))
        DestString = ", ".join(self.DestFileList)
        CommandString = "\n\t".join(self.CommandList)
        return "%s : %s\n\t%s" % (DestString, SourceString, CommandString)

    def IsSupported(self, FileExt):
        return FileExt in self.SourceFileExtList

    def Apply(self, SourceFile, RelativeToDir, PathSeparator):
        # source file
        if not self.IsMultipleInput:
            SrcFileName = os.path.basename(SourceFile)
            SrcFileBase, SrcFileExt = os.path.splitext(SrcFileName)
            if RelativeToDir != None:
                SrcFileDir = os.path.dirname(SourceFile)
                if SrcFileDir == "":
                    SrcFileDir = "."

                SrcFile = PathSeparator.join(["$(WORKSPACE)", RelativeToDir, SourceFile])
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
            #for File in SourceFile:
            #    if RelativeToDir != None:
            #        SrcFileList.append(PathSeparator.join(["$(WORKSPACE)", RelativeToDir, File]))
            #    else:
            #        SrcFileList.append(File)
            for FileType in self.SourceFileType:
                Macro = FileType2Macro(FileType)
                SrcFileList.append(Macro)
            SrcFile = " ".join(SrcFileList)

        # destination file
        for Index in range(len(self.DestFileList)):
            self.DestFileList[Index] = self.DestFileList[Index].replace("(+)", PathSeparator)
        for Index in range(len(self.CommandList)):
            self.CommandList[Index] = self.CommandList[Index].replace("(+)", PathSeparator)

        if self.DestFile == "":
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
            #"d_dir"     :   SrcFileDir,
            "d_name"    :   self.DestFileName,
            "d_base"    :   self.DestFileBase,
            "d_ext"     :   self.DestFileExt,
        }

        DstFileList = []
        for FileString in self.DestFileList:
            FileString = string.Template(FileString).safe_substitute(BuildRulePlaceholderDict)
            FileString = string.Template(FileString).safe_substitute(BuildRulePlaceholderDict)
            DstFileList.append(FileString)
        CommandList = []
        for CommandString in self.CommandList:
            CommandString = string.Template(CommandString).safe_substitute(BuildRulePlaceholderDict)
            CommandString = string.Template(CommandString).safe_substitute(BuildRulePlaceholderDict)
            CommandList.append(CommandString)
        #print "%s : %s\n\t%s" % (DstFileList[0], SrcFile, "\n\t".join(CommandList))
        return SrcFile, self.ExtraSourceFileList, DstFileList[0], CommandList

class BuildRule:
    _SectionHeader = "SECTIONHEADER"
    _Section = "SECTION"
    _SubSectionHeader = "SUBSECTIONHEADER"
    _SubSection = "SUBSECTION"
    _InputFile = "INPUTFILE"
    _OutputFile = "OUTPUTFILE"
    _Command = "COMMAND"
    _UnknownSection = "UNKNOWNSECTION"

    _SubSectionList = [_InputFile, _OutputFile, _Command]

    def __init__(self, File=None, Content=None, LineIndex=0, SupportedFamily=["MSFT", "INTEL", "GCC"]):
        self.RuleFile = File
        if File != None:
            try:
                self.RuleContent = open(File, 'r').readlines()
            except:
                EdkLogger.error("BuildRuleParser", FILE_OPEN_FAILURE, ExtraData=File)
        elif Content != None:
            self.RuleContent = Content
        else:
            EdkLogger.error("BuildRuleParser", PARSER_ERROR, "No rule file or string given")

        self.SupportedToolChainFamilyList = SupportedFamily
        self.RuleDatabase = {}  # {version : {family : {file type : FileBuildRule object}}}
        self.FileTypeDict = {}  # {ext : file-type}

        self._LineIndex = LineIndex
        self._BuildVersion = "*"
        self._RuleInfo = {}     # {toolchain family : {"InputFile": {}, "OutputFile" : [], "Command" : []}}
        self._FileTypeList = []
        self._FamilyList = []
        self._State = ""
        self._RuleObjectList = [] # FileBuildRule object list
        self.Parse()

    def Parse(self):
        self._State = self._Section
        for Index in range(self._LineIndex, len(self.RuleContent)):
            Line = self.RuleContent[Index].strip()
            self.RuleContent[Index] = Line

            # skip empty or comment line
            if Line == "" or Line[0] == "#":
                continue

            if Line[0] == '[' and Line[-1] == ']':
                self.EndOfSection()
                self._State = self._SectionHeader
            elif Line[0] == '<' and Line[-1] == '>':
                if self._State != self._UnknownSection:
                    self._State = self._SubSectionHeader

            self._StateHandler[self._State](self, Index)
        self.EndOfSection()
        for RuleObject in self._RuleObjectList:
            for FileType in RuleObject.SourceFileType:
                for FileExt in RuleObject.SourceFileType[FileType]:
                    self.FileTypeDict[FileExt] = FileType

    def ParseSection(self, LineIndex):
        TokenList = self.RuleContent[LineIndex].split("=", 1)
        if len(TokenList) != 2 or TokenList[0] != "BUILD_VERSION":
            EdkLogger.error("BuildRuleParser", PARSER_ERROR, "Invalid definition",
                            File=RuleFile, Line=LineIndex+1, ExtraData=self.RuleContent[LineIndex])

        try:
            self._BuildVersion = int(TokenList[1].strip(), 0)
        except:
            EdkLogger.error("BuildRuleParser", PARSER_ERROR, "Version is not a valid number",
                            File=self.RuleFile, Line=LineIndex+1, ExtraData=self.RuleContent[LineIndex])

    def ParseSubSection(self, LineIndex):
        pass

    def SkipSection(self, LineIndex):
        pass

    def EndOfSection(self):
        if self._FileTypeList == [] or self._RuleInfo == {}:
            return

        Database = self.RuleDatabase
        if self._BuildVersion not in Database:
            Database[self._BuildVersion] = {}
        Database = self.RuleDatabase[self._BuildVersion]

        # expand *
        FamilyList = self._RuleInfo.keys()
        if "*" in FamilyList and len(FamilyList) > 1:
            FamilyList.remove("*")

        NewRuleInfo = {}
        for Family in self._RuleInfo:
            Rule = self._RuleInfo[Family]
            if Family == "*" and Family not in FamilyList:
                NewFamilyList = FamilyList
            else:
                NewFamilyList = [Family]

            for NewFamily in NewFamilyList:
                if NewFamily not in NewRuleInfo:
                    NewRuleInfo[NewFamily] = {}

                if self._InputFile in Rule:
                    NewRuleInfo[NewFamily][self._InputFile] = Rule[self._InputFile]
                if self._OutputFile in Rule:
                    NewRuleInfo[NewFamily][self._OutputFile] = Rule[self._OutputFile]
                if self._Command in Rule:
                    NewRuleInfo[NewFamily][self._Command] = Rule[self._Command]

        for NewFamily in FamilyList:
            Rule = NewRuleInfo[NewFamily]
            if NewFamily not in Database:
                Database[NewFamily] = {}

            if self._InputFile in Rule:
                Input = Rule[self._InputFile]
            else:
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "No input files found for a rule")

            if self._OutputFile in Rule:
                Output = Rule[self._OutputFile]
            else:
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "No output files found a rule")

            if self._Command in Rule:
                Command = Rule[self._Command]
            else:
                Command = []

            if NewFamily == "*":
                for Family in self.SupportedToolChainFamilyList:
                    if Family not in Database:
                        Database[Family] = {}
                    RuleObject = FileBuildRule(Input, Output, Command)
                    self._RuleObjectList.append(RuleObject)
                    for FileType in RuleObject.SourceFileType:
                        Database[Family][FileType] = RuleObject
            else:
                RuleObject = FileBuildRule(Input, Output, Command)
                self._RuleObjectList.append(RuleObject)
                for FileType in RuleObject.SourceFileType:
                    Database[NewFamily][FileType] = RuleObject

        self._RuleInfo = {}

    def ParseSectionHeader(self, LineIndex):
        BuildVersion = ""
        FileTypeList = []
        RuleNameList = self.RuleContent[LineIndex][1:-1].split(',')
        for RuleName in RuleNameList:
            TokenList = RuleName.split('.')
            if len(TokenList) == 1:
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "Invalid rule section",
                                File=self.RuleFile, Line=LineIndex+1, ExtraData=self.RuleContent[LineIndex])

            Rule = TokenList[0].strip()
            if Rule.upper() != "BUILD":
                self._State = self._UnknownSection
                return

            FileType = TokenList[1].strip()
            if FileType == '':
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "No file type given",
                                File=self.RuleFile, Line=LineIndex+1, ExtraData=Line)
            FileTypeList.append(FileType)

        self._FileTypeList = FileTypeList
        self._BuildVersion = "*"
        self._State = self._Section

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
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "Two different section types are not allowed",
                                File=self.RuleFile, Line=LineIndex+1, ExtraData=Line)

            if len(TokenList) > 1:
                Family = TokenList[1].strip().upper()
            else:
                Family = "*"

            if Family not in FamilyList:
                FamilyList.append(Family)

        self._FamilyList = FamilyList
        self._State = SectionType.upper()

    def ParseInputFile(self, LineIndex):
        Line = self.RuleContent[LineIndex]
        TokenList = Line.split("=")
        FileType = ""
        if len(TokenList) > 1:
            FileType = TokenList[0].strip()
            if FileType not in self._FileTypeList:
                EdkLogger.error("BuildRuleParser", PARSER_ERROR,
                                "File type must be one of %s: %s" % (self._FileTypeList, FileType),
                                File=self.RuleFile, ExtraData=Line, Line=LineIndex+1)
            FileString = TokenList[1]
        else:
            if len(self._FileTypeList) > 1:
                EdkLogger.error("BuildRuleParser", PARSER_ERROR, "File type must be given",
                                File=self.RuleFile, Line=LineIndex, ExtraData=Line)
            else:
                FileType = self._FileTypeList[0]
            FileString = TokenList[0]

        FileList = FileString.split(",")
        for File in FileList:
            File = File.strip()
            for Family in self._FamilyList:
                if Family not in self._RuleInfo:
                    self._RuleInfo[Family] = {}
                if self._State not in self._RuleInfo[Family]:
                    self._RuleInfo[Family][self._State] = {}
                if FileType not in self._RuleInfo[Family][self._State]:
                    self._RuleInfo[Family][self._State][FileType] = []
                self._RuleInfo[Family][self._State][FileType].append(File)

    def ParseOutputFile(self, LineIndex):
        FileList = self.RuleContent[LineIndex].split(",")
        for File in FileList:
            File = File.strip()
            for Family in self._FamilyList:
                if Family not in self._RuleInfo:
                    self._RuleInfo[Family] = {}
                    self._RuleInfo[Family][self._State] = []
                if self._State not in self._RuleInfo[Family]:
                    self._RuleInfo[Family][self._State] = []
                self._RuleInfo[Family][self._State].append(File)

    def ParseCommand(self, LineIndex):
        Command = self.RuleContent[LineIndex]
        for Family in self._FamilyList:
            if Family not in self._RuleInfo:
                self._RuleInfo[Family] = {}
                self._RuleInfo[Family][self._State] = []
            if self._State not in self._RuleInfo[Family]:
                self._RuleInfo[Family][self._State] = []
            self._RuleInfo[Family][self._State].append(Command)

    # FileBuildRule object
    def Get(self, FileExt, ToolChainFamily, BuildVersion="*"):
        if FileExt not in self.FileTypeDict:
            return None, None
        FileType = self.FileTypeDict[FileExt]
        Database = {}
        BuildRuleObject = None
        if BuildVersion in self.RuleDatabase:
            Database = self.RuleDatabase[BuildVersion]
        elif BuildVersion != "*":
            if "*" not in self.RuleDatabase:
                return FileType, None
            Database = self.RuleDatabase["*"]
        else:
            # BuildVersion == "*" and "*" not in self.RuleDatabase
            # try to match ToolChainFamily
            for Ver in self.RuleDatabase:
                Database = self.RuleDatabase[Ver]
                if ToolChainFamily not in Database:
                    continue
                if FileType not in Database[ToolChainFamily]:
                    continue
                break
            else:
                return FileType, None

        if ToolChainFamily not in Database:
            return FileType, None
        if FileType not in Database[ToolChainFamily]:
            return FileType, None
        if not Database[ToolChainFamily][FileType].IsSupported(FileExt):
            return FileType, None

        return FileType, Database[ToolChainFamily][FileType]

    _StateHandler = {
        _SectionHeader     : ParseSectionHeader,
        _Section           : ParseSection,
        _SubSectionHeader  : ParseSubSectionHeader,
        _SubSection        : ParseSubSection,
        _InputFile         : ParseInputFile,
        _OutputFile        : ParseOutputFile,
        _Command           : ParseCommand,
        _UnknownSection    : SkipSection,
    }



# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    pass
