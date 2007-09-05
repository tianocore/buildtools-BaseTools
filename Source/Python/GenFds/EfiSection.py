import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs
import os
from CommonDataClass.FdfClassObject import EfiSectionClassObject
import shutil

class EfiSection (EfiSectionClassObject):
    
    def __init__(self):
          EfiSectionClassObject.__init__(self)

    def GenSection(self, OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None) :
        """Prepare the parameter of GenSection"""
        if FfsInf != None :
            InfFileName = FfsInf.InfFileName
            SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            Filename = FfsInf.__ExtendMarco__(self.FileName)
            """print 'Buile Num: %s' %self.BuildNum"""
            BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            """print 'After extend Build Num: %s' %self.BuildNum"""
            """print 'version Num: %s' %self.VersionNum"""
            VersionNum = FfsInf.__ExtendMarco__(self.VersionNum)
            """print 'After extend Version Num: %s' %self.VersionNum"""
            StringData = FfsInf.__ExtendMarco__(self.StringData)
        else:
            SectionType = self.SectionType
            Filename = self.Filename
            BuildNum = self.BuildNum
            VerstionNum = self.VersionNum
            InfFileName = ''
            
        if self.Optional == True :
            if Filename == None or Filename =='':
                GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                return '', None
            
       
        
        FileList, IsSect = Section.Section.GetFileList(FfsInf, self.FileType, self.FileExtension)
        if IsSect :
            return FileList, self.Alignment

        Num = SecNum
        
        """ If Section type is 'VERSION'"""
        
        OutputFileList = []
        if SectionType == 'VERSION':
            if FileList != []:
                for FileName in FileList:
                    OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + Num + Ffs.SectionSuffix.get(SectionType))
                    Num = Num + 1
                    f = open (Filename, 'r')
                    VerString = f.read()
                    VerString = ' -n '          + \
                                ' \"'           + \
                                VerString       + \
                                ' \"'
                    if BuildNum != None and BuildNum != '':
                        BuildNumString = ' -j ' + \
                                         BuildNum
                    GenSectionCmd = 'GenSec -o '                + \
                                     OutputFile                 + \
                                     ' -s EFI_SECTION_VERSION'  + \
                                     VerString                  + \
                                     BuildNumString
                    GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                    OutputFileList.append(OutputFile)
                    
            else:
                if StringData != None:
                    VerString = ' -n '          + \
                                '\"'            + \
                                StringData      + \
                                '\"'
                else:
                    VerString = ''

                if BuildNum != None and BuildNum != '':
                        BuildNumString = ' -j ' + \
                                         BuildNum
                else:
                    BuildNumString = ''
                    
                if VerString == '' and BuildNumString == '':
                    if self.Optional == True :
                        GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                        return [], None
                    else:
                        raise Exception ("File: %s miss Version Section value" %InfFileName)
                GenSectionCmd = 'GenSec -o '                + \
                                     OutputFile                 + \
                                     ' -s EFI_SECTION_VERSION'  + \
                                     VerString                  + \
                                     BuildNumString
                GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                OutputFileList.append(OutputFile)

        #
        # If Section Type is 'UI'
        #
        elif SectionType == 'UI':
            if FileList != []:
                for Filename in FileList:
                    f = open (Filename, 'r')
                    UiString = f.read()
                    UiString = ' -n '         + \
                                '\"'          + \
                                UiString      + \
                                '\"'
                    GenSectionCmd = 'GenSec -o '                       + \
                                 OutputFile                        + \
                                 ' -s EFI_SECTION_USER_INTERFACE'  + \
                                 UiString
                                 
                    GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                    OutputFileList.append(OutputFile)
            else:
                if StringData != None:
                    UiString = ' -n '        + \
                               '\"'          + \
                               StringData    + \
                               '\"'
                else:
                    UiString = ''

                if UiString == '':
                    if self.Optional == True :
                        GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                        return '', None
                    else:
                        raise Exception ("File: %s miss UI Section value" %InfFileName)
                GenSectionCmd = 'GenSec -o '                       + \
                                 OutputFile                        + \
                                 ' -s EFI_SECTION_USER_INTERFACE'  + \
                                 UiString

                GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                OutputFileList.append(OutputFile)

                
        else:
            """If File List is empty"""
            if FileList == [] :
                if self.Optional == True:
                     GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                     return [], None
                else:
                     raise Exception(" %s does't exist" %Filename)
            
            else:
                """Convert the File to Section file one by one """
                for Filename in FileList:
                    """ Copy Map file to FFS output path """
                    Filename = GenFdsGlobalVariable.ExtendMarco(Filename)
                    if Filename[(len(Filename)-4):] == '.efi':
                        MapFile = Filename.replace('.efi', '.map')
                        if os.path.exists(MapFile):
                            CopyMapFile = os.path.join(OutputPath, ModuleName + '.map')
                            shutil.copyfile(MapFile, CopyMapFile)

                    """For TE Section call GenFw to generate TE image"""

                    if SectionType == 'TE':
                        TeFile = os.path.join( OutputPath, ModuleName + 'Te.raw')
                        GenTeCmd = 'GenFW -t '    + \
                                   ' -o '         + \
                                    TeFile        + \
                                    ' '           + \
                                   GenFdsGlobalVariable.ExtendMarco(Filename)
                        GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
                        Filename = TeFile

                    """Call GenSection"""
                    GenSectionCmd = 'GenSec -o '                                         + \
                                         OutputFile                                      + \
                                         ' -s '                                          + \
                                         Section.Section.SectionType.get (SectionType)   + \
                                         ' '                                             + \
                                         GenFdsGlobalVariable.ExtendMarco(Filename)
                        
                    GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                    OutputFileList.append(OutputFile)
            
        return OutputFile , self.Alignment
