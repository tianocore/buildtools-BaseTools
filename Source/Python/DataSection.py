class DataSection :
    def __init__(self):
        self.Alignemnt = None
        self.SecType = None
        self.SectFileName = None
        self.SectionList = None
        
    def GenSection(self, OutputPath, ModuleName):
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + ModuleName + Ffs.SectionSuffix(self.SecType)
        GenSectionCmd = 'GenSection - o ' + OutputFile + ' -s ' + \
                         Section.SectionType (self.SecType) + ' ' + \
                         GenFdsGlobalVariable.ExtendMarco(self.SectFileName)

        #
        # Call GenSection
        #
        popen (GenSectionCmd, mod = 'r')
        
        return OutputFile
