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
            pass

    #
    # Check whether a Library Instance has been defined for all dependent library classes
    #
    def MetaDataFileCheckLibraryInstanceDependent(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceDependent == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            pass

    #
    # Check whether the Library Instances specified by the LibraryClasses sections are listed in order of dependencies
    #
    def MetaDataFileCheckLibraryInstanceOrder(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryInstanceOrder == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            pass

    #
    # Check whether the unnecessary inclusion of library classes in the Inf file
    #
    def MetaDataFileCheckLibraryNoUse(self):
        if EccGlobalData.gConfig.MetaDataFileCheckLibraryNoUse == '1' or EccGlobalData.gConfig.MetaDataFileCheckAll == '1':
            pass

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

##
#
# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
#
if __name__ == '__main__':
    Check = Check()
    Check.Check()

