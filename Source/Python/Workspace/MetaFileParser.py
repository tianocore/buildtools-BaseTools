## @file
# This file is used to create a database used by ECC tool
#
# Copyright (c) 2007 ~ 2008, Intel Corporation
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
import sqlite3
import os
import time

import Common.EdkLogger as EdkLogger
from CommonDataClass.DataClass import *
from Common.DataType import *
from Common.String import *
from Common.Misc import Blist

class MetaFileParser(object):
    _DataType = {}
    def __init__(self, FilePath, FileType, Table, Macros={}, Owner=-1, From=-1):
        self._Table = Table
        self._FileType = FileType
        self._FilePath = FilePath
        self._FileDir = os.path.dirname(self._FilePath)
        self._Macros = Macros
        # for recursive parsing 
        self._Owner = Owner
        self._From = From

        # for parsing
        self._Content = None
        self._ValueList = ['', '', '', '', '']
        self._Scope = []
        self._LineIndex = 0
        self._CurrentLine = ''
        self._SectionType = MODEL_UNKNOWN
        self._SectionName = ''
        self._InSubsection = False
        self._SubsectionType = MODEL_UNKNOWN
        self._SubsectionName = ''
        self._LastItem = -1
        self._Enabled = 0

    def _Store(self, *Args):
        return self._Table.Insert(*Args)

    def Start(self):
        raise NotImplementedError 

    def _Done(self):
        self._Table.SetEndFlag()

    def _CommonParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_VALUE_SPLIT)
        self._ValueList[0:len(TokenList)] = TokenList

    def _PathParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_VALUE_SPLIT)
        self._ValueList[0:len(TokenList)] = TokenList
        if len(self._Macros) > 0:
            for Index in range(0, len(self._ValueList)):
                Value = self._ValueList[Index]
                if Value == None or Value == '':
                    continue
                self._ValueList[Index] = NormPath(Value, self._Macros)

    def _Skip(self):
        self._ValueList[0:1] = [self._CurrentLine]

    def _SectionHeaderParser(self):
        self._Scope = []
        for Item in GetSplitValueList(self._CurrentLine[1:-1], TAB_COMMA_SPLIT):
            ItemList = GetSplitValueList(Item, TAB_SPLIT)
            self._SectionName = ItemList[0].upper()
            if self._SectionName in self._DataType:
                self._SectionType = self._DataType[self._SectionName]
            else:
                self._SectionType = MODEL_UNKNOWN
            # S1 is always Arch
            if len(ItemList) > 1:
                S1 = ItemList[1].upper()
            else:
                S1 = 'COMMON'
            # S2 may be Platform or ModuleType
            if len(ItemList) > 2:
                S2 = ItemList[2].upper()
            else:
                S2 = 'COMMON'
            self._Scope.append([S1, S2])

    def _DefineParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        self._ValueList[0:len(TokenList)] = TokenList
        if self._ValueList[1] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No value specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)

    def _MacroParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, ' ', 1)
        if len(TokenList) < 2 or TokenList[1] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No macro name/value given",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)
        TokenList = GetSplitValueList(TokenList[1], TAB_EQUAL_SPLIT, 1)
        if len(TokenList) < 1:
            return
        if self._Macros == None:
            self._Macros = {}
        self._Macros[TokenList[0]] = TokenList[1]

    _SectionParser = {}

class InfParser(MetaFileParser):
    _DataType = {
        TAB_UNKNOWN.upper() : MODEL_UNKNOWN,
        TAB_INF_DEFINES.upper() : MODEL_META_DATA_HEADER,
        TAB_BUILD_OPTIONS.upper() : MODEL_META_DATA_BUILD_OPTION,
        TAB_INCLUDES.upper() : MODEL_EFI_INCLUDE,
        TAB_LIBRARIES.upper() : MODEL_EFI_LIBRARY_INSTANCE,
        TAB_LIBRARY_CLASSES.upper() : MODEL_EFI_LIBRARY_CLASS,
        TAB_PACKAGES.upper() : MODEL_META_DATA_PACKAGE,
        TAB_NMAKE.upper() : MODEL_META_DATA_NMAKE,
        TAB_INF_FIXED_PCD.upper() : MODEL_PCD_FIXED_AT_BUILD,
        TAB_INF_PATCH_PCD.upper() : MODEL_PCD_PATCHABLE_IN_MODULE,
        TAB_INF_FEATURE_PCD.upper() : MODEL_PCD_FEATURE_FLAG,
        TAB_INF_PCD_EX.upper() : MODEL_PCD_DYNAMIC_EX,
        TAB_INF_PCD.upper() : MODEL_PCD_DYNAMIC,
        TAB_SOURCES.upper() : MODEL_EFI_SOURCE_FILE,
        TAB_GUIDS.upper() : MODEL_EFI_GUID,
        TAB_PROTOCOLS.upper() : MODEL_EFI_PROTOCOL,
        TAB_PPIS.upper() : MODEL_EFI_PPI,
        TAB_DEPEX.upper() : MODEL_EFI_DEPEX,
        TAB_BINARIES.upper() : MODEL_EFI_BINARY_FILE,
        TAB_USER_EXTENSIONS.upper() : MODEL_META_DATA_USER_EXTENSION
    }

    def __init__(self, FilePath, FileId, FileType, Table, Macros={}):
        MetaFileParser.__init__(self, FilePath, FileType, Table, Macros)

    def Start(self):
        try:
            self._Content = open(self._FilePath, 'r').readlines()
        except:
            EdkLogger.error("Parser", FILE_READ_FAILURE, ExtraData=self._FilePath)

        for Index in range(0, len(self._Content)):
            Line = CleanString(self._Content[Index])
            if Line == '':
                continue
            self._CurrentLine = Line
            self._LineIndex = Index

            # section header
            if Line[0] == TAB_SECTION_START and Line[-1] == TAB_SECTION_END:
                self._SectionHeaderParser()
                continue
            elif Line.upper().startswith('DEFINE '):
                self._MacroParser()
                continue

            # section content
            self._ValueList = ['','','']
            self._SectionParser[self._SectionType](self)
            if self._ValueList == None:
                continue
            # 
            # Model, Value1, Value2, Value3, Value4, Value5, Arch, Platform, BelongsToFile=-1, 
            # LineBegin=-1, ColumnBegin=-1, LineEnd=-1, ColumnEnd=-1, BelongsToItem=-1, FeatureFlag='', 
            # Enabled=-1
            # 
            for Arch, Platform in self._Scope:
                self._Store(self._SectionType,
                            self._ValueList[0],
                            self._ValueList[1],
                            self._ValueList[2],
                            Arch,
                            Platform,
                            self._Owner,
                            self._LineIndex+1,
                            -1,
                            self._LineIndex+1,
                            -1,
                            0
                            )
        self._Done()
            
    def _BuildOptionParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        TokenList2 = GetSplitValueList(TokenList[0], ':', 1)
        if len(TokenList2) == 2:
            self._ValueList[0] = TokenList2[0]
            self._ValueList[1] = TokenList2[1]
        else:
            self._ValueList[1] = TokenList[0]
        self._ValueList[2] = ReplaceMacro(TokenList[1], self._Macros)

    def _NmakeParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        self._ValueList[0:len(TokenList)] = TokenList
        # remove self-reference in macro setting
        self._ValueList[1] = ReplaceMacro(self._ValueList[1], {self._ValueList[0]:''})

    def _PcdParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_VALUE_SPLIT, 1)
        self._ValueList[0:1] = GetSplitValueList(TokenList[0], TAB_SPLIT)
        if len(TokenList) > 1:
            self._ValueList[2] = TokenList[1]
        if self._ValueList[0] == '' or self._ValueList[1] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No token space GUID or PCD name specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)

    def _DepexParser(self):
        self._ValueList[0:1] = [self._CurrentLine]

    _SectionParser = {
        MODEL_UNKNOWN                   :   MetaFileParser._Skip,
        MODEL_META_DATA_HEADER          :   MetaFileParser._DefineParser,
        MODEL_META_DATA_BUILD_OPTION    :   _BuildOptionParser,
        MODEL_EFI_INCLUDE               :   MetaFileParser._PathParser,     # for R8.x modules
        MODEL_EFI_LIBRARY_INSTANCE      :   MetaFileParser._CommonParser,   # for R8.x modules
        MODEL_EFI_LIBRARY_CLASS         :   MetaFileParser._PathParser,
        MODEL_META_DATA_PACKAGE         :   MetaFileParser._PathParser,
        MODEL_META_DATA_NMAKE           :   _NmakeParser,                   # for R8.x modules
        MODEL_PCD_FIXED_AT_BUILD        :   _PcdParser,
        MODEL_PCD_PATCHABLE_IN_MODULE   :   _PcdParser,
        MODEL_PCD_FEATURE_FLAG          :   _PcdParser,
        MODEL_PCD_DYNAMIC_EX            :   _PcdParser,
        MODEL_PCD_DYNAMIC               :   _PcdParser,
        MODEL_EFI_SOURCE_FILE           :   MetaFileParser._PathParser,
        MODEL_EFI_GUID                  :   MetaFileParser._CommonParser,
        MODEL_EFI_PROTOCOL              :   MetaFileParser._CommonParser,
        MODEL_EFI_PPI                   :   MetaFileParser._CommonParser,
        MODEL_EFI_DEPEX                 :   _DepexParser,
        MODEL_EFI_BINARY_FILE           :   MetaFileParser._PathParser,
        MODEL_META_DATA_USER_EXTENSION  :   MetaFileParser._Skip,
    }    

class DscParser(MetaFileParser):
    _DataType = {
        TAB_SKUIDS.upper()                          :   MODEL_EFI_SKU_ID,
        TAB_LIBRARIES.upper()                       :   MODEL_EFI_LIBRARY_INSTANCE,
        TAB_LIBRARY_CLASSES.upper()                 :   MODEL_EFI_LIBRARY_CLASS,
        TAB_BUILD_OPTIONS.upper()                   :   MODEL_META_DATA_BUILD_OPTION,
        TAB_PCDS_FIXED_AT_BUILD_NULL.upper()        :   MODEL_PCD_FIXED_AT_BUILD,
        TAB_PCDS_PATCHABLE_IN_MODULE_NULL.upper()   :   MODEL_PCD_PATCHABLE_IN_MODULE,
        TAB_PCDS_FEATURE_FLAG_NULL.upper()          :   MODEL_PCD_FEATURE_FLAG,
        TAB_PCDS_DYNAMIC_DEFAULT_NULL.upper()       :   MODEL_PCD_DYNAMIC_DEFAULT,
        TAB_PCDS_DYNAMIC_HII_NULL.upper()           :   MODEL_PCD_DYNAMIC_HII,
        TAB_PCDS_DYNAMIC_VPD_NULL.upper()           :   MODEL_PCD_DYNAMIC_VPD,
        TAB_PCDS_DYNAMIC_EX_DEFAULT_NULL.upper()    :   MODEL_PCD_DYNAMIC_EX_DEFAULT,
        TAB_PCDS_DYNAMIC_EX_HII_NULL.upper()        :   MODEL_PCD_DYNAMIC_EX_HII,
        TAB_PCDS_DYNAMIC_EX_VPD_NULL.upper()        :   MODEL_PCD_DYNAMIC_EX_VPD,
        TAB_COMPONENTS.upper()                      :   MODEL_META_DATA_COMPONENT,
        TAB_DSC_DEFINES.upper()                     :   MODEL_META_DATA_HEADER,
        TAB_INCLUDE.upper()                         :   MODEL_META_DATA_INCLUDE,
        TAB_IF.upper()                              :   MODEL_META_DATA_CONDITIONAL_STATEMENT_IF,
        TAB_IF_DEF.upper()                          :   MODEL_META_DATA_CONDITIONAL_STATEMENT_IFDEF,
        TAB_IF_N_DEF.upper()                        :   MODEL_META_DATA_CONDITIONAL_STATEMENT_IFNDEF,
        TAB_ELSE_IF.upper()                         :   MODEL_META_DATA_CONDITIONAL_STATEMENT_ELSEIF,
        TAB_ELSE.upper()                            :   MODEL_META_DATA_CONDITIONAL_STATEMENT_ELSE,
        TAB_END_IF.upper()                          :   MODEL_META_DATA_CONDITIONAL_STATEMENT_ENDIF,
    }

    _IncludeAllowedSection = [
        TAB_LIBRARIES.upper(), 
        TAB_LIBRARY_CLASSES.upper(), 
        TAB_SKUIDS.upper(),
        TAB_COMPONENTS.upper(),
        TAB_BUILD_OPTIONS.upper(),
        TAB_PCDS_FIXED_AT_BUILD_NULL.upper(),
        TAB_PCDS_PATCHABLE_IN_MODULE_NULL.upper(),
        TAB_PCDS_FEATURE_FLAG_NULL.upper(),
        TAB_PCDS_DYNAMIC_DEFAULT_NULL.upper(),
        TAB_PCDS_DYNAMIC_HII_NULL.upper(),
        TAB_PCDS_DYNAMIC_VPD_NULL.upper(),
        TAB_PCDS_DYNAMIC_EX_DEFAULT_NULL.upper(),
        TAB_PCDS_DYNAMIC_EX_HII_NULL.upper(),
        TAB_PCDS_DYNAMIC_EX_VPD_NULL.upper(),
        ]

    _OP_ = {
        "!"     :   lambda a:   not a,
        "!="    :   lambda a,b: a!=b,
        "=="    :   lambda a,b: a==b,
        ">"     :   lambda a,b: a>b,
        "<"     :   lambda a,b: a<b,
        "=>"    :   lambda a,b: a>=b,
        ">="    :   lambda a,b: a>=b,
        "<="    :   lambda a,b: a<=b,
        "=<"    :   lambda a,b: a<=b,
    }

    def __init__(self, FilePath, FileId, FileType, Table, Macros={}, Owner=-1, From=-1):
        MetaFileParser.__init__(self, FilePath, FileType, Table, Macros, Owner, From)
        # to store conditional directive evaluation result
        self._Eval = Blist()

    def Start(self):
        try:
            if self._Content == None:
                self._Content = open(self._FilePath, 'r').readlines()
        except:
            EdkLogger.error("Parser", FILE_READ_FAILURE, ExtraData=self._FilePath)

        for Index in range(0, len(self._Content)):
            Line = CleanString(self._Content[Index])
            # skip empty line
            if Line == '':
                self._LineIndex += 1
                continue
            self._CurrentLine = Line
            self._LineIndex = Index

            # section header
            if Line[0] == TAB_SECTION_START and Line[-1] == TAB_SECTION_END:
                self._SectionHeaderParser()
                continue
            elif Line[0] == '}':
                self._InSubsection = False
                self._Owner = -1
                continue
            elif Line[0] == TAB_OPTION_START and Line[-1] == TAB_OPTION_END:
                self._SubsectionHeaderParser()
                continue
            # directive line
            elif Line[0] == '!':
                self._DirectiveParser()
                continue
            elif Line.upper().startswith('DEFINE '):
                self._MacroParser()
                continue

            # section content
            if self._InSubsection:
                SectionType = self._SubsectionType
                SectionName = self._SubsectionName
                if self._Owner == -1:
                    self._Owner = self._LastItem
            else:
                SectionType = self._SectionType
                SectionName = self._SectionName
            self._ValueList = ['', '', '']
            self._SectionParser[SectionType](self)
            if self._ValueList == None:
                continue

            # 
            # Model, Value1, Value2, Value3, Arch, Platform, BelongsToFile=-1, 
            # LineBegin=-1, ColumnBegin=-1, LineEnd=-1, ColumnEnd=-1, BelongsToItem=-1, 
            # Enabled=-1
            # 
            for Arch, ModuleType in self._Scope:
                self._LastItem = self._Store(
                    SectionType,
                    self._ValueList[0],
                    self._ValueList[1],
                    self._ValueList[2],
                    Arch,
                    ModuleType,
                    self._Owner,
                    self._From,
                    self._LineIndex+1,
                    -1,
                    self._LineIndex+1,
                    -1,
                    self._Enabled
                    )
        self._Done()

    def _DefineParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        if len(TokenList) < 2:
            EdkLogger.error('Parser', FORMAT_INVALID, "No value specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)
        if TokenList[0] in ['FLASH_DEFINITION', 'OUTPUT_DIRECTORY']:
            TokenList[1] = NormPath(TokenList[1], self._Macros)
        self._ValueList[0:len(TokenList)] = TokenList    
            
    def _SubsectionHeaderParser(self):
        self._SubsectionName = self._CurrentLine[1:-1].upper()
        if self._SubsectionName in self._DataType:
            self._SubsectionType = self._DataType[self._SubsectionName]
        else:
            self._SubsectionType = MODEL_UNKNOWN

    def _DirectiveParser(self):
        self._ValueList = ['','','']
        TokenList = GetSplitValueList(self._CurrentLine, ' ', 1)
        self._ValueList[0:len(TokenList)] = TokenList
        if self._ValueList[1] == '':
            EdkLogger.error("Parser", FORMAT_INVALID, "Missing expression", 
                            File=self._FilePath, Line=self._LineIndex+1,
                            ExtraData=self._CurrentLine)
        DirectiveName = self._ValueList[0].upper()
        self._LastItem = self._Store(
            self._DataType[DirectiveName],
            self._ValueList[0],
            self._ValueList[1],
            self._ValueList[2],
            'COMMON',
            'COMMON',
            self._Owner,
            self._LineIndex + 1,
            -1,
            self._LineIndex + 1,
            -1,
            0
            )
        # process the directive
        if DirectiveName == "!INCLUDE":
            if not self._SectionName in self._IncludeAllowedSection:
                EdkLogger.error("Parser", FORMAT_INVALID, File=self._FilePath, Line=self._LineIndex+1,
                                ExtraData="'!include' is not allowed under section [%s]" % self._SectionName)
            # the included file must be relative to the parsing file
            IncludedFile = os.path.join(self._FileDir, self._ValueList[1])
            Parser = DscParser(IncludedFile, self._FileType, self._Table, self._Macros, From=self._LastItem)
            Parser._SectionName = self._SectionName
            Parser._SectionType = self._SectionType
            Parser._Scope = self._Scope
            Parser._Enabled = self._Enabled
            try:
                Parser.Start()
            except:
                EdkLogger.error("Parser", PARSER_ERROR, File=self._FilePath, Line=self._LineIndex+1,
                                ExtraData="Failed to parse content in file %s" % IncludedFile)
            self._SectionName = Parser._SectionName
            self._SectionType = Parser._SectionType
            self._Scope       = Parser._Scope
            self._Enabled     = Parser._Enabled
        else:
            if DirectiveName in ["!IF", "!IFDEF", "!IFNDEF"]:
                # evaluate the expression
                Result = self._Evaluate(self._ValueList[1])
                if DirectiveName == "!IFNDEF":
                    Result = not Result
                self._Eval.append(Result)
            elif DirectiveName in ["!ELSEIF"]:
                # evaluate the expression
                self._Eval[-1] = (not self._Eval[-1]) & self._Evaluate(self._ValueList[1])
            elif DirectiveName in ["!ELSE"]:
                self._Eval[-1] = not self._Eval[-1]
            elif DirectiveName in ["!ENDIF"]:
                if len(self._Eval) > 0:
                    self._Eval.pop()
                else:
                    EdkLogger.error("Parser", FORMAT_INVALID, "!IF..[!ELSE]..!ENDIF doesn't match",
                                    File=self._FilePath, Line=self._LineIndex+1)
            if self._Eval.Result == False:
                self._Enabled = 0 - len(self._Eval)
            else:
                self._Enabled = len(self._Eval)

    def _Evaluate(self, Expression):
        TokenList = Expression.split()
        TokenNumber = len(TokenList)
        if TokenNumber == 1:
            return TokenList[0] in self._Macros
        elif TokenNumber == 2:
            Op = TokenList[0]
            if Op not in self._OP_:
                EdkLogger.error('Parser', FORMAT_INVALID, "Unsupported operator", File=self._FilePath,
                                Line=self._LineIndex+1, ExtraData=Expression)
            if TokenList[1].upper() == 'TRUE':
                Value = True
            else:
                Value = False
            return self._OP_[Op](Value)
        elif TokenNumber == 3:
            Name = TokenList[0]
            if Name not in self._Macros:
                return False
            Value = TokenList[2]
            if Value[0] in ["'", '"']:
                Value = Value[1:-1]
            Op = TokenList[1]
            return self._OP_[Op](self._Macros[Macro], Value)
        else:
            EdkLogger.error('Parser', FORMAT_INVALID, File=self._FilePath, Line=self._LineIndex+1,
                            ExtraData=Expression)

    def _BuildOptionParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        TokenList2 = GetSplitValueList(TokenList[0], ':', 1)
        if len(TokenList2) == 2:
            self._ValueList[0] = TokenList2[0]
            self._ValueList[1] = TokenList2[1]
        else:
            self._ValueList[1] = TokenList[0]
        self._ValueList[2] = ReplaceMacro(TokenList[1], self._Macros)

    def _PcdParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_VALUE_SPLIT, 1)
        self._ValueList[0:1] = GetSplitValueList(TokenList[0], TAB_SPLIT)
        self._ValueList[2] = TokenList[1]
        if self._ValueList[0] == '' or self._ValueList[1] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No token space GUID or PCD name specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)
        if self._ValueList[2] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No PCD value given",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)

    def _ComponentParser(self):        
        if self._CurrentLine[-1] == '{':
            self._InSubsection = True
            self._ValueList[0] = self._CurrentLine[0:-1].strip()
        else:
            self._ValueList[0] = self._CurrentLine
        if len(self._Macros) > 0:
            self._ValueList[0] = NormPath(self._ValueList[0], self._Macros)

    _SectionParser = {
        MODEL_META_DATA_HEADER          :   MetaFileParser._DefineParser,
        MODEL_EFI_SKU_ID                :   MetaFileParser._CommonParser,
        MODEL_EFI_LIBRARY_INSTANCE      :   MetaFileParser._PathParser,
        MODEL_EFI_LIBRARY_CLASS         :   MetaFileParser._PathParser,
        MODEL_PCD_FIXED_AT_BUILD        :   _PcdParser,
        MODEL_PCD_PATCHABLE_IN_MODULE   :   _PcdParser,
        MODEL_PCD_FEATURE_FLAG          :   _PcdParser,
        MODEL_PCD_DYNAMIC_DEFAULT       :   _PcdParser,
        MODEL_PCD_DYNAMIC_HII           :   _PcdParser,
        MODEL_PCD_DYNAMIC_VPD           :   _PcdParser,
        MODEL_PCD_DYNAMIC_EX_DEFAULT    :   _PcdParser,
        MODEL_PCD_DYNAMIC_EX_HII        :   _PcdParser,
        MODEL_PCD_DYNAMIC_EX_VPD        :   _PcdParser,
        MODEL_META_DATA_COMPONENT       :   _ComponentParser,
        MODEL_META_DATA_BUILD_OPTION    :   _BuildOptionParser,
        MODEL_UNKNOWN                   :   MetaFileParser._Skip,
        MODEL_META_DATA_USER_EXTENSION  :   MetaFileParser._Skip,
    }

class DecParser(MetaFileParser):
    _DataType = {
        TAB_DEC_DEFINES.upper()                     :   MODEL_META_DATA_HEADER,
        TAB_INCLUDES.upper()                        :   MODEL_EFI_INCLUDE,
        TAB_LIBRARY_CLASSES.upper()                 :   MODEL_EFI_LIBRARY_CLASS,
        TAB_GUIDS.upper()                           :   MODEL_EFI_GUID,
        TAB_PPIS.upper()                            :   MODEL_EFI_PPI,
        TAB_PROTOCOLS.upper()                       :   MODEL_EFI_PROTOCOL,
        TAB_PCDS_FIXED_AT_BUILD_NULL.upper()        :   MODEL_PCD_FIXED_AT_BUILD,
        TAB_PCDS_PATCHABLE_IN_MODULE_NULL.upper()   :   MODEL_PCD_PATCHABLE_IN_MODULE,
        TAB_PCDS_FEATURE_FLAG_NULL.upper()          :   MODEL_PCD_FEATURE_FLAG,
        TAB_PCDS_DYNAMIC_NULL.upper()               :   MODEL_PCD_DYNAMIC,
        TAB_PCDS_DYNAMIC_EX_NULL.upper()            :   MODEL_PCD_DYNAMIC_EX,
    }

    def __init__(self, FilePath, FileId, FileType, Table, Macro={}):
        MetaFileParser.__init__(self, FilePath, FileType, Table, Macro, -1)

    def Start(self):
        try:
            if self._Content == None:
                self._Content = open(self._FilePath, 'r').readlines()
        except:
            EdkLogger.error("Parser", FILE_READ_FAILURE, ExtraData=self._FilePath)

        for Index in range(0, len(self._Content)):
            Line = CleanString(self._Content[Index])
            # skip empty line
            if Line == '':
                continue
            self._CurrentLine = Line
            self._LineIndex = Index

            # section header
            if Line[0] == TAB_SECTION_START and Line[-1] == TAB_SECTION_END:
                self._SectionHeaderParser()
                continue
            elif Line.startswith('DEFINE '):
                self._MacroParser()
                continue

            # section content
            self._ValueList = ['','','']
            self._SectionParser[self._SectionType](self)
            if self._ValueList == None:
                continue

            # 
            # Model, Value1, Value2, Value3, Value4, Value5, Arch, Platform, BelongsToFile=-1, 
            # LineBegin=-1, ColumnBegin=-1, LineEnd=-1, ColumnEnd=-1, BelongsToItem=-1, FeatureFlag='', 
            # Enabled=-1
            # 
            for Arch, ModuleType in self._Scope:
                self._LastItem = self._Store(
                    self._SectionType,
                    self._ValueList[0],
                    self._ValueList[1],
                    self._ValueList[2],
                    Arch,
                    ModuleType,
                    self._Owner,
                    self._LineIndex+1,
                    -1,
                    self._LineIndex+1,
                    -1,
                    0
                    )
        self._Done()
            
    def _GuidParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_EQUAL_SPLIT, 1)
        if len(TokenList) < 2:
            EdkLogger.error('Parser', FORMAT_INVALID, "No value specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)
        self._ValueList[0] = TokenList[0]
        self._ValueList[1] = TokenList[1]

    def _PcdParser(self):
        TokenList = GetSplitValueList(self._CurrentLine, TAB_VALUE_SPLIT, 1)
        self._ValueList[0:1] = GetSplitValueList(TokenList[0], TAB_SPLIT)
        self._ValueList[2] = TokenList[1]
        if self._ValueList[0] == '' or self._ValueList[1] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No token space GUID or PCD name specified",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)
        if self._ValueList[2] == '':
            EdkLogger.error('Parser', FORMAT_INVALID, "No PCD Datum information given",
                            ExtraData=self._CurrentLine, File=self._FilePath, Line=self._LineIndex+1)

    _SectionParser = {
        MODEL_META_DATA_HEADER          :   MetaFileParser._DefineParser,
        MODEL_EFI_INCLUDE               :   MetaFileParser._PathParser,
        MODEL_EFI_LIBRARY_CLASS         :   MetaFileParser._PathParser,
        MODEL_EFI_GUID                  :   _GuidParser,
        MODEL_EFI_PPI                   :   _GuidParser,
        MODEL_EFI_PROTOCOL              :   _GuidParser,
        MODEL_PCD_FIXED_AT_BUILD        :   _PcdParser,
        MODEL_PCD_PATCHABLE_IN_MODULE   :   _PcdParser,
        MODEL_PCD_FEATURE_FLAG          :   _PcdParser,
        MODEL_PCD_DYNAMIC               :   _PcdParser,
        MODEL_PCD_DYNAMIC_EX            :   _PcdParser,
        MODEL_UNKNOWN                   :   MetaFileParser._Skip,
        MODEL_META_DATA_USER_EXTENSION  :   MetaFileParser._Skip,
    }

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    pass

