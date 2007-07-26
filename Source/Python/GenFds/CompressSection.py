from Ffs import Ffs
import Section
import subprocess
import os
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import CompressSectionClassObject

class CompressSection (CompressSectionClassObject) :
    CompTypeDict = {
        'PI_STD'     : ' -c PI_STD ',
        'NON_PI_STD' : ' -c NON_PI_STD '
    }
    
    def __init__(self):
        CompressSectionClassObject.__init__(self)
        

    def GenSection(self, OutputPath, ModuleName,  KeyStringList, FfsInf = None):
        #
        # Generate all section
        #
        if FfsInf != None:
            self.CompType = FfsInf.__ExtendMarco__(self.CompType)
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            
        SectFiles = ''
        for Sect in self.SectionList:
            sect, align = Sect.GenSection(OutputPath, ModuleName, KeyStringList, FfsInf)
            if sect != None:
                SectFiles = SectFiles + \
                            ' '       + \
                            sect
                        

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     Ffs.SectionSuffix['COMPRESS']
        OutputFile = os.path.normpath(OutputFile)
        
        GenSectionCmd = 'GenSec -o '                                  + \
                         OutputFile                                   + \
                         ' -s '                                       + \
                         Section.Section.SectionType['COMPRESS']      + \
                         self.CompTypeDict[self.CompType]             + \
                         SectFiles
        #
        # Call GenSection
        #
        print GenSectionCmd
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
        
        return OutputFile, self.Alignment

        
