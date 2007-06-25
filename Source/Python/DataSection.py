import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs

class DataSection (Section.Section):
    def __init__(self):
        self.Alignemnt = None
        self.SecType = None
        self.SectFileName = None
        self.SectionList = []
        
    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignemnt)
            self.SecType = FfsInf.__ExtendMarco__(self.SecType)
            self.SectFileName = FfsInf.__ExtendMarco__(self.SectFileName)

        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get(self.SecType)
                     
        GenSectionCmd = 'GenSection -o '                                 + \
                         OutputFile                                      + \
                         ' -s '                                          + \
                         Section.Section.SectionType.get (self.SecType)  + \
                         ' '                                             + \
                         GenFdsGlobalVariable.ExtendMarco(self.SectFileName)

        #
        # Call GenSection
        #
        
        print GenSectionCmd
        subprocess.Popen (GenSectionCmd).communicate()
        
        return OutputFile
