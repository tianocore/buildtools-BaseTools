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
            print "Use GenSection function Generate CRC32 Section"
            GenSectionCmd = 'GenSection -o '                               + \
                             OutputFile                                    + \
                             ' -s '                                        + \
                             Section.Section.SectionType[self.SectionType] + \
                             SectFile
            PopenObject = subprocess.Popen(GenSectionCmd)
            PopenObject.communicate()
            if PopenObject.returncode != 0:
                raise Exception("GenSection Failed!")
            return OutputFile
        else:
            #
            # Call GenSection with DUMMY section type.
            #
            GenSectionCmd = 'GenSection -o '                               + \
                             OutputFile                                    + \
                             ' -s '                                        + \
                             SectFile
        
            print GenSectionCmd
            PopenObject = subprocess.Popen (GenSectionCmd)
            PopenObject.communicate()
            if PopenObject.returncode != 0:
                raise Exception ("GenSection Failed!")
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
                             
            GenSectionCmd = 'GenSection -o '                        + \
                             OutputFile                             + \
                             ' -s '                                 + \
                             Section.Section.SectionType['GUIDED']  + \
                             ' -g '                                 + \
                             self.NameGuid                          + \
                             attribute                              + \
                             ' '                                    + \
                             TempFile
                        
            print GenSectionCmd
            PopenObject = subprocess.Popen(GenSectionCmd)
            PopenObject.communicate()
            if PopenObject.returncode != 0:
                raise Exception ("GenSection Failed!")
            return OutputFile
