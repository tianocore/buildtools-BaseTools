## @file
# process data section generation
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
import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs
import os
from CommonDataClass.FdfClassObject import DataSectionClassObject
import shutil

## generate data section
#
#
class DataSection (DataSectionClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        DataSectionClassObject.__init__(self)
    
    ## GenSection() method
    #
    #   Generate compressed section
    #
    #   @param  self        The object pointer
    #   @param  OutputPath  Where to place output file
    #   @param  ModuleName  Which module this section belongs to
    #   @param  SecNum      Index of section
    #   @param  KeyStringList  Filter for inputs of section generation
    #   @param  FfsInf      FfsInfStatement object that contains this section data
    #   @param  Dict        dictionary contains macro and its value
    #   @retval tuple       (Generated file name list, section alignment)
    #    
    def GenSection(self, OutputPath, ModuleName, SecNum, keyStringList, FfsFile = None, Dict = {}):
        #
        # Prepare the parameter of GenSection
        #
        if FfsFile != None:
#            self.Alignment = FfsInf.__ExtendMacro__(self.Alignemnt)
#            self.SecType = FfsInf.__ExtendMacro__(self.SecType)
            self.SectFileName = GenFdsGlobalVariable.ReplaceWorkspaceMacro(self.SectFileName)
            self.SectFileName = GenFdsGlobalVariable.MacroExtend(self.SectFileName, Dict, FfsFile.CurrentArch)
        else:
#            raise Exception ("Module %s GenDataSection for None!" %ModuleName)
            self.SectFileName = GenFdsGlobalVariable.ReplaceWorkspaceMacro(self.SectFileName)
            self.SectFileName = GenFdsGlobalVariable.MacroExtend(self.SectFileName, Dict)
        
        """Check Section file exist or not !"""

        if not os.path.exists(self.SectFileName):
            self.SectFileName = os.path.join (GenFdsGlobalVariable.WorkSpaceDir,
                                              self.SectFileName)
        
        """Copy Map file to Ffs output"""
        Filename = GenFdsGlobalVariable.MacroExtend(self.SectFileName)
        if Filename[(len(Filename)-4):] == '.efi':
            MapFile = Filename.replace('.efi', '.map')
            if os.path.exists(MapFile):
                CopyMapFile = os.path.join(OutputPath, ModuleName + '.map')
                shutil.copyfile(MapFile, CopyMapFile) 
        
        NoStrip = True
        if self.SecType in ('TE', 'PE32'):
            if self.KeepReloc != None:
                NoStrip = self.KeepReloc
        
        if not NoStrip:
            FileBeforeStrip = os.path.join(OutputPath, ModuleName + '.efi')
            shutil.copyfile(self.SectFileName, FileBeforeStrip)
            StrippedFile = os.path.join(OutputPath, ModuleName + '.stripped')
            StripCmd = (
                'GenFw',
                '-l',
                '-o', StrippedFile,
                GenFdsGlobalVariable.MacroExtend(self.SectFileName, Dict),
                )
            GenFdsGlobalVariable.CallExternalTool(StripCmd, "Strip Failed !")
            self.SectFileName = StrippedFile
        
        if self.SecType == 'TE':
            TeFile = os.path.join( OutputPath, ModuleName + 'Te.raw')
            GenTeCmd = (
                'GenFw',
                '-t',
                '-o', TeFile,
                GenFdsGlobalVariable.MacroExtend(self.SectFileName, Dict),
                )
            GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
            self.SectFileName = TeFile    
                 
        OutputFile = os.path.join (OutputPath, ModuleName + 'SEC' + SecNum + Ffs.SectionSuffix.get(self.SecType))
        OutputFile = os.path.normpath(OutputFile)
        
        GenSectionCmd = (
            'GenSec',
             '-o', OutputFile,
             '-s', Section.Section.SectionType.get (self.SecType),
             self.SectFileName,
            )
                         
        #
        # Call GenSection
        #
        
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
        FileList = [OutputFile]
        return FileList, self.Alignment
