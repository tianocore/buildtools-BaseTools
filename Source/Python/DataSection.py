import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs
import os

class DataSection (Section.Section):
    def __init__(self):
        self.Alignemnt = None
        self.SecType = None
        self.SectFileName = None
        self.SectionList = []
        
    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignemnt)
            self.SecType = FfsInf.__ExtendMarco__(self.SecType)
            self.SectFileName = FfsInf.__ExtendMarco__(self.SectFileName)
            
        """Check Section file exist or not !"""
        if not os.path.exists(self.SectFileName):
            self.SectFileName = os.path.join (GenFdsGlobalVariable.WorkSpaceDir,
                                              self.SectFileName)

        OutputFile = OutputPath + \
                     os.sep     + \
                     ModuleName + \
                     Ffs.SectionSuffix.get(self.SecType)
        OutputFile = os.path.normpath(OutputFile)
        print "DataSection SectionType: %s" %self.SecType
        print "DataSection SectFileName: %s" %self.SectFileName
        
        GenSectionCmd = 'GenSection -o '                                 + \
                         OutputFile                                      + \
                         ' -s '                                          + \
                         Section.Section.SectionType.get (self.SecType)  + \
                         ' '                                             + \
                         GenFdsGlobalVariable.ExtendMarco(self.SectFileName)

        #
        # Call GenSection
        #
        
        print GenSectionCmd
        PopenObject = subprocess.Popen (GenSectionCmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0:
            raise Exception("GenSection Failed!")
        
        return OutputFile
