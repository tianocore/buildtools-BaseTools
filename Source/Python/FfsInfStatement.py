import Rule
class FfsInfStatement :
    def __init__(self):
        self.Rule = None
        self.ver = None
        self.Ui = None
        self.InfFileName = None
        
    def GenFfs():
        Rule = FdsParse.RuleDict(Self.Rule)
        FileType = Ffs.ModuleTypeToFileType(self.Rule.ModuleType)
        #
        # For the rule only has simpleFile
        #
        if not (Rule.SimpleFile == None) :
            #
            # Prepare the parameter of GenSection
            #
            InputFile     = GenFdsGlobbalVariable.ExtendMarco(Rule.SimpleFile.FileName)
            SectionType   = Rule.SimpleFile.SectionType
            OutPutPath    = GenFdsGlobalVariable.FfsDir + os.sep + Rule.NameGuid \
                            + os.sep
            OutputFile    = Rule.NameGuid + Ffs.SectionSuffix(SectionType)
            genSectionCmd = 'GenSect -o ' + OutputPath + OutputFile + ' -s ' + \
                             SectionType + ' ' + InputFile
            #
            # Call GenSection
            #
            popen (genSectionCmd, mod ='r')
            
            #
            # Prepare the parameter of GenFfs
            #
            FileType = ' - t ' + Ffs.ModuleTypeToFileType(Rule.ModuleType)
            if not (Rule.SimpleFile.Fixed == None):
                Fixed = ' -x '
            else :
                Fixed = ''
            if not (Rule.SimpleFile.CheckSum == None):
                CheckSum = ' -s '
            else :
                CheckSume = ''
            if not (Rule.SimpleFile.Alignemnt == None):
                Alignment = ' -a ' + Rule.SimpleFile.Alignment
            else :
                Alignment = ''
                
            FfsOutput = '-o ' + OutputPath + Rule.NameGuid + '.ffs'
            InputSection = ' -i ' + OutputPath + OutputFile
            GenFfsCmd = 'GenFfs ' + FileType + Fixed + CheckSum + Alignment + \
                         FfsOutput + InputSection
            #
            # Call GenSection
            #
            popen (genSectionCmd, mod= 'r')
            
            return OutputPaht + Rule.NameGuid + '.ffs'
        
