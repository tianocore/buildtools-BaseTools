# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.    The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.

#
#This file is used to define some common useful string functions
#

import DataType
import os.path
import string
from BuildToolError import *

#
# Get a value list from a string with multiple values splited with SplitTag
# The default SplitTag is DataType.TAB_VALUE_SPLIT
# 'AAA|BBB|CCC' -> ['AAA', 'BBB', 'CCC']
#
def GetSplitValueList(String, SplitTag = DataType.TAB_VALUE_SPLIT, MaxSplit = -1):
    return map(lambda l: l.strip(), String.split(SplitTag, MaxSplit))

#
# Find a key's all arches in dict, add the new arch to the list
# If not exist any arch, set the arch directly
#
def MergeArches(Dict, Key, Arch):
    if Key in Dict.keys():
        Dict[Key].append(Arch)
    else:
        Dict[Key] = Arch.split()

#
# Parse a string with format "DEFINE <VarName> = <PATH>"
# Generate a map Defines[VarName] = PATH
# Return False if invalid format
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

#
# Parse a string with format "!include <Filename>"
# Return the file path
# Return False if invalid format or NOT FOUND
#
def GenInclude(String, IncludeFiles, Arch):
    if String.upper().find(DataType.TAB_INCLUDE.upper() + ' ') > -1:
        IncludeFile = CleanString(String[String.upper().find(DataType.TAB_INCLUDE.upper() + ' ') + len(DataType.TAB_INCLUDE + ' ') : ])
        MergeArches(IncludeFiles, IncludeFile, Arch)
        return True
    else:
        return False
    
#
# Parse a string with format "InfFilename [EXEC = ExecFilename]"
# Return (InfFilename, ExecFilename)
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

#
# Parse a string with format "[<Family>:]<ToolFlag>=Flag"
# Return (Family, ToolFlag, Flag)
#
def GetBuildOption(String):
    (Family, ToolChain, Flag) = ('', '', '')
    List = GetSplitValueList(String, DataType.TAB_EQUAL_SPLIT, MaxSplit = 1)
    if List[0].find(':') > -1:
        Family = CleanString(List[0][ : List[0].find(':')])
        ToolChain = CleanString(List[0][List[0].find(':') + 1 : ])
    else:
        ToolChain = CleanString(List[0])                    
    Flag = CleanString(List[1])
    
    return (Family, ToolChain, Flag)

#
# Parse block of the components defined in dsc file
# Return KeyValues [ ['component name', [lib1, lib2, lib3], [bo1, bo2, bo3], [pcd1, pcd2, pcd3]], ...]
#
def GetComponents(Lines, Key, KeyValues, CommentCharacter):
    #KeyValues [ ['component name', [lib1, lib2, lib3], [bo1, bo2, bo3], [pcd1, pcd2, pcd3]], ...]
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
            #find '{' at line tail
            if Line.endswith('{'):
                findBlock = True
                ListItem = CleanString(Line.rsplit('{', 1)[0], CommentCharacter)

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
                #find '}' at line tail
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

#
# Get Library Class definition when no module type defined
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

#
# Get Dynamic Pcds
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

#
# Split ModuleType out of section defien to get key
# [LibraryClass.Arch.ModuleType|ModuleType|ModuleType] -> [ 'LibraryClass.Arch', ['ModuleType', 'ModuleType', 'ModuleType'] ]
#
def SplitModuleType(Key):
    KeyList = Key.split(DataType.TAB_SPLIT)
    KeyList.append('')                    # Fill in for arch
    KeyList.append('')                    # Fill in for moduletype
    ReturnValue = []
    KeyValue = KeyList[0]
    if KeyList[1] != '':
        KeyValue = KeyValue + DataType.TAB_SPLIT + KeyList[1]
    ReturnValue.append(KeyValue)
    ReturnValue.append(GetSplitValueList(KeyList[2]))
    
    return ReturnValue
    
#
# Create a normal path
# And replace DFEINE in the path
#
def NormPath(Path, Defines = {}):
    if Path != '':
        # Replace with Define
        for Key in Defines.keys():
            Path = Path.replace(Key, Defines[Key])

        # Remove ${WORKSPACE}
        Path = Path.replace(DataType.TAB_WORKSPACE, '')

        # To local path format
        Path = os.path.normpath(Path)
        if Path[0] == os.path.sep:
            Path = Path[1:]

    return Path

#
# Remove comments in a string
# Remove spaces
#
def CleanString(Line, CommentCharacter = DataType.TAB_COMMENT_SPLIT):
    #remove whitespace
    Line = Line.strip();
    #remove comments
    Line = Line.split(CommentCharacter, 1)[0];
    #remove whitespace again
    Line = Line.strip();
    
    return Line

def GetMultipleValuesOfKeyFromLines(Lines, Key, KeyValues, CommentCharacter):
    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    LineList = Lines.split('\n')
    for Line in LineList:
        Line = CleanString(Line, CommentCharacter)
        if Line != '' and Line[0] != CommentCharacter:
            KeyValues += [Line]

    return True

def GetDefineValue(String, Key, CommentCharacter):
    String = CleanString(String)
    return String[String.find(Key + ' ') + len(Key + ' ') : ]

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
            DefineValues.append(GetDefineValue(Line, DataType.TAB_INF_DEFINES_DEFINE, CommentCharacter))
            continue
        if Line.find(DataType.TAB_INF_DEFINES_SPEC + ' ') > -1:
            SpecValues.append(GetDefineValue(Line, DataType.TAB_INF_DEFINES_SPEC, CommentCharacter))
            continue
                
        #
        # Handle Others
        #
        LineList = Line.split(KeySplitCharacter, 1)
        if len(LineList) >= 2:
            Key = LineList[0].split()
            if len(Key) == 1 and Key[0][0] != CommentCharacter:
                #Remove comments and white spaces
                LineList[1] = CleanString(LineList[1], CommentCharacter)
                if ValueSplitFlag:
                    Value = map(string.strip, LineList[1].replace('\\','/').split(ValueSplitCharacter))
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

#
# Do pre-check for a file before it is parsed
# Check $()
# Check []
#
def PreCheck(FileName, FileContent, SupSectionTag):
    LineNo = 0
    IsFailed = False
    for Line in FileContent.splitlines():
        LineNo = LineNo + 1
        Line = CleanString(Line)
        #
        # Check $()
        #
        if Line.find('$') > -1:
            if Line.find('$(') < 0 or Line.find(')') < 0:
                raise ParserError(FORMAT_INVALID, lineno = LineNo, name = FileName)

        #
        # Check []
        #
        if Line.find('[') > -1 or Line.find(']') > -1:
            #
            # Only get one '[' or one ']'
            #
            if not (Line.find('[') > -1 and Line.find(']') > -1):
                raise ParserError(FORMAT_INVALID, lineno = LineNo, name = FileName)

            #
            # Tag not in defined value
            #
            TagList = GetSplitValueList(Line, DataType.TAB_COMMA_SPLIT)
            for Tag in TagList:
                Tag = Tag.split(DataType.TAB_SPLIT, 1)[0].replace('[', '').replace(']', '').strip()
                if Tag.upper() == DataType.TAB_COMMON_DEFINES.upper():
                    break
                if Tag.upper() not in map(lambda s: s.upper(), SupSectionTag):
                    ErrorMsg = "'%s' is not a supportted section name found at line %s in file '%s'" % (Tag, LineNo, FileName)
                    raise ParserError(PARSER_ERROR, msg = ErrorMsg)
    
    if IsFailed:
       raise ParserError(FORMAT_INVALID, lineno = LineNo, name = FileName)

#
# Check if the Filename is including ExtName
# Pass if it exists
# Raise a error message if it not exists
#
def CheckFileType(CheckFilename, ExtName, ContainerFilename, SectionName, Line):
    if CheckFilename != '' and CheckFilename != None:
        (Root, Ext) = os.path.splitext(CheckFilename)
        if Ext.upper() != ExtName.upper():
            ContainerFile = open(ContainerFilename, 'r').read()
            LineNo = GetLineNo(ContainerFile, Line)
            ErrorMsg = "Invalid %s '%s' defined at line %s in file '%s', it is NOT a valid '%s' file" % (SectionName, CheckFilename, LineNo, ContainerFilename, ExtName) 
            raise ParserError(PARSER_ERROR, msg = ErrorMsg)
    
    return True

#
# Check if the file exists
# Pass if it exists
# Raise a error message if it not exists
#
def CheckFileExist(WorkspaceDir, CheckFilename, ContainerFilename, SectionName, Line):
    if CheckFilename != '' and CheckFilename != None:
        CheckFile = WorkspaceFile(WorkspaceDir, NormPath(CheckFilename))
        if os.path.exists(CheckFile) and os.path.isfile(CheckFile):
            pass
        else:
            ContainerFile = open(ContainerFilename, 'r').read()
            LineNo = GetLineNo(ContainerFile, Line)
            ErrorMsg = "Can't find file '%s' defined in section %s at line %s in file '%s'" % (CheckFile, SectionName, LineNo, ContainerFilename) 
            raise ParserError(PARSER_ERROR, msg = ErrorMsg)
    
    return True

#
# Find the index of a line in a file
#
def GetLineNo(FileContent, Line):
    LineNo = -1
    LineList = FileContent.splitlines()
    for Index in range(len(LineList)):
        if LineList[Index].find(Line) > -1:
            return Index + 1

#
# Return a full path with workspace dir
#
def WorkspaceFile(WorkspaceDir, Filename):
    return os.path.join(NormPath(WorkspaceDir), NormPath(Filename))

if __name__ == '__main__':
    print SplitModuleType('LibraryClasses.common.DXE_RUNTIME_DRIVER')
    print SplitModuleType('Library.common')
    print SplitModuleType('Librarsdsfwe')
    print NormPath('sdfas//dsfsadf//dsfsd')
    print NormPath('\\dsfsdf\\\\sd\\fsd\\dsfsdfsdf\\\\')
