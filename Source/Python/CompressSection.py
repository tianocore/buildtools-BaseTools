from Ffs import Ffs
import Section
import subprocess

class CompressSection (Section.Section) :
    CompTypeDict = {
        'PI_STD'     : ' -c PI_STD ',
        'NON_PI_STD' : ' -c NON_PI_STD '
    }
    
    def __init__(self):
        self.Alignment = None
        self.CompType = None
        self.SectionList = []
        

    def GenSection(self, OutputPath, ModuleName):
        #
        # Generate all section
        #
        SectFiles = ''
        for Sect in self.SectionList:
            SectFiles = SectFiles + \
                        ' '       + \
                        Sect.GenSection(OutputPath, ModuleName)

        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix['COMPRESS']
                     
        GenSectionCmd = 'GenSection -o '                              + \
                         OutputFile                                   + \
                         ' -s '                                       + \
                         Section.Section.SectionType['COMPRESS']      + \
                         self.CompTypeDict[self.CompType]             + \
                         SectFiles
        #
        # Call GenSection
        #
        print GenSectionCmd
        subprocess.Popen (GenSectionCmd).communicate()
        
        return OutputFile

        
