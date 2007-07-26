from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
from CommonDataClass.FdfClassObject import VtfClassObject
T_CHAR_LF = '\n'

class Vtf (VtfClassObject):
    def __init__(self):
##        self.KeyArch = None
##        self.ArchList = None
##        self.UiName = None
####        self.OptionStatement = None
##        self.ResetBin = None
##        self.ComponentStatementList = []
        VtfClassObject.__init__(self)

    def GenVtf(self, fdAddDict) :
        self.GenBsfInf()
        OutputFile = os.path.join(GenFdsGlobalVariable.FvDir, self.UiName + '.Vtf')
        BaseAddArg = self.GetBaseAddArg(fdAddDict)
        outputArg, VtfRawDict = self.GenOutputArg()
        
        cmd = "GenVtf "        + \
               outputArg       + \
               ' -f '          + \
               self.BsfInfName + \
               ' '             + \
               BaseAddArg      
               
        print cmd
        GenFdsGlobalVariable.CallExternalTool(cmd, "GenFv -Vtf Failed!")
        return VtfRawDict
        
    def GenBsfInf (self):
        fvList = self.GetFvList()
        self.BsfInfName = os.path.join(GenFdsGlobalVariable.FvDir, self.UiName + '.inf')
        BsfInf = open (self.BsfInfName, 'w+')
        BsfInf.writelines ("[COMPONENTS]" + T_CHAR_LF)

        for component in self.ComponentStatementList :
            BsfInf.writelines ("COMP_NAME"        + \
                               " = "              + \
                               component.CompName + \
                               T_CHAR_LF )
            if component.CompLoc.upper() == 'NONE' :
                BsfInf.writelines ("COMP_LOC"        + \
                                   " = "             + \
                                   'N'               + \
                                   T_CHAR_LF )
            else:
                index = fvList.index(component.CompLoc.upper())
                if index == 0:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       'F'               + \
                                       T_CHAR_LF )
                elif index == 1:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       'S'                 + \
                                       T_CHAR_LF )
                
            BsfInf.writelines ("COMP_TYPE"        + \
                               " = "              + \
                               component.CompType + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_VER"        + \
                               " = "             + \
                               component.CompVer + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_CS"        + \
                               " = "            + \
                               component.CompCs + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_BIN"        + \
                               " = "             + \
                               GenFdsGlobalVariable.ReplaceWorkspaceMarco(component.CompBin) + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_SYM"        + \
                               " = "             + \
                               GenFdsGlobalVariable.ReplaceWorkspaceMarco(component.CompSym) + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_SIZE"        + \
                               " = "              + \
                               component.CompSize + \
                               T_CHAR_LF )
            BsfInf.writelines (T_CHAR_LF )
            
        BsfInf.close()

    def GetFvList(self):
        fvList = []
        for component in self.ComponentStatementList :
            if component.CompLoc.upper() != 'NONE' and not (component.CompLoc.upper() in fvList):
                fvList.append(component.CompLoc.upper())
                
        return fvList

    def GetBaseAddArg(self, fdAddDict):
        fvList = self.GetFvList()
        cmdStr = ''
        for i in fvList:
            (baseAdd, size) = fdAddDict.get(i)
            cmdStr = cmdStr               + \
                     ' -r 0x%x' %baseAdd  + \
                     ' -s 0x%x' %size
        return cmdStr
                     
    def GenOutputArg(self):
        fvVtfDict = {}
        outPutFileName = ''
        fvList = self.GetFvList()
        index = 0
        arg = ''
        for fv in fvList:
            index = index +1
            outputFileName = 'Vtf%d.raw' %index
            outPutFileName = os.path.join(GenFdsGlobalVariable.FvDir, outputFileName)
            arg = arg    + \
                  ' -o ' + \
                  outPutFileName
            fvVtfDict[fv.upper()] = outPutFileName
            
        return arg, fvVtfDict
                
