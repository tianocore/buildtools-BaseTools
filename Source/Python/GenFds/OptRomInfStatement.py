## @file
# process OptionROM generation from INF statement
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
import RuleSimpleFile
import RuleComplexFile
import Section

from FfsInfStatement import FfsInfStatement
from GenFdsGlobalVariable import GenFdsGlobalVariable
## 
#
#
class OptRomInfStatement (FfsInfStatement):
    ## The constructor
    #
    #   @param  self        The object pointer
    #
    def __init__(self):
        FfsInfStatement.__init__(self)
        self.OverrideAttribs = None

    ## GenFfs() method
    #
    #   Generate FFS
    #
    #   @param  self        The object pointer
    #   @retval string      Generated .efi file name
    #
    def GenFfs(self):
        #
        # Parse Inf file get Module related information
        #

        self.__InfParse__()
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
            EfiOutputList = self.__GenSimpleFileSection__(Rule)
            return EfiOutputList
        #
        # For Rule has ComplexFile
        #
        elif isinstance(Rule, RuleComplexFile.RuleComplexFile):
            EfiOutputList = self.__GenComplexFileSection__(Rule)
            return EfiOutputList

    ## __GenSimpleFileSection__() method
    #
    #   Get .efi files according to simple rule.
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @retval string      File name of the generated section file
    #
    def __GenSimpleFileSection__(self, Rule):
        #
        # Prepare the parameter of GenSection
        #

        OutputFileList = []
        if Rule.FileName != None:
            GenSecInputFile = self.__ExtendMacro__(Rule.FileName)
            OutputFileList.append(GenSecInputFile)
        else:
            OutputFileList, IsSect = Section.Section.GetFileList(self, '', Rule.FileExtension)

        return OutputFileList


    ## __GenComplexFileSection__() method
    #
    #   Get .efi by sections in complex Rule
    #
    #   @param  self        The object pointer
    #   @param  Rule        The rule object used to generate section
    #   @retval string      File name of the generated section file
    #
    def __GenComplexFileSection__(self, Rule):

        OutputFileList = []
        for Sect in Rule.SectionList:
            if Sect.SectionType == 'PE32':
                if Sect.FileName != None:
                    GenSecInputFile = self.__ExtendMacro__(Sect.FileName)
                    OutputFileList.append(GenSecInputFile)
                else:
                    FileList, IsSect = Section.Section.GetFileList(self, '', Sect.FileExtension)
                    OutputFileList.extend(FileList)    
        
        return OutputFileList

    