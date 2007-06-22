import Ffs
import Rule
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
import subprocess
class FileStatements (Ffs.Ffs) :
    def __init__(self):
        Ffs.Ffs.__init__(self)
        Ffs.Ffs.CheckSum = ''
        Ffs.Ffs.Fixed = ''
        Ffs.Ffs.NameGuid = ''
        Ffs.Ffs.Alignment = ''
        Ffs.Ffs.SectionList = []
        self.FvType = ''
        self.FilePath = None
        
    def GenFfs(self):
        SectionFiles = ''
        
        for section in self.SectionList :
            SectionFiles = SectionFiles                          + \
                           ' -i '                                + \
                           section.GenSection(GenFdsGlobalVariable.\
                           OuputDir, self.NameGuid)
        #
        # Prepare the parameter
        #
        if not (self.Fixed == None):
                Fixed = ' -x '
        else :
                Fixed = ''
        if not (self.CheckSum == None):
                CheckSum = ' -s '
        else :
                CheckSume = ''
        if not (self.Alignment == None):
                Alignment = ' -a ' + '%d' %self.Alignment
        else :
                Alignment = ''
                
        FileType = Ffs.Ffs.FvTypeToFileType.get(self.FvType)
        if not (FileType == None):
            FileType = ' - t ' + FileType
        else:
            FileType = ''

        FfsOutput = GenFdsGlobalVariable.OuputDir + \
                    self.NameGuid                 + \
                    '.ffs'
                    
        InputSection = ' -i '                         + \
                        GenFdsGlobalVariable.OuputDir + \
                        FfsOutput
  
        GenFfsCmd = 'GenFfsFile' +  \
                     FileType +     \
                     Fixed +        \
                     CheckSum +     \
                     Alignment +    \
                     ' -o ' +       \
                     FfsOutput +    \
                     ' -g ' +       \
                     self.NameGuid +\
                     SectionFiles
        #GenFfsCmd = "GenFfsFile -p1 Ffs.inf"
        #
        # Call GenSection
        #
        print GenFfsCmd
        #subprocess.Popen (GenFfsCmd).communicate()
        #FfsOutput = GenFdsGlobalVariable.OuputDir + \
        #           "1BCAB7B3-8D0A-4740-B021-A42945A229F9-PeiIOMMIORegisterLibBbTest.PEI"
        
        return FfsOutput
        

