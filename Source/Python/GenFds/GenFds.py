## @file
# generate flash image
#
#  Copyright (c) 2007, Intel Corporation
#
#  All rights reserved. This program and the accompanying materials
#  are licensed and made available under the terms and conditions of the BSD License
#  which accompanies this distribution.  The full text of the license may be found at
#  http://opensource.org/licenses/bsd-license.php
#
#  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
#  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
from optparse import OptionParser
import sys
import os
import linecache
import FdfParser
from Common import BuildToolError
from GenFdsGlobalVariable import GenFdsGlobalVariable
from Workspace.WorkspaceDatabase import WorkspaceDatabase
import RuleComplexFile
from EfiSection import EfiSection
import StringIO
import Common.TargetTxtClassObject as TargetTxtClassObject
import Common.DataType
import Common.GlobalData as GlobalData
from Common import EdkLogger
from Common.String import *

## Version and Copyright
versionNumber = "1.0"
__version__ = "%prog Version " + versionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."

## Tool entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
#   @retval 0     Tool was successful
#   @retval 1     Tool failed
#
def main():
    global Options
    Options = myOptionParser()
    global Workspace
    Workspace = ""
    ArchList = None
    ReturnCode = 0

    EdkLogger.Initialize()
    try:
        if Options.verbose != None:
            EdkLogger.SetLevel(EdkLogger.VERBOSE)
            GenFdsGlobalVariable.VerboseMode = True
        if Options.quiet != None:
            EdkLogger.SetLevel(EdkLogger.QUIET)
        if Options.debug != None:
            EdkLogger.SetLevel(Options.debug + 1)
            GenFdsGlobalVariable.DebugLevel = Options.debug
        else:
            EdkLogger.SetLevel(EdkLogger.INFO)

        if (Options.Workspace == None):
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "WORKSPACE not defined",
                            ExtraData="Please use '-w' switch to pass it or set the WORKSPACE environment variable.")
        else:
            Workspace = Options.Workspace
            GenFdsGlobalVariable.WorkSpaceDir = Workspace
            if 'EDK_SOURCE' in os.environ.keys():
                GenFdsGlobalVariable.EdkSourceDir = os.environ['EDK_SOURCE']
            if (Options.debug):
                GenFdsGlobalVariable.VerboseLogger( "Using Workspace:" + Workspace)
        os.chdir(GenFdsGlobalVariable.WorkSpaceDir)

        if (Options.filename):
            FdfFilename = Options.filename
            FdfFilename = GenFdsGlobalVariable.ReplaceWorkspaceMacro(FdfFilename)
        else:
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "Missing FDF filename")

        if (Options.BuildTarget):
            GenFdsGlobalVariable.TargetName = Options.BuildTarget
        else:
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "Missing build target")

        if (Options.ToolChain):
            GenFdsGlobalVariable.ToolChainTag = Options.ToolChain
        else:
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "Missing tool chain tag")

        if FdfFilename[0:2] == '..':
            FdfFilename = os.path.realpath(FdfFilename)
        if FdfFilename[1] != ':':
            FdfFilename = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, FdfFilename)

        if not os.path.exists(FdfFilename):
            EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, ExtraData=FdfFilename)
        GenFdsGlobalVariable.FdfFile = FdfFilename
        GenFdsGlobalVariable.FdfFileTimeStamp = os.path.getmtime(FdfFilename)

        if (Options.activePlatform):
            ActivePlatform = Options.activePlatform
            ActivePlatform = GenFdsGlobalVariable.ReplaceWorkspaceMacro(ActivePlatform)

            if ActivePlatform[0:2] == '..':
                ActivePlatform = os.path.realpath(ActivePlatform)

            if ActivePlatform[1] != ':':
                ActivePlatform = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, ActivePlatform)

            if not os.path.exists(ActivePlatform)  :
                EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, "ActivePlatform doesn't exist!")

            if ActivePlatform.find(Workspace) == -1:
                EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, "ActivePlatform doesn't exist in Workspace!")

            ActivePlatform = ActivePlatform.replace(Workspace, '')
            if len(ActivePlatform) > 0 :
                if ActivePlatform[0] == '\\' or ActivePlatform[0] == '/':
                    ActivePlatform = ActivePlatform[1:]
            else:
                EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, "ActivePlatform doesn't exist!")
        else :
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "Missing active platform")

        GenFdsGlobalVariable.ActivePlatform = NormPath(ActivePlatform)

        if (Options.archList) :
            ArchList = Options.archList.split(',')
        else:
            EdkLogger.error("GenFds", BuildToolError.OPTION_MISSING, "Missing build ARCH")

        BuildConfigurationFile = os.path.normpath(os.path.join(GenFdsGlobalVariable.WorkSpaceDir, "Conf/target.txt"))
        if os.path.isfile(BuildConfigurationFile) == True:
            TargetTxtClassObject.TargetTxtClassObject(BuildConfigurationFile)
        else:
            EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, ExtraData=BuildConfigrationFile)

        if Options.Macros:
            for Pair in Options.Macros:
                Pair.strip('"')
                List = Pair.split('=')
                if len(List) == 2:
                    FdfParser.InputMacroDict[List[0].strip()] = List[1].strip()
                    GlobalData.gGlobalDefines[List[0].strip()] = List[1].strip()
                else:
                    FdfParser.InputMacroDict[List[0].strip()] = None

        """call Workspace build create database"""
        os.environ["WORKSPACE"] = Workspace
        BuildWorkSpace = WorkspaceDatabase(':memory:', GlobalData.gGlobalDefines)
        BuildWorkSpace.InitDatabase()

        for Arch in ArchList:
            GenFdsGlobalVariable.OutputDirFromDscDict[Arch] = NormPath(BuildWorkSpace.BuildObject[ActivePlatform, Arch].OutputDirectory)

        if (Options.outputDir):
            OutputDirFromCommandLine = GenFdsGlobalVariable.ReplaceWorkspaceMacro(Options.outputDir)
            for Arch in ArchList:
                GenFdsGlobalVariable.OutputDirDict[Arch] = OutputDirFromCommandLine
        else:
            for Arch in ArchList:
                GenFdsGlobalVariable.OutputDirDict[Arch] = os.path.join(GenFdsGlobalVariable.OutputDirFromDscDict[Arch], GenFdsGlobalVariable.TargetName + '_' + GenFdsGlobalVariable.ToolChainTag)

        for Key in GenFdsGlobalVariable.OutputDirDict:
            OutputDir = GenFdsGlobalVariable.OutputDirDict[Key]
            if OutputDir[0:2] == '..':
                OutputDir = os.path.realpath(OutputDir)

            if OutputDir[1] != ':':
                OutputDir = os.path.join (GenFdsGlobalVariable.WorkSpaceDir, OutputDir)

            if not os.path.exists(OutputDir):
                EdkLogger.error("GenFds", BuildToolError.FILE_NOT_FOUND, ExtraData=OutputDir)
            GenFdsGlobalVariable.OutputDirDict[Key] = OutputDir

        """ Parse Fdf file, has to place after build Workspace as FDF may contain macros from DSC file """
        FdfParserObj = FdfParser.FdfParser(FdfFilename)
        FdfParserObj.ParseFile()

        if FdfParserObj.CycleReferenceCheck():
            EdkLogger.error("GenFds", BuildToolError.FORMAT_NOT_SUPPORTED, "Cycle Reference Detected in FDF file")

        if (Options.uiFdName) :
            if Options.uiFdName.upper() in FdfParserObj.Profile.FdDict.keys():
                GenFds.currentFd = Options.uiFdName
            else:
                EdkLogger.error("GenFds", BuildToolError.OPTION_VALUE_INVALID,
                                "No such an FD in FDF file: %s" % Options.uiFdName)

        if (Options.uiFvName) :
            if Options.uiFvName.upper() in FdfParserObj.Profile.FvDict.keys():
                GenFds.currentFv = Options.uiFvName
            else:
                EdkLogger.error("GenFds", BuildToolError.OPTION_VALUE_INVALID,
                                "No such an FV in FDF file: %s" % Options.uiFvName)

        """Call GenFds"""
        GenFds.GenFd('', FdfParserObj, BuildWorkSpace, ArchList)
        
        """Display FV space info."""
        GenFds.DisplayFvSpaceInfo(FdfParserObj)
        
    except FdfParser.Warning, X:
        EdkLogger.error(X.ToolName, BuildToolError.FORMAT_INVALID, File=X.FileName, Line=X.LineNumber, ExtraData=X.Message, RaiseError = False)
        ReturnCode = BuildToolError.FORMAT_INVALID
    except FatalError, X:
        if Options.debug != None:
            import traceback
            EdkLogger.quiet(traceback.format_exc())
        ReturnCode = X.args[0]
    except:
        import traceback
        EdkLogger.error(
                    "\nPython",
                    CODE_ERROR,
                    "Tools code failure",
                    ExtraData="Please submit bug report in www.TianoCore.org, attaching following call stack trace!\n",
                    RaiseError=False
                    )
        EdkLogger.quiet(traceback.format_exc())
        ReturnCode = CODE_ERROR
    return ReturnCode

## Parse command line options
#
# Using standard Python module optparse to parse command line option of this tool.
#
#   @retval Opt   A optparse.Values object containing the parsed options
#   @retval Args  Target of build command
#
def myOptionParser():
    usage = "%prog [options] -f input_file -a arch_list -b build_target -p active_platform -t tool_chain_tag -y \"MacroName [= MacroValue]\""
    Parser = OptionParser(usage=usage,description=__copyright__,version="%prog " + str(versionNumber))
    Parser.add_option("-f", "--file", dest="filename", help="Name of FDF file to convert")
    Parser.add_option("-a", "--arch", dest="archList", help="comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt?s TARGET_ARCH")
    Parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    Parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    Parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
    Parser.add_option("-p", "--platform", dest="activePlatform", help="Set the ACTIVE_PLATFORM, overrides target.txt ACTIVE_PLATFORM setting.")
    Parser.add_option("-w", "--workspace", dest="Workspace", default=os.environ.get('WORKSPACE'), help="Set the WORKSPACE")
    Parser.add_option("-o", "--outputDir", dest="outputDir", help="Name of Build Output directory")
    Parser.add_option("-r", "--rom_image", dest="uiFdName", help="Build the image using the [FD] section named by FdUiName.")
    Parser.add_option("-i", "--FvImage", dest="uiFvName", help="Buld the FV image using the [FV] section named by UiFvName")
    Parser.add_option("-b", "--buildtarget", action="store", type="choice", choices=['DEBUG','RELEASE'], dest="BuildTarget", help="Build TARGET is one of list: DEBUG, RELEASE.")
    Parser.add_option("-t", "--tagname", action="store", type="string", dest="ToolChain", help="Using the tools: TOOL_CHAIN_TAG name to build the platform.")
    Parser.add_option("-y", "--define", action="append", type="string", dest="Macros", help="Macro: \"Name [= Value]\".")
    (Options, args) = Parser.parse_args()
    return Options

## The class implementing the EDK2 flash image generation process
#
#   This process includes:
#       1. Collect workspace information, includes platform and module information
#       2. Call methods of Fd class to generate FD
#       3. Call methods of Fv class to generate FV that not belong to FD
#
class GenFds :
    FdfParsef = None
    # FvName in FDF, FvBinFile name
    FvBinDict = {}
    OnlyGenerateThisFd = None
    OnlyGenerateThisFv = None

    ## GenFd()
    #
    #   @param  OutputDir           Output directory
    #   @param  FdfParser           FDF contents parser
    #   @param  Workspace           The directory of workspace
    #   @param  ArchList            The Arch list of platform
    #
    def GenFd (OutputDir, FdfParser, WorkSpace, ArchList):
        GenFdsGlobalVariable.SetDir ('', FdfParser, WorkSpace, ArchList)

        GenFdsGlobalVariable.VerboseLogger("   Gen Fd  !")
        if GenFds.OnlyGenerateThisFd != None and GenFds.OnlyGenerateThisFd.upper() in GenFdsGlobalVariable.FdfParser.Profile.FdDict.keys():
            FdObj = GenFdsGlobalVariable.FdfParser.Profile.FdDict.get(GenFds.OnlyGenerateThisFd.upper())
            if FdObj != None:
                FdObj.GenFd(GenFds.FvBinDict)
        elif GenFds.OnlyGenerateThisFv == None:
            for FdName in GenFdsGlobalVariable.FdfParser.Profile.FdDict.keys():
                FdObj = GenFdsGlobalVariable.FdfParser.Profile.FdDict[FdName]
                FdObj.GenFd(GenFds.FvBinDict)

        GenFdsGlobalVariable.VerboseLogger(" Gen FV ! ")
        if GenFds.OnlyGenerateThisFv != None and GenFds.OnlyGenerateThisFv.upper() in GenFdsGlobalVariable.FdfParser.Profile.FvDict.keys():
            FvObj = GenFdsGlobalVariable.FdfParser.Profile.FvDict.get(GenFds.OnlyGenerateThisFv.upper())
            if FvObj != None:
                Buffer = StringIO.StringIO()
                # Get FV base Address
                FvObj.AddToBuffer(Buffer, None, GenFds.GetFvBlockSize(FvObj))
                Buffer.close()
                return
        elif GenFds.OnlyGenerateThisFd == None:
            for FvName in GenFdsGlobalVariable.FdfParser.Profile.FvDict.keys():
                Buffer = StringIO.StringIO('')
                FvObj = GenFdsGlobalVariable.FdfParser.Profile.FvDict[FvName]
                # Get FV base Address
                FvObj.AddToBuffer(Buffer, None, GenFds.GetFvBlockSize(FvObj))
                Buffer.close()

        if GenFds.OnlyGenerateThisFv == None and GenFds.OnlyGenerateThisFd == None:
            GenFdsGlobalVariable.VerboseLogger(" Gen Capsule !")
            for CapsuleObj in GenFdsGlobalVariable.FdfParser.Profile.CapsuleList:
                CapsuleObj.GenCapsule()

    ## GetFvBlockSize()
    #
    #   @param  FvObj           Whose block size to get
    #   @retval int             Block size value
    #
    def GetFvBlockSize(FvObj):
        FdObj = None
        if GenFds.OnlyGenerateThisFd != None and GenFds.OnlyGenerateThisFd.upper() in GenFdsGlobalVariable.FdfParser.Profile.FdDict.keys():
            FdObj = GenFdsGlobalVariable.FdfParser.Profile.FdDict[GenFds.OnlyGenerateThisFd.upper()]
        if FdObj == None:
            for ElementFd in GenFdsGlobalVariable.FdfParser.Profile.FdDict.values():
                for ElementRegion in ElementFd.RegionList:
                    if ElementRegion.RegionType == 'FV':
                        for ElementRegionData in ElementRegion.RegionDataList:
                            if ElementRegionData != None and ElementRegionData.upper() == FvObj.UiFvName:
                                if FvObj.BlockSizeList != []:
                                    return FvObj.BlockSizeList[0][0]
                                else:
                                    return ElementRegion.BlockSizeOfRegion(ElementFd.BlockSizeList)
            return 0x10000
        else:
            for ElementRegion in FdObj.RegionList:
                    if ElementRegion.RegionType == 'FV':
                        for ElementRegionData in ElementRegion.RegionDataList:
                            if ElementRegionData != None and ElementRegionData.upper() == FvObj.UiFvName:
                                if FvObj.BlockSizeList != []:
                                    return FvObj.BlockSizeList[0][0]
                                else:
                                    return ElementRegion.BlockSizeOfRegion(ElementFd.BlockSizeList)
            return 0x10000

    
    def DisplayFvSpaceInfo(FdfParser):
        
        FvSpaceInfoList = []
        MaxFvNameLength = 0
        for FvName in FdfParser.Profile.FvDict:
            if len(FvName) > MaxFvNameLength:
                MaxFvNameLength = len(FvName)
            FvSpaceInfoFileName = os.path.join(GenFdsGlobalVariable.FfsDir, FvName.upper() + '.inf')
            if os.path.exists(FvSpaceInfoFileName):
                FileLinesList = linecache.getlines(FvSpaceInfoFileName)
                TotalFound = False
                Total = ''
                UsedFound = False
                Used = ''
                FreeFound = False
                Free = ''
                for Line in FileLinesList:
                    NameValue = Line.split('=')
                    if len(NameValue) == 2:
                        if NameValue[0].strip() == 'EFI_FV_TOTAL_SIZE':
                            TotalFound = True
                            Total = NameValue[1].strip()
                        if NameValue[0].strip() == 'EFI_FV_TAKEN_SIZE':
                            UsedFound = True
                            Used = NameValue[1].strip()
                        if NameValue[0].strip() == 'EFI_FV_SPACE_SIZE':
                            FreeFound = True
                            Free = NameValue[1].strip()
                
                if TotalFound and UsedFound and FreeFound:
                    FvSpaceInfoList.append((FvName, Total, Used, Free))
                
        GenFdsGlobalVariable.InfLogger('\nFV Space Information')
        for FvSpaceInfo in FvSpaceInfoList:
            Name = FvSpaceInfo[0]
            TotalSizeValue = long(FvSpaceInfo[1], 0)
            UsedSizeValue = long(FvSpaceInfo[2], 0)
            FreeSizeValue = long(FvSpaceInfo[3], 0)
            GenFdsGlobalVariable.InfLogger(Name + ' ' + '[' + str((UsedSizeValue+0.0)/TotalSizeValue)[0:4].lstrip('0.') + '%Full] ' + str(TotalSizeValue) + ' total, ' + str(UsedSizeValue) + ' used, ' + str(FreeSizeValue) + ' free')

    ##Define GenFd as static function
    GenFd = staticmethod(GenFd)
    GetFvBlockSize = staticmethod(GetFvBlockSize)
    DisplayFvSpaceInfo = staticmethod(DisplayFvSpaceInfo)

if __name__ == '__main__':
    sys.exit(main())

