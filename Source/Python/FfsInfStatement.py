import Rule
import os
import GenFdsGlobalVariable
import Ffs
import subprocess
class FfsInfStatement(Ffs.Ffs):
    def __init__(self):
        Ffs.Ffs.__init__(self)
        self.Rule = None
        self.ver = None
        self.Ui = None
        self.InfFileName = None
        #self.__infParse__(self.InfFileName)

    def __infParse__(self, InfFile):
        Inf = open (InfFile, mode = 'r')
        self.Version = ''
        self.Guid = ''
        self.Name = ''
        self.ModuleType = ''


    def GenFfs(self):
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
            
            OutPutPath    = GenFdsGlobalVariable.FfsDir + \
                            os.sep                      + \
                            Rule.NameGuid               + \
                            os.sep
                            
            OutputFile    = Rule.NameGuid + \
                            Ffs.SectionSuffix(SectionType)
                            
            genSectionCmd = 'GenSect -o ' + \
                             OutputPath   + \
                             OutputFile   + \
                             ' -s '       + \
                             SectionType  + \
                             ' '          + \
                             InputFile
            #
            # Call GenSection
            #
            subprocess.Popen (genSectionCmd).communicate()
            
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
                
            FfsOutput = OutputPath    + \
                        Rule.NameGuid + \
                        '.ffs'
            
            InputSection = ' -i '     + \
                           OutputPath + \
                           OutputFile
                           
            GenFfsCmd = 'GenFfs '  + \
                         FileType  + \
                         Fixed     + \
                         CheckSum  + \
                         Alignment + \
                         ' -o '    + \
                         FfsOutput + \
                         ' -g '    + \
                         self.Guid + \
                         InputSection
            #
            # Call GenSection
            #
            subprocess.Popen (GenFfsCmd).communicate()
            
            return FfsOutput
        #
        # For Rule has ComplexFile
        #
        else:
            OutPutPath = os.path.join(OutputDir, os.path.dirname(self.InfFileName), 'OUTPUT')
            for Sect in self.Rule.CompliexFile.SectionList:
                SectFiles = ' -i ' + Sect.GenSection(OutputPath, self.Guid)
                
            FfsOutput = OutputPath + \
                        self.Guid +  \
                        '.ffs'
                        
            GenFfsCmd = 'GenFfs '                                + \
                        '-t '                                    + \
                        FFs.ModuleTypeToFileType(self.ModuleType)+ \
                        ' -g '                                   + \
                        self.Guid                                + \
                        SectionFiles
                        
            subprocess.Popen(GenFfsCmd).communicate()
            return FfsOutput
                

        
