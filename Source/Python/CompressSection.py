import Ffs
import Section
import subprocess

class CompressSection (Section.Section) :
    CompTypeDict = {
        'PI_STD'     : ' -c ',
        'NON_PI_STD' : ''
    }
    
    def __init__(self):
        self.Alignment = None
        self.CompType = None
        self.SectionList = []
        

    def GenSection(self, OutputPath, ModuleName):
        #
        # Generate all section
        #
        for Sect in self.SectionList:
            SectFile = ' ' + Sect.GenSection(OutputPath, ModuleName)

        OutputFile = OutputPath + \
                     ModuleName + \
                     FFs.SectionSuffix ('COMPRESS')
                     
        GenSectionCmd = 'GenSection -o '                  + \
                         OutputFile                       + \
                         ' -s '                           + \
                         Section.SectionType('COMPRESS')  + \
                         self.CompTypeDict(self.CompType) + \
                         SectFile
        #
        # Call GenSection
        #
        subprocess.Popen (GenSectionCmd).communicate()
        
        return OutputFile

        
