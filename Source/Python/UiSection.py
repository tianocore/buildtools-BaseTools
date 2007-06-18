import Section
from Ffs import Ffs
import subprocess

class UiSection (Section.Section):
    def __init__(self):
        self.Alignment = None
        self.StringData = None
        self.FileName = None


    def GenSection(self, OutputPath, ModuleName):
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get('UI')
                     
        if self.StringData != None :
            NameString = self.StringData
        elif self.FileName != None:
            f = open(self.FileName, 'r')
            NameString = f.read()
            f.close()
        else:
            NameString = ''
            
            
        GenSectionCmd = 'GenSection -o ' +                   \
                         OutputFile +                        \
                         ' -s EFI_SECTION_USER_INTERFACE ' + \
                         '-n '                             + \
                          '\"'                             + \
                          NameString                       + \
                          '\"'
        #
        # Call GenSection
        #
        print GenSectionCmd
        subprocess.Popen(GenSectionCmd).communicate()

        return OutputFile
