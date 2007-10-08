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
        self.TargetOverrideList = []

    def __infParse__(self, Dict = {}):
        self.CurrentArch = self.GetCurrentArch()
        #
        # Get the InfClass object
        #
##        for item in GenFdsGlobalVariable.WorkSpace.InfDatabase:
##            print item
        self.InfFileName = NormPath(self.InfFileName)
        self.InfFileName = GenFdsGlobalVariable.MacroExtend(self.InfFileName, Dict)
        (self.SourceDir, InfName) = os.path.split(self.InfFileName)
        if self.CurrentArch != None and self.InfFileName in GenFdsGlobalVariable.WorkSpace.Build[self.CurrentArch].ModuleDatabase.keys():
            
            Inf = GenFdsGlobalVariable.WorkSpace.Build[self.CurrentArch].ModuleDatabase[self.InfFileName]
            #
            # Set Ffs BaseName, MdouleGuid, ModuleType, Version, OutputPath
            #
            self.BaseName = Inf.BaseName
            self.ModuleGuid = Inf.Guid
            self.ModuleType = Inf.ModuleType
            self.VersionString = Inf.Version
            self.BinFileList = Inf.Binaries
        
        elif self.InfFileName in GenFdsGlobalVariable.WorkSpace.InfDatabase.keys():
            Inf = GenFdsGlobalVariable.WorkSpace.InfDatabase[self.InfFileName]
            self.BaseName = Inf.Module.Header.Name
            self.ModuleGuid = Inf.Module.Header.Guid
            self.ModuleType = Inf.Module.Header.ModuleType
            self.VersionString = Inf.Module.Header.Version
            self.BinFileList = Inf.Module.Binaries
            if self.BinFileList == []:
                raise Exception ("INF %s specified in FDF could not be found in build ARCH %s!" % (self.InfFileName, GenFdsGlobalVariable.ArchList))
                sys.exit(1)
        
        else:
            raise Exception ("INF %s specified in FDF could not be found in database!" % self.InfFileName)
            sys.exit(1)
        
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
            
        self.EfiOutputPath = self.__GetEFIOutPutPath__()
        GenFdsGlobalVariable.VerboseLogger( "ModuelEFIPath: " + self.EfiOutputPath)
                             
    def GenFfs(self, Dict = {}):
        #
        # Parse Inf file get Module related information
        #
        GenFdsGlobalVariable.VerboseLogger( " Begine parsing INf file : %s" %self.InfFileName)
        
        """ Replace $(WORKSPACE) to None!"""
        self.InfFileName = self.InfFileName.replace('$(WORKSPACE)', '')
        if self.InfFileName[0] == '\\' or self.InfFileName[0] == '/' :
            self.InfFileName = self.InfFileName[1:]
        
 
        self.__infParse__(Dict)
        #
        # Get the rule of how to generate Ffs file
        #
        Rule = self.__GetRule__()
        GenFdsGlobalVariable.VerboseLogger( "Packing binaries from INf file : %s" %self.InfFileName)
        #FileType = Ffs.Ffs.ModuleTypeToFileType[Rule.ModuleType]
        #
        # For the rule only has simpleFile
        #
        if isinstance (Rule, RuleSimpleFile.RuleSimpleFile) :
            SectionOutputList = self.__GenSimpleFileSection__(Rule)
            FfsOutput = self.__GenSimpleFileFfs__(Rule, SectionOutputList)
            return FfsOutput
        #
        # For Rule has ComplexFile
        #
        elif isinstance(Rule, RuleComplexFile.RuleComplexFile):
           
            InputSectList = self.__GenComplexFileSection__(Rule)
            FfsOutput = self.__GenComplexFileFfs__(Rule, InputSectList)
            
            return FfsOutput
                
    def __ExtendMarco__ (self, String):
        MacroDict = {
            '$(INF_OUTPUT)'  : self.EfiOutputPath,
            '$(MODULE_NAME)' : self.BaseName,
            '$(BUILD_NUMBER)': self.BuildNum,
            '$(INF_VERSION)' : self.VersionString,
            '$(NAMED_GUID)'  : self.ModuleGuid        
        }
        String = GenFdsGlobalVariable.MacroExtend(String, MacroDict)
        return String

    def __GetRule__ (self) :
        currentArchList = self.CurrentArch
        if currentArchList == None:
            currentArchList = ['common']
        
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

    def __GetPlatformArchList__(self):
        targetArchList = GenFdsGlobalVariable.ArchList
        if len(targetArchList) == 0:
            targetArchList = GenFdsGlobalVariable.WorkSpace.SupArchList
        else:
            targetArchList = set(GenFdsGlobalVariable.WorkSpace.SupArchList) & set(targetArchList)
            
        InfFileKey = os.path.normpath(self.InfFileName)
        dscArchList = []
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IA32').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if InfFileKey in PlatformDataBase.Modules:
                dscArchList.append ('IA32')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('X64').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if InfFileKey in PlatformDataBase.Modules:
                dscArchList.append ('X64')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IPF').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if PlatformDataBase != None:
            if InfFileKey in (PlatformDataBase.Modules):
                dscArchList.append ('IPF')

        curArchList = targetArchList
        if dscArchList != []:
            curArchList = set (targetArchList) & set (dscArchList)
        GenFdsGlobalVariable.VerboseLogger ("Valid target architecture(s) is : " + " ".join(curArchList))
        return list(curArchList)
    
    def GetCurrentArch(self) :
        curArchList = self.__GetPlatformArchList__()
        ArchList = []
        if self.KeyStringList != []:
            for Key in self.KeyStringList:
                Key = GenFdsGlobalVariable.MacroExtend(Key)
                Target, Tag, Arch = Key.split('_')
                if Arch in curArchList:
                    ArchList.append(Arch)
                if Target not in self.TargetOverrideList:
                    self.TargetOverrideList.append(Target)
        else:
            ArchList = curArchList
                
        if len(ArchList) == 1:
            Arch = ArchList[0]
            return Arch
        elif len(ArchList) > 1:
#            raise Exception("Module %s has too many build ARCH !" %self.InfFileName)
            return None 
        else:
            raise Exception("Don't find legal ARCH in Module %s !" %self.InfFileName)
#        if len(curArchList) > 1 :
#            
#        elif len(curArchList) == 1 :
#            Arch = curArchList.pop()
#            return Arch
    
    def __GetEFIOutPutPath__(self):
        Arch = ''
        OutputPath = ''
        (ModulePath, fileName) = os.path.split(self.InfFileName)
        index = fileName.find('.')
        fileName = fileName[0:index]
        Arch = "NoneArch"
        if self.CurrentArch != None:
            Arch = self.CurrentArch
        
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
        FileList = []
        OutputFileList = []
        if Rule.FileName != None:
            GenSecInputFile = self.__ExtendMarco__(Rule.FileName)
        else:
            FileList, IsSect = Section.Section.GetFileList(self, '', Rule.FileExtension)

        Index = 1
        SectionType     = Rule.SectionType
        if FileList != [] :
            for File in FileList:
                SecNum = '%d' %Index
                GenSecOutputFile= self.__ExtendMarco__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType] + 'SEC' + SecNum   
                Index = Index + 1             
                OutputFile = os.path.join(self.OutputPath, GenSecOutputFile)
                genSectionCmd = 'GenSec -o '                                + \
                                 OutputFile                                 + \
                                 ' -s '                                     + \
                                 Section.Section.SectionType[SectionType]   + \
                                 ' '                                        + \
                                 File
                #
                # Call GenSection
                #
                GenFdsGlobalVariable.CallExternalTool(genSectionCmd, "Gen section Failed!")
                OutputFileList.append(GenSecOutputFile)
        else:
            SecNum = '%d' %Index
            GenSecOutputFile= self.__ExtendMarco__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType] + 'SEC' + SecNum
            OutputFile = os.path.join(self.OutputPath, GenSecOutputFile)
            
            genSectionCmd = 'GenSec -o '                                + \
                             OutputFile                                 + \
                             ' -s '                                     + \
                             Section.Section.SectionType[SectionType]   + \
                             ' '                                        + \
                             GenSecInputFile
            #
            # Call GenSection
            #
            GenFdsGlobalVariable.CallExternalTool(genSectionCmd, "Gen section Failed!")
            OutputFileList.append(GenSecOutputFile)

        return OutputFile
    
    def __GenSimpleFileFfs__(self, Rule, InputFileList):
        #
        # Prepare the parameter of GenFfs
        #
        (FileType,Fixed, CheckSum, Alignment) = self.__GetGenFfsComParamter__(Rule)
        
        FfsOutput = self.OutputPath                     + \
                    os.sep                              + \
                    self.__ExtendMarco__(Rule.NameGuid) + \
                    '.ffs'

        GenFdsGlobalVariable.VerboseLogger(self.__ExtendMarco__(Rule.NameGuid))
        InputSection = ''
        for InputFile in InputFileList:
            InputSection = InputSection + \
                           ' -i '       + \
                           InputFile
            if Alignment != '':
                InputSection = InputSection  + \
                               ' -n '        + \
                               Alignment


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
        Index = 1
        for Sect in Rule.SectionList:
           SecIndex = '%d' %Index
           SectList  = []
           if Rule.KeyStringList != []:
               SectList, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, Rule.KeyStringList, self)
           else :
               SectList, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, self.KeyStringList, self)
           for SecName in  SectList :
               SectFiles = SectFiles    + \
                           ' -i '       + \
                           SecName
               if Align != None:
                   SectFiles = SectFiles + \
                               ' -n '    + \
                               Align
           Index = Index + 1
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
            CheckSum = ''
            
        if Rule.Alignment != None and Rule.Alignment != '':
            Alignment = ' -a %s' %Rule.Alignment
        else :
            Alignment = ''
            
        return FileType, Fixed, CheckSum, Alignment