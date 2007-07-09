import Ffs
import Rule
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
import subprocess
class FileStatements (Ffs.Ffs) :
    def __init__(self):
        Ffs.Ffs.__init__(self)
##        Ffs.Ffs.CheckSum = False
##        Ffs.Ffs.Fixed = False
##        Ffs.Ffs.NameGuid = None
##        Ffs.Ffs.Alignment = None
        Ffs.Ffs.SectionList = []
        self.FvType = None
        self.FileName = None
        self.KeyStringList = []
        
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
                SectionFiles = SectionFiles                          + \
                               ' -i '                                + \
                               section.GenSection(OutputDir, self.NameGuid, self.KeyStringList)
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
        PopenObject = subprocess.Popen (GenFfsCmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0:
            raise Exception("GenFfs Failed !")
        
        return FfsFileOutput
        

