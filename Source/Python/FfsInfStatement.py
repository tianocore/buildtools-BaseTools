import Rule
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Ffs
import subprocess
import sys
import Section

class FfsInfStatement(Ffs.Ffs):
    def __init__(self):
        Ffs.Ffs.__init__(self)
        self.Rule = None
        self.ver = None
        self.Ui = None
        self.InfFileName = None
        self.BuildNum = ''

    def __infParse__(self, InfFile):
        #
        # Get the InfClass object
        #
        InfFile = os.path.normpath (InfFile)
        Inf = GenFdsGlobalVariable.WorkSpace.InfDatabase[InfFile]
        #
        # Set Ffs BaseName, MdouleGuid, ModuleType, Version, OutputPath
        #
        self.BaseName = Inf.Defines.DefinesDictionary['BASE_NAME'][0]
        self.ModuleGuid = Inf.Defines.DefinesDictionary['FILE_GUID'][0]
        self.ModuleType = Inf.Defines.DefinesDictionary['MODULE_TYPE'][0]
        self.VersionString = Inf.Defines.DefinesDictionary['VERSION_STRING'][0]

        #
        # Set OutputPath = ${WorkSpace}\Build\Fv\Ffs\${ModuleGuid}+ ${MdouleName}\
        #

        self.OutputPath = GenFdsGlobalVariable.FfsDir + \
                          os.sep                      + \
                          self.ModuleGuid         + \
                          self.BaseName
                                  
        self.OutputPath = os.path.normpath(self.OutputPath)
        self.OutputPath = self.OutputPath + os.sep
        if not os.path.exists(self.OutputPath) :
            os.makedirs(self.OutputPath)

    def GenFfs(self):
        #
        # Parse Inf file get Module related information
        #
        self.__infParse__(self.InfFileName)
        #
        # Get the rule of how to generate Ffs file
        #
        Rule = self.__GetRule__()
                                                       
        FileType = Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]
        #
        # For the rule only has simpleFile
        #
        if (Rule.SimpleFile != None) :
            #
            # Prepare the parameter of GenSection
            #
            GenSecInputFile = self.__ExtendMarco__(Rule.SimpleFile.FileName)
            
            SectionType     = Rule.SimpleFile.SectionType

            GenSecOutputFile= self.__ExtendMarco__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType]
                            
            genSectionCmd = 'GenSection -o '                               + \
                             self.OutputPath                               + \
                             os.sep                                        + \
                             GenSecOutputFile                              + \
                             ' -s '                                        + \
                             Section.Section.SectionType[SectionType]      + \
                             ' '                                           + \
                             GenSecInputFile
            #
            # Call GenSection
            #
            print genSectionCmd
            subprocess.Popen (genSectionCmd).communicate()
            
            #
            # Prepare the parameter of GenFfs
            #
            FileType = ' - t ' + \
                       Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]
                       
            if not (Rule.Fixed == None):
                Fixed = ' -x '
            else :
                Fixed = ''
            if not (Rule.CheckSum == None):
                CheckSum = ' -s '
            else :
                CheckSume = ''
            if not (Rule.Alignment == None):
                Alignment = ' -a %d' %Rule.Alignment
            else :
                Alignment = ''
                
            FfsOutput = self.OutputPath                     + \
                        os.sep                              + \
                        self.__ExtendMarco__(Rule.NameGuid) + \
                        '.ffs'
                        
            print self.__ExtendMarco__(Rule.NameGuid)
            InputSection = ' -i '     + \
                           self.OutputPath + \
                           os.sep          + \
                           GenSecOutputFile

           
            GenFfsCmd = 'GenFfs '  + \
                         FileType  + \
                         Fixed     + \
                         CheckSum  + \
                         Alignment + \
                         ' -o '    + \
                         FfsOutput + \
                         ' -g '    + \
                         self.NameGuid + \
                         InputSection
            #
            # Call GenSection
            #
            print GenFfsCmd
            subprocess.Popen (GenFfsCmd).communicate()
            
            return FfsOutput
        #
        # For Rule has ComplexFile
        #
        else:
            SectFiles = ''
            for Sect in Rule.ComplexFile.SectionList:
                SectFiles = SectFiles    + \
                            ' -i '       + \
                            Sect.GenSection(self.OutputPath , self.ModuleGuid)
                
            FfsOutput = self.OutputPath + \
                        self.ModuleGuid + \
                        '.ffs'
                        
            print "###ComplexFile RUle"
            GenFfsCmd = 'GenFfs '                                    + \
                        '-t '                                        + \
                        Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]+ \
                        ' -g '                                       + \
                        ' -o '                                       + \
                        FfsOutput                                    + \
                        self.NameGuid                                + \
                        SectFiles
                        
            print GenFfsCmd
            subprocess.Popen(GenFfsCmd).communicate()
            return FfsOutput
                
    def __ExtendMarco__ (self, String):
        MarcoDict = {
            '$(INF_OUTPUT)'  : self.OutputPath,
            '$(MODULE_NAME)' : self.BaseName,
            '$(BUILD_NUMBER)': self.BuildNum,
            '$(INF_VERSION)' : self.VersionString,
            '$(NAME_GUID)'   : self.ModuleGuid
        }
        
        for Marco in MarcoDict.keys():
            if String.find(Marco) >= 0 :
                String = String.replace (Marco, MarcoDict[Marco])
        return String

    def __GetRule__ (self) :
        currentArch = 'IA32'
        
        RuleName = 'RULE'      + \
                   '.'         + \
                   currentArch + \
                   '.'         + \
                   self.ModuleType.upper()
        print "Want To Find Rule Name is : " + RuleName

        Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
        if Rule == None :
            RuleName = 'RULE'      + \
                       '.'         + \
                       'COMMON'    + \
                       '.'         + \
                       self.ModuleType.upper()
            Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
            if Rule == None :
                print 'Dont Find Related Rule, Using Default Rule !!!'
                return GenFdsGlobalVariable.DefaultRule
            
        return Rule
