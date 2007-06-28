import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs
import os

class EfiSection (Section.Section):
    
    def __init__(self):
        
        self.SectionType = None
        self.Optional = False
        # store file name composed of MACROs
        # Currently only support the String after UI section
        self.Filename = None
        self.BuildNum = None
        self.VersionNum = None

    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None :
            self.SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            print 'File Name : %s' %self.Filename
            self.Filename = FfsInf.__ExtendMarco__(self.Filename)
            print 'After Extend File Name: %s' %self.Filename
            print 'Buile Num: %s' %self.BuildNum
            self.BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            print 'After extend Build Num: %s' %self.BuildNum
            print 'version Num: %s' %self.VersionNum
            self.VersionNum = FfsInf.__ExtendMarco__(self.VersionNum)
            print 'After extend Version Num: %s' %self.VersionNum
            
        print '### EfiSection  Line 21##'
        print self.SectionType
        OutputFile = os.path.join( OutputPath, ModuleName + Ffs.SectionSuffix.get(self.SectionType))
        #
        #  If Section type is 'VERSION'
        #
        if self.SectionType == 'VERSION':
            if self.Filename != None:
                VerString = ' -n '           + \
                             ' \"'           + \
                             self.Filename   + \
                             ' \"'
            else:
                VerString = ''
                             
            if self.BuildNum != None and self.BuildNum != '':
                BuildNumString = ' -j ' + \
                                 self.BuildNum
            else :
                BuildNumString = ''
                                 
            GenSectionCmd = 'GenSection -o '            + \
                             OutputFile                 + \
                             ' -s EFI_SECTION_VERSION'  + \
                             VerString                  + \
                             BuildNumString
        #
        # If Section Type is 'UI'
        #
        elif self.SectionType == 'UI':
            #if self.Filename != None :
            #    f = open (self.Filename, 'r')
            #    UiString = f.read ()
            #    f.close()
            #    UiString = ' -n '    + \
            #                '\"'     + \
            #                UiString + \
            #                '\"'
            if self.Filename != None:
                UiString = ' -n '        + \
                           '\"'          + \
                           self.Filename + \
                           '\"'
            else:
                UiString = ''
            GenSectionCmd = 'GenSection -o '                   + \
                             OutputFile                        + \
                             ' -s EFI_SECTION_USER_INTERFACE'  + \
                             UiString
        else:
             GenSectionCmd = 'GenSection -o '                                 + \
                              OutputFile                                      + \
                              ' -s '                                          + \
                              Section.Section.SectionType.get (self.SectionType)  + \
                              ' '                                             + \
                              GenFdsGlobalVariable.ExtendMarco(self.Filename)
        #
        # Call GenSection
        #
        print GenSectionCmd
        PopenObject = subprocess.Popen (GenSectionCmd)
        PopenObject.communicate()
        if PopenObject.returncode != 0:
            raise Exception ("GenSection Failed !")

        return OutputFile
