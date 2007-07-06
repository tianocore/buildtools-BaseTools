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
        
        

    def GenVtf(self) :
        self.GenBsfInf()
        OutputFile = os.path.join(GenFdsGlobalVariabel.FvDir, self.UiName + '.Vtf')
        BaseAddArg = ''
        for item in self.BaseAddressList :
            BaseAddArg = BaseAddArg   + \
                         ' -a '       + \
                         item[0]      + \
                         ' -s '       + \
                         item[1]
        cmd = "GenVtf -i "     + \
               ' -o '          + \
               OutputFile      + \
               self.BsfInfName + \
               BaseAddArg
               
        print cmd
        PopenObject = subprocess.Popen(cmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0 :
            raise Exception ("GenFv Failed!")
        
        
    def GenBsfInf (self):
        self.BaseAddressList = []
        self.BsfInfName = os.path.join(GenFdsGlobalVariable.FvDir, self.UiName + '.inf')
        BsfInf = open (self.BsfInfName, 'w+')
        BsfInf.writelines ("[COMPONENTS]" + T_CHAR_LF)

        for component in self.ComponentStatementList :
            BsfInf.writelines ("COMP_NAME"        + \
                               " = "              + \
                               component.CompName + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_LOC"        + \
                               " = "             + \
                               component.CompLoc + \
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
                               component.CompBin + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_SYM"        + \
                               " = "             + \
                               component.CompSym + \
                               T_CHAR_LF )
            BsfInf.writelines ("COMP_SIZE"        + \
                               " = "              + \
                               component.CompSize + \
                               T_CHAR_LF )
            BsfInf.writelines (T_CHAR_LF )
            
            if component[1] == 'F' :
                for fd in GenFdsGlobalVariable.FdfParser.profile.FdDict :
                    BaseAddress = fd.RegionList[0].Offset
                    Size = fd.RegionList[0].Size
            elif component[1] == 'S':
                for fd in GenFdsGlobalVariable.FdfParser.profile.FdDict :
                    BaseAddress = fd.RegionList[1].Offset
                    Size = fd.RegionList[1].Size
            self.BaseAddressList.append(BaseAddress, Size)
        BsfInf.close()
