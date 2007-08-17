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
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None :
            InfFileName = FfsInf.InfFileName
            SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            #print 'File Name : %s' %self.Filename
            Filename = FfsInf.__ExtendMarco__(self.Filename)
            #print 'After Extend File Name: %s' %self.Filename
            #print 'Buile Num: %s' %self.BuildNum
            BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            #print 'After extend Build Num: %s' %self.BuildNum
            #print 'version Num: %s' %self.VersionNum
            VersionNum = FfsInf.__ExtendMarco__(self.VersionNum)
            #print 'After extend Version Num: %s' %self.VersionNum
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
            
        OutputFile = os.path.join( OutputPath, ModuleName + 'SEC' + SecNum + Ffs.SectionSuffix.get(SectionType))
        #
        #  If Section type is 'VERSION'
        #
        if SectionType == 'VERSION':
            if Filename != None:
                Filename = GenFdsGlobalVariable.ReplaceWorkspaceMarco(Filename)
                f = open (Filename, 'r')
                VerString = f.read()
                VerString = ' -n '           + \
                             ' \"'           + \
                             VerString       + \
                             ' \"'
                             
            elif StringData != None:
                VerString = ' -n '          + \
                            '\"'            + \
                            StringData      + \
                            '\"'
            else:
                VerString = ''
                             
            if BuildNum != None and BuildNum != '':
                BuildNumString = ' -j ' + \
                                 BuildNum
            else :
                BuildNumString = ''
            if VerString == '' and BuildNumString == '':
                if self.Optional == True :
                    GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                    return '', None
                else:
                    raise Exception ("File: %s miss Version Section value" %InfFileName)
            GenSectionCmd = 'GenSec -o '                + \
                             OutputFile                 + \
                             ' -s EFI_SECTION_VERSION'  + \
                             VerString                  + \
                             BuildNumString
            
        #
        # If Section Type is 'UI'
        #
        elif SectionType == 'UI':
            #if self.Filename != None :
            #    f = open (self.Filename, 'r')
            #    UiString = f.read ()
            #    f.close()
            #    UiString = ' -n '    + \
            #                '\"'     + \
            #                UiString + \
            #                '\"'
            if Filename != None:
               Filename = GenFdsGlobalVariable.ReplaceWorkspaceMarco(Filename)
               f = open (Filename, 'r')
               UiString = f.read()
               UiString = ' -n '         + \
                           '\"'          + \
                           UiString      + \
                           '\"'
                           
            elif StringData != None:
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
        else:
             if Filename == None or not os.path.exists(Filename) :
                 if self.Optional == True:
                     GenFdsGlobalVariable.VerboseLogger( "Optional Section don't exist!")
                     return '', None
                 else:
                     raise Exception(" %s does't exist" %Filename)
             #
             # For TE Section call GenFw to generate TE image
             #
             if SectionType == 'TE':
                 TeFile = os.path.join( OutputPath, ModuleName + 'Te.raw')
                 GenTeCmd = 'GenFW -t '    + \
                            ' -o '         + \
                             TeFile        + \
                             ' '           + \
                             GenFdsGlobalVariable.ExtendMarco(Filename)
                 GenFdsGlobalVariable.CallExternalTool(GenTeCmd, "GenFw Failed !")
                 
                 """ Copy Map file to FFS output path """
                 Filename = GenFdsGlobalVariable.ExtendMarco(Filename)
                 if Filename[(len(Filename)-4):] == '.efi':
                     MapFile = Filename.replace('.efi', '.map')
                     if os.path.exists(MapFile):
                         CopyMapFile = os.path.join(OutputPath, ModuleName + '.map')
                         shutil.copyfile(MapFile, CopyMapFile)
                 Filename = TeFile

                 
             GenSectionCmd = 'GenSec -o '                                     + \
                              OutputFile                                      + \
                              ' -s '                                          + \
                              Section.Section.SectionType.get (SectionType)   + \
                              ' '                                             + \
                              GenFdsGlobalVariable.ExtendMarco(Filename)

             """ Copy Map file to FFS output path """
             if SectionType != 'TE':
                 Filename = GenFdsGlobalVariable.ExtendMarco(Filename)
                 if Filename[(len(Filename)-4):] == '.efi':
                     MapFile = Filename.replace('.efi', '.map')
                     if os.path.exists(MapFile):
                         CopyMapFile = os.path.join(OutputPath, ModuleName + '.map')
                         shutil.copyfile(MapFile, CopyMapFile)

        #
        # Call GenSection
        #
        
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
        return OutputFile , self.Alignment
