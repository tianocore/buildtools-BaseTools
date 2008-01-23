## @file
# process FFS generation from INF statement
#
#  Copyright (c) 2007, Intel Corporation
#
#  All rights reserved. This program and the accompanying materials
#  are licensed and made available under the terms and conditions of the BSD License
#  which accompanies this distribution.  The full text of the license may be found at
#  http://opensource.org/licenses/bsd-license.php
#
#  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
#  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import Rule
import os
import shutil
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Ffs
import subprocess
import sys
import Section
import RuleSimpleFile
import RuleComplexFile
from CommonDataClass.FdfClassObject import FfsInfStatementClassObject
from Common.String import *

## generate FFS from INF
#
#
class FfsInfStatement(FfsInfStatementClassObject):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsInfStatementClassObject.__init__(self)
        self.TargetOverrideList = []
        self.ShadowFromInfFile = None
        self.KeepRelocFromRule = None

    ## __InfParse() method
    #
    #   Parse inf file to get module information
    #
    #   @param  self        The object pointer
    #   @param  Dict        dictionary contains macro and value pair
    #    
    def __InfParse__(self, Dict = {}):
        self.CurrentArch = self.GetCurrentArch()
        #
        # Get the InfClass object
        #

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
            if Inf.AutoGenVersion < 0x00010005:
                self.ModuleType = GenFdsGlobalVariable.WorkSpace.InfDatabase[self.InfFileName].Module.Header[self.CurrentArch].ComponentType
            self.VersionString = Inf.Version
            self.BinFileList = Inf.Binaries
            if self.KeepReloc == None and Inf.Shadow != '':
                if Inf.Shadow.upper() == "TRUE":
                    self.ShadowFromInfFile = True
                else:
                    self.ShadowFromInfFile = False 
        
        elif self.InfFileName in GenFdsGlobalVariable.WorkSpace.InfDatabase.keys():
            Inf = GenFdsGlobalVariable.WorkSpace.InfDatabase[self.InfFileName]
            self.BaseName = Inf.Module.Header[self.CurrentArch].Name
            self.ModuleGuid = Inf.Module.Header[self.CurrentArch].Guid
            self.ModuleType = Inf.Module.Header[self.CurrentArch].ModuleType
            self.VersionString = Inf.Module.Header[self.CurrentArch].Version
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
    
    ## GenFfs() method
    #
    #   Generate FFS
    #
    #   @param  self        The object pointer
    #   @param  Dict        dictionary contains macro and value pair
    #   @retval string      Generated FFS file name
    #                          
    def GenFfs(self, Dict = {}):
        #
        # Parse Inf file get Module related information
        #
        GenFdsGlobalVariable.VerboseLogger( " Begine parsing INf file : %s" %self.InfFileName)
        
        self.InfFileName = self.InfFileName.replace('$(WORKSPACE)', '')
        if self.InfFileName[0] == '\\' or self.InfFileName[0] == '/' :
            self.InfFileName = self.InfFileName[1:]
        
 
        self.__InfParse__(Dict)
        #
        # Get the rule of how to generate Ffs file
        #
        Rule = self.__GetRule__()
        GenFdsGlobalVariable.VerboseLogger( "Packing binaries from inf file : %s" %self.InfFileName)
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
                
    ## __ExtendMacro__() method
    #
    #   Replace macro with its value
    #
    #   @param  self        The object pointer
    #   @param  String      The string to be replaced
    #   @retval string      Macro replaced string
    # 
    def __ExtendMacro__ (self, String):
        MacroDict = {
            '$(INF_OUTPUT)'  : self.EfiOutputPath,
            '$(MODULE_NAME)' : self.BaseName,
            '$(BUILD_NUMBER)': self.BuildNum,
            '$(INF_VERSION)' : self.VersionString,
            '$(NAMED_GUID)'  : self.ModuleGuid        
        }
        String = GenFdsGlobalVariable.MacroExtend(String, MacroDict)
        return String

    ## __GetRule__() method
    #
    #   Get correct rule for generating FFS for this INF
    #
    #   @param  self        The object pointer
    #   @retval Rule        Rule object
    # 
    def __GetRule__ (self) :
        CurrentArchList = []
        if self.CurrentArch == None:
            CurrentArchList = ['common']
        else:
            CurrentArchList.append(self.CurrentArch)
        
        for CurrentArch in CurrentArchList:
            RuleName = 'RULE'              + \
                       '.'                 + \
                       CurrentArch.upper() + \
                       '.'                 + \
                       self.ModuleType.upper()
            if self.Rule != None:
                RuleName = RuleName + \
                           '.'      + \
                           self.Rule.upper()
                           
            Rule = GenFdsGlobalVariable.FdfParser.Profile.RuleDict.get(RuleName)
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
                       
        GenFdsGlobalVariable.VerboseLogger ('Trying to apply common rule %s for INF %s' % (RuleName, self.InfFileName))               
        
        Rule = GenFdsGlobalVariable.FdfParser.Profile.RuleDict.get(RuleName)
        if Rule != None:
            GenFdsGlobalVariable.VerboseLogger ("Want To Find Rule Name is : " + RuleName)
            return Rule

        if Rule == None :
            raise Exception ('Don\'t Find common rule %s for INF %s' % (RuleName, self.InfFileName))

    ## __GetPlatformArchList__() method
    #
    #   Get Arch list this INF built under
    #
    #   @param  self        The object pointer
    #   @retval list        Arch list
    # 
    def __GetPlatformArchList__(self):
        TargetArchList = GenFdsGlobalVariable.ArchList
        if len(TargetArchList) == 0:
            TargetArchList = GenFdsGlobalVariable.WorkSpace.SupArchList
        else:
            TargetArchList = set(GenFdsGlobalVariable.WorkSpace.SupArchList) & set(TargetArchList)
            
        InfFileKey = os.path.normpath(self.InfFileName)
        DscArchList = []
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IA32').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if InfFileKey in PlatformDataBase.Modules:
                DscArchList.append ('IA32')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('X64').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if  PlatformDataBase != None:
            if InfFileKey in PlatformDataBase.Modules:
                DscArchList.append ('X64')
                
        PlatformDataBase = GenFdsGlobalVariable.WorkSpace.Build.get('IPF').PlatformDatabase.get(GenFdsGlobalVariable.ActivePlatform)
        if PlatformDataBase != None:
            if InfFileKey in (PlatformDataBase.Modules):
                DscArchList.append ('IPF')

        CurArchList = TargetArchList
        if DscArchList != []:
            CurArchList = set (TargetArchList) & set (DscArchList)
        GenFdsGlobalVariable.VerboseLogger ("Valid target architecture(s) is : " + " ".join(CurArchList))
        return list(CurArchList)
    
    ## GetCurrentArch() method
    #
    #   Get Arch list of the module from this INF is to be placed into flash
    #
    #   @param  self        The object pointer
    #   @retval list        Arch list
    # 
    def GetCurrentArch(self) :
        CurArchList = self.__GetPlatformArchList__()
        ArchList = []
        if self.KeyStringList != []:
            for Key in self.KeyStringList:
                Key = GenFdsGlobalVariable.MacroExtend(Key)
                Target, Tag, Arch = Key.split('_')
                if Arch in CurArchList:
                    ArchList.append(Arch)
                if Target not in self.TargetOverrideList:
                    self.TargetOverrideList.append(Target)
        else:
            ArchList = CurArchList
                
        if len(ArchList) == 1:
            Arch = ArchList[0]
            return Arch
        elif len(ArchList) > 1:
            raise Exception("Not able to determine ARCH for Module %s !" %self.InfFileName) 
        else:
            raise Exception("Don't find legal ARCH in Module %s !" %self.InfFileName)
    
    ## __GetEFIOutPutPath__() method
    #
    #   Get the output path for generated files
    #
    #   @param  self        The object pointer
    #   @retval string      Path that output files from this INF go to
    # 
    def __GetEFIOutPutPath__(self):
        Arch = ''
        OutputPath = ''
        (ModulePath, FileName) = os.path.split(self.InfFileName)
        Index = FileName.find('.')
        FileName = FileName[0:Index]
        Arch = "NoneArch"
        if self.CurrentArch != None:
            Arch = self.CurrentArch
        
        OutputPath = os.path.join(GenFdsGlobalVariable.OutputDir,
                                  Arch ,
                                  ModulePath,
                                  FileName,
                                  'OUTPUT'
                                  )
        OutputPath = os.path.realpath(OutputPath)
        return OutputPath
    
    ## __GenSimpleFileSection__() method
    #
    #   Generate section by specified file name or a list of files with file extension
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @retval string      File name of the generated section file
    #     
    def __GenSimpleFileSection__(self, Rule):
        #
        # Prepare the parameter of GenSection
        #
        FileList = []
        OutputFileList = []
        if Rule.FileName != None:
            GenSecInputFile = self.__ExtendMacro__(Rule.FileName)
        else:
            FileList, IsSect = Section.Section.GetFileList(self, '', Rule.FileExtension)

        Index = 1
        SectionType     = Rule.SectionType
        NoStrip = True
        if self.ModuleType in ('SEC', 'PEI_CORE', 'PEIM'):
            if self.KeepReloc != None:
                NoStrip = self.KeepReloc
            elif Rule.KeepReloc != None:
                NoStrip = Rule.KeepReloc
            elif self.ShadowFromInfFile != None:
                NoStrip = self.ShadowFromInfFile
                
        if FileList != [] :
            for File in FileList:
                
                SecNum = '%d' %Index
                GenSecOutputFile= self.__ExtendMacro__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType] + 'SEC' + SecNum   
                Index = Index + 1             
                OutputFile = os.path.join(self.OutputPath, GenSecOutputFile)
                
                if not NoStrip:
                    FileBeforeStrip = os.path.join(self.OutputPath, ModuleName + '.reloc')
                    shutil.copyfile(File, FileBeforeStrip)
                    StrippedFile = os.path.join(self.OutputPath, ModuleName + '.stipped')
                    StripCmd = (
                        'GenFw',
                        '-l',
                        '-o', StrippedFile,
                        GenFdsGlobalVariable.MacroExtend(File, Dict),
                        )
                    GenFdsGlobalVariable.CallExternalTool(StripCmd, "Strip Failed !")
                    File = StrippedFile
                    
                if SectionType == 'TE':
                    TeFile = os.path.join( self.OutputPath, self.ModuleGuid + 'Te.raw')
                    GenTeCmd = (
                        'GenFw',
                        '-t',
                        '-o', TeFile,
                        GenFdsGlobalVariable.MacroExtend(File, Dict),
                        )
                    GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
                    File = TeFile
                
                GenSectionCmd = (
                    'GenSec',
                    '-o', OutputFile,
                    '-s', Section.Section.SectionType[SectionType],
                    File,
                    )
                #
                # Call GenSection
                #
                GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "Gen section Failed!")
                OutputFileList.append(OutputFile)
        else:
            SecNum = '%d' %Index
            GenSecOutputFile= self.__ExtendMacro__(Rule.NameGuid) + \
                              Ffs.Ffs.SectionSuffix[SectionType] + 'SEC' + SecNum
            OutputFile = os.path.join(self.OutputPath, GenSecOutputFile)
            
            if not NoStrip:
                FileBeforeStrip = os.path.join(self.OutputPath, ModuleName + '.reloc')
                shutil.copyfile(File, FileBeforeStrip)
                StrippedFile = os.path.join(self.OutputPath, ModuleName + '.stipped')
                StripCmd = (
                    'GenFw',
                    '-l',
                    '-o', StrippedFile,
                    GenFdsGlobalVariable.MacroExtend(File, Dict),
                    )
                GenFdsGlobalVariable.CallExternalTool(StripCmd, "Strip Failed !")
                File = StrippedFile
            
            if SectionType == 'TE':
                TeFile = os.path.join( self.OutputPath, self.ModuleGuid + 'Te.raw')
                GenTeCmd = (
                    'GenFw',
                    '-t',
                    '-o', TeFile,
                    GenFdsGlobalVariable.MacroExtend(File, Dict),
                    )
                GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
                GenSecInputFile = TeFile
            
            GenSectionCmd = (
                'GenSec',
                '-o', OutputFile,
                '-s', Section.Section.SectionType[SectionType],
                GenSecInputFile,
                )
            #
            # Call GenSection
            #
            GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "Gen section Failed!")
            OutputFileList.append(OutputFile)

        return OutputFileList
    
    ## __GenSimpleFileFfs__() method
    #
    #   Generate FFS
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @param  InputFileList        The output file list from GenSection
    #   @retval string      Generated FFS file name
    #
    def __GenSimpleFileFfs__(self, Rule, InputFileList):
        #
        # Prepare the parameter of GenFfs
        #
        CmdParams = self.__GetGenFfsCmdParameter__(Rule)

        FfsOutput = self.OutputPath                     + \
                    os.sep                              + \
                    self.__ExtendMacro__(Rule.NameGuid) + \
                    '.ffs'

        GenFdsGlobalVariable.VerboseLogger(self.__ExtendMacro__(Rule.NameGuid))
        InputSection = tuple()
        for InputFile in InputFileList:
            InputSection += ('-i', InputFile)
            for i in range(len(CmdParams) - 1):
                if CmdParams[i] == '-a':
                    InputSection += ('-n', CmdParams[i+1])
                    break

        GenFfsCmd = (
            'GenFfs',
             '-g', self.NameGuid,
             '-o', FfsOutput,
            ) + CmdParams + InputSection
        #
        # Call GenSection
        #
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed!")
        return FfsOutput
    
    ## __GenComplexFileSection__() method
    #
    #   Generate section by sections in Rule
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @retval string      File name of the generated section file
    #  
    def __GenComplexFileSection__(self, Rule):
        
        if self.ModuleType in ('SEC', 'PEI_CORE', 'PEIM'):
            if Rule.KeepReloc != None:
                self.KeepRelocFromRule = Rule.KeepReloc
        
        SectFiles = tuple()
        Index = 1
        for Sect in Rule.SectionList:
           SecIndex = '%d' %Index
           SectList  = []
           if Rule.KeyStringList != []:
               SectList, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, Rule.KeyStringList, self)
           else :
               SectList, Align = Sect.GenSection(self.OutputPath , self.ModuleGuid, SecIndex, self.KeyStringList, self)
           for SecName in  SectList :
               SectFiles += ('-i', SecName)
               if Align != None:
                   SectFiles += ('-n', Align)
           Index = Index + 1
        return SectFiles

    ## __GenComplexFileFfs__() method
    #
    #   Generate FFS
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @param  InputFileList        The output file list from GenSection
    #   @retval string      Generated FFS file name
    #
    def __GenComplexFileFfs__(self, Rule, InputFile):
        
        CmdParams = self.__GetGenFfsCmdParameter__(Rule)
        
        FfsOutput = os.path.join( self.OutputPath, self.ModuleGuid + '.ffs')
        GenFfsCmd = (
            'GenFfs',
            ) + CmdParams + (
             '-g', self.ModuleGuid,
             '-o', FfsOutput,
            ) + InputFile

        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd, "GenFfs Failed !")
        return FfsOutput

    ## __GetGenFfsCmdParameter__() method
    #
    #   Create parameter string for GenFfs
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @retval tuple       (FileType, Fixed, CheckSum, Alignment)
    #
    def __GetGenFfsCmdParameter__(self, Rule):
        result = tuple()
        result += ('-t', Ffs.Ffs.FdfFvFileTypeToFileType[Rule.FvFileType])
        #FileType = ' -t ' + \
        #           Ffs.Ffs.FdfFvFileTypeToFileType[Rule.FvFileType]
        if Rule.Fixed != False:
            result += ('-x',)
        if Rule.CheckSum != False:
            result += ('-s',)
            
        if Rule.Alignment != None and Rule.Alignment != '':
            result += ('-a', Rule.Alignment)
            
        return result
