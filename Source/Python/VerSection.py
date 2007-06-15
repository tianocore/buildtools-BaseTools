from Ffs import Ffs
import Section
import os
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
        OutputFile = OutputPath + ModuleName + Ffs.SectionSuffix.get('VERSION')
        if not (self.BuildNum == None) :
            BuildNum = ' -j ' + '%f' %self.BuildNum;
        else :
            BuidNum = None
        GenSectionCmd = 'GenSection -o ' + OutputFile + ' -s EFI_SECTION_VERSION ' \
                         + '-n ' + '\"' + self.StringData + '\"' + BuildNum
        #
        # Call GenSection
        #
        # Call GenSection
        #
        print GenSectionCmd
        os.popen(GenSectionCmd,'r')
        
        return OutputFile
