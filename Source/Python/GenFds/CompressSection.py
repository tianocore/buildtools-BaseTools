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
        

    def GenSection(self, OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None, Dict = {}):
        #
        # Generate all section
        #
        if FfsInf != None:
            self.CompType = FfsInf.__ExtendMarco__(self.CompType)
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            
        SectFiles = ''
        Index = 0
        for Sect in self.SectionList:
            Index = Index + 1
            SecIndex = '%s.%d' %(SecNum, Index)
            ReturnSectList, align = Sect.GenSection(OutputPath, ModuleName, SecIndex, KeyStringList, FfsInf, Dict)
            if ReturnSectList != []:
                for file in ReturnSectList:
                   SectFiles = SectFiles + \
                               ' '       + \
                               file
                        

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     'SEC'      + \
                     SecNum     + \
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
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed!")
        OutputFileList = []
        OutputFileList.append(OutputFile)
        return OutputFileList, self.Alignment

        
