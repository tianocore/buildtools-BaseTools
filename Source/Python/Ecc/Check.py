## @file
# This file is used to define checkpoints used by ECC tool
#
# Copyright (c) 2008, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#
import os
import re
from CommonDataClass.DataClass import *
from EccToolError import *
import EccGlobalData
import c

## Check
#
# This class is to define checkpoints used by ECC tool
#
# @param object:          Inherited from object class
#
class Check(object):
    def __init__(self):
        pass
     
    #
    # Check all required checkpoints
    #   
    def Check(self):
        self.MetaDataFileCheck()
        self.DoxygenCheck()
        self.IncludeFileCheck()
        self.PredicateExpressionCheck()
        self.DeclAndDataTypeCheck()
        self.FunctionLayoutCheck()
        self.NamingConventionCheck()
    
    #
    # C Function Layout Checking
    #
    def FunctionLayoutCheck(self):
        self.FunctionLayoutCheckReturnType()
        self.FunctionLayoutCheckModifier()
        self.FunctionLayoutCheckName()
        self.FunctionLayoutCheckPrototype()
        self.FunctionLayoutCheckBody()
        self.FunctionLayoutCheckLocalVariable()
    
    # Check whether return type exists and in the first line
    def FunctionLayoutCheckReturnType(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckReturnType == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout return type ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutReturnType(FullName)
    
    # Check whether any optional functional modifiers exist and next to the return type
    def FunctionLayoutCheckModifier(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckOptionalFunctionalModifier == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout modifier ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutModifier(FullName)
                        
    # Check whether the next line contains the function name, left justified, followed by the beginning of the parameter list
    # Check whether the closing parenthesis is on its own line and also indented two spaces
    def FunctionLayoutCheckName(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckFunctionName == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout function name ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutName(FullName)
    # Check whether the function prototypes in include files have the same form as function definitions
    def FunctionLayoutCheckPrototype(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckFunctionPrototype == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout function prototype ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutPrototype(FullName)

    # Check whether the body of a function is contained by open and close braces that must be in the first column
    def FunctionLayoutCheckBody(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckFunctionBody == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout function body ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutBody(FullName)

    # Check whether the data declarations is the first code in a module.
    #self.CFunctionLayoutCheckDataDeclaration = 1
    # Check whether no initialization of a variable as part of its declaration
    def FunctionLayoutCheckLocalVariable(self):
        if EccGlobalData.gConfig.CFunctionLayoutCheckNoInitOfVariable == '1' or EccGlobalData.gConfig.CFunctionLayoutCheckAll == '1':
            EdkLogger.quiet("Checking function layout local variables ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckFuncLayoutLocalVariable(FullName)

    # Check whether no use of STATIC for functions
    #self.CFunctionLayoutCheckNoStatic = 1
    
    #
    # Declarations and Data Types Checking
    #
    def DeclAndDataTypeCheck(self):
        self.DeclCheckNoUseCType()
        self.DeclCheckInOutModifier()
        self.DeclCheckEFIAPIModifier()
        self.DeclCheckEnumeratedType()
        self.DeclCheckStructureDeclaration()
        self.DeclCheckUnionType()
    
    
    # Check whether no use of int, unsigned, char, void, static, long in any .c, .h or .asl files.
    def DeclCheckNoUseCType(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckNoUseCType == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            EdkLogger.quiet("Checking Declaration No use C type ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckDeclNoUseCType(FullName)
    
    # Check whether the modifiers IN, OUT, OPTIONAL, and UNALIGNED are used only to qualify arguments to a function and should not appear in a data type declaration
    def DeclCheckInOutModifier(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckInOutModifier == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            EdkLogger.quiet("Checking Declaration argument modifier ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckDeclArgModifier(FullName)
    
    # Check whether the EFIAPI modifier should be used at the entry of drivers, events, and member functions of protocols
    def DeclCheckEFIAPIModifier(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckEFIAPIModifier == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            pass
    
    # Check whether Enumerated Type has a 'typedef' and the name is capital
    def DeclCheckEnumeratedType(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckEnumeratedType == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            EdkLogger.quiet("Checking Declaration enum typedef ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckDeclEnumTypedef(FullName)
    
    # Check whether Structure Type has a 'typedef' and the name is capital
    def DeclCheckStructureDeclaration(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckStructureDeclaration == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            EdkLogger.quiet("Checking Declaration struct typedef ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckDeclStructTypedef(FullName)
    
    # Check whether Union Type has a 'typedef' and the name is capital
    def DeclCheckUnionType(self):
        if EccGlobalData.gConfig.DeclarationDataTypeCheckUnionType == '1' or EccGlobalData.gConfig.DeclarationDataTypeCheckAll == '1':
            EdkLogger.quiet("Checking Declaration union typedef ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckDeclUnionTypedef(FullName)
    
    #
    # Predicate Expression Checking
    #
    def PredicateExpressionCheck(self):
        self.PredicateExpressionCheckBooleanValue()
        self.PredicateExpressionCheckNonBooleanOperator()
        self.PredicateExpressionCheckComparisonNullType()
    
    # Check whether Boolean values, variable type BOOLEAN not use explicit comparisons to TRUE or FALSE
    def PredicateExpressionCheckBooleanValue(self):
        if EccGlobalData.gConfig.PredicateExpressionCheckBooleanValue == '1' or EccGlobalData.gConfig.PredicateExpressionCheckAll == '1':
            EdkLogger.quiet("Checking predicate expression Boolean value ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckBooleanValueComparison(FullName)
    # Check whether Non-Boolean comparisons use a compare operator (==, !=, >, < >=, <=). 
    def PredicateExpressionCheckNonBooleanOperator(self):
        if EccGlobalData.gConfig.PredicateExpressionCheckNonBooleanOperator == '1' or EccGlobalData.gConfig.PredicateExpressionCheckAll == '1':
            EdkLogger.quiet("Checking predicate expression Non-Boolean variable...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckNonBooleanValueComparison(FullName)
    # Check whether a comparison of any pointer to zero must be done via the NULL type
    def PredicateExpressionCheckComparisonNullType(self):
        if EccGlobalData.gConfig.PredicateExpressionCheckComparisonNullType == '1' or EccGlobalData.gConfig.PredicateExpressionCheckAll == '1':
            EdkLogger.quiet("Checking predicate expression NULL pointer ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.c'):
                        FullName = os.path.join(Dirpath, F)
                        c.CheckPointerNullComparison(FullName)
    #
    # Include file checking
    #
    def IncludeFileCheck(self):
        self.IncludeFileCheckIfndef()
        self.IncludeFileCheckData()
    
    #
    # Check whether all include file contents is guarded by a #ifndef statement.
    #
    def IncludeFileCheckIfndef(self):
        if EccGlobalData.gConfig.IncludeFileCheckIfndefStatement == '1' or EccGlobalData.gConfig.IncludeFileCheckAll == '1':
            EdkLogger.quiet("Checking header file ifndef ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckHeaderFileIfndef(FullName)
    
    #
    # Check whether include files NOT contain code or define data variables
    #
    def IncludeFileCheckData(self):
        if EccGlobalData.gConfig.IncludeFileCheckData == '1' or EccGlobalData.gConfig.IncludeFileCheckAll == '1':
            EdkLogger.quiet("Checking header file data ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckHeaderFileData(FullName)
        
    #
    # Doxygen document checking
    #
    def DoxygenCheck(self):
        self.DoxygenCheckFileHeader()
        self.DoxygenCheckFunctionHeader()
        self.DoxygenCheckCommentDescription()
        self.DoxygenCheckCommentFormat()
        self.DoxygenCheckCommand()
    
    #
    # Check whether the file headers are followed Doxygen special documentation blocks in section 2.3.5
    #
    def DoxygenCheckFileHeader(self):
        if EccGlobalData.gConfig.DoxygenCheckFileHeader == '1' or EccGlobalData.gConfig.DoxygenCheckAll == '1':
            EdkLogger.quiet("Checking Doxygen file header ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckFileHeaderDoxygenComments(FullName)
    
    #
    # Check whether the function headers are followed Doxygen special documentation blocks in section 2.3.5
    #
    def DoxygenCheckFunctionHeader(self):
        if EccGlobalData.gConfig.DoxygenCheckFunctionHeader == '1' or EccGlobalData.gConfig.DoxygenCheckAll == '1':
            EdkLogger.quiet("Checking Doxygen function header ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
#            ParseErrorFileList = []
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckFuncHeaderDoxygenComments(FullName)
#                        for Msg in MsgList:
#                            print Msg                
                            
    #
    # Check whether the first line of text in a comment block is a brief description of the element being documented. 
    # The brief description must end with a period.
    #
    def DoxygenCheckCommentDescription(self):
        if EccGlobalData.gConfig.DoxygenCheckCommentDescription == '1' or EccGlobalData.gConfig.DoxygenCheckAll == '1':
            pass

    #
    # Check whether comment lines with '///< ... text ...' format, if it is used, it should be after the code section.
    #
    def DoxygenCheckCommentFormat(self):
        if EccGlobalData.gConfig.DoxygenCheckCommentFormat == '1' or EccGlobalData.gConfig.DoxygenCheckAll == '1':
            EdkLogger.quiet("Checking Doxygen comment ///< ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckDoxygenTripleForwardSlash(FullName)
        
    #
    # Check whether only Doxygen commands allowed to mark the code are @bug and @todo.
    #
    def DoxygenCheckCommand(self):
        if EccGlobalData.gConfig.DoxygenCheckCommand == '1' or EccGlobalData.gConfig.DoxygenCheckAll == '1':
            EdkLogger.quiet("Checking Doxygen command ...")
            Tuple = os.walk(EccGlobalData.gTarget)
            IgnoredPattern = re.compile(r'.*[\\/](?:BUILD|CVS|\.SVN|INTELRESTRICTEDTOOLS|INTELRESTRICTEDPKG)[\\/].*')
        
            for Dirpath, Dirnames, Filenames in Tuple:
                if IgnoredPattern.match(Dirpath.upper()) or Dirpath.find('.svn') != -1:
                    continue
                for F in Filenames:
                    if os.path.splitext(F)[1] in ('.h', '.c'):
                        FullName = os.path.join(Dirpath, F)
                        MsgList = c.CheckDoxygenCommand(FullName)
    
    #
    # Meta-Data File Processing Checking
    #
    def MetaDataFileCheck(self):
        self.MetaDataFileCheckPathName()
        self.MetaDataFileCheckGenerateFileList()
        self.MetaDataFileCheckLibraryInstance()
        self.MetaDataFileCheckLibraryInstanceDependent()
        self.MetaDataFileCheckLibraryInstanceOrder()
        self.MetaDataFileCheckLibraryNoUse()
        self.MetaDataFileCheckBinaryInfInFdf()
        self.MetaDataFileCheckPcdDuplicate()
        self.MetaDataFileCheckPcdFlash()
        self.MetaDataFileCheckPcdNoUse()
        self.MetaDataFileCheckGuidDuplicate()

    #
    # Check whether each file defined in meta-data exists
    #
    def MetaDataFileCheckPathName(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPathName == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            # This item is covered when parsing Inf/Dec/Dsc files
            pass
    
    #
    # Generate a list for all files defined in meta-data files
    #
    def MetaDataFileCheckGenerateFileList(self):
        if EccGlobalData.gConfig.MetaDataFileCheckGenerateFileList == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            # This item is covered when parsing Inf/Dec/Dsc files
            pass
    
    #
    # Check whether all Library Instances defined for a given module (or dependent library instance) match the module's type.  
    # Each Library Instance must specify the Supported Module Types in its Inf file, 
    # and any module specifying the library instance must be one of the supported types.
    #
    def MetaDataFileCheckLibraryInstance(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstance == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for library instance type issue ...")
            SqlCommand = """select ID, Value2 from Inf where Value1 = 'LIBRARY_CLASS' and Model = %s group by BelongsToFile""" % MODEL_META_DATA_HEADER
            RecordSet = EccGlobalData.gDb.TblInf.Exec(SqlCommand)
            LibraryClasses = {}
            for Record in RecordSet:
                List = Record[1].split('|', 1)
                if len(List) != 2:
                    EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_LIBRARY_INSTANCE_2, OtherMsg = "The Library Class '%s' does not specify its supported module types" % (List[0]), BelongsToTable = 'Inf', BelongsToItem = Record[0])
                else:
                    LibraryClasses[List[0]] = List[1]
            SqlCommand = """select A.ID, A.Value1, B.Value2 from Inf as A left join Inf as B 
                            where A.Model = %s and B.Value1 = '%s' and B.Model = %s and B.BelongsToFile = A.BelongsToFile""" \
                            % (MODEL_EFI_LIBRARY_CLASS, 'MODULE_TYPE', MODEL_META_DATA_HEADER)
            RecordSet = EccGlobalData.gDb.TblInf.Exec(SqlCommand)
            for Record in RecordSet:
                if Record[1] in LibraryClasses and LibraryClasses[Record[1]].find(Record[2]) < 0:
                    EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_LIBRARY_INSTANCE_1, OtherMsg = "The type of Library Class '%s' defined in Inf file does not match the type of the module" % (Record[1]), BelongsToTable = 'Inf', BelongsToItem = Record[0])
    #
    # Check whether a Library Instance has been defined for all dependent library classes
    #
    def MetaDataFileCheckLibraryInstanceDependent(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceDependent == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for library instance dependent issue ...")
            SqlCommand = """select ID, Value1, Value2 from Dsc where Model = %s""" % MODEL_EFI_LIBRARY_CLASS
            LibraryClasses = EccGlobalData.gDb.TblDsc.Exec(SqlCommand)
            for LibraryClass in LibraryClasses:
                if LibraryClass[1].upper() != 'NULL':
                    LibraryIns = os.path.normpath(os.path.join(EccGlobalData.gWorkspace, LibraryClass[2]))
                    SqlCommand = """select Value2 from Inf where BelongsToFile = 
                                    (select ID from File where lower(FullPath) = lower('%s'))
                                    and Value1 = '%s'""" % (LibraryIns, 'LIBRARY_CLASS')
                    RecordSet = EccGlobalData.gDb.TblInf.Exec(SqlCommand)
                    IsFound = False
                    for Record in RecordSet:
                        LibName = Record[0].split('|', 1)[0]
                        if LibraryClass[1] == LibName:
                            IsFound = True
                    if not IsFound:
                        EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_LIBRARY_INSTANCE_DEPENDENT, OtherMsg = "The Library Class '%s' is not specified in '%s'" % (LibraryClass[1], LibraryClass[2]), BelongsToTable = 'Dsc', BelongsToItem = LibraryClass[0])
    #
    # Check whether the Library Instances specified by the LibraryClasses sections are listed in order of dependencies
    #
    def MetaDataFileCheckLibraryInstanceOrder(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceOrder == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            # This checkpoint is not necessary for Ecc check
            pass

    #
    # Check whether the unnecessary inclusion of library classes in the Inf file
    #
    def MetaDataFileCheckLibraryNoUse(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryNoUse == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for library instance not used ...")
            SqlCommand = """select ID, Value1 from Inf as A where A.Model = %s and A.Value1 not in (select B.Value1 from Dsc as B where Model = %s)""" % (MODEL_EFI_LIBRARY_CLASS, MODEL_EFI_LIBRARY_CLASS)
            RecordSet = EccGlobalData.gDb.TblInf.Exec(SqlCommand)
            for Record in RecordSet:
                EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_LIBRARY_NO_USE, OtherMsg = "The Library Class '%s' is not used in any platform" % (Record[1]), BelongsToTable = 'Inf', BelongsToItem = Record[0])

    #
    # Check whether an Inf file is specified in the FDF file, but not in the Dsc file, then the Inf file must be for a Binary module only
    #
    def MetaDataFileCheckBinaryInfInFdf(self):
        if EccGlobalData.gConfig.MetaDataFileCheckBinaryInfInFdf == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for non-binary modules defined in FDF files ...")
            SqlCommand = """select A.ID, A.Value1 from Fdf as A
                         where A.Model = %s
                         and A.Enabled > -1
                         and A.Value1 not in 
                         (select B.Value1 from Dsc as B
                         where B.Model = %s
                         and B.Enabled > -1)""" % (MODEL_META_DATA_COMPONENT, MODEL_META_DATA_COMPONENT)
            RecordSet = EccGlobalData.gDb.TblFdf.Exec(SqlCommand)
            for Record in RecordSet:
                FdfID = Record[0]
                FilePath = Record[1]
                FilePath = os.path.normpath(os.path.join(EccGlobalData.gWorkspace, FilePath))
                SqlCommand = """select ID from Inf where Model = %s and BelongsToFile = (select ID from File where FullPath like '%s')
                                """ % (MODEL_EFI_SOURCE_FILE, FilePath)
                NewRecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                if NewRecordSet!= []:
                    EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_BINARY_INF_IN_FDF, OtherMsg = "File %s defined in FDF file and not in DSC file must be a binary module" % (FilePath), BelongsToTable = 'Fdf', BelongsToItem = FdfID)

    #
    # Check whether a PCD is set in a Dsc file or the FDF file, but not in both.
    #
    def MetaDataFileCheckPcdDuplicate(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdDuplicate == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for duplicate PCDs defined in both DSC and FDF files ...")
            SqlCommand = """
                         select A.ID, A.Value2, B.ID, B.Value2 from Dsc as A, Fdf as B 
                         where A.Model >= %s and A.Model < %s 
                         and B.Model >= %s and B.Model < %s 
                         and A.Value2 = B.Value2
                         and A.Enabled > -1
                         and B.Enabled > -1
                         """% (MODEL_PCD, MODEL_META_DATA_HEADER, MODEL_PCD, MODEL_META_DATA_HEADER)
            RecordSet = EccGlobalData.gDb.TblDsc.Exec(SqlCommand)
            for Record in RecordSet:
                EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_PCD_DUPLICATE, OtherMsg = "The PCD '%s' is defined in both FDF file and DSC file" % (Record[1]), BelongsToTable = 'Dsc', BelongsToItem = Record[0])
                EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_PCD_DUPLICATE, OtherMsg = "The PCD '%s' is defined in both FDF file and DSC file" % (Record[3]), BelongsToTable = 'Fdf', BelongsToItem = Record[2])

    #
    # Check whether PCD settings in the FDF file can only be related to flash.
    #
    def MetaDataFileCheckPcdFlash(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdFlash == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking only Flash related PCDs are used in FDF ...")
            SqlCommand = """
                         select ID, Value2, BelongsToFile from Fdf as A
                         where A.Model >= %s and Model < %s
                         and A.Enabled > -1
                         and A.Value2 not like '%%Flash%%'
                         """% (MODEL_PCD, MODEL_META_DATA_HEADER)
            RecordSet = EccGlobalData.gDb.TblFdf.Exec(SqlCommand)
            for Record in RecordSet:
                EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_PCD_FLASH, OtherMsg = "The PCD '%s' defined in FDF file is not related to Flash" % (Record[1]), BelongsToTable = 'Fdf', BelongsToItem = Record[0])
        
    #
    # Check whether PCDs used in Inf files but not specified in Dsc or FDF files
    #
    def MetaDataFileCheckPcdNoUse(self):
        if EccGlobalData.gConfig.MetaDataFileCheckPcdNoUse == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for non-specified PCDs ...")
            SqlCommand = """
                         select ID, Value2, BelongsToFile from Inf as A 
                         where A.Model >= %s and Model < %s
                         and A.Enabled > -1
                         and A.Value2 not in 
                             (select Value2 from Dsc as B 
                              where B.Model >= %s and B.Model < %s
                              and B.Enabled > -1)
                         and A.Value2 not in
                             (select Value2 from Fdf as C 
                              where C.Model >= %s and C.Model < %s
                              and C.Enabled > -1)
                         """% (MODEL_PCD, MODEL_META_DATA_HEADER, MODEL_PCD, MODEL_META_DATA_HEADER, MODEL_PCD, MODEL_META_DATA_HEADER)
            RecordSet = EccGlobalData.gDb.TblInf.Exec(SqlCommand)
            for Record in RecordSet:
                EccGlobalData.gDb.TblReport.Insert(ERROR_META_DATA_FILE_CHECK_PCD_NO_USE, OtherMsg = "The PCD '%s' defined in INF file is not specified in either DSC or FDF files" % (Record[1]), BelongsToTable = 'Inf', BelongsToItem = Record[0])
        
    #
    # Check whether having duplicate guids defined for Guid/Protocol/Ppi
    #
    def MetaDataFileCheckGuidDuplicate(self):
        if EccGlobalData.gConfig.MetaDataFileCheckGuidDuplicate == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            EdkLogger.quiet("Checking for duplicate GUID/PPI/PROTOCOL ...")
            #
            # Check Guid
            #
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_GUID, MODEL_EFI_GUID, EccGlobalData.gDb.TblDec)
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_GUID, MODEL_EFI_GUID, EccGlobalData.gDb.TblDsc)
            self.CheckGuidProtocolPpiValue(ERROR_META_DATA_FILE_CHECK_DUPLICATE_GUID, MODEL_EFI_GUID)
            #
            # Check protocol
            #
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PROTOCOL, MODEL_EFI_PROTOCOL, EccGlobalData.gDb.TblDec)
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PROTOCOL, MODEL_EFI_PROTOCOL, EccGlobalData.gDb.TblDsc)
            self.CheckGuidProtocolPpiValue(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PROTOCOL, MODEL_EFI_PROTOCOL)
            #
            # Check ppi
            #
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PPI, MODEL_EFI_PPI, EccGlobalData.gDb.TblDec)
            self.CheckGuidProtocolPpi(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PPI, MODEL_EFI_PPI, EccGlobalData.gDb.TblDsc)
            self.CheckGuidProtocolPpiValue(ERROR_META_DATA_FILE_CHECK_DUPLICATE_PPI, MODEL_EFI_PPI)

            #EdkLogger.quiet("Checking duplicate guid/ppi/protocol done!")
    
    #
    # Check whether these is duplicate Guid/Ppi/Protocol name
    #
    def CheckGuidProtocolPpi(self, ErrorID, Model, Table):
        Name = ''
        if Model == MODEL_EFI_GUID:
            Name = 'guid'
        if Model == MODEL_EFI_PROTOCOL:
            Name = 'protocol'
        if Model == MODEL_EFI_PPI:
            Name = 'ppi'
        SqlCommand = """
                     select A.ID, A.Value1 from %s as A, %s as B 
                     where A.Model = %s and B.Model = %s 
                     and A.Value1 = B.Value1 and A.ID <> B.ID 
                     and A.Enabled > -1
                     and B.Enabled > -1
                     group by A.ID
                     """ % (Table.Table, Table.Table, Model, Model)
        RecordSet = Table.Exec(SqlCommand)
        for Record in RecordSet:
            EccGlobalData.gDb.TblReport.Insert(ErrorID, OtherMsg = "The %s name '%s' is defined more than one time" % (Name.upper(), Record[1]), BelongsToTable = Table.Table, BelongsToItem = Record[0])

    #
    # Check whether these is duplicate Guid/Ppi/Protocol value
    #
    def CheckGuidProtocolPpiValue(self, ErrorID, Model):
        Name = ''
        Table = EccGlobalData.gDb.TblDec
        if Model == MODEL_EFI_GUID:
            Name = 'guid'
        if Model == MODEL_EFI_PROTOCOL:
            Name = 'protocol'
        if Model == MODEL_EFI_PPI:
            Name = 'ppi'
        SqlCommand = """
                     select A.ID, A.Value2 from %s as A, %s as B 
                     where A.Model = %s and B.Model = %s 
                     and A.Value2 = B.Value2 and A.ID <> B.ID 
                     group by A.ID
                     """ % (Table.Table, Table.Table, Model, Model)
        RecordSet = Table.Exec(SqlCommand)
        for Record in RecordSet:
            EccGlobalData.gDb.TblReport.Insert(ErrorID, OtherMsg = "The %s value '%s' is used more than one time" % (Name.upper(), Record[1]), BelongsToTable = Table.Table, BelongsToItem = Record[0])

    #
    # Naming Convention Check
    #
    def NamingConventionCheck(self):
        self.NamingConventionCheckDefineStatement()
        self.NamingConventionCheckTypedefStatement()
        self.NamingConventionCheckIfndefStatement()
        self.NamingConventionCheckPathName()
        self.NamingConventionCheckVariableName()
        self.NamingConventionCheckFunctionName()
        self.NamingConventionCheckSingleCharacterVariable()
        
    #
    # Check whether only capital letters are used for #define declarations
    #
    def NamingConventionCheckDefineStatement(self):
        if EccGlobalData.gConfig.NamingConventionCheckDefineStatement == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of #define statement ...")
            for IdentifierTable in EccGlobalData.gIdentifierTableList:
                SqlCommand = """select ID, Value from %s where Model = %s""" %(IdentifierTable, MODEL_IDENTIFIER_MACRO_DEFINE)
                RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                for Record in RecordSet:
                    Name = Record[1].strip().split()[1]
                    Name = Name[0:Name.find('(')]
                    if Name.upper() != Name:
                        EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_DEFINE_STATEMENT, OtherMsg = "The #define name '%s' does not follow the rules" % (Name), BelongsToTable = IdentifierTable, BelongsToItem = Record[0])
    
    #
    # Check whether only capital letters are used for typedef declarations
    #
    def NamingConventionCheckTypedefStatement(self):
        if EccGlobalData.gConfig.NamingConventionCheckTypedefStatement == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of #typedef statement ...")
            for IdentifierTable in EccGlobalData.gIdentifierTableList:
                SqlCommand = """select ID, Name from %s where Model = %s""" %(IdentifierTable, MODEL_IDENTIFIER_TYPEDEF)
                RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                for Record in RecordSet:
                    Name = Record[1].strip()
                    if Name[0] == '(':
                        Name = Name[1:Name.find(')')]
                    if Name.find('(') > -1:
                        Name = Name[Name.find('(') + 1 : Name.find(')')]
                    Name = Name.replace('WINAPI', '')
                    Name = Name.replace('*', '').strip()
                    if Name.upper() != Name:
                        EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_TYPEDEF_STATEMENT, OtherMsg = "The #typedef name '%s' does not follow the rules" % (Name), BelongsToTable = IdentifierTable, BelongsToItem = Record[0])
    
    #
    # Check whether the #ifndef at the start of an include file uses both prefix and postfix underscore characters, '_'.
    #
    def NamingConventionCheckIfndefStatement(self):
        if EccGlobalData.gConfig.NamingConventionCheckTypedefStatement == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of #ifndef statement ...")
            for IdentifierTable in EccGlobalData.gIdentifierTableList:
                SqlCommand = """select ID, Value from %s where Model = %s""" %(IdentifierTable, MODEL_IDENTIFIER_MACRO_IFNDEF)
                RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                for Record in RecordSet:
                    Name = Record[1].replace('#ifndef', '').strip()
                    if Name[0] != '_' or Name[-1] != '_':
                        EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_IFNDEF_STATEMENT, OtherMsg = "The #ifndef name '%s' does not follow the rules" % (Name), BelongsToTable = IdentifierTable, BelongsToItem = Record[0])
    
    #
    # Rule for path name, variable name and function name
    # 1. First character should be upper case
    # 2. Existing lower case in a word
    # 3. No space existence
    # Check whether the path name followed the rule
    #
    def NamingConventionCheckPathName(self):
        if EccGlobalData.gConfig.NamingConventionCheckPathName == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of file path name ...")
            Pattern = re.compile(r'^[A-Z]+\S*[a-z]\S*$')
            SqlCommand = """select ID, Name from File"""
            RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
            for Record in RecordSet:
                if not Pattern.match(Record[1]):
                    EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_PATH_NAME, OtherMsg = "The file path '%s' does not follow the rules" % (Record[1]), BelongsToTable = 'File', BelongsToItem = Record[0])
    
    #
    # Rule for path name, variable name and function name
    # 1. First character should be upper case
    # 2. Existing lower case in a word
    # 3. No space existence
    # 4. Global variable name must start with a 'g'
    # Check whether the variable name followed the rule
    #
    def NamingConventionCheckVariableName(self):
        if EccGlobalData.gConfig.NamingConventionCheckVariableName == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of variable name ...")
            Pattern = re.compile(r'^[A-Zgm]+\S*[a-z]\S*$')
            for IdentifierTable in EccGlobalData.gIdentifierTableList:
                SqlCommand = """select ID, Name from %s where Model = %s""" %(IdentifierTable, MODEL_IDENTIFIER_VARIABLE)
                RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                for Record in RecordSet:
                    if not Pattern.match(Record[1]):
                        EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_VARIABLE_NAME, OtherMsg = "The variable name '%s' does not follow the rules" % (Record[1]), BelongsToTable = IdentifierTable, BelongsToItem = Record[0])

    #
    # Rule for path name, variable name and function name
    # 1. First character should be upper case
    # 2. Existing lower case in a word
    # 3. No space existence
    # Check whether the function name followed the rule
    #
    def NamingConventionCheckFunctionName(self):
        if EccGlobalData.gConfig.NamingConventionCheckFunctionName == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of function name ...")
            Pattern = re.compile(r'^[A-Z]+\S*[a-z]\S*$')
            SqlCommand = """select ID, Name from Function"""
            RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
            for Record in RecordSet:
                if not Pattern.match(Record[1]):
                    EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_FUNCTION_NAME, OtherMsg = "The function name '%s' does not follow the rules" % (Record[1]), BelongsToTable = 'Function', BelongsToItem = Record[0])

    #
    # Check whether NO use short variable name with single character
    #
    def NamingConventionCheckSingleCharacterVariable(self):
        if EccGlobalData.gConfig.NamingConventionCheckSingleCharacterVariable == '1' or EccGlobalData.gConfig.NamingConventionCheckAll == '1':
            EdkLogger.quiet("Checking naming covention of single character variable name ...")
            for IdentifierTable in EccGlobalData.gIdentifierTableList:
                SqlCommand = """select ID, Name from %s where Model = %s""" %(IdentifierTable, MODEL_IDENTIFIER_VARIABLE)
                RecordSet = EccGlobalData.gDb.TblFile.Exec(SqlCommand)
                for Record in RecordSet:
                    Variable = Record[1].replace('*', '')
                    if len(Variable) == 1:
                        EccGlobalData.gDb.TblReport.Insert(ERROR_NAMING_CONVENTION_CHECK_SINGLE_CHARACTER_VARIABLE, OtherMsg = "The variable name '%s' does not follow the rules" % (Record[1]), BelongsToTable = IdentifierTable, BelongsToItem = Record[0])

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    Check = Check()
    Check.Check()
