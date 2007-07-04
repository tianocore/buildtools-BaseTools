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

import os, sys, string, glob, time
from optparse import OptionParser
from os.path import normpath

from subprocess import *

from TargetTxtClassObject import *
from EdkIIWorkspaceBuild import *
from AutoGen import *

VersionNumber = "0.01"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."


# target, command options process
##-a, --arch <ARCHS>
##      ARCHS is a comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt?s TARGET_ARCH
##-p, --platform PlatformName.dsc
##      Build the platform specified by the DSC file name argument, over rides the ACTIVE_PLATFORM
##-m, --module Module.inf
##      Build the module specified by the INF file name argument.
##-b, --buildtarget BuildTarget
##      Build the platform using the BuildTarget, overrides target.txt?s TARGET definition.
##-t, --tagname Tagname
##      Build the platform using the Tool chain, Tagname, overrides target.txt?s TOOL_CHAIN_TAG definition.
##-s, --spawn
##      If this flag is specified, the first two phases, AutoGen and MAKE are mixed, such that as soon as a module can be built, the build will start, without waiting for AutoGen to complete on remaining modules.  While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.
##-n #
##      Build the platform using multi-threaded compiler with # threads, values less than 2 will disable multi-thread builds.  Overrides target.txt?s MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER
##-f, --fdf Filename.fdf
##      The name of the FDF file to use, over-riding the setting in the DSC file.
##-k, --msft
##      Make Option: Generate only NMAKE Makefiles: Makefile
##-g, --gcc
##      Make Option: Generate only GMAKE Makefiles: GNUmakefile
##-l, --all
##      Make Option: Generate both NMAKE and GMAKE makefiles.

# VFR related options: should not be in this tool
##-r, --vfr VfrScriptFile
##      VFR Option: Name of the VFR Script File to use
##-e, --CreateC [Filename]
##      VFR Option: [DEFAULT] Create the C File, named Filename, otherwise use the VfrScriptFile name as the C code?s filename, i.e., VfrFilename.c
##-x, --CreateList [Filename]
##      VFR Option: Create the text list file, named Filename, otherwise use the VfrScriptFile name as the List file?s filename, i.e., VfrFilename.lst
##-i, --include [Path]
##      One or more statements to add to the include path for searching.
##-o, --outdir [DirName]
##      VFR Option: Directory Location where the C, Lst and/or IFR files are to be created.
##-b, --Bin [Filename]
##      VFR Option: Create a binary IFR HII pack file, named Filename, otherwise use the VfrScriptFile name as the IFR file?s name, i.e., VfrFilename.i

#
##-c, --flashheader [Filename]
##      Flash option: Create a header file, default to FlashMap.h, containing flash device definitions for EDK modules which need those flash information.
##--version
##      Print version and copyright of this program and exit
##-v, --verbose
##      Turn on verbose output with informational messages printed. This is a count value, so specifying ?vv can be used to increase the verbosity level.
##-q, --quiet
##      disable all messages except FATAL ERRORS
##-d, --debug [#]
##      Enable debug messages, at level #
##-h, --help
##      Print copyright, version and usage of this program and exit code: PASS

def CheckEnvVariable():
    print "Running Operating System =", sys.platform

    if os.getenv("EDK_TOOLS_PATH") == None:
        print "Please set environment variable: EDK_TOOLS_PATH !\n"
        exit()
    else:
        EDK_TOOLS_PATH = os.environ["EDK_TOOLS_PATH"]
        print "EDK_TOOLS_PATH = %s" % EDK_TOOLS_PATH

    if os.getenv("WORKSPACE") == None:
        print "Please set environment variable: WORKSPACE !\n"
        exit()
    else:
        WORKSPACE = os.environ["WORKSPACE"]
        print "WORKSPACE = %s" % WORKSPACE

    if os.getenv("PATH") == None:
        print "Please set environment variable: PATH !\n"
        exit()
    else:
        PATH = os.environ["PATH"]
        if sys.platform == "win32":
            #print EDK_TOOLS_PATH + "\Bin\Win32"
            if str(PATH).find(EDK_TOOLS_PATH + "\Bin\Win32") == -1:
                print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win32 in environment variable: PATH!\n" % (EDK_TOOLS_PATH, EDK_TOOLS_PATH)
                exit()
        if sys.platform == "win64":
            #print EDK_TOOLS_PATH + "\Bin\Win64"
            if str(PATH).find(EDK_TOOLS_PATH + "\Bin\Win64") == -1:
                print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win64 in environment variable: PATH!\n" % (EDK_TOOLS_PATH, EDK_TOOLS_PATH)
                exit()


def MyOptionParser():
    parser = OptionParser(description=__copyright__,version=__version__,prog="bld.exe",usage="%prog [options] [target]")
    parser.add_option("-a", "--arch", action="append", type="choice", choices=[str('IA32'),"X64","IPF","EBC"], dest="TARGET_ARCH",
        help="ARCHS is a comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt's TARGET_ARCH")
    parser.add_option("-p", "--platform", action="store", type="string", dest="DSCFILE",
        help="Build the platform specified by the DSC file name argument, over rides the ACTIVE_PLATFORM")
    parser.add_option("-m", "--module", action="store", type="string", dest="INFFILE",
        help="Build the module specified by the INF file name argument.")
    parser.add_option("-b", "--buildtarget", action="append", type="choice", choices=['DEBUG','RELEASE'], dest="TARGET",
        help="Build the platform using the BuildTarget, overrides target.txt?s TARGET definition.")
    parser.add_option("-t", "--tagname", action="append", type="string", dest="TOOL_CHAIN_TAG",
        help="Build the platform using the Tool chain, Tagname, overrides target.txt?s TOOL_CHAIN_TAG definition.")
    parser.add_option("-s", "--spawn", action="store_true", type=None,
        help="If this flag is specified, the first two phases, AutoGen and MAKE are mixed, such that as soon as a module can be built, the build will start, without waiting for AutoGen to complete on remaining modules.  While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.")
    parser.add_option("-n", action="store", type="int", dest="NUM",
        help="Build the platform using multi-threaded compiler with # threads, values less than 2 will disable multi-thread builds.  Overrides target.txt?s MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER")
    parser.add_option("-f", "--fdf", action="store", type="string", dest="FDFFILE",
        help="The name of the FDF file to use, over-riding the setting in the DSC file.")
    parser.add_option("-k", "--msft", action="store_true", type=None, help="Make Option: Generate only NMAKE Makefiles: Makefile")
    parser.add_option("-g", "--gcc", action="store_true", type=None, help="Make Option: Generate only GMAKE Makefiles: GNUmakefile")
    parser.add_option("-l", "--all", action="store_true", type=None, help="Make Option: Generate both NMAKE and GMAKE makefiles.")
    (opt, args)=parser.parse_args()
    return (opt, args)


if __name__ == '__main__':
#
# only for Debug, should be removed in release version
#
#    os.chdir("C:\Work\EDK2\MdeModulePkg\Application\HelloWorld")
#    os.chdir("C:\Work\EDK2\MdeModulePkg")
#    os.chdir("C:\Work\edk2\MdePkg")

#
# Record Start Time
#
    StartTime = time.time()
    print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
#
# Check environment variable: EDK_TOOLS_PATH, WORKSPACE, PATH
#
    CheckEnvVariable()

# be compatibile with Ant build.bat ???

#
# Parse the options and args
#
    (opt, args) = MyOptionParser()
    
    GenC = set(['GenC']) & set(args)
    GenMake = set(['GenMake']) & set(args)
    t = str(' '.join(args))

#
# Call Parser
#
    ewb = WorkspaceBuild(opt.DSCFILE)  #opt.DSCFILE is relative path plus filename

#
# Merge the Build Options with Parser's Result
#
    if opt.TARGET_ARCH == None:
        opt.TARGET_ARCH = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
        if opt.TARGET_ARCH == ['']:
            print "TARGET_ARCH is None. Don't What to Build.\n"
            exit()
    print "TARGET_ARCH is", " ".join(opt.TARGET_ARCH)
            
    if opt.DSCFILE == None:
        opt.DSCFILE = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM][0]
        if opt.DSCFILE == '':
            print "ACTIVE_PLATFORM is None. Don't What to Build.\n"
#            exit()
    print "ACTIVE_PLATFORM is %s" % opt.DSCFILE

    if opt.TARGET == None:
        opt.TARGET = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
        if opt.TARGET == ['']:
            print "TARGET is None. Don't What to Build.\n"
            exit()
    print "TARGET is", " ".join(opt.TARGET)

    if opt.TOOL_CHAIN_TAG == None:
        opt.TOOL_CHAIN_TAG = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
        if opt.TOOL_CHAIN_TAG == ['']:
            print "TOOL_CHAIN_TAG is None. Don't What to Build.\n"
            exit()
    print "TOOL_CHAIN_TAG is", " ".join(opt.TOOL_CHAIN_TAG)

    if opt.NUM == None:
        opt.NUM = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER][0]
        if opt.NUM == '':
            print "NUM is 0. Don't What to Build.\n"
            exit()
    print "MAX_CONCURRENT_THREAD_NUMBER is", " ".join(opt.NUM)

    if opt.FDFFILE == None and opt.DSCFILE != '':
        opt.FDFFILE = ewb.DscDatabase[os.path.normpath(opt.DSCFILE)].Defines.DefinesDictionary[TAB_DSC_DEFINES_FLASH_DEFINITION][0]
        if opt.FDFFILE == '':
            pass
    print "FDF FILE is", " ".join(str(opt.FDFFILE))

    
#
# Platform Build or Module Build
#
    CurWorkDir = os.getcwd()
    
    FileList = glob.glob(CurWorkDir + '\\*.inf')
    FileNum = len(FileList)
    if len(FileList) > 0:
        if len(FileList) >= 2:
            print "There are %d INF filss in %s.\n" % (FileNum, CurWorkDir)
            exit()
        if opt.DSCFILE:
            ModuleFile = FileList[0][len(ewb.Workspace.WorkspaceDir)+1:]
            print "Module build:", ModuleFile
            PlatformFile = str(os.path.normpath(opt.DSCFILE))
            print os.path.normpath(opt.DSCFILE)
            print "PlatformFile is:", PlatformFile
            for Target in opt.TARGET:
                for ToolChain in opt.TOOL_CHAIN_TAG:
                    for Arch in opt.TARGET_ARCH:
                        ModuleAutoGen = AutoGen(ModuleFile, PlatformFile, ewb, str(Target), ToolChain, str(Arch))
                        if GenC != set([]):
                            ModuleAutoGen.CreateAutoGenFile()
                            exit()
                        elif GenMake != set([]):
                            makefile = ModuleAutoGen.CreateMakefile()
                            exit()
                        else:
                            ModuleAutoGen.CreateAutoGenFile()
                            makefile = ModuleAutoGen.CreateMakefile()
                            if makefile != "":
                                p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()
                            else:
                                print "Can find Makefile.\n"
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"
    elif opt.DSCFILE:
        PlatformFile = os.path.normpath(opt.DSCFILE)
        print "PlatformFile is:", PlatformFile
        for Target in opt.TARGET:
                for ToolChain in opt.TOOL_CHAIN_TAG:
                    for Arch in opt.TARGET_ARCH:
                        PlatformAutoGen = AutoGen(None, PlatformFile, ewb, str(Target), ToolChain, str(Arch))
                        if GenC != set([]):
                            PlatformAutoGen.CreateAutoGenFile()
                            exit()
                        elif GenMake != set([]):
                            makefile = PlatformAutoGen.CreateMakefile()
                            exit()
                        else:
                            PlatformAutoGen.CreateAutoGenFile()
                            makefile = PlatformAutoGen.CreateMakefile()
                            if makefile != "":
                                p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()
                            else:
                                print "Can find Makefile.\n"
    else:
        FileList = glob.glob(CurWorkDir + '\\*.dsc')
        FileNum = len(FileList)
        if len(FileList) > 0:
            if len(FileList) >= 2:
                print "There are %d DSC files in %s.\n" % (FileNum, CurWorkDir)
                exit()
            PlatformFile = FileList[0][len(ewb.Workspace.WorkspaceDir)+1:]
            print "Platform build:", PlatformFile
            #
            # Call Parser Again
            #
            ewb = WorkspaceBuild(PlatformFile)
            
            for Target in opt.TARGET:
                for ToolChain in opt.TOOL_CHAIN_TAG:
                    for Arch in opt.TARGET_ARCH:
                        PlatformAutoGen = AutoGen(None, PlatformFile, ewb, str(Target), ToolChain, str(Arch))
                        if GenC != set([]):
                            PlatformAutoGen.CreateAutoGenFile()
                            exit()
                        elif GenMake != set([]):
                            makefile = PlatformAutoGen.CreateMakefile()
                            exit()
                        else:
                            PlatformAutoGen.CreateAutoGenFile()
                            makefile = PlatformAutoGen.CreateMakefile()
                            if makefile != "":
                                p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()
                            else:
                                print "Can find Makefile.\n"

        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"

#
# Record Build Process Time
#
    print time.strftime("Current time is %a, %d %b %Y %H:%M:%S +0000", time.localtime())
    Hour = 0
    Min = 0
    Sec = int(time.time() - StartTime)
    Hour = Sec/3600
    Min = (Sec%3600)/60
    Sec = (Sec%3600)%60
    if Hour < 10 and Min < 10 and Sec < 10:
        print "Totol Run Time is 0%d:0%d:0%d" %(Hour, Min, Sec)
    elif Hour < 10 and Min < 10 and Sec > 10:
        print "Totol Run Time is 0%d:0%d:%2d" %(Hour, Min, Sec)
    elif Hour < 10 and Min > 10 and Sec < 10:
        print "Totol Run Time is 0%d:%2d:0%d" %(Hour, Min, Sec)
    elif Hour < 10 and Min > 10 and Sec > 10:
        print "Totol Run Time is 0%d:%2d:%2d" %(Hour, Min, Sec)
    elif Hour > 10 and Min < 10 and Sec < 10:
        print "Totol Run Time is %2d:0%d:0%d" %(Hour, Min, Sec)
    elif Hour > 10 and Min < 10 and Sec > 10:
        print "Totol Run Time is %2d:0%d:%2d" %(Hour, Min, Sec)
    elif Hour > 10 and Min > 10 and Sec < 10:
        print "Totol Run Time is %2d:%2d:0%d" %(Hour, Min, Sec)
    elif Hour > 10 and Min < 10 and Sec > 10:
        print "Totol Run Time is %2d:%2d:0%d" %(Hour, Min, Sec)
