import Rule
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Ffs
import subprocess
import sys
import Section
import RuleSimpleFile
import RuleComplexFile
from String import *

class FfsInfStatement(Ffs.Ffs):
    def __init__(self):
        Ffs.Ffs.__init__(self)
        self.Rule = None
        self.ver = None
        self.Ui = None
        self.InfFileName = None
        self.BuildNum = ''
        self.KeyStringList = []

    def __infParse__(self):
        #
        # Get the InfClass object
        #
##        for item in GenFdsGlobalVariable.WorkSpace.InfDatabase:
##            print item
        self.InfFileName = os.path.normpath(self.InfFileName)
        Inf = GenFdsGlobalVariable.WorkSpace.InfDatabase[self.InfFileName]
        #
        # Set Ffs BaseName, MdouleGuid, ModuleType, Version, OutputPath
        #
        self.BaseName = Inf.Defines.DefinesDictionary['BASE_NAME'][0]
        self.ModuleGuid = Inf.Defines.DefinesDictionary['FILE_GUID'][0]
        self.ModuleType = Inf.Defines.DefinesDictionary['MODULE_TYPE'][0]
        self.VersionString = Inf.Defines.DefinesDictionary['VERSION_STRING'][0]
        print "BaseName : %s" %self.BaseName
        print "ModuleGuid : %s" %self.ModuleGuid
        print "ModuleType : %s" %self.ModuleType
        print "VersionString : %s" %self.VersionString
        print "InfFileName :" , self.InfFileName
        #
        # Set OutputPath = ${WorkSpace}\Build\Fv\Ffs\${ModuleGuid}+ ${MdouleName}\
        #

        self.OutputPath = os.path.join(GenFdsGlobalVariable.FfsDir, \
                                       self.ModuleGuid + self.BaseName)
        self.OutputPath = os.path.normcase(self.OutputPath)
        if not os.path.exists(self.OutputPath) :
            os.makedirs(self.OutputPath)
            
        self.InfOutputPath = self.__GetEFIOutPutPath__()
        print "ModuelEFIPath: " ,self.InfOutputPath
                             
    def GenFfs(self):
        #
        # Parse Inf file get Module related information
        #
        print " Begion parsing INf file : %s" %self.InfFileName
        
        """ Replace $(WORKSPACE) to None!"""
        self.InfFileName = self.InfFileName.replace('$(WORKSPACE)', '')
        if self.InfFileName[0] == '\\' or self.InfFileName[0] == '/' :
            self.InfFileName = self.InfFileName[1:]
        
 
        self.__infParse__()
        #
        # Get the rule of how to generate Ffs file
        #
        Rule = self.__GetRule__()
                                                       
        FileType = Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]
        #
        # For the rule only has simpleFile
        #
        if isinstance (Rule, RuleSimpleFile.RuleSimpleFile) :
            SectionOutput = self.__GenSimpleFileSection__(Rule)
            FfsOutput = self.__GenSimpleFileFfs__(Rule, SectionOutput)
            return FfsOutput
        #
        # For Rule has ComplexFile
        #
        elif isinstance(Rule, RuleComplexFile.RuleComplexFile):
           
            InputSectList = self.__GenComplexFileSection__(Rule)
            FfsOutput = self.__GenComplexFileFfs__(Rule, InputSectList)
            
            return FfsOutput
                
    def __ExtendMarco__ (self, String):
        MarcoDict = {
            '$(INF_OUTPUT)'  : self.InfOutputPath,
            '$(MODULE_NAME)' : self.BaseName,
            '$(BUILD_NUMBER)': self.BuildNum,
            '$(INF_VERSION)' : self.VersionString,
            '$(NAMED_GUID)'  : self.ModuleGuid,
            '$(WORKSPACE)'   : GenFdsGlobalVariable.WorkSpaceDir
        }
        if String == None :
            return None
        for Marco in MarcoDict.keys():
            if String.find(Marco) >= 0 :
                String = String.replace (Marco, MarcoDict[Marco])
        return String

    def __GetRule__ (self) :
        currentArch = 'IA32'
        #for item in GenFdsGlobalVariable.FdfParser.profile.RuleDict :
        #    print item
        RuleName = 'RULE'      + \
                   '.'         + \
                   currentArch + \
                   '.'         + \
                   self.ModuleType.upper()
        
        Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
        if Rule == None :
            RuleName = 'RULE'      + \
                       '.'         + \
                       'COMMON'    + \
                       '.'         + \
                       self.ModuleType.upper()
            print "Want To Find Rule Name is : " + RuleName
            Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
            if Rule == None :
                print 'Dont Find Related Rule, Using Default Rule !!!'
                if GenFdsGlobalVariable.DefaultRule == None:
                    raise Exception ("Default Rule doesn't exist!!")
                return GenFdsGlobalVariable.DefaultRule
        print "Want To Find Rule Name is : " + RuleName
        return Rule
    
    def __GetEFIOutPutPath__(self):
        Flag = False
        Arch = ''
        OutputPath = ''
        (ModulePath, fileName) = os.path.split(self.InfFileName)
        index = fileName.find('.')
        fileName = fileName[0:index]
        Platform = os.path.normpath(GenFdsGlobalVariable.WorkSpace.TargetTxt.TargetTxtDictionary["ACTIVE_PLATFORM"][0])
        targetArchList = GenFdsGlobalVariable.WorkSpace.TargetTxt.TargetTxtDictionary["TARGET_ARCH"]
        if len(targetArchList) == 0:
            myArchList = GenFdsGlobalVariable.WorkSpace.SupArchList
        else:
            myArchList = set(GenFdsGlobalVariable.WorkSpace.SupArchList) & set(targetArchList)
            print "Valid target architecture(s) is", " ".join(myArchList)

        if len(myArchList) > 1 :
            for Key in self.KeyStringList:
                Target, Tag, Arch = Key.split('_')
                ArchList = set (ArchList) & Arch
                if ArchList == 1:
                    Arch = ArchList[0]
                else:
                    raise Exception("Module %s has too many bulid Arch !" %self.InfFileNames)
        elif len(myArchList) == 1 :
            Arch = myArchList.pop()
            
        OutputPath = os.path.join(GenFdsGlobalVariable.OuputDir,
                                  Arch ,
                                  ModulePath,
                                  fileName,
                                  'OUTPUT'
                                  )
        OutputPath = os.path.normcase(OutputPath)
        return OutputPath
        
    def __GenSimpleFileSection__(self, Rule):
        #
        # Prepare the parameter of GenSection
        #
        GenSecInputFile = self.__ExtendMarco__(Rule.FileName)

        SectionType     = Rule.SectionType

        GenSecOutputFile= self.__ExtendMarco__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType]
                              
        OutputFile = os.path.join(self.OutputPath, GenSecOutputFile)
        
        genSectionCmd = 'GenSec -o '                                   + \
                         OutputFile                                    + \
                         ' -s '                                        + \
                         Section.Section.SectionType[SectionType]      + \
                         ' '                                           + \
                         GenSecInputFile
        #
        # Call GenSection
        #
        print genSectionCmd
        GenFdsGlobalVariable.CallExternalTool(genSectionCmd, "Gensection Failed!")
        return OutputFile
    
    def __GenSimpleFileFfs__(self, Rule, InputFile):
        #
        # Prepare the parameter of GenFfs
        #
        (FileType,Fixed, CheckSum, Alignment) = self.__GetGenFfsComParamter__(Rule)
        
        FfsOutput = self.OutputPath                     + \
                    os.sep                              + \
                    self.__ExtendMarco__(Rule.NameGuid) + \
                    '.ffs'

        print self.__ExtendMarco__(Rule.NameGuid)
        InputSection = ' -i '     + \
                       InputFile


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
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed!")
        return FfsOutput
    
    def __GenComplexFileSection__(self, Rule):
        SectFiles = ''
        for Sect in Rule.SectionList:
           print 'GenSection: %s %s :' %(self.OutputPath ,self.ModuleGuid)
           secName = ''
           secName, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, self.KeyStringList, self)
           if secName != '':
               SectFiles = SectFiles    + \
                           ' -i '       + \
                           secName
               if Align != None:
                   SectFiles = SectFiles + \
                               ' -n '    + \
                               Align
        return SectFiles

    def __GenComplexFileFfs__(self, Rule, InputFile):
        
        (FileType,Fixed, CheckSum, Alignment) = self.__GetGenFfsComParamter__(Rule)
        
        FfsOutput = os.path.join( self.OutputPath, self.ModuleGuid + '.ffs')
        GenFfsCmd = 'GenFfs '                                     + \
                     Fixed                                        + \
                     CheckSum                                     + \
                     Alignment                                    + \
                     FileType                                     + \
                     ' -g '                                       + \
                     self.ModuleGuid                              + \
                     ' -o '                                       + \
                     FfsOutput                                    + \
                     InputFile
                     
        print GenFfsCmd
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed !")
        return FfsOutput

    def __GetGenFfsComParamter__(self, Rule):
        FileType = ' -t ' + \
                   Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]
        print "Rule.Fixed = ", Rule.Fixed
        if Rule.Fixed != False:
            Fixed = ' -x '
        else :
            Fixed = ''
        if Rule.CheckSum != False:
            CheckSum = ' -s '
        else :
            CheckSume = ''
            
        if Rule.Alignment != None and Rule.Alignment != '':
            Alignment = ' -a %s' %Rule.Alignment
        else :
            Alignment = ''
            
        return FileType, Fixed, CheckSum, Alignment
