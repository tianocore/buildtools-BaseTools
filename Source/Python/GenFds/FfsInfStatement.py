import Rule
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Ffs
import subprocess
import sys
import Section
import RuleSimpleFile
import RuleComplexFile
from CommonDataClass.FdfClassObject import FfsInfStatementClassObject
from Common.String import *

#from String import *

class FfsInfStatement(FfsInfStatementClassObject):
    def __init__(self):
        FfsInfStatementClassObject.__init__(self)

    def __infParse__(self):
        #
        # Get the InfClass object
        #
##        for item in GenFdsGlobalVariable.WorkSpace.InfDatabase:
##            print item
        self.InfFileName = NormPath(self.InfFileName)
        Inf = GenFdsGlobalVariable.WorkSpace.InfDatabase[self.InfFileName]
        #
        # Set Ffs BaseName, MdouleGuid, ModuleType, Version, OutputPath
        #
        self.BaseName = Inf.Defines.DefinesDictionary['BASE_NAME'][0]
        self.ModuleGuid = Inf.Defines.DefinesDictionary['FILE_GUID'][0]
        self.ModuleType = Inf.Defines.DefinesDictionary['MODULE_TYPE'][0]
        self.VersionString = Inf.Defines.DefinesDictionary['VERSION_STRING'][0]
        GenFdsGlobalVariable.VerboseLogger( "BaseName : %s" %self.BaseName)
        GenFdsGlobalVariable.VerboseLogger("ModuleGuid : %s" %self.ModuleGuid)
        GenFdsGlobalVariable.VerboseLogger("ModuleType : %s" %self.ModuleType)
        GenFdsGlobalVariable.VerboseLogger("VersionString : %s" %self.VersionString)
        GenFdsGlobalVariable.VerboseLogger("InfFileName :%s"  %self.InfFileName)
        
        #
        # Set OutputPath = ${WorkSpace}\Build\Fv\Ffs\${ModuleGuid}+ ${MdouleName}\
        #

        self.OutputPath = os.path.join(GenFdsGlobalVariable.FfsDir, \
                                       self.ModuleGuid + self.BaseName)
        if not os.path.exists(self.OutputPath) :
            os.makedirs(self.OutputPath)
            
        self.InfOutputPath = self.__GetEFIOutPutPath__()
        GenFdsGlobalVariable.VerboseLogger( "ModuelEFIPath: " + self.InfOutputPath)
                             
    def GenFfs(self):
        #
        # Parse Inf file get Module related information
        #
        GenFdsGlobalVariable.VerboseLogger( " Begion parsing INf file : %s" %self.InfFileName)
        
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
        currentArchList = self.__GetCurrentArch__()
        
        #for item in GenFdsGlobalVariable.FdfParser.profile.RuleDict :
        #    print item
        for currentArch in currentArchList:
            RuleName = 'RULE'              + \
                       '.'                 + \
                       currentArch.upper() + \
                       '.'                 + \
                       self.ModuleType.upper()
            if self.Rule != None:
                RuleName = RuleName + \
                           '.'      + \
                           self.Rule.upper()
                           
            Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
            if Rule != None:
                GenFdsGlobalVariable.VerboseLogger ("Want To Find Rule Name is : " + RuleName)
                return Rule
            
        RuleName = 'RULE'      + \
                   '.'         + \
                   'COMMON'    + \
                   '.'         + \
                   self.ModuleType.upper()
        if self.Rule != None:
            RuleName = RuleName + \
                       '.'      + \
                       self.Rule.upper()
                       
        Rule = GenFdsGlobalVariable.FdfParser.profile.RuleDict.get(RuleName)
        if Rule != None:
            GenFdsGlobalVariable.VerboseLogger ("Want To Find Rule Name is : " + RuleName)
            return Rule

        if Rule == None :
            GenFdsGlobalVariable.VerboseLogger ('Dont Find Related Rule, Using Default Rule !!!')
            if GenFdsGlobalVariable.DefaultRule == None:
                raise Exception ("Default Rule doesn't exist!!")
            else:
                return GenFdsGlobalVariable.DefaultRule

    def __GetCurrentArch__(self):
        targetArchList = GenFdsGlobalVariable.ArchList
        if len(targetArchList) == 0:
            targetArchList = GenFdsGlobalVariable.WorkSpace.SupArchList
        else:
            targetArchList = set(GenFdsGlobalVariable.WorkSpace.SupArchList) & set(targetArchList)
            
        #activePlatform = GenFdsGlobalVariable.WorkSpace.TargetTxt.TargetTxtDictionary.get('ACTIVE_PLATFORM')[0]
        dscArchList = []
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IA32').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if self.InfFileName in PlatformDataBase.Modules:
                dscArchList.append ('IA32')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('X64').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if self.InfFileName in PlatformDataBase.Modules:
                dscArchList.append ('X64')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IPF').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if PlatformDataBase != None:
            if self.InfFileName in (PlatformDataBase.Modules):
                dscArchList.append ('IPF')

        curArchList = set (targetArchList) & set (dscArchList)
        GenFdsGlobalVariable.VerboseLogger ("Valid target architecture(s) is : " + " ".join(curArchList))
        return curArchList
    
    def __GetEFIOutPutPath__(self):
        Arch = ''
        OutputPath = ''
        (ModulePath, fileName) = os.path.split(self.InfFileName)
        index = fileName.find('.')
        fileName = fileName[0:index]

        curArchList = self.__GetCurrentArch__()
        if len(curArchList) > 1 :
            for Key in self.KeyStringList:
                Target, Tag, Arch = Key.split('_')
                ArchList = set (ArchList) & Arch
            if len(ArchList) == 1:
                Arch = ArchList[0]
            elif len(ArchList) > 1:
                raise Exception("Module %s has too many bulid Arch !" %self.InfFileNames)
            else:
                raise Exception("Don't find legal Arch in Module %s !" %self.InfFileNames)
        elif len(curArchList) == 1 :
            Arch = curArchList.pop()
            
        OutputPath = os.path.join(GenFdsGlobalVariable.OuputDir,
                                  Arch ,
                                  ModulePath,
                                  fileName,
                                  'OUTPUT'
                                  )
                                  
        OutputPath = os.path.realpath(OutputPath)
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

        GenFdsGlobalVariable.VerboseLogger(self.__ExtendMarco__(Rule.NameGuid))
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
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed!")
        return FfsOutput
    
    def __GenComplexFileSection__(self, Rule):
        SectFiles = ''
        Index = 0
        for Sect in Rule.SectionList:
           Index = Index + 1
           SecIndex = '%d' %Index
           secName = ''
           if Rule.KeyStringList != []:
               secName, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, Rule.KeyStringList, self)
           else :
               secName, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, self.KeyStringList, self)
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
                     
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed !")
        return FfsOutput

    def __GetGenFfsComParamter__(self, Rule):
        FileType = ' -t ' + \
                   Ffs.Ffs.FvTypeToFileType[Rule.FvType]
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