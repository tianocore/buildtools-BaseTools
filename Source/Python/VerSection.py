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
            BuildNum = ' -j ' + '%d' %self.BuildNum;
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
                         
        #
        # Call GenSection
        #
        print GenSectionCmd
        subprocess.Popen(GenSectionCmd).communicate()

        return OutputFile
