import Section
import subprocess
from Ffs import Ffs
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import GuidSectionClassObject
from Common import ToolDefClassObject
import sys

class GuidSection(GuidSectionClassObject) :
    
    def __init__(self):
        GuidSectionClassObject.__init__(self)
        
    def GenSection(self, OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None, Dict = {}):
        #
        # Generate all section
        #
        self.keyStringList = KeyStringList
        
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            self.NameGuid = FfsInf.__ExtendMarco__(self.NameGuid)
            self.SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            
        SectFile = ''
        Index = 0
        for Sect in self.SectionList:
            Index = Index + 1
            SecIndex = '%s.%d' %(SecNum,Index)
            ReturnSectList, align = Sect.GenSection(OutputPath, ModuleName, SecIndex, KeyStringList,FfsInf, Dict)
            if ReturnSectList != []:
                for file in ReturnSectList:
                    SectFile = SectFile + \
                               '  '     + \
                               file
                       

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     'SEC'      + \
                     SecNum     + \
                     Ffs.SectionSuffix['GUIDED']
        OutputFile = os.path.normpath(OutputFile)
        
        ExternalTool = None
        if self.NameGuid != None:
            ExternalTool = self.__FindExtendTool__()
        #
        # If not have GUID , call default
        # GENCRC32 section
        #
        if self.NameGuid == None :
            GenFdsGlobalVariable.VerboseLogger( "Use GenSection function Generate CRC32 Section")
            GenSectionCmd = 'GenSec -o '                                   + \
                             OutputFile                                    + \
                             ' -s '                                        + \
                             Section.Section.SectionType[self.SectionType] + \
                             SectFile
                             
            GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
            OutputFileList = []
            OutputFileList.append(OutputFile)
            return OutputFileList, self.Alignment
        #or GUID not in External Tool List
        elif ExternalTool == None:
            print "No tool found with GUID %s" % self.NameGuid
            sys.exit(1)
        else:
            #
            # Call GenSection with DUMMY section type.
            #
            GenSectionCmd = 'GenSec -o '                                   + \
                             OutputFile                                    + \
                             SectFile
        
            GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
            #
            # Use external tool process the Output
            #
            InputFile = OutputFile
            TempFile = OutputPath + \
                       os.sep     + \
                       ModuleName + \
                       'SEC'      + \
                       SecNum     + \
                       '.tmp'
            TempFile = os.path.normpath(TempFile)
            
            ExternalToolCmd = ExternalTool                             + \
                              ' -e '                                   + \
                              ' -o '                                   + \
                              TempFile                                 + \
                              ' '                                      + \
                              InputFile

            #
            # Call external tool
            #
            GenFdsGlobalVariable.CallExternalTool(ExternalToolCmd, "Gensec Failed!")
            #
            # Call Gensection Add Secntion Header
            #
            PROCSSING_REQUIRED = ''
            AUTH_STATUS_VALID = ''
            if self.ProcessRequired == True:
                PROCSSING_REQUIRED = "PROCSSING_REQUIRED"
            if self.AuthStatusValid == True:
                AUTH_STATUS_VALID = "AUTH_STATUS_VALID"
            if PROCSSING_REQUIRED != '' or AUTH_STATUS_VALID != '':
                attribute = ' -a '              + \
                             PROCSSING_REQUIRED + \
                             AUTH_STATUS_VALID
            else :
                attribute = ''
            GenSectionCmd = 'GenSec -o '                            + \
                             OutputFile                             + \
                             ' -s '                                 + \
                             Section.Section.SectionType['GUIDED']  + \
                             ' -g '                                 + \
                             self.NameGuid                          + \
                             attribute                              + \
                             ' '                                    + \
                             TempFile
                        
            GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
            OutputFileList = []
            OutputFileList.append(OutputFile)
            return OutputFileList, self.Alignment
        
    def __FindExtendTool__(self):
        tool = None
        if self.keyStringList == None or self.keyStringList == []:
            return tool
        toolDefinition = ToolDefClassObject.ToolDefDict(GenFdsGlobalVariable.WorkSpaceDir).ToolsDefTxtDictionary
        for toolDef in toolDefinition.items():
            if self.NameGuid == toolDef[1]:
                keyList = toolDef[0].split('_')
                key = keyList[0] + \
                      '_'        + \
                      keyList[1] + \
                      '_'        + \
                      keyList[2]
                if key in self.keyStringList and keyList[4] == 'GUID':
#                    toolMaro = keyList[3]
#                    toolName = toolDefinition.get( key        + \
#                                                   '_'        + \
#                                                   keyList[3] + \
#                                                   '_'        + \
#                                                   'NAME')
                    toolPath = toolDefinition.get( key        + \
                                                   '_'        + \
                                                   keyList[3] + \
                                                   '_'        + \
                                                   'PATH')
#                    tool = os.path.join (toolPath, toolName)
                    return toolPath
        return tool


                
