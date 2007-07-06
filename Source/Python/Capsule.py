from GenFdsGlobalVariable import GenFdsGlobalVariable

T_CHAR_LF = '\n'
class Capsule :
    def __init__(self):
        self.SpecName = None
        self.UiCapsuleName = None
        self.CreateFile = None
        self.GroupIdNumber = None
#        self.DefineStatementList = None
#        self.SetSatementList = None
        # DefineVarDict[var] = value
        self.DefineVarDict = {}
        # SetVarDict[var] = value
        self.SetVarDict = {}
        # TokensDict[var] = value
        self.TokensDict = {}
        self.CapsuleDataList = []
        
        self.BlockSize = None          # For GenFv
        self.BlockNum = None           # For GenFv
        
    def GenCapsule(self):
        if self.CapsuleData.FfsList != None and self.CapsuleData.FfsList != []:
            self.GenFvInf()
            fvInfFile = self.GenFvInf()
            
            fvInfFile.writelines("[files]" + T_CHAR_LF)
            for FfsFile in self.FfsList :
                FileName = FfsFile.GenFfs()
                self.FvInfFile.writelines("EFI_FILE_NAME = " + \
                                           FileName          + \
                                           T_CHAR_LF)
            fvInfFile.close()
            #
            # Call GenFv tool
            #

            FvOutputFile = os.path.join(GenFdsGlobalVariable.FvDir, self.UiCapsuleName)
            FvOutputFile = FvOutputFile + '.Fv'
            cmd = 'GenFv -i '                 + \
                   self.InfFileName           + \
                   ' -o '                     + \
                   FvOutputFile
            #
            # Call GenFv Tools
            #
            print cmd
            PopenObject = subprocess.Popen(cmd)
            PopenObject.communicate()
            if PopenObject.returncode != 0 :
                raise Exception ("GenFv Failed!")
            self.GenCapInf(FvOutputFile)
        else:
            self.GenCapInf(GenFdsGlobalVariable.ReplaceWorkspaceMarco(CapsuleData.FvStatementsList[0]))

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
        PopenObject = subprocess.Popen(cmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0:
            raise Excetpion ("GefFv GenCapsule Failed!")


    def GenFvInf():
        self.InfFileName = os.path.join(GenFdsGlobalVariable.FvDir,
                                   self.UiFvName + '.inf')
        FvInfFile = open (self.InfFileName, 'w+')
        
        self.FvInfFile.writelines("[options]" + T_CHAR_LF)
        if self.BlockSize != None and self.BlockNum != None:
            self.FvInfFile.writelines("EFI_BLOCK_SIZE = " + \
                                      '0x%x' %self.BlockSize    + \
                                      T_CHAR_LF)
            self.FvInfFile.writelines("EFI_NUM_BLOCKS   = "  + \
                                      ' 0x%x' %self.BlockNum    + \
                                      T_CHAR_LF)
                                      
        self.FvInfFile.writelines("[attributes]" + T_CHAR_LF)
        return FvInfFile
        
    def GenCapInf(FvVolumeName):
        self.CapInfFileName = os.path.join(GenFdsGlobalVariable.FvDir,
                                   self.UiFvName +  "_Cap" + '.inf')
        capInfFile = open (self.CapInfFileName , 'w+')
        
        capInfFile.writelines("[options]" + T_CHAR_LF)
        for item in self.TokensDict.keys():
            capInfFile.writelines("EFI_"                    + \
                                  Item                      + \
                                  ' = '                     + \
                                  self.TokensDict.get(item) + \
                                  T_CHAR_LF)

        capInfFile.writelines("[attributes]" + T_CHAR_LF)
        capInfFile.writelines("[fvimage]" + T_CHAR_LF)
        capInfFile.writelines("EFI_FILE_NAME = " + \
                               FvVolumeName                 + \
                               T_CHAR_LF)
