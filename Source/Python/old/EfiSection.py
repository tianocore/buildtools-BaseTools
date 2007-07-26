import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs
import os

class EfiSection (Section.Section):
    
    def __init__(self):
        self.Alignment = None
        self.SectionType = None
        self.Optional = False
        # store file name composed of MACROs
        # Currently only support the String after UI section
        self.Filename = None
        self.BuildNum = None
        self.VersionNum = None

    def GenSection(self, OutputPath, ModuleName, KeyStringList, FfsInf = None) :
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
        else:
            SectionType = self.SectionType
            Filename = self.Filename
            BuildNum = self.BuildNum
            VerstionNum = self.VersionNum
            InfFileName = ''
            
        if self.Optional == True :
            if Filename == None or Filename =='':
                print "Optional Section don't exist!"
                return '', None
            
        OutputFile = os.path.join( OutputPath, ModuleName + Ffs.SectionSuffix.get(SectionType))
        #
        #  If Section type is 'VERSION'
        #
        if SectionType == 'VERSION':
            if Filename != None:
                VerString = ' -n '           + \
                             ' \"'           + \
                             Filename        + \
                             ' \"'
            else:
                VerString = ''
                             
            if BuildNum != None and BuildNum != '':
                BuildNumString = ' -j ' + \
                                 BuildNum
            else :
                BuildNumString = ''
            if VerString == '' and BuildNumString == '':
                if self.Optional == True :
                    print "Optional Section don't exist!"
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
                UiString = ' -n '        + \
                           '\"'          + \
                           Filename      + \
                           '\"'
            else:
                UiString = ''

            if UiString == '':
                if self.Optional == True :
                    print "Optional Section don't exist!"
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
                     print "Optional Section don't exist!"
                     return '', None
                 else:
                     raise Exception(" %s does't exist" %Filename)
                 
             GenSectionCmd = 'GenSec -o '                                     + \
                              OutputFile                                      + \
                              ' -s '                                          + \
                              Section.Section.SectionType.get (SectionType)   + \
                              ' '                                             + \
                              GenFdsGlobalVariable.ExtendMarco(Filename)
        #
        # Call GenSection
        #
        print GenSectionCmd
        GenFdsGlobalVariable.CallExternalTool(GenSectionCmd, "GenSection Failed !")
        return OutputFile , self.Alignment
