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

    def GenSection(self, OutputPath, ModuleName, SecNum, KeyStringList, FfsInf = None, Dict = {}) :
        """Prepare the parameter of GenSection"""
        if FfsInf != None :
            InfFileName = FfsInf.InfFileName
            SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            Filename = FfsInf.__ExtendMarco__(self.FileName)
            """print 'Buile Num: %s' %self.BuildNum"""
            BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            """print 'After extend Build Num: %s' %self.BuildNum"""
            
            StringData = FfsInf.__ExtendMarco__(self.StringData)
            
        else:
            SectionType = self.SectionType
            Filename = self.Filename
            BuildNum = self.BuildNum
            
            InfFileName = ''
        """If the file name was pointed out, add it in FileList"""     
        FileList = []
        if Filename != None:
            Filename = GenFdsGlobalVariable.MacroExtend(Filename, Dict)
            if not self.Optional:
                FileList.append(Filename)
            elif os.path.exists(Filename):                 
                FileList.append(Filename)
        else:
            FileList, IsSect = Section.Section.GetFileList(FfsInf, self.FileType, self.FileExtension, Dict)
            if IsSect :
                return FileList, self.Alignment

        Index = 0
              
        """ If Section type is 'VERSION'"""
        OutputFileList = []
        if SectionType == 'VERSION':
            
            InfOverrideVerString = False
            if FfsInf.ver != None:
                StringData = FfsInf.ver
                InfOverrideVerString = True
            
            if InfOverrideVerString:
                VerString = ' -n '          + \
                                '\"'            + \
                                StringData      + \
                                '\"'
                if BuildNum != None and BuildNum != '':
                        BuildNumString = ' -j ' + \
                                         BuildNum
                else:
                    BuildNumString = ''
                    
                Num = SecNum
                OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + str(Num) + Ffs.SectionSuffix.get(SectionType))
                GenSectionCmd = 'GenSec -o '                + \
                                     OutputFile                 + \
                                     ' -s EFI_SECTION_VERSION'  + \
                                     VerString                  + \
                                     BuildNumString
                GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                OutputFileList.append(OutputFile)    
                
            elif FileList != []:
                for File in FileList:
                    Index = Index + 1
                    Num = '%s.%d' %(SecNum , Index)
                    OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + Num + Ffs.SectionSuffix.get(SectionType))
                    f = open (File, 'r')
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
                if StringData != None and len(StringData) > 0:
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
                Num = SecNum
                OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + str(Num) + Ffs.SectionSuffix.get(SectionType))
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
            
            InfOverrideUiString = False
            if FfsInf.Ui != None:
                StringData = FfsInf.Ui
                InfOverrideUiString = True
            
            if InfOverrideUiString:
                UiString = ' -n '        + \
                               '\"'          + \
                               StringData    + \
                               '\"'
                Num = SecNum
                OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + str(Num) + Ffs.SectionSuffix.get(SectionType))
                GenSectionCmd = 'GenSec -o '                       + \
                                 OutputFile                        + \
                                 ' -s EFI_SECTION_USER_INTERFACE'  + \
                                 UiString

                GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                OutputFileList.append(OutputFile)
                
            elif FileList != []:
                for File in FileList:
                    Index = Index + 1
                    Num = '%s.%d' %(SecNum , Index)
                    OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + Num + Ffs.SectionSuffix.get(SectionType))
                    f = open (File, 'r')
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
                if StringData != None and len(StringData) > 0:
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
                Num = SecNum
                OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + str(Num) + Ffs.SectionSuffix.get(SectionType))
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
                     raise Exception("Section with type %s could not be found for %s" % (SectionType, InfFileName))
            
            else:
                """Convert the File to Section file one by one """
                for File in FileList:
                    """ Copy Map file to FFS output path """
                    Index = Index + 1
                    Num = '%s.%d' %(SecNum , Index)
                    OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + Num + Ffs.SectionSuffix.get(SectionType))
                    File = GenFdsGlobalVariable.MacroExtend(File, Dict)
                    if File[(len(File)-4):] == '.efi':
                        MapFile = File.replace('.efi', '.map')
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
                                   GenFdsGlobalVariable.MacroExtend(File, Dict)
                        GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
                        File = TeFile

                    """Call GenSection"""
                    GenSectionCmd = 'GenSec -o '                                         + \
                                         OutputFile                                      + \
                                         ' -s '                                          + \
                                         Section.Section.SectionType.get (SectionType)   + \
                                         ' '                                             + \
                                         GenFdsGlobalVariable.MacroExtend(File)
                        
                    GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
                    OutputFileList.append(OutputFile)
            
        return OutputFileList, self.Alignment
