import Section
import subprocess
from Ffs import Ffs
import os
class GuidSection(Section.Section) :
    
    def __init__(self):
        self.Alignment = None
        self.NameGuid = None
        self.SectionList = []
        self.SectionType = None
        self.ProcessRequired = False
        self.AuthStatusValid = False
        
    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Generate all section
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            self.NameGuid = FfsInf.__ExtendMarco__(self.NameGuid)
            self.SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            
        SectFile = ''
        for Sect in self.SectionList:
            SectFile = SectFile + \
                       '  '     + \
                       Sect.GenSection(OutputPath, ModuleName, FfsInf)

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     Ffs.SectionSuffix['GUIDED']
        OutputFile = os.path.normpath(OutputFile)
        
        ExternalTool = Section.Section.ToolGuild.get(self.NameGuid)
        #
        # If not have GUID or GUID not in External Tool List, call default
        # GENCRC32 section
        #
        if self.NameGuid == None or ExternalTool == None :
            GenSectionCmd = 'GenSection -o '                               + \
                             OutputFile                                    + \
                             ' -s '                                        + \
                             Section.Section.SectionType[self.SectionType] + \
                             SectFile
            return OutputFile
        else:
            #
            # Call GenSection
            #
            GenSectionCmd = 'GenSection -o '                               + \
                             OutputFile                                    + \
                             ' -s '                                        + \
                             SectFile
        
            print GenSectionCmd
            subprocess.Popen (GenSectionCmd).communicate()
        
            #
            # Use external tool process the Output
            #
            InputFile = OutputFile
            TempFile = OutputPath + \
                       os.sep     + \
                       ModuleName + \
                       '.tmp'
            TempFile = os.path.normpath(TempFile)
            
            ExternalToolCmd = Section.Section.ToolGuild[self.NameGuid] + \
                              ' -o '                                   + \
                              TempFile                                 + \
                              ' '                                      + \
                              InputFile

            #
            # Call external tool
            #
            print ExternalToolCmd
            subprocess.Popen (ExternalToolCmd).communicate()
            #
            # Call Gensection Add Secntion Header
            #
            GenSectionCmd = 'GenSection -o '                        + \
                             OutputFile                             + \
                             ' -s '                                 + \
                             Section.Section.SectionType['GUIDED']  + \
                             ' '                                    + \
                             TempFile
                        
            print GenSectionCmd
            subprocess.Popen(GenSectionCmd).communicate()
            return OutputFile
