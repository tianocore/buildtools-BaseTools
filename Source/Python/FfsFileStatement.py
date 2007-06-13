class FileStatements ("parent: Ffs") :
    def __init__(self):
        self.FvType = None
        self.NameGuild = None
        self.Fixed = None
        self.Alignment = None
        self.SectionList = None
        
    def GenFfs():
        for section in self.SectionList :
            SectionFiles = ' -i ' + section.GenSection()
        #
        # Prepare the parameter
        #
        if not (self.Fixed == None):
                Fixed = ' -x '
        else :
                Fixed = ''
        if not (self.CheckSum == None):
                CheckSum = ' -s '
        else :
                CheckSume = ''
        if not (self.Alignemnt == None):
                Alignment = ' -a ' + self.Alignment
        else :
                Alignment = ''
                
        FileType = ' - t ' + Ffs.ModuleTypeToFileType(Rule.ModuleType)
        FfsOutput = OutputPath + Rule.NameGuid + '.ffs'
        InputSection = ' -i ' + OutputPath + OutputFile
        GenFfsCmd = 'GenFfs ' + FileType + Fixed + CheckSum + Alignment + \
                     ' -o ' + FfsOutput + ' -g ' + self.NameGuild + SectionFiles
        #
        # Call GenSection
        #
        popen (genSectionCmd, mod= 'r')
        
        return FfsOutput
        

