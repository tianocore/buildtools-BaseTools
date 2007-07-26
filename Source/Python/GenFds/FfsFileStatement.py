import Ffs
import Rule
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
import subprocess
from CommonDataClass.FdfClassObject import FileStatementsClassObject

class FileStatements (FileStatementsClassObject) :
    def __init__(self):
        FileStatementsClassObject.__init__(self)
        
    def GenFfs(self):
        OutputDir = os.path.join(GenFdsGlobalVariable.FfsDir, self.NameGuid)
        if not os.path.exists(OutputDir):
             os.makedirs(OutputDir)

        if self.FileName != None :
            SectionFiles = ' -i ' + \
                          GenFdsGlobalVariable.ReplaceWorkspaceMarco(self.FileName)
        else:
            SectionFiles = ''
            for section in self.SectionList :
                sect, align = section.GenSection(OutputDir, self.NameGuid, self.KeyStringList)
                if sect != None:
                    SectionFiles = SectionFiles  + \
                                   ' -i '        + \
                                   sect
                    if align != None:
                        SectionFiles = SectionFiles  + \
                                       ' -n '        + \
                                       align
                               
        #
        # Prepare the parameter
        #
        print "Fixe = ", self.Fixed
        if self.Fixed != False:
                Fixed = ' -x '
        else :
                Fixed = ''
        print "CheckSum=", self.CheckSum
        if self.CheckSum != False :
                CheckSum = ' -s '
        else :
                CheckSum = ''
                
        if self.Alignment != None and self.Alignment !='':
                Alignment = ' -a ' + '%s' %self.Alignment
        else :
                Alignment = ''
                
        if not (self.FvType == None):
            FileType = ' -t ' + Ffs.Ffs.FvTypeToFileType.get(self.FvType)
        else:
            FileType = ''

        FfsFileOutput = os.path.join(OutputDir, self.NameGuid + '.ffs')
                    
  
        GenFfsCmd = 'GenFfs' +  \
                     FileType +     \
                     Fixed +        \
                     CheckSum +     \
                     Alignment +    \
                     ' -o ' +       \
                     FfsFileOutput +    \
                     ' -g ' +       \
                     self.NameGuid +\
                     SectionFiles
     
        print GenFfsCmd
        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd,"GenFfs Failed !")
        return FfsFileOutput
        

