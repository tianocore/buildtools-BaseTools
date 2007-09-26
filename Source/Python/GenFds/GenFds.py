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
from Common.String import *

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
        GenFdsGlobalVariable.VerboseMode = True
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
        fdfFilename = GenFdsGlobalVariable.ReplaceWorkspaceMarco(fdfFilename)
    else:
        GenFdsGlobalVariable.InfLogger("ERROR: E0001 - You must specify an input filename")
        sys.exit(1)

    if fdfFilename[0:2] == '..':
        fdfFilename = os.path.realpath(fdfFilename)
    if fdfFilename[1] != ':':
        fdfFilename = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, fdfFilename)
            
    if not os.path.exists(fdfFilename):
        GenFdsGlobalVariable.InfLogger ("ERROR: E1000: File %s not found" % (fdfFilename))
        sys.exit(1)

    if (options.activePlatform):
        activePlatform = options.activePlatform
        activePlatform = GenFdsGlobalVariable.ReplaceWorkspaceMarco(activePlatform)

        if activePlatform[0:2] == '..':
            activePlatform = os.path.realpath(activePlatform)

        if activePlatform[1] != ':':
            activePlatform = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, activePlatform)

        if not os.path.exists(activePlatform)  :
            raise Exception ("ActivePlatform doesn't exist!")
        
        if activePlatform.find(workspace) == -1:
            raise Exception ("ActivePlatform doesn't exist in Workspace!")
        
        activePlatform = activePlatform.replace(workspace, '')
        if len(activePlatform) > 0 :
            if activePlatform[0] == '\\' or activePlatform[0] == '/':
                activePlatform = activePlatform[1:]
        else:
            raise Exception ("ActivePlatform doesn't exist!")
    else :
        Target = Common.TargetTxtClassObject.TargetTxtDict(GenFdsGlobalVariable.WorkSpaceDir)
        activePlatform = Target.TargetTxtDictionary[Common.DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]

    GenFdsGlobalVariable.ActivePlatform = NormPath(activePlatform)
        
    if (options.outputDir):
        outputDir = options.outputDir
        outputDir = GenFdsGlobalVariable.ReplaceWorkspaceMarco(outputDir)
    else:
        #print "ERROR: E0001 - You must specify an Output directory"
        GenFdsGlobalVariable.InfLogger("ERROR: E0001 - You must specify an Output directory")
        sys.exit(1)

    if outputDir[0:2] == '..':
        outputDir = os.path.realpath(outputDir)
        
    if outputDir[1] != ':':
        outputDir = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, outputDir)

    if not os.path.exists(outputDir):
        GenFdsGlobalVariable.InfLogger ("ERROR: E1000: Directory %s not found" % (outputDir))
        sys.exit(1)

    if (options.archList) :
        archList = options.archList.split(',')
    else:
        Target = Common.TargetTxtClassObject.TargetTxtDict(GenFdsGlobalVariable.WorkSpaceDir)
        archList = Target.TargetTxtDictionary['TARGET_ARCH']
        
    """ Parse Fdf file """
    fdfParser = FdfParser.FdfParser(fdfFilename)
    fdfParser.ParseFile()
    
    
    if (options.uiFdName) :
        if options.uiFdName.upper() in fdfParser.profile.FdDict.keys():
            GenFds.currentFd = options.uiFdName
        else:
            GenFdsGlobalVariable.InfLogger("ERROR: E0001 - No such an FD in FDF file.")
            sys.exit(1)

    if (options.uiFvName) :
        if options.uiFvName.upper() in fdfParser.profile.FvDict.keys():
            GenFds.currentFv = options.uiFvName
        else:
            GenFdsGlobalVariable.InfLogger("ERROR: E0001 - No such an FV in FDF file.")
            sys.exit(1)
        
    """call workspace build create database"""
    os.environ["WORKSPACE"] = workspace
    buildWorkSpace = Common.EdkIIWorkspaceBuild.WorkspaceBuild(GenFdsGlobalVariable.ActivePlatform, GenFdsGlobalVariable.WorkSpaceDir)
    buildWorkSpace.GenBuildDatabase({}, fdfParser.profile.InfList)
    
    """Call GenFds"""
    GenFds.GenFd(outputDir, fdfParser, buildWorkSpace, archList)
    print "\nDone!\n"
    
def myOptionParser():
    usage = "%prog [options] -f input_file"
    parser = OptionParser(usage=usage,description=__copyright__,version="%prog " + str(versionNumber))
    parser.add_option("-f", "--file", dest="filename", help="Name of FDF file to convert")
    parser.add_option("-a", "--arch", dest="archList", help="comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt?s TARGET_ARCH")
    parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
    parser.add_option("-p", "--platform", dest="activePlatform", help="Set the Active platform")
    parser.add_option("-w", "--workspace", dest="workspace", default=str(os.environ.get('WORKSPACE')), help="Set the WORKSPACE")
    parser.add_option("-o", "--outputDir", dest="outputDir", help="Name of Build Output directory")
    parser.add_option("-r", "--rom_image", dest="uiFdName", help="Build the image using the [FD] section named by FdUiName.")
    parser.add_option("-i", "--FvImage", dest="uiFvName", help="Buld the FV image using the [FV] section named by UiFvName")
    (options, args) = parser.parse_args()
    return options


class GenFds :
    FdfParsef = None
    FvBinDict = {}      # FvName in Fdf, FvBinFile
    OnlyGenerateThisFd = None
    OnlyGenerateThisFv = None
#    CurrentFdName = None
#    CurrentFvName = None
    
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
        ruleComplexFile1.Alignment = 32
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
        if GenFds.OnlyGenerateThisFd != None and GenFds.OnlyGenerateThisFd.upper() in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
            fd = GenFdsGlobalVariable.FdfParser.profile.FdDict.get(GenFds.OnlyGenerateThisFd.upper())
            if fd != None:
                fd.GenFd(GenFds.FvBinDict)
        elif GenFds.OnlyGenerateThisFv == None:
            for item in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
                fd = GenFdsGlobalVariable.FdfParser.profile.FdDict[item]
                fd.GenFd(GenFds.FvBinDict)
            
        GenFdsGlobalVariable.VerboseLogger(" Gen FV ! ")
        if GenFds.OnlyGenerateThisFv != None and GenFds.OnlyGenerateThisFv.upper() in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
            fv = GenFdsGlobalVariable.FdfParser.profile.FvDict.get(GenFds.OnlyGenerateThisFv.upper())
            if fv != None:
                Buffer = StringIO.StringIO()
                # Get FV base Address
                fv.AddToBuffer(Buffer, None, GenFds.GetFvBlockSize(fv))
                Buffer.close()
                return
        elif GenFds.OnlyGenerateThisFd == None:
            for FvName in GenFdsGlobalVariable.FdfParser.profile.FvDict.keys():
                if not FvName in GenFds.FvBinDict.keys():
                    Buffer = StringIO.StringIO()
                    fv = GenFdsGlobalVariable.FdfParser.profile.FvDict[FvName]
                    # Get FV base Address
                    fv.AddToBuffer(Buffer, None, GenFds.GetFvBlockSize(fv))
                    Buffer.close()
        
        if GenFds.OnlyGenerateThisFv == None and GenFds.OnlyGenerateThisFd == None:
            GenFdsGlobalVariable.VerboseLogger(" Gen Capsule !")
            for capsule in GenFdsGlobalVariable.FdfParser.profile.CapsuleList:
                capsule.GenCapsule()

    def GetFvBlockSize(fv):
        fd = None
        if GenFds.OnlyGenerateThisFd != None and GenFds.OnlyGenerateThisFd.upper() in GenFdsGlobalVariable.FdfParser.profile.FdDict.keys():
            fd = GenFdsGlobalVariable.FdfParser.profile.FdDict[GenFds.OnlyGenerateThisFd.upper()]
        if fd == None:
            for elementFd in GenFdsGlobalVariable.FdfParser.profile.FdDict.values():
                for elementRegion in elementFd.RegionList:
                    if elementRegion.RegionType == 'FV':
                        for elementRegionData in elementRegion.RegionDataList:
                            if elementRegionData != None and elementRegionData.upper() == fv.UiFvName:
                                if fv.BlockSizeList != []:
                                    return fv.BlockSizeList[0][0]
                                else:
                                    return elementRegion.BlockSizeOfRegion(elementFd.BlockSizeList)
            return 0x10000
        else:
            for elementRegion in fd.RegionList:
                    if elementRegion.RegionType == 'FV':
                        for elementRegionData in elementRegion.RegionDataList:
                            if elementRegionData != None and elementRegionData.upper() == fv.UiFvName:
                                if fv.BlockSizeList != []:
                                    return fv.BlockSizeList[0][0]
                                else:
                                    return elementRegion.BlockSizeOfRegion(elementFd.BlockSizeList)
            return 0x10000
        
    """Define GenFd as static function"""
    GenFd = staticmethod(GenFd)
    GetFvBlockSize = staticmethod(GetFvBlockSize)

if __name__ == '__main__':
    
    main()
