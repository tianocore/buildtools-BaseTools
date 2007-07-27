from optparse import OptionParser
import sys
import os
import FdfParser
from GenFdsGlobalVariable import GenFdsGlobalVariable
import Common.EdkIIWorkspaceBuild
import RuleComplexFile
from EfiSection import EfiSection
import StringIO
import Common.TargetTxtClassObject
import Common.DataType
from Common import EdkLogger
versionNumber = "1.0"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."


def main():
    global options
    options = myOptionParser()
    global workspace
    workspace = ""
    ArchList = None

    if options.verbose != None:
        EdkLogger.setLevel(EdkLogger.VERBOSE)
    elif options.quiet != None:
        EdkLogger.setLevel(EdkLogger.QUIET)
    elif options.debug != None:
        EdkLogger.setLevel(options.debug)
    else:
        EdkLogger.setLevel(EdkLogger.INFO)
        
    if (options.workspace == None):
        GenFdsGlobalVariable.InfLogger("ERROR: E0000: WORKSPACE not defined.\n  Please set the WORKSPACE environment variable to the location of the EDK II install directory.")
        sys.exit(1)
    else:
        workspace = options.workspace
        GenFdsGlobalVariable.WorkSpaceDir = workspace
        if (options.debug):
            GenFdsGlobalVariable.VerboseLogger( "Using Workspace:", workspace)

    if (options.filename):
        fdfFilename = options.filename
    else:
        GenFdsGlobalVariable.InfLogger("ERROR: E0001 - You must specify an input filename")
        sys.exit(1)

    if not os.path.exists(fdfFilename):
        GenFdsGlobalVariable.InfLogger ("ERROR: E1000: File %s not found" % (filename))
        sys.exit(1)

    if (options.activePlatform):
        activePlatform = options.activePlatform
        activePlatform = os.path.realpath(activePlatform)
        
        if not os.path.exists(activePlatform)  :
            raise Exception ("ActivePlatform doesn't exist!")
        
        if activePlatform.find(workspace) == -1:
            raise Exception ("ActivePlatform doesn't exist in Workspace!")
        
        activePlatform = activePlatform.replace(workspace, '')
        if len(activePlatform) > 0 :
            activePlatform = activePlatform[1:]
        else:
            raise Exception ("ActivePlatform doesn't exist!")
    else :
        Target = Common.TargetTxtClassObject.TargetTxtDict(GenFdsGlobalVariable.WorkSpaceDir)
        activePlatform = Target.TargetTxtDictionary[Common.DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]

    GenFdsGlobalVariable.ActivePlatform = activePlatform
        
    if (options.outputDir):
        outputDir = options.outputDir
    else:
        #print "ERROR: E0001 - You must specify an Output directory"
        GenFdsGlobalVariable.InfLogger("ERROR: E0001 - You must specify an Output directory")
        sys.exit(1)
        
    if (options.archList) :
        archList = options.archList.split(',')
    else:
        Target = Common.TargetTxtClassObject.TargetTxtDict(GenFdsGlobalVariable.WorkSpaceDir)
        archList = Target.TargetTxtDictionary['TARGET_ARCH']
        
    """ Parse Fdf file """
    fdfParser = FdfParser.FdfParser(fdfFilename)
    fdfParser.ParseFile()
    
    """call workspace build create database"""
    os.environ["WORKSPACE"] = workspace
    buildWorkSpace = Common.EdkIIWorkspaceBuild.WorkspaceBuild(GenFdsGlobalVariable.ActivePlatform, GenFdsGlobalVariable.WorkSpaceDir)
    buildWorkSpace.GenBuildDatabase()
    
    """Call GenFds"""
    GenFds.GenFd(outputDir, fdfParser, buildWorkSpace, archList)
    
def myOptionParser():
    usage = "%prog [options] -f input_file"
    parser = OptionParser(usage=usage,description=__copyright__,version="%prog " + str(versionNumber))
    parser.add_option("-f", "--file", dest="filename", help="Name of FDF file to convert")
    parser.add_option("-a", "--arch", dest="archList", help="comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt?s TARGET_ARCH")
    parser.add_option("-i", "--interactive", action="store_true", dest="interactive", default=False, help="Set Interactive mode, user must approve each change.")
    parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
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

        GenFdsGlobalVariable.VerboseLogger("   Gen Fd  !")
        for item in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
            fd = GenFdsGlobalVariable.FdfParser.profile.FdDict[item]
            fd.GenFd(GenFds.FvBinDict)
            
        GenFdsGlobalVariable.VerboseLogger(" Gen FV ! ")
        for FvName in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
            if not FvName in GenFds.FvBinDict.keys():
                Buffer = StringIO.StringIO()
                fv = GenFdsGlobalVariable.FdfParser.profile.FvDict[FvName]
                fv.AddToBuffer(Buffer)
                Buffer.close()
        
        GenFdsGlobalVariable.VerboseLogger(" Gen Capsule !")
        for capsule in GenFdsGlobalVariable.FdfParser.profile.CapsuleList:
            capsule.GenCapsule()


    """Define GenFd as static function"""
    GenFd = staticmethod(GenFd)

if __name__ == '__main__':
    
    main()
