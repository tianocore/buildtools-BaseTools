## @file
# process VTF generation
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
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
from CommonDataClass.FdfClassObject import VtfClassObject
T_CHAR_LF = '\n'

## generate VTF
#
#
class Vtf (VtfClassObject):
    
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        VtfClassObject.__init__(self)

    ## GenVtf() method
    #
    #   Generate VTF
    #
    #   @param  self        The object pointer
    #   @param  FdAddDict   dictionary contains FV name and its base address
    #   @retval Dict        FV and corresponding VTF file name
    #
    def GenVtf(self, fdAddDict) :
        self.GenBsfInf()
        OutputFile = os.path.join(GenFdsGlobalVariable.FvDir, self.UiName + '.Vtf')
        BaseAddArg = self.GetBaseAddressArg(fdAddDict)
        OutputArg, VtfRawDict = self.GenOutputArg()
        
        Cmd = "GenVtf "        + \
               OutputArg       + \
               ' -f '          + \
               self.BsfInfName + \
               ' '             + \
               BaseAddArg      
               
        GenFdsGlobalVariable.CallExternalTool(Cmd, "GenFv -Vtf Failed!")
        GenFdsGlobalVariable.SharpCounter = 0
        
        return VtfRawDict
        
    ## GenBsfInf() method
    #
    #   Generate inf used to generate VTF
    #
    #   @param  self        The object pointer
    #
    def GenBsfInf (self):
        FvList = self.GetFvList()
        self.BsfInfName = os.path.join(GenFdsGlobalVariable.FvDir, self.UiName + '.inf')
        BsfInf = open (self.BsfInfName, 'w+')
        BsfInf.writelines ("[COMPONENTS]" + T_CHAR_LF)

        for ComponentObj in self.ComponentStatementList :
            BsfInf.writelines ("COMP_NAME"        + \
                               " = "              + \
                               ComponentObj.CompName + \
                               T_CHAR_LF )
            if ComponentObj.CompLoc.upper() == 'NONE':
                BsfInf.writelines ("COMP_LOC"        + \
                                   " = "             + \
                                   'N'               + \
                                   T_CHAR_LF )
            
            elif ComponentObj.FilePos != None:
                BsfInf.writelines ("COMP_LOC"        + \
                                   " = "             + \
                                   ComponentObj.FilePos + \
                                   T_CHAR_LF )
            else:
                Index = FvList.index(ComponentObj.CompLoc.upper())
                if Index == 0:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       'F'               + \
                                       T_CHAR_LF )
                elif Index == 1:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       'S'                 + \
                                       T_CHAR_LF )
                
            BsfInf.writelines ("COMP_TYPE"        + \
                               " = "              + \
                               ComponentObj.CompType + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_VER"        + \
                               " = "             + \
                               ComponentObj.CompVer + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_CS"        + \
                               " = "            + \
                               ComponentObj.CompCs + \
                               T_CHAR_LF )
            
            BinPath = ComponentObj.CompBin
            if BinPath != '-':
                BinPath = GenFdsGlobalVariable.MacroExtend(GenFdsGlobalVariable.ReplaceWorkspaceMarco(BinPath))
            BsfInf.writelines ("COMP_BIN"        + \
                               " = "             + \
                               BinPath + \
                               T_CHAR_LF )
            
            SymPath = ComponentObj.CompSym
            if SymPath != '-':
                SymPath = GenFdsGlobalVariable.MacroExtend(GenFdsGlobalVariable.ReplaceWorkspaceMarco(SymPath))
            BsfInf.writelines ("COMP_SYM"        + \
                               " = "             + \
                               SymPath + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_SIZE"        + \
                               " = "              + \
                               ComponentObj.CompSize + \
                               T_CHAR_LF )
            BsfInf.writelines (T_CHAR_LF )
            
        BsfInf.close()

    ## GenFvList() method
    #
    #   Get FV list referenced by VTF components
    #
    #   @param  self        The object pointer
    #
    def GetFvList(self):
        fvList = []
        for component in self.ComponentStatementList :
            if component.CompLoc.upper() != 'NONE' and not (component.CompLoc.upper() in fvList):
                fvList.append(component.CompLoc.upper())
                
        return fvList

    ## GetBaseAddressArg() method
    #
    #   Get base address arguments for GenVtf
    #
    #   @param  self        The object pointer
    #
    def GetBaseAddressArg(self, FdAddressDict):
        FvList = self.GetFvList()
        CmdStr = ''
        for i in FvList:
            (BaseAddress, Size) = FdAddressDict.get(i)
            CmdStr = CmdStr               + \
                     ' -r 0x%x' %BaseAddress  + \
                     ' -s 0x%x' %Size
        return CmdStr
    
    ## GenOutputArg() method
    #
    #   Get output arguments for GenVtf
    #
    #   @param  self        The object pointer
    #                 
    def GenOutputArg(self):
        FvVtfDict = {}
        OutPutFileName = ''
        FvList = self.GetFvList()
        Index = 0
        Arg = ''
        for FvObj in FvList:
            Index = Index +1
            OutputFileName = 'Vtf%d.raw' %Index
            OutPutFileName = os.path.join(GenFdsGlobalVariable.FvDir, OutputFileName)
            Arg = Arg    + \
                  ' -o ' + \
                  OutPutFileName
            FvVtfDict[FvObj.upper()] = OutPutFileName
            
        return Arg, FvVtfDict
                
