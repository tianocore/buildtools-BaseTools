from Ffs import Ffs
import Section
import subprocess
import os

class CompressSection (Section.Section) :
    CompTypeDict = {
        'PI_STD'     : ' -c PI_STD ',
        'NON_PI_STD' : ' -c NON_PI_STD '
    }
    
    def __init__(self):
        self.Alignment = None
        self.CompType = None
        self.SectionList = []
        

    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Generate all section
        #
        if FfsInf != None:
            self.CompType = FfsInf.__ExtendMarco__(self.CompType)
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            
        SectFiles = ''
        for Sect in self.SectionList:
            SectFiles = SectFiles + \
                        ' '       + \
                        Sect.GenSection(OutputPath, ModuleName,FfsInf)

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     Ffs.SectionSuffix['COMPRESS']
        OutputFile = os.path.normpath(OutputFile)
        
        GenSectionCmd = 'GenSection -o '                              + \
                         OutputFile                                   + \
                         ' -s '                                       + \
                         Section.Section.SectionType['COMPRESS']      + \
                         self.CompTypeDict[self.CompType]             + \
                         SectFiles
        #
        # Call GenSection
        #
        print GenSectionCmd
        PopenObject = subprocess.Popen (GenSectionCmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0 :
            raise Exception("GenSection Failed!")
        
        return OutputFile

        
