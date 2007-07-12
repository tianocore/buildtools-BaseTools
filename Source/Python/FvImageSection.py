import Section
import StringIO
from Ffs import Ffs
import subprocess
from GenFdsGlobalVariable import GenFdsGlobalVariable

class FvImageSection(Section.Section):
    def __init__(self):
        self.Aligenment = None
        self.Fv = None
        self.FvName = None
    def GenSection(self, OutputPath, ModuleName, KeyStringList, FfsInf = None):
        Buffer = StringIO.StringIO('')
        #
        # Generate Fv
        #
        if self.FvName != None:
            Fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.FvName)
            if self.Fv == None:
                self.Fv = Fv
            else:
                raise Exception("FvImageSection Failed! Can't describe the \
                                 FvImageSection both in FvUiName and \
                                 FvImageArg!")
                                 
        self.Fv.AddToBuffer(Buffer)
        
        FvFileName = OutputPath + \
                     ModuleName + \
                     '.fv'
        FvFile = open ( FvFileName, 'w+')
        FvFile.write(Buffer.getvalue())
        FvFile.close()
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get("FV_IMAGE")
                     
        GenSectionCmd = 'GenSec -o '                      + \
                         OutputFile                           + \
                         ' -s '                               + \
                         'EFI_SECTION_FIRMWARE_VOLUME_IMAGE ' + \
                         FvFileName
                         
        print GenSectionCmd
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
        return OutputFile, self.Aligenment
