import Ffs
import Section
class CompressSection (Section.Sction) :
    self.CompTypeDict = {
        'PI_STD'     : ' -c ',
        'NON_PI_STD' : ''
    }
    
    def __init__(self):
        self.Alignment = None
        self.CompType = None
        self.SectList = None
        

    def GenSection(OutputPath, ModuleName):
        #
        # Generate all section
        #
        for Sect in self.SectList:
            SectFile = ' ' + Sect.GenSection(OutputPath, ModuleName)

        OutputFile = OutputPath + ModuleName + FFs.SectionSuffix ('COMPRESS')
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s ' + \
                        Section.SectionType('COMPRESS') + \
                        self.CompTypeDict(self.CompType) + SectFile
        #
        # Call GenSection
        #
        popen (GenSectionCmd, mod = 'r')
        
        return OutputFile

        
