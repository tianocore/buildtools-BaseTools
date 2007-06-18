import Ffs
import Rule
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
class FileStatements (Ffs.Ffs) :
    def __init__(self):
        Ffs.Ffs.CheckSum = ''
        Ffs.Ffs.Fixed = ''
        Ffs.Ffs.NameGuid = ''
        Ffs.Ffs.Alignment = ''
        Ffs.Ffs.SectionList = []
        self.FvType = None
        self.FilePath = None
        
    def GenFfs(self):
        for section in self.SectionList :
            SectionFiles = ' -i ' + section.GenSection(GenFdsGlobalVariable.\
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

        FfsOutput = GenFdsGlobalVariable.OuputDir + self.NameGuid + '.ffs'
        InputSection = ' -i ' + GenFdsGlobalVariable.OuputDir + FfsOutput
  
        GenFfsCmd = 'GenFfs ' + FileType + Fixed + CheckSum + Alignment + \
                    ' -o ' + FfsOutput + ' -g ' + self.NameGuid + SectionFiles
        #
        # Call GenSection
        #
        print GenFfsCmd
        os.popen (GenFfsCmd, 'r')
        
        return FfsOutput
        

