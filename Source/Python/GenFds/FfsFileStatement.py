import Ffs
import Rule
from GenFdsGlobalVariable import GenFdsGlobalVariable
import os
import StringIO
import subprocess
from CommonDataClass.FdfClassObject import FileStatementsClassObject

class FileStatements (FileStatementsClassObject) :
    def __init__(self):
        FileStatementsClassObject.__init__(self)
        
    def GenFfs(self, Dict = {}):
        OutputDir = os.path.join(GenFdsGlobalVariable.FfsDir, self.NameGuid)
        if not os.path.exists(OutputDir):
             os.makedirs(OutputDir)

        Dict.update(self.DefineVarDict)
        
        if self.FvName != None :
            Buffer = StringIO.StringIO('')
            if self.FvName.upper() not in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
                raise Exception ("FV (%s) is NOT described in FDF file!" % (self.FvName))
            Fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(self.FvName.upper())
            FileName = Fv.AddToBuffer(Buffer)
            SectionFiles = ' -i ' + FileName
            
        elif self.FdName != None:
            if self.FdName.upper() not in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
                raise Exception ("FD (%s) is NOT described in FDF file!" % (self.FdName))
            Fd = GenFdsGlobalVariable.FdfParser.profile.FdDict.get(self.FdName.upper())
            FvBin = {}
            FileName = Fd.GenFd(FvBin)
            SectionFiles = ' -i ' + FileName
        
        elif self.FileName != None:
            self.FileName = GenFdsGlobalVariable.ReplaceWorkspaceMarco(self.FileName)
            SectionFiles = ' -i ' + GenFdsGlobalVariable.MacroExtend(self.FileName, Dict)
            
        else:
            SectionFiles = ''
            Index = 0
            for section in self.SectionList :
                Index = Index + 1
                SecIndex = '%d' %Index
                sectList, align = section.GenSection(OutputDir, self.NameGuid, SecIndex, self.KeyStringList, None, Dict)
                if sectList != []:
                    for sect in sectList:
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
        if self.Fixed != False:
                Fixed = ' -x '
        else :
                Fixed = ''
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


        GenFfsCmd = 'GenFfs'       +  \
                     FileType      +  \
                     Fixed         +  \
                     CheckSum      +  \
                     Alignment     +  \
                     ' -o '        +  \
                     FfsFileOutput +  \
                     ' -g '        +  \
                     self.NameGuid +  \
                     SectionFiles

        GenFdsGlobalVariable.CallExternalTool(GenFfsCmd,"GenFfs Failed !")
        return FfsFileOutput
        

