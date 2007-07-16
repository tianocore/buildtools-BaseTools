from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
T_CHAR_LF = '\n'

class Vtf:
    def __init__(self):
        self.KeyArch = None
        self.ArchList = None
        self.UiName = None
##        self.OptionStatement = None
        self.ResetBin = None
        self.ComponentStatementList = []
        

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
        PopenObject = subprocess.Popen(cmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0:
            raise Exception(errorMess)
        #GenFdsGlobalVariable.CallExternalTool(cmd, "GenFv -Vtf Failed!")
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
            if component.CompLoc == None:
                BsfInf.writelines ("COMP_LOC"        + \
                                   " = "             + \
                                   'N'               + \
                                   T_CHAR_LF )
            else:
                index = fvList.index(component.CompLoc)
                if index == 0:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       'F'               + \
                                       T_CHAR_LF )
                elif index == 1:
                    BsfInf.writelines ("COMP_LOC"        + \
                                       " = "             + \
                                       S                 + \
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
            if component.CompLoc != None and not (component.CompLoc in fvList):
                fvList.append(component.CompLoc)
                
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
            fvVtfDict[fv] = outPutFileName
            
        return arg, fvVtfDict
                
