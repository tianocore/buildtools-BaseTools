import Section
from GenFdsGlobalVariable import GenFdsGlobalVariable
import subprocess
from Ffs import Ffs

class EfiSection (Section.Section):
    
    def __init__(self):
        
        self.SectionType = None
        self.Optional = False
        # store file name composed of MACROs
        self.Filename = None
        self.BuildNum = None
        self.VersionNum = None

    def GenSection(self, OutputPath, ModuleName, FfsInf = None):
        #
        # Prepare the parameter of GenSection
        #
        if FfsInf != None :
            self.SectionType = FfsInf.__ExtendMarco__(self.SectionType)
            self.Filename = FfsInf.__ExtendMarco__(self.Filename)
            self.BuildNum = FfsInf.__ExtendMarco__(self.BuildNum)
            self.VersionNum = FfsInf.__ExtendMarco__(self.VersionNum)
            
        print '### EfiSection  Line 21##'
        print self.SectionType
        OutputFile = OutputPath + \
                     ModuleName + \
                     Ffs.SectionSuffix.get(self.SectionType)
        #
        #  If Section type is 'VERSION'
        #
        if self.SectionType == 'VERSION':
            if self.VersionNum != None:
                VerString = ' - n '          + \
                             ' \"'           + \
                             self.VersionNum + \
                             ' \"'
            else:
                VerString = ''
                             
            if self.BuildNum != None :
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
            if self.Filename != None :
                f = open (self.Filename, 'r')
                UiString = f.read ()
                f.close()
                UiString = ' -n '    + \
                            '\"'     + \
                            UiString + \
                            '\"'
            else:
                UiString = ''
            GenSectionCmd = 'GenSection -o '            + \
                             OutputFile                 + \
                             ' -s EFI_SECTION_VERSION'  + \
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
        subprocess.Popen (GenSectionCmd).communicate()

        return OutputFile
