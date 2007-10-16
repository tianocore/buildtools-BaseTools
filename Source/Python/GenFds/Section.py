## @file
# section base class
#
#  Copyright (c) 2007, Intel Corporation
#
#  All rights reserved. This program and the accompanying materials
#  are licensed and made available under the terms and conditions of the BSD License
#  which accompanies this distribution.  The full text of the license may be found at
#  http://opensource.org/licenses/bsd-license.php
#
#  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
#  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
from CommonDataClass.FdfClassObject import SectionClassObject
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os

## section base class
#
#
class Section (SectionClassObject):
    SectionType = {
        'RAW'       : 'EFI_SECTION_RAW',
        'FREEFORM'  : 'EFI_SECTION_FREEFORM_SUBTYPE_GUID',
        'PE32'      : 'EFI_SECTION_PE32',
        'PIC'       : 'EFI_SECTION_PIC',
        'TE'        : 'EFI_SECTION_TE',
        'FV_IMAGE'  : 'EFI_SECTION_FIRMWARE_VOLUME_IMAGE',
        'DXE_DEPEX' : 'EFI_SECTION_DXE_DEPEX',
        'PEI_DEPEX' : 'EFI_SECTION_PEI_DEPEX',
        'GUIDED'    : 'EFI_SECTION_GUID_DEFINED',
        'COMPRESS'  : 'EFI_SECTION_COMPRESSION',
        'UI'        : 'EFI_SECTION_USER_INTERFACE'
    }

    BinFileType = {
        'GUID'          : '.guid',
        'ACPI'          : '.acpi',
        'ASL'           : '.asl' ,
        'UEFI_APP'      : '.app',
        'LIB'           : '.lib',
        'PE32'          : '.pe32',
        'PIC'           : '.pic',
        'PEI_DEPEX'     : '.depex',
        'SEC_PEI_DEPEX' : '.depex',
        'TE'            : '.te',
        'UNI_VER'       : '.ver',
        'VER'           : '.ver',
        'UNI_UI'        : '.ui',
        'UI'            : '.ui',
        'BIN'           : '.bin',
        'RAW'           : '.raw',
        'COMPAT16'      : '.comp16',
        'FV'            : '.fv'
    }

    SectFileType = {
        'SEC_GUID'      : '.sec' ,
        'SEC_PE32'      : '.sec' ,
        'SEC_PIC'       : '.sec',
        'SEC_TE'        : '.sec',
        'SEC_VER'       : '.sec',
        'SEC_UI'        : '.sec',
        'SEC_COMPAT16'  : '.sec',
        'SEC_BIN'       : '.sec'
    }
    
    ToolGuid = {
        '0xa31280ad-0x481e-0x41b6-0x95e8-0x127f-0x4c984779' : 'TianoCompress',
        '0xee4e5898-0x3914-0x4259-0x9d6e-0xdc7b-0xd79403cf' : 'LzmaCompress'
    }
    
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        SectionClassObject.__init__(self)
        
    ## GenSection() method
    #
    #   virtual function
    #
    #   @param  self        The object pointer
    #   @param  OutputPath  Where to place output file
    #   @param  ModuleName  Which module this section belongs to
    #   @param  SecNum      Index of section
    #   @param  KeyStringList  Filter for inputs of section generation
    #   @param  FfsInf      FfsInfStatement object that contains this section data
    #   @param  Dict        dictionary contains macro and its value
    #
    def GenSection(self, OutputPath, GuidName, SecNum, keyStringList, FfsInf = None, Dict = {}):
        pass

    ## GetFileList() method
    #
    #   Generate compressed section
    #
    #   @param  self        The object pointer
    #   @param  FfsInf      FfsInfStatement object that contains file list
    #   @param  FileType    File type to get
    #   @param  FileExtension  File extension to get
    #   @param  Dict        dictionary contains macro and its value
    #   @retval tuple       (File list, boolean)
    #
    def GetFileList(FfsInf, FileType, FileExtension, Dict = {}):
        if FileType in Section.SectFileType.keys() :
            IsSect = True
        else :
            IsSect = False
            
        if FileExtension != None:
            Suffix = FileExtension
        elif IsSect :
            Suffix = Section.SectionType.get(FileType)
        else:
            Suffix = Section.BinFileType.get(FileType)
        if FfsInf == None:
            raise Exception ('Inf File does not exist!')
        
        FileList = []
        if FileType != None:
            for File in FfsInf.BinFileList:
                if FfsInf.CurrentArch in File.SupArchList:
                    if File.FileType == FileType:
                        if '*' in FfsInf.TargetOverrideList or File.Target == '*' or File.Target in FfsInf.TargetOverrideList or FfsInf.TargetOverrideList == []:
                            FileList.append(os.path.join(GenFdsGlobalVariable.WorkSpaceDir, FfsInf.SourceDir, File.BinaryFile))
                        else:
                            GenFdsGlobalVariable.InfLogger ("\nBuild Target \'%s\' of File %s is not in the Scope of %s specified by INF %s in FDF" %(File.Target, File.BinaryFile, FfsInf.TargetOverrideList, FfsInf.InfFileName))
                    else:
                        GenFdsGlobalVariable.InfLogger ("\nFile Type \'%s\' of File %s is not same with %s from rule in FDF" %(File.FileType, FileType))
                else:
                        GenFdsGlobalVariable.InfLogger ("\nCurrent ARCH \'%s\' of File %s is not in the Scope of %s specified by INF %s in FDF" %(FfsInf.CurrentArch, File.BinaryFile, File.SupArchList, FfsInf.InfFileName))
            
        if os.path.exists(FfsInf.EfiOutputPath):
            for FileName in os.listdir(FfsInf.EfiOutputPath):
                Name, Ext = os.path.splitext(FileName)
                if Ext == Suffix:
                   FileList.append(os.path.join(FfsInf.EfiOutputPath, FileName))
                   
        return FileList, IsSect 
    GetFileList = staticmethod(GetFileList)
