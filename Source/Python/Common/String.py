## @file
# This file is used to define common string related functions used in parsing process 
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
import DataType
import os.path
import string
import EdkLogger
from BuildToolError import *

## GetSplitValueList
#
# Get a value list from a string with multiple values splited with SplitTag
# The default SplitTag is DataType.TAB_VALUE_SPLIT
# 'AAA|BBB|CCC' -> ['AAA', 'BBB', 'CCC']
#
# @param String:    The input string to be splitted
# @param SplitTag:  The split key, default is DataType.TAB_VALUE_SPLIT
# @param MaxSplit:  The max number of split values, default is -1
#
# @retval list() A list for splitted string
#
def GetSplitValueList(String, SplitTag = DataType.TAB_VALUE_SPLIT, MaxSplit = -1):
    return map(lambda l: l.strip(), String.split(SplitTag, MaxSplit))

## MergeArches
#
# Find a key's all arches in dict, add the new arch to the list
# If not exist any arch, set the arch directly
#
# @param Dict:  The input value for Dict
# @param Key:   The input value for Key
# @param Arch:  The Arch to be added or merged
#
def MergeArches(Dict, Key, Arch):
    if Key in Dict.keys():
        Dict[Key].append(Arch)
    else:
        Dict[Key] = Arch.split()

## GenDefines
#
# Parse a string with format "DEFINE <VarName> = <PATH>"
# Generate a map Defines[VarName] = PATH
# Return False if invalid format
#
# @param String:   String with DEFINE statement
# @param Arch:     Supportted Arch
# @param Defines:  DEFINE statement to be parsed
#
# @retval 0   DEFINE statement found, and valid
# @retval 1   DEFINE statement found, but not valid
# @retval -1  DEFINE statement not found
#
def GenDefines(String, Arch, Defines):
    if String.find(DataType.TAB_DEFINE + ' ') > -1:
        List = String.replace(DataType.TAB_DEFINE + ' ', '').split(DataType.TAB_EQUAL_SPLIT)
        if len(List) == 2:
            Defines[(CleanString(List[0]), Arch)] = CleanString(List[1])
            return 0
        else:
            return -1

    return 1

## GenInclude
#
# Parse a string with format "!include <Filename>"
# Return the file path
# Return False if invalid format or NOT FOUND
#
# @param String:        String with INCLUDE statement
# @param IncludeFiles:  INCLUDE statement to be parsed
# @param Arch:          Supportted Arch
#
# @retval True
# @retval False
#
def GenInclude(String, IncludeFiles, Arch):
    if String.upper().find(DataType.TAB_INCLUDE.upper() + ' ') > -1:
        IncludeFile = CleanString(String[String.upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
        MergeArches(IncludeFiles, IncludeFile, Arch)
        return True
    else:
        return False

## GetExec
#
# Parse a string with format "InfFilename [EXEC = ExecFilename]"
# Return (InfFilename, ExecFilename)
#
# @param String:  String with EXEC statement
#
# @retval truple() A pair as (InfFilename, ExecFilename)
#
def GetExec(String):
    InfFilename = ''
    ExecFilename = ''
    if String.find('EXEC') > -1:
        InfFilename = String[ : String.find('EXEC')].strip()
        ExecFilename = String[String.find('EXEC') + len('EXEC') : ].strip()
    else:
        InfFilename = String.strip()

    return (InfFilename, ExecFilename)

## GetBuildOption
#
# Parse a string with format "[<Family>:]<ToolFlag>=Flag"
# Return (Family, ToolFlag, Flag)
#
# @param String:  String with BuildOption statement
# @param File:    The file which defines build option, used in error report
#
# @retval truple() A truple structure as (Family, ToolChain, Flag)
#
def GetBuildOption(String, File):
    if String.find(DataType.TAB_EQUAL_SPLIT) < 0:
        RaiseParserError(String, 'BuildOptions', File, '[<Family>:]<ToolFlag>=Flag')
    (Family, ToolChain, Flag) = ('', '', '')
    List = GetSplitValueList(String, DataType.TAB_EQUAL_SPLIT, MaxSplit = 1)
    if List[0].find(':') > -1:
        Family = CleanString(List[0][ : List[0].find(':')])
        ToolChain = CleanString(List[0][List[0].find(':') + 1 : ])
    else:
        ToolChain = CleanString(List[0])
    Flag = CleanString(List[1])

    return (Family, ToolChain, Flag)

## GetComponents
#
# Parse block of the components defined in dsc file
# Set KeyValues as [ ['component name', [lib1, lib2, lib3], [bo1, bo2, bo3], [pcd1, pcd2, pcd3]], ...]
#
# @param Lines:             The content to be parsed
# @param Key:               Reserved 
# @param KeyValues:         To store data after parsing
# @param CommentCharacter:  Comment char, used to ignore comment content
#
# @retval True Get component successfully
#
def GetComponents(Lines, Key, KeyValues, CommentCharacter):
    if Lines.find(DataType.TAB_SECTION_END) > -1:
        Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    (findBlock, findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, False, False, False, False, False, False)
    ListItem = None
    LibraryClassItem = []
    BuildOption = []
    Pcd = []

    LineList = Lines.split('\n')
    for Line in LineList:
        Line = CleanString(Line, CommentCharacter)
        if Line == None or Line == '':
            continue

        if findBlock == False:
            ListItem = Line
            #
            # find '{' at line tail
            #
            if Line.endswith('{'):
                findBlock = True
                ListItem = CleanString(Line.rsplit('{', 1)[0], CommentCharacter)

        #
        # Parse a block content
        #
        if findBlock:
            if Line.find('<LibraryClasses>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (True, False, False, False, False, False, False)
                continue
            if Line.find('<BuildOptions>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, True, False, False, False, False, False)
                continue
            if Line.find('<PcdsFeatureFlag>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, True, False, False, False, False)
                continue
            if Line.find('<PcdsPatchableInModule>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, False, True, False, False, False)
                continue
            if Line.find('<PcdsFixedAtBuild>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, False, False, True, False, False)
                continue
            if Line.find('<PcdsDynamic>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, False, False, False, True, False)
                continue
            if Line.find('<PcdsDynamicEx>') != -1:
                (findLibraryClass, findBuildOption, findPcdsFeatureFlag, findPcdsPatchableInModule, findPcdsFixedAtBuild, findPcdsDynamic, findPcdsDynamicEx) = (False, False, False, False, False, False, True)
                continue
            if Line.endswith('}'):
                #
                # find '}' at line tail
                #
                KeyValues.append([ListItem, LibraryClassItem, BuildOption, Pcd])
                findBlock = False
                findLibraryClass = False
                findBuildOption = False
                findPcdsFeatureFlag = False
                findPcdsPatchableInModule = False
                findPcdsFixedAtBuild = False
                findPcdsDynamic = False
                findPcdsDynamicEx = False
                LibraryClassItem = []
                BuildOption = []
                Pcd = []
                continue

        if findBlock:
            if findLibraryClass:
                LibraryClassItem.append(Line)
            elif findBuildOption:
                BuildOption.append(Line)
            elif findPcdsFeatureFlag:
                Pcd.append((DataType.TAB_PCDS_FEATURE_FLAG, Line))
            elif findPcdsPatchableInModule:
                Pcd.append((DataType.TAB_PCDS_PATCHABLE_IN_MODULE, Line))
            elif findPcdsFixedAtBuild:
                Pcd.append((DataType.TAB_PCDS_FIXED_AT_BUILD, Line))
            elif findPcdsDynamic:
                Pcd.append((DataType.TAB_PCDS_DYNAMIC, Line))
            elif findPcdsDynamicEx:
                Pcd.append((DataType.TAB_PCDS_DYNAMIC_EX, Line))
        else:
            KeyValues.append([ListItem, [], [], []])

    return True

## GetLibraryClassesWithModuleType
#
# Get Library Class definition when no module type defined
#
# @param Lines:             The content to be parsed
# @param Key:               Reserved 
# @param KeyValues:         To store data after parsing
# @param CommentCharacter:  Comment char, used to ignore comment content
#
# @retval True Get library classes successfully
#
def GetLibraryClassesWithModuleType(Lines, Key, KeyValues, CommentCharacter):
    newKey = SplitModuleType(Key)
    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    LineList = Lines.splitlines()
    for Line in LineList:
        Line = CleanString(Line, CommentCharacter)
        if Line != '' and Line[0] != CommentCharacter:
            KeyValues.append([CleanString(Line, CommentCharacter), newKey[1]])

    return True

## GetDynamics
#
# Get Dynamic Pcds
#
# @param Lines:             The content to be parsed
# @param Key:               Reserved 
# @param KeyValues:         To store data after parsing
# @param CommentCharacter:  Comment char, used to ignore comment content
#
# @retval True Get Dynamic Pcds successfully
#
def GetDynamics(Lines, Key, KeyValues, CommentCharacter):
    #
    # Get SkuId Name List
    #
    SkuIdNameList = SplitModuleType(Key)

    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    LineList = Lines.splitlines()
    for Line in LineList:
        Line = CleanString(Line, CommentCharacter)
        if Line != '' and Line[0] != CommentCharacter:
            KeyValues.append([CleanString(Line, CommentCharacter), SkuIdNameList[1]])

    return True

## SplitModuleType
#
# Split ModuleType out of section defien to get key
# [LibraryClass.Arch.ModuleType|ModuleType|ModuleType] -> [ 'LibraryClass.Arch', ['ModuleType', 'ModuleType', 'ModuleType'] ]
#
# @param Key:  String to be parsed
#
# @retval ReturnValue A list for module types
#
def SplitModuleType(Key):
    KeyList = Key.split(DataType.TAB_SPLIT)
    #
    # Fill in for arch
    #
    KeyList.append('')
    #
    # Fill in for moduletype
    #
    KeyList.append('')
    ReturnValue = []
    KeyValue = KeyList[0]
    if KeyList[1] != '':
        KeyValue = KeyValue + DataType.TAB_SPLIT + KeyList[1]
    ReturnValue.append(KeyValue)
    ReturnValue.append(GetSplitValueList(KeyList[2]))

    return ReturnValue

## NormPath
#
# Create a normal path
# And replace DFEINE in the path
#
# @param Path:     The input value for Path to be converted
# @param Defines:  A set for DEFINE statement
#
# @retval Path Formatted path
#
def NormPath(Path, Defines = {}):
    if Path != '':
        #
        # Replace with Define
        #
        for Key in Defines.keys():
            Path = Path.replace(Key, Defines[Key])

        #
        # Remove ${WORKSPACE}
        #
        if Path.find(DataType.TAB_WORKSPACE) > -1:
            Path = Path.replace(DataType.TAB_WORKSPACE, '')
            if Path.find(DataType.TAB_SLASH) == 0:
                Path = Path[1:]
            if Path.find(DataType.TAB_BACK_SLASH) == 0:
                Path = Path[1:]

        #
        # To local path format
        #
        Path = os.path.normpath(Path)

    return Path

## CleanString
#
# Remove comments in a string
# Remove spaces
#
# @param Line:              The string to be cleaned
# @param CommentCharacter:  Comment char, used to ignore comment content, default is DataType.TAB_COMMENT_SPLIT
#
# @retval Path Formatted path
#
def CleanString(Line, CommentCharacter = DataType.TAB_COMMENT_SPLIT):
    #
    # remove whitespace
    #
    Line = Line.strip();
    #
    # remove comments
    #
    Line = Line.split(CommentCharacter, 1)[0];
    #
    # remove whitespace again
    #
    Line = Line.strip();

    return Line

## GetMultipleValuesOfKeyFromLines
#
# Parse multiple strings to clean comment and spaces
# The result is saved to KeyValues
#
# @param Lines:             The content to be parsed
# @param Key:               Reserved 
# @param KeyValues:         To store data after parsing
# @param CommentCharacter:  Comment char, used to ignore comment content
#
# @retval True Successfully executed
#
def GetMultipleValuesOfKeyFromLines(Lines, Key, KeyValues, CommentCharacter):
    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    LineList = Lines.split('\n')
    for Line in LineList:
        Line = CleanString(Line, CommentCharacter)
        if Line != '' and Line[0] != CommentCharacter:
            KeyValues += [Line]

    return True

## GetDefineValue
#
# Parse a DEFINE statement to get defined value
# DEFINE Key Value
#
# @param String:            The content to be parsed
# @param Key:               The key of DEFINE statement
# @param CommentCharacter:  Comment char, used to ignore comment content
#
# @retval string The defined value
#
def GetDefineValue(String, Key, CommentCharacter):
    String = CleanString(String)
    return String[String.find(Key + ' ') + len(Key + ' ') : ]

## GetSingleValueOfKeyFromLines
#
# Parse multiple strings as below to get value of each definition line
# Key1 = Value1
# Key2 = Value2
# The result is saved to Dictionary
#
# @param Lines:                The content to be parsed
# @param Dictionary:           To store data after parsing
# @param CommentCharacter:     Comment char, be used to ignore comment content
# @param KeySplitCharacter:    Key split char, between key name and key value. Key1 = Value1, '=' is the key split char
# @param ValueSplitFlag:       Value split flag, be used to decide if has multiple values
# @param ValueSplitCharacter:  Value split char, be used to split multiple values. Key1 = Value1|Value2, '|' is the value split char
#
# @retval True Successfully executed
#
def GetSingleValueOfKeyFromLines(Lines, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
    Lines = Lines.split('\n')
    Keys = []
    Value = ''
    DefineValues = ['']
    SpecValues = ['']

    for Line in Lines:
        #
        # Handle DEFINE and SPEC
        #
        if Line.find(DataType.TAB_INF_DEFINES_DEFINE + ' ') > -1:
            if '' in DefineValues:
                DefineValues.remove('')
            DefineValues.append(GetDefineValue(Line, DataType.TAB_INF_DEFINES_DEFINE, CommentCharacter))
            continue
        if Line.find(DataType.TAB_INF_DEFINES_SPEC + ' ') > -1:
            if '' in SpecValues:
                SpecValues.remove('')
            SpecValues.append(GetDefineValue(Line, DataType.TAB_INF_DEFINES_SPEC, CommentCharacter))
            continue

        #
        # Handle Others
        #
        LineList = Line.split(KeySplitCharacter, 1)
        if len(LineList) >= 2:
            Key = LineList[0].split()
            if len(Key) == 1 and Key[0][0] != CommentCharacter:
                #
                # Remove comments and white spaces
                #
                LineList[1] = CleanString(LineList[1], CommentCharacter)
                if ValueSplitFlag:
                    Value = map(string.strip, LineList[1].split(ValueSplitCharacter))
                else:
                    Value = CleanString(LineList[1], CommentCharacter).splitlines()

                if Key[0] not in Keys:
                    Dictionary[Key[0]] = Value
                    Keys.append(Key[0])
                else:
                    Dictionary[Key[0]].extend(Value)

    if DefineValues == []:
        DefineValues == ['']
    if SpecValues == []:
        SpecValues == ['']
    Dictionary[DataType.TAB_INF_DEFINES_DEFINE] = DefineValues
    Dictionary[DataType.TAB_INF_DEFINES_SPEC] = SpecValues

    return True

## The content to be parsed
#
# Do pre-check for a file before it is parsed
# Check $()
# Check []
#
# @param FileName:       Used for error report
# @param FileContent:    File content to be parsed
# @param SupSectionTag:  Used for error report
#
def PreCheck(FileName, FileContent, SupSectionTag):
    LineNo = 0
    IsFailed = False
    NewFileContent = ''
    for Line in FileContent.splitlines():
        LineNo = LineNo + 1
        #
        # Clean current line
        #
        Line = CleanString(Line)
        
        #
        # Remove commented line
        #
        if Line.find(DataType.TAB_COMMA_SPLIT) == 0:
            Line = ''
        #
        # Check $()
        #
        if Line.find('$') > -1:
            if Line.find('$(') < 0 or Line.find(')') < 0:
                EdkLogger.error("Parser", FORMAT_INVALID, Line=LineNo, File=FileName)

        #
        # Check []
        #
        if Line.find('[') > -1 or Line.find(']') > -1:
            #
            # Only get one '[' or one ']'
            #
            if not (Line.find('[') > -1 and Line.find(']') > -1):
                EdkLogger.error("Parser", FORMAT_INVALID, Line=LineNo, File=FileName)

            #
            # Tag not in defined value
            #
            TagList = GetSplitValueList(Line, DataType.TAB_COMMA_SPLIT)
            for Tag in TagList:
                Tag = Tag.split(DataType.TAB_SPLIT, 1)[0].replace('[', '').replace(']', '').strip()
                if Tag.upper() == DataType.TAB_COMMON_DEFINES.upper():
                    break
                if Tag.upper() == DataType.TAB_USER_EXTENSIONS.upper():
                    break
                if Tag.upper() not in map(lambda s: s.upper(), SupSectionTag):
                    ErrorMsg = "'%s' is not a supportted section name." % Tag
                    EdkLogger.error("Parser", PARSER_ERROR, ErrorMsg, File=FileName, Line=LineNo)
        
        #
        # Regenerate FileContent
        #
        NewFileContent = NewFileContent + Line + '\r\n'

    if IsFailed:
       EdkLogger.error("Parser", FORMAT_INVALID, Line=LineNo, File=FileName)
    
    return NewFileContent

## CheckFileType
#
# Check if the Filename is including ExtName
# Return True if it exists
# Raise a error message if it not exists
#
# @param CheckFilename:      Name of the file to be checked
# @param ExtName:            Ext name of the file to be checked
# @param ContainerFilename:  The container file which describes the file to be checked, used for error report
# @param SectionName:        Used for error report
# @param Line:               The line in container file which defines the file to be checked
#
# @retval True The file type is correct
#
def CheckFileType(CheckFilename, ExtName, ContainerFilename, SectionName, Line):
    if CheckFilename != '' and CheckFilename != None:
        (Root, Ext) = os.path.splitext(CheckFilename)
        if Ext.upper() != ExtName.upper():
            ContainerFile = open(ContainerFilename, 'r').read()
            LineNo = GetLineNo(ContainerFile, Line)
            ErrorMsg = "Invalid %s. '%s' is found, but '%s' file is needed" % (SectionName, CheckFilename, ExtName)
            EdkLogger.error("Parser", PARSER_ERROR, ErrorMsg, Line=LineNo,
                            File=ContainerFilename)

    return True

## CheckFileExist
#
# Check if the file exists
# Return True if it exists
# Raise a error message if it not exists
#
# @param CheckFilename:      Name of the file to be checked
# @param WorkspaceDir:       Current workspace dir
# @param ContainerFilename:  The container file which describes the file to be checked, used for error report
# @param SectionName:        Used for error report
# @param Line:               The line in container file which defines the file to be checked
#
# @retval True The file exists
#
def CheckFileExist(WorkspaceDir, CheckFilename, ContainerFilename, SectionName, Line):
    if CheckFilename != '' and CheckFilename != None:
        CheckFile = WorkspaceFile(WorkspaceDir, CheckFilename)
        if os.path.exists(CheckFile) and os.path.isfile(CheckFile):
            pass
        else:
            ContainerFile = open(ContainerFilename, 'r').read()
            LineNo = GetLineNo(ContainerFile, Line)
            ErrorMsg = "Can't find file '%s' defined in section '%s'" % (CheckFile, SectionName)
            EdkLogger.error("Parser", PARSER_ERROR, ErrorMsg,
                            File=ContainerFilename, Line=LineNo)

    return True

## CheckPcdTokenInfo
#
# Check if PcdTokenInfo is following <TokenSpaceGuidCName>.<PcdCName>
#
# @param TokenInfoString:  String to be checked
# @param Section:          Used for error report
# @param File:             Used for error report
#
# @retval True PcdTokenInfo is in correct format
#
def CheckPcdTokenInfo(TokenInfoString, Section, File):
    if TokenInfoString != '' and TokenInfoString != None:
        Format = '<TokenSpaceGuidCName>.<PcdCName>'
        TokenInfoList = GetSplitValueList(TokenInfoString, DataType.TAB_SPLIT)
        if len(TokenInfoList) != 2:
            RaiseParserError(TokenInfoString, Section, File, Format)

    return True

## GetLineNo
#
# Find the index of a line in a file
#
# @param FileContent:  Search scope
# @param Line:         Search key
#
# @retval int  Index of the line
# @retval -1     The line is not found
#
def GetLineNo(FileContent, Line):
    LineList = FileContent.splitlines()
    for Index in range(len(LineList)):
        if LineList[Index].find(Line) > -1:
            #
            # Ignore statement in comment
            #
            if LineList[Index].strip()[0] == DataType.TAB_COMMENT_SPLIT:
                continue
            return Index + 1

    return -1

## RaiseParserError
#
# Raise a parser error
#
# @param Line:     String which has error
# @param Section:  Used for error report
# @param File:     File which has the string
# @param Format:   Correct format
#
def RaiseParserError(Line, Section, File, Format):
    LineNo = GetLineNo(open(os.path.normpath(File), 'r').read(), Line)
    ErrorMsg = "Invalid statement '%s' is found in section '%s'" % (Line, Section)
    EdkLogger.error("Parser", PARSER_ERROR, ErrorMsg, File=File, Line=LineNo,
                    ExtraData="Correct format is " + Format)

## WorkspaceFile
#
# Return a full path with workspace dir
#
# @param WorkspaceDir:  Workspace dir
# @param Filename:      Relative file name
#
# @retval string A full path
# 
def WorkspaceFile(WorkspaceDir, Filename):
    return os.path.join(NormPath(WorkspaceDir), NormPath(Filename))

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    print SplitModuleType('LibraryClasses.common.DXE_RUNTIME_DRIVER')
    print SplitModuleType('Library.common')
    print SplitModuleType('Librarsdsfwe')
    print NormPath('sdfas//dsfsadf//dsfsd')
    print NormPath('\\dsfsdf\\\\sd\\fsd\\dsfsdfsdf\\\\')
