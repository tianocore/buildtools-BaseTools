from Ffs import Ffs
import Section
import os
import subprocess
from GenFdsGlobalVariable import GenFdsGlobalVariable
from CommonDataClass.FdfClassObject import VerSectionClassObject

class VerSection (VerSectionClassObject):
    def __init__(self):
        VerSectionClassObject.__init__(self)
        
    def GenSection(self,OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None, Dict = {}):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None:
            self.Alignment = FfsInf.__ExtendMarco__(self.Alignment)
            self.BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            self.StringData = FfsInf.__ExtendMarco__(self.StringData)
            self.FileName = FfsInf.__ExtendMarco__(self.FileName)
            
        OutputFile = os.path.join(OutputPath,
                                  ModuleName + 'SEC' + SecNum + Ffs.SectionSuffix.get('VERSION'))
        OutputFile = os.path.normpath(OutputFile)
        
        """Get Build Num """
        BuildNum = ''
        if not (self.BuildNum == None) :
            BuildNum = ' -j ' + '%d' %self.BuildNum;
 
        """Get String Data"""
        StringData = ''
        if self.StringData != None:
             StringData = self.StringData
        elif self.FileName != None:
            file = GenFdsGlobalVariable.ReplaceWorkspaceMarco(self.FileName)
            file = GenFdsGlobalVariable.MacroExtend(file, Dict)
            f = open (file, 'r')
            StringData = f.read()
            StringData = '\"' + StringData + '\"'
            f.close()
        else:
            StringData = ''
            
        GenSectionCmd = 'GenSec -o '                + \
                         OutputFile                 + \
                         ' -s EFI_SECTION_VERSION ' + \
                         '-n '                      + \
                         StringData                 + \
                         BuildNum                   
                         
        #
        # Call GenSection
        #
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "Gensection Failed!")
        OutputFileList = []
        OutputFileList.append(OutputFile)
        return OutputFileList, self.Alignment
