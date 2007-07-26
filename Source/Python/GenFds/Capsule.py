from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import CapsuleClassObject
import os
import subprocess

T_CHAR_LF = '\n'
class Capsule (CapsuleClassObject) :
    def __init__(self):
##        self.SpecName = None
##        self.UiCapsuleName = None
##        self.CreateFile = None
##        self.GroupIdNumber = None
###        self.DefineStatementList = None
###        self.SetSatementList = None
##        # DefineVarDict[var] = value
##        self.DefineVarDict = {}
##        # SetVarDict[var] = value
##        self.SetVarDict = {}
##        # TokensDict[var] = value
##        self.TokensDict = {}
##        self.CapsuleDataList = []
        CapsuleClassObject.__init__(self)
        self.BlockSize = None          # For GenFv
        self.BlockNum = None           # For GenFv
        
    def GenCapsule(self):
        capInfFile = self.GenCapInf()
        capInfFile.writelines("[files]" + T_CHAR_LF)
        
        for file in self.CapsuleDataList :
            fileName = file.GenCapsuleSubItem()
            capInfFile.writelines("EFI_FILE_NAME = " + \
                                   fileName      + \
                                   T_CHAR_LF)
        capInfFile.close()
        #
        # Call GenFv tool to generate capsule
        #
        CapOutputFile = os.path.join(GenFdsGlobalVariable.FvDir, self.UiCapsuleName)
        CapOutputFile = CapOutputFile + '.Cap'
        cmd = 'GenFv -i '          + \
               self.CapInfFileName + \
               ' -o '              + \
               CapOutputFile       + \
               ' -c '
        print cmd
        GenFdsGlobalVariable.CallExternalTool(cmd, "GefFv GenCapsule Failed!")

##
##    def GenFvInf():
##        self.InfFileName = os.path.join(GenFdsGlobalVariable.FvDir,
##                                   self.UiFvName + '.inf')
##        FvInfFile = open (self.InfFileName, 'w+')
##
##        self.FvInfFile.writelines("[options]" + T_CHAR_LF)
##        if self.BlockSize != None and self.BlockNum != None:
##            self.FvInfFile.writelines("EFI_BLOCK_SIZE = " + \
##                                      '0x%x' %self.BlockSize    + \
##                                      T_CHAR_LF)
##            self.FvInfFile.writelines("EFI_NUM_BLOCKS   = "  + \
##                                      ' 0x%x' %self.BlockNum    + \
##                                      T_CHAR_LF)
##
##        self.FvInfFile.writelines("[attributes]" + T_CHAR_LF)
##        return FvInfFile
        
    def GenCapInf(self):
        self.CapInfFileName = os.path.join(GenFdsGlobalVariable.FvDir,
                                   self.UiCapsuleName +  "_Cap" + '.inf')
        capInfFile = open (self.CapInfFileName , 'w+')
        
        capInfFile.writelines("[options]" + T_CHAR_LF)
        capInfFile.writelines("EFI_CAPSULE_VERSION = " + \
                              self.SpecName            + \
                              T_CHAR_LF)
                              
        for item in self.TokensDict.keys():
            capInfFile.writelines("EFI_"                    + \
                                  item                      + \
                                  ' = '                     + \
                                  self.TokensDict.get(item) + \
                                  T_CHAR_LF)

        return capInfFile
