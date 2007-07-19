from optparse import OptionParser
import sys
import os
import FdfParser
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Common.EdkIIWorkspaceBuild
import RuleComplexFile
from EfiSection import EfiSection
import StringIO

versionNumber = "1.0"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."


def main():
    global options
    options = myOptionParser()
    global workspace
    workspace = ""
    ArchList = None
    
    if (options.workspace == None):
        print "ERROR: E0000: WORKSPACE not defined.\n  Please set the WORKSPACE environment variable to the location of the EDK II install directory."
        sys.exit(1)
    else:
        workspace = options.workspace
        if (options.debug):
            print "Using Workspace:", workspace

    if (options.filename):
        fdfFilename = options.filename
    else:
        print "ERROR: E0001 - You must specify an input filename"
        sys.exit(1)

    if not os.path.exists(fdfFilename):
        print "ERROR: E1000: File %s not found" % (filename)
        sys.exit(1)

    if (options.activePlatform):
        activePlatform = options.activePlatform
    else :
        activePlatform = None
        
    if (options.outputDir):
        outputDir = options.outputDir
    else:
        print "ERROR: E0001 - You must specify an Output directory"
        sys.exit(1)
        
    if (options.archList) :
        archList = options.archList.split(',')
    else:
        archList = None
        
    """ Parse Fdf file """
    fdfParser = FdfParser.FdfParser(fdfFilename)
    fdfParser.ParseFile()
    
    """call workspace build create database"""
    os.environ["WORKSPACE"] = workspace
    buildWorkSpace = Common.EdkIIWorkspaceBuild.WorkspaceBuild(activePlatform)
    
    """Call GenFds"""
    GenFds.GenFd(outputDir, fdfParser, buildWorkSpace, archList)
    
def myOptionParser():
    usage = "%prog [options] -f input_file"
    parser = OptionParser(usage=usage,description=__copyright__,version="%prog " + str(versionNumber))
    parser.add_option("-f", "--file", dest="filename", help="Name of FDF file to convert")
    parser.add_option("-a", "--arch", dest="archList", help="comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt?s TARGET_ARCH")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="Set Interactive mode, user must approve each change.")
    parser.add_option("-q", "--quiet", action="store_const", const=0, dest="verbose", help="Do not print any messages, just return either 0 for succes or 1 for failure")
    parser.add_option("-v", "--verbose", action="count", dest="verbose", default=0, help="Do not print any messages, just return either 0 for succes or 1 for failure")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", default=False, help="Enable printing of debug messages.")
    parser.add_option("-p", "--platform", dest="activePlatform", help="Set the Active platform")
    parser.add_option("-w", "--workspace", dest="workspace", default=str(os.environ.get('WORKSPACE')), help="Enable printing of debug messages.")
    parser.add_option("-o", "--outputDir", dest="outputDir", help="Name of Output directory")
    (options, args) = parser.parse_args()
    return options


class GenFds :
    FdfParsef = None
    FvBinDict = {}      # FvName in Fdf, FvBinFile
    
    def GenFd (OutputDir, FdfParser, WorkSpace, ArchList):
        GenFdsGlobalVariable.SetDir (OutputDir, FdfParser, WorkSpace, ArchList)
        """Set Default Rule! Hard code here will be move"""
        verSection1 = EfiSection()
        verSection1.BuildNum = "$(BUILD_NUMBER)"
        verSection1.SectionType = "VERSION"
        verSection1.Filename = "$(INF_VERSION)"
        verSection1.VersionNum = "$(INF_VERSION)"
        
        uiSection1 = EfiSection()
        uiSection1.SectionType = 'UI'
        uiSection1.Filename = "$(INF_VERSION)"
        uiSection1.VersionNum = "$(INF_VERSION)"

        dataSection = EfiSection()
        dataSection.SectionType = "PE32"
        dataSection.Filename = "$(INF_OUTPUT)/$(MODULE_NAME).efi"

        ruleComplexFile1 = RuleComplexFile.RuleComplexFile()
        ruleComplexFile1.Alignment = 16
        ruleComplexFile1.Arch = 'COMMON'
        ruleComplexFile1.CheckSum = True
        ruleComplexFile1.Fixed = True
        ruleComplexFile1.FvType = "APPLICATION"
        ruleComplexFile1.ModuleType = "UEFI_APPLICATION"
        ruleComplexFile1.NameGuid = "$(MODULE_NAME)"
        ruleComplexFile1.TemplateName = ''
        ruleComplexFile1.SectionList = [uiSection1, verSection1, dataSection]
        GenFdsGlobalVariable.SetDefaultRule(ruleComplexFile1)
        
        for item in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
            fd = GenFdsGlobalVariable.FdfParser.profile.FdDict[item]
            fd.GenFd(GenFds.FvBinDict)
        for FvName in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
            if not FvName in GenFds.FvBinDict.keys():
                Buffer = StringIO.StringIO()
                fv = GenFdsGlobalVariable.FdfParser.profile.FvDict[FvName]
                fv.AddToBuffer(Buffer)
                Buffer.close()
                
        #print "#########   Gen Capsule              ####################"
        for capsule in GenFdsGlobalVariable.FdfParser.profile.CapsuleList:
            capsule.GenCapsule()

##        for vtf in GenFdsGlobalVariable.FdfParser.profile.VtfList:
##            vtf.GenVtf()

    #Finish GenFd()
    def GenVTFList() :
        for item in GenFdsGlobalVariable.FdfParser.profile.VtfList:
            for comp in item.ComponentStatementList:
                if comp.CompLoc != None :
                    compList.append(comp.Loc)
            GenFdsGlobalVariable.VtfDict[item.UiName] = compList
    #
    # Define GenFd as static function
    #
    GenFd = staticmethod(GenFd)

if __name__ == '__main__':
    
    main()
