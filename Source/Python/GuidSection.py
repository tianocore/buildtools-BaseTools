import Section
class GuidSection(Section.Section) :
    def __init__(self):
        self.Alignment = None
        self.NameGuid = None
        self.SectList = None
        
    def GenSection(self, OutputPath, ModuleName):
        #
        # Generate all section
        #
        for Sect in self.SectList:
            SectFile = ' ' + Sect.GenSection(OutputPath, ModuleName)

        OutputFile = OutputPath + ModuleName + FFs.SectionSuffix ('GUIDED')
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s ' + \
                        self.CompTypeDict(self.CompType) + SectFile
        #
        # Call GenSection
        #
        popen (GenSectionCmd, mod = 'r')
        
        #
        # Use external tool process the Output
        #
        InputFile = OutputFile
        TempFile = OutputPath + ModuleName + '.tmp'
        ExternalToolCmd = Section.ToolGuid(self.NameGuid) + ' -o ' + TempFile \
                          + InputFile

        #
        # Call external tool
        #
        popen (GenSectnionCmd, mod = 'r')
        #
        # Call Gensection Add Secntion Header
        #
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s ' + \
                        Section.SectionType('GUIDED') + ' ' + TempFile
                        
        return OutputFile
