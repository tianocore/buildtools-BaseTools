import Section
import subprocess
from Ffs import Ffs
class GuidSection(Section.Section) :
    def __init__(self):
        self.Alignment = None
        self.NameGuid = None
        self.SectionList = []
        
    def GenSection(self, OutputPath, ModuleName):
        #
        # Generate all section
        #
        SectFile = ''
        for Sect in self.SectionList:
            SectFile = SectFile + \
                       '  '     + \
                       Sect.GenSection(OutputPath, ModuleName)

        OutputFile = OutputPath + \
                     ModuleName + \
                     FFs.SectionSuffix.get('GUIDED')
                     
        GenSectionCmd = 'GenSection -o '                  + \
                         OutputFile                       + \
                         ' -s '                           + \
                         self.CompTypeDict(self.CompType) + \
                         SectFile
        #
        # Call GenSection
        #
        subprocess.Popen (GenSectionCmd).communicate()
        
        #
        # Use external tool process the Output
        #
        InputFile = OutputFile
        TempFile = OutputPath + \
                   ModuleName + \
                   '.tmp'
                   
        ExternalToolCmd = Section.ToolGuid(self.NameGuid) + \
                          ' -o ' +                          \
                          TempFile +                        \
                          InputFile

        #
        # Call external tool
        #
        subprocess.Popen (GenSectnionCmd).communicate()
        #
        # Call Gensection Add Secntion Header
        #
        GenSectionCmd = 'GenSection -o '                + \
                         OutputFile                     + \
                         ' -s '                         + \
                         Section.SectionType('GUIDED')  + \
                         ' '                            + \
                         TempFile
                        
        subprocess.Popen(GenSectionCmd).communicate()
        return OutputFile
