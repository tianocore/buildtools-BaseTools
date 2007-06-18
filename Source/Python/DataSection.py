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
        
    def GenSection(self, OutputPath, ModuleName):
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get(self.SecType)
                     
        GenSectionCmd = 'GenSection -o '                                 + \
                         OutputFile                                      + \
                         ' -s '                                          + \
                         Section.Section.SectionType.get (self.SecType)  + \
                         ' '                                             + \
                         ' -i '                                          + \
                         GenFdsGlobalVariable.ExtendMarco(self.SectFileName)

        #
        # Call GenSection
        #
        GenSectionCmd = "GenSection -i c:\work\Sct\Tools\TestOutput\PeiMain.te \
                        -s EFI_SECTION_TE \
                        -o C:\work\Sct\Tools\TestOutput\\52C05B14-0B98-496c-BC3B-04B50211D680.te"
        print GenSectionCmd
        subprocess.Popen (GenSectionCmd).communicate()
        
        return OutputFile
