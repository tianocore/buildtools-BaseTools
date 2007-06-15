import Section
class VerSection (Section.Section):
    def __init__(self):
        self.Alignment = None
        self.BuildNum = None
        self.StringData = None
        self.FileName = None
        
    def GenSection(OutputPath, ModuleName):
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + ModuleName + Ffs.SectionSuffix('VERSION')
        if not (self.BuildNum == None) :
            BuildNum = '-j ' + self.BuildNum;
        else :
            BuidNum = None
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s EFI_SECTION_VERSION ' \
                         + '-n ' + '\"' + self.StringData + '\"' + BuildNum
        #
        # Call GenSection
        #
        popen(GenSectionCmd, mod = 'r')
        
        return OutputFile
