from Ffs import Ffs
import Section
import os
import subprocess
class VerSection (Section.Section):
    def __init__(self):
        self.Alignment = None
        self.BuildNum = None
        self.StringData = None
        self.FileName = None
        
    def GenSection(self,OutputPath, ModuleName):
        #
        # Prepare the parameter of GenSection
        #
        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get('VERSION')
                     
        if not (self.BuildNum == None) :
            BuildNum = ' -j ' + '%f' %self.BuildNum;
        else :
            BuidNum = None

        if self.StringData != None:
             StringData = self.StringData
        elif self.FileName != None:
            f = open (self.FileName, 'r')
            StringData = f.read()
            f.close()
        else:
            StringData = ''
            
        GenSectionCmd = 'GenSection -o ' +            \
                         OutputFile +                 \
                         ' -s EFI_SECTION_VERSION ' + \
                         '-n '                      + \
                         '\"'                       + \
                         StringData                 + \
                         '\"'                       + \
                         BuildNum
                         
        # For Test
        GenSectionCmd = "GenSection -o 001-001-001-009-008-007-008.ver \
                         -s EFI_SECTION_VERSION -v \"0.01\""
                         
        #
        # Call GenSection
        #
        print GenSectionCmd
        subprocess.Popen(GenSectionCmd).communicate()

        return OutputFile
