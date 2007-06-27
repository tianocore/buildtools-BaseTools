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

def MergeModulePcds(pcds, pcdsFixedAtBuild, pcdsPatchableInModule, pcdsFeatureFlag, pcdsDynamic):
    #[ ['PcdName|PcdGuid|PcdType', 'IA32|X64|IPF|EBC'], ...]
    
    Item = pcdsFixedAtBuild
    for index in range(len(Item)):
        pcds.append([(Item[index][0].split(DataType.TAB_VALUE_SPLIT))[1] + DataType.TAB_VALUE_SPLIT + DataType.TAB_PCDS_FIXED_AT_BUILD, Item[index][1]])

    Item = pcdsPatchableInModule
    for index in range(len(Item)):
        pcds.append([(Item[index][0].split(DataType.TAB_VALUE_SPLIT))[1] + DataType.TAB_VALUE_SPLIT + DataType.TAB_PCDS_PATCHABLE_IN_MODULE, Item[index][1]])
                                 
    Item = pcdsFeatureFlag
    for index in range(len(Item)):
        pcds.append([(Item[index][0].split(DataType.TAB_VALUE_SPLIT))[1] + DataType.TAB_VALUE_SPLIT + DataType.TAB_PCDS_FEATURE_FLAG, Item[index][1]])
                                 
    Item = pcdsDynamic
    for index in range(len(Item)):
        pcds.append([(Item[index][0].split(DataType.TAB_VALUE_SPLIT))[1] + DataType.TAB_VALUE_SPLIT + DataType.TAB_PCDS_DYNAMIC, Item[index][1]])

def MergeAllArch(list1, listCommon, listIa32, listX64, listIpf, listEbc):
    isFound = False
    for j in range(len(list1)):
        list1[j] = [list1[j], '']
    
    for i in listCommon:
        if i not in list1:
            list1.append([i, ''])
    for i in listIa32:
        for j in range(len(list1)):
            if i == list1[j][0]:
                isFound = True
                list1[j] = [list1[j][0], 'IA32|']
                break
        if not isFound:
            list1.append([i, 'IA32|'])
        isFound = False
    
    for i in listX64:
        for j in range(len(list1)):
            if i == list1[j][0]:
                isFound = True
                list1[j] = [list1[j][0], list1[j][1] + 'X64|']
                break
        if not isFound:
            list1.append([i, 'X64|'])
        isFound = False
    
    for i in listIpf:
        for j in range(len(list1)):
            if i == list1[j][0]:
                isFound = True
                list1[j] = [list1[j][0], list1[j][1] + 'Ipf|']
                break
        if not isFound:
            list1.append([i, 'Ipf|'])
        isFound = False
        
    for i in listEbc:
        for j in range(len(list1)):
            if i == list1[j][0]:
                isFound = True
                list1[j] = [list1[j][0], list1[j][1] + 'Ebc|']
                break
        if not isFound:
            list1.append([i, 'Ebc|'])
        isFound = False
        
    #Remove DataType.TAB_VALUE_SPLIT
    for i in range(len(list1)):
        if list1[i][1].endswith(DataType.TAB_VALUE_SPLIT):
            list1[i][1] = list1[i][1].rsplit(DataType.TAB_VALUE_SPLIT, 1)[0]

    #print list1

def GetComponents(Lines, Key, KeyValues, CommentCharacter):
    #KeyValues [ ['component name', [lib1, lib2, lib3], [bo1, bo2, bo3]], ...]
    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    findBlock = False
    findLibraryClass = False
    findBuildOption = False
    ListItem = None
    LibraryClassItem = []
    BuildOption = []
    
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
            if Line.find('<LibraryClass>') != -1:
                findLibraryClass = True
                continue
            if Line.find('<BuildOptions>') != -1:
                findBuildOption = True
                continue
            if Line.endswith('}'):
                #find '}' at line tail
                KeyValues.append([ListItem, LibraryClassItem, BuildOption])
                findBlock = False
                findLibraryClass = False
                findBuildOption = False
                LibraryClassItem = []
                BuildOption = []
                continue

        if findBlock:
            if findLibraryClass:
                LibraryClassItem.append(Line)
            elif findBuildOption:
                BuildOption.append(Line)
        else:
            KeyValues.append([ListItem, [], []])
        
    return True

def GetLibraryClassesWithModuleType(Lines, Key, KeyValues, CommentCharacter):
    newKey = SplitModuleType(Key)
    Lines = Lines.split(DataType.TAB_SECTION_END, 1)[1]
    LineList = Lines.splitlines()
    for Line in LineList:
        if Line != '' and Line[0] != CommentCharacter:
            KeyValues.append([CleanString(Line, CommentCharacter), newKey[1]])

    return True

def SplitModuleType(Key):
    #from DataType import *
    KeyList = Key.split(DataType.TAB_SPLIT)
    rtv = []
    if len(KeyList) == 3:
        rtv.append(KeyList[0] + DataType.TAB_SPLIT + KeyList[1])
        rtv.append(KeyList[2])
        return rtv
    else:
        rtv.append(Key)
        rtv.append(None)
        return rtv
    
def NormPath(path):
    if path != '':
        return os.path.normpath(path)
    else:
        return path

def CleanString(Line, CommentCharacter = DataType.TAB_COMMENT_SPLIT):
    #remove whitespace
    Line = Line.strip();
    #remove comments
    Line = Line.split(CommentCharacter, 1)[0];
    #replace '\\', '\' with '/'
    Line = Line.replace('\\', '/')
    Line = Line.replace('//', '/')
    #remove ${WORKSPACE}
    Line = Line.replace(DataType.TAB_WORKSPACE1, '')
    Line = Line.replace(DataType.TAB_WORKSPACE2, '')
    #remove '/' at the beginning
#    if Line.startswith('/'):
#        Line = Line.replace('/', '')
    #Change path
    #Line = os.path.normpath(Line)
    
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

def GetSingleValueOfKeyFromLines(Lines, Dictionary, CommentCharacter, KeySplitCharacter, ValueSplitFlag, ValueSplitCharacter):
    Lines = Lines.split('\n')
    Keys = []
    Value = ''
    for Line in Lines:
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
    return True


if __name__ == '__main__':
    print SplitModuleType('LibraryClasses.common.DXE_RUNTIME_DRIVER')
    print SplitModuleType('Library.common')
    print SplitModuleType('Librarsdsfwe')
