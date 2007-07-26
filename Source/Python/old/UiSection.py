import Section
from Ffs import Ffs
import subprocess
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
class UiSection (Section.Section):
    def __init__(self):
        self.Alignment = None
        self.StringData = None
        self.FileName = None


    def GenSection(self, OutputPath, ModuleName, KeyStringList, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            self.StringData = FfsInf.__ExtendMarco__(self.StringData)
            self.FileName = FfsInf.__ExtendMarco__(self.FileName)
            
        OutputFile = os.path.join(OutputPath, ModuleName + Ffs.SectionSuffix.get('UI'))
                     
        if self.StringData != None :
            NameString = self.StringData
        elif self.FileName != None:
            f = open(self.FileName, 'r')
            NameString = f.read()
            f.close()
        else:
            NameString = ''
            
            
        GenSectionCmd = 'GenSec -o '                       + \
                         OutputFile                        + \
                         ' -s EFI_SECTION_USER_INTERFACE ' + \
                         '-n '                             + \
                          '\"'                             + \
                          NameString                       + \
                          '\"'
        #
        # Call GenSection
        #
        print GenSectionCmd
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd,"GenSection Failed!")
        return OutputFile, self.Alignment
