from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import CapsuleClassObject
import os
import subprocess

T_CHAR_LF = '\n'
class Capsule (CapsuleClassObject) :
    def __init__(self):
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
        GenFdsGlobalVariable.CallExternalTool(cmd, "GefFv GenCapsule Failed!")
        GenFdsGlobalVariable.SharpCounter = 0

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
