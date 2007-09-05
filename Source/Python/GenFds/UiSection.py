import Section
from Ffs import Ffs
import subprocess
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import UiSectionClassObject

class UiSection (UiSectionClassObject):
    def __init__(self):
        UiSectionClassObject.__init__(self)

    def GenSection(self, OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            self.StringData = FfsInf.__ExtendMarco__(self.StringData)
            self.FileName = FfsInf.__ExtendMarco__(self.FileName)
            
        OutputFile = os.path.join(OutputPath, ModuleName + 'SEC' + SecNum + Ffs.SectionSuffix.get('UI'))
                     
        if self.StringData != None :
            NameString = self.StringData
        elif self.FileName != None:
            file = GenFdsGlobalVariable.ReplaceWorkspaceMarco(self.FileName)
            f = open(file, 'r')
            NameString = f.read()
            NameString = '\"' + NameString + "\""
            f.close()
        else:
            NameString = ''
            
            
        GenSectionCmd = 'GenSec -o '                       + \
                         OutputFile                        + \
                         ' -s EFI_SECTION_USER_INTERFACE ' + \
                         '-n '                             + \
                          NameString                       
        #
        # Call GenSection
        #
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd,"GenSection Failed!")
        OutputFileList = []
        OutputFileList.append(OutputFile)
        return OutputFileList, self.Alignment
