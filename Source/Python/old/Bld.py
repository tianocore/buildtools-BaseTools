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

import os, sys, string, glob, time, traceback
from threading import *
from optparse import OptionParser
from os.path import normpath


from subprocess import *

from TargetTxtClassObject import *
from EdkIIWorkspaceBuild import *
from AutoGen import *
from BuildToolError import *
import EdkLogger
from BuildSpawn import *


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
        return 1
    else:
        EDK_TOOLS_PATH = os.environ["EDK_TOOLS_PATH"]
        print "EDK_TOOLS_PATH = %s" % EDK_TOOLS_PATH

    if os.getenv("WORKSPACE") == None:
        print "Please set environment variable: WORKSPACE !\n"
        return 1
    else:
        WORKSPACE = os.environ["WORKSPACE"]
        print "WORKSPACE = %s" % WORKSPACE

    if os.getenv("PATH") == None:
        print "Please set environment variable: PATH !\n"
        return 1
    else:
        PATH = os.environ["PATH"]
        if sys.platform == "win32":
            #print EDK_TOOLS_PATH + "\Bin\Win32"
            if str(PATH).find(EDK_TOOLS_PATH + "\Bin\Win32") == -1:
                print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win32 in environment variable: PATH!\n" % (EDK_TOOLS_PATH, EDK_TOOLS_PATH)
                return 1
        if sys.platform == "win64":
            #print EDK_TOOLS_PATH + "\Bin\Win64"
            if str(PATH).find(EDK_TOOLS_PATH + "\Bin\Win64") == -1:
                print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win64 in environment variable: PATH!\n" % (EDK_TOOLS_PATH, EDK_TOOLS_PATH)
                return 1
    return 0


def MyOptionParser():
    parser = OptionParser(description=__copyright__,version=__version__,prog="bld.exe",usage="%prog [options] [target]")
    parser.add_option("-a", "--arch", action="append", type="choice", choices=['IA32','X64','IPF','EBC'], dest="TARGET_ARCH",
        help="ARCHS is a comma separated list containing one or more of: IA32, X64, IPF or EBC which should be built, overrides target.txt's TARGET_ARCH")
    parser.add_option("-p", "--platform", action="store", type="string", dest="DSCFILE",
        help="Build the platform specified by the DSC file name argument, over rides the ACTIVE_PLATFORM")
    parser.add_option("-m", "--module", action="store", type="string", dest="INFFILE",
        help="Build the module specified by the INF file name argument.")
    parser.add_option("-b", "--buildtarget", action="append", type="choice", choices=['DEBUG','RELEASE'], dest="TARGET",
        help="Build the platform using the BuildTarget, overrides target.txt's TARGET definition.")
    parser.add_option("-t", "--tagname", action="append", type="string", dest="TOOL_CHAIN_TAG",
        help="Build the platform using the Tool chain, Tagname, overrides target.txt's TOOL_CHAIN_TAG definition.")
    parser.add_option("-s", "--spawn", action="store_true", type=None,
        help="If this flag is specified, the first two phases, AutoGen and MAKE are mixed, such that as soon as a module can be built, the build will start, without waiting for AutoGen to complete on remaining modules.  While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.")
    parser.add_option("-n", action="store", type="int", dest="NUM",
        help="Build the platform using multi-threaded compiler with # threads, values less than 2 will disable multi-thread builds. Overrides target.txt's MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER")
    parser.add_option("-f", "--fdf", action="store", type="string", dest="FDFFILE",
        help="The name of the FDF file to use, over-riding the setting in the DSC file.")
    parser.add_option("-k", "--msft", action="store_true", type=None, help="Make Option: Generate only NMAKE Makefiles: Makefile")
    parser.add_option("-g", "--gcc", action="store_true", type=None, help="Make Option: Generate only GMAKE Makefiles: GNUmakefile")
    parser.add_option("-l", "--all", action="store_true", type=None, help="Make Option: Generate both NMAKE and GMAKE makefiles.")
    parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")
    
    (opt, args)=parser.parse_args()
    return (opt, args)

def Process(ModuleFile, PlatformFile, ewb, opt, args, StartTime):

    t = str(' '.join(args))
    GenC = 0
    GenMake = 0
    All = 0

# Add a check to limit multi-args

    t = t.lower()
    if t == 'genc':
        GenC = 1
    elif t == 'genmake':
        GenMake = 1
    elif t == '' or t == 'all':
        All = 1
            

#spawn build
    Sem = BoundedSemaphore(int(opt.NUM))

    if opt.spawn == True:
        for a in opt.TARGET:
            for b in opt.TOOL_CHAIN_TAG:
                if ModuleFile == None:
                    PlatformAutoGen = AutoGen(None, PlatformFile, ewb, str(a), b, opt.TARGET_ARCH)
                    print "PlatformAutoGen : %s", PlatformFile
                    for c in opt.TARGET_ARCH:
                        li = []
                        for d in PlatformAutoGen.Platform[str(c)].Modules:
                            if ewb.InfDatabase[d].Defines.DefinesDictionary['LIBRARY_CLASS'] == ['']:
                                print "Module : %s, Arch : %s" % (d, str(c))
                                ModuleAutoGen = AutoGen(d, PlatformFile, ewb, str(a), b, str(c))
                                for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                                    print "Library: %s, Arch : %s" % (e, str(c))
                                    if e in li:
                                        continue
                                    else:
                                        li.append(e)
                                    LibBuild(e, PlatformFile, ewb, str(a), b, str(c), Sem, StartTime)
                                ModuleBuild(d, PlatformFile, ewb, str(a), b, str(c), Sem, StartTime, ModuleAutoGen)
                            else:
                                LibBuild(d, PlatformFile, ewb, str(a), b, str(c), Sem, StartTime)

                    for i in range(0, int(opt.NUM)):
                        Sem.acquire()
                    print "successful"
                    for i in range(0, int(opt.NUM)):
                        Sem.release()
                    # call GenFds
                    #GenFds -f C:\Work\Temp\T1\Nt32Pkg\Nt32Pkg.fdf -o $(BUILD_DIR) -p Nt32Pkg\Nt32Pkg.dsc
                    PlatformAutoGen.CreateAutoGenFile()
                    PlatformAutoGen.CreateMakefile()

                    if opt.FDFFILE != '':
                        opt.FDFFILE =  os.environ["WORKSPACE"] + '\\' + opt.FDFFILE.replace('/','\\')
                        f = ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY'][0]
                        f = os.environ["WORKSPACE"] + '\\' + f.replace('/', '\\') + '\\' + a + '_' + b
                        if os.path.isdir(f + "\\" + "FV") != True:
                            os.mkdir(f + "\\" + "FV")
                        p = Popen(["GenFds", "-f", opt.FDFFILE, "-o", f, "-p", opt.DSCFILE], env=os.environ, cwd=os.path.dirname(opt.FDFFILE))
                        p.communicate()
                        if p.returncode != 0:
                            return p.returncode
                            
                else:
                    for c in opt.TARGET_ARCH:
                        ModuleAutoGen = AutoGen(ModuleFile, PlatformFile, ewb, str(a), b, str(c))
                        print "ModuleAutoGen : %s"  % ModuleFile
                        for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                            print "Library: %s" % str(e)
                            LibBuild(e, PlatformFile, ewb, str(a), b, str(c), Sem, StartTime)
                        ModuleBuild(ModuleFile, PlatformFile, ewb, str(a), b, str(c), Sem, StartTime, ModuleAutoGen)
        return 0

# normal build
    for a in opt.TARGET:
        for b in opt.TOOL_CHAIN_TAG:
            if ModuleFile == None:
                if GenC == 1:
                    GenCFunc(ModuleFile, PlatformFile, ewb, a, b, opt.TARGET_ARCH)
                elif GenMake == 1:
                    GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, opt.TARGET_ARCH)
                elif All == 1:
                    ALLFunc(ModuleFile, PlatformFile, ewb, a, b, opt.TARGET_ARCH)
                else:
                    OtherFunc(ModuleFile, PlatformFile, ewb, a, b, opt.TARGET_ARCH, t)
            else:
                for c in opt.TARGET_ARCH:
                    if GenC == 1:
                        GenCFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                    elif GenMake == 1:
                        GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                    elif All == 1:
                        ALLFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                    else:
                        OtherFunc(ModuleFile, PlatformFile, ewb, a, b, c, t)
    return 0


def LibBuild(LibFile, PlatformFile, ewb, a, b, c, Sem, StartTime):
    LibraryAutoGen = AutoGen(LibFile, PlatformFile, ewb, str(a), b, str(c))
    LibraryAutoGen.CreateAutoGenFile()
    LibraryAutoGen.CreateMakefile()
    for f in ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY']:
        (filename, ext) = os.path.splitext(os.environ["WORKSPACE"] + '\\' + f.replace('/','\\') + '\\' + a + '_' + b + '\\' + c + '\\' + str(LibFile))
        DestDir = filename
        print DestDir
        FileList = glob.glob(DestDir + '\\makefile')
        FileNum = len(FileList)
        if FileNum > 0:
            SameTypeFileInDir(FileNum, 'makefile', DestDir, StartTime)
            BuildSpawn(Sem, FileList[0], 'lbuild', 1).start()
        else:
            print "There isn't makefils in %s.\n" % DestDir
            return 1

def ModuleBuild(ModuleFile, PlatformFile, ewb, a, b, c, Sem, StartTime, ModuleAutoGen):
    ModuleAutoGen.CreateAutoGenFile()
    ModuleAutoGen.CreateMakefile()
    for f in ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY']:
        (filename, ext) = os.path.splitext(os.environ["WORKSPACE"] + '\\' + f.replace('/','\\') + '\\' + a + '_' + b + '\\' + c + '\\' + ModuleFile)
        DestDir = filename
        FileList = glob.glob(DestDir + '\\makefile')
        FileNum = len(FileList)
        if FileNum > 0:
            SameTypeFileInDir(FileNum, 'makefile', DestDir, StartTime)
            for i in range(0, int(opt.NUM)):
                Sem.acquire()
            p = Popen(["nmake", "/nologo", "-f", FileList[0], 'pbuild'], env=os.environ, cwd=os.path.dirname(FileList[0]))
            p.communicate()
            if p.returncode != 0:
                return p.returncode
            for i in range(0, int(opt.NUM)):
                Sem.release()
        else:
            print "There isn't makefile in %s.\n" % DestDir
            return 1

def GenCFunc(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
    try:
        AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
        AutoGenResult.CreateAutoGenFile()
    except Exception, e:
        TrackInfo(opt.debug)
        print e
        return 1

def GenMakeFunc(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
    try:
        AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
        AutoGenResult.CreateAutoGenFile()
        makefile = AutoGenResult.CreateMakefile()
    except Exception, e:
        TrackInfo(opt.debug)
        print e
        return 1

def OtherFunc(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch, t):
    for d in ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY']:
        if ModuleFile == None:
            DestDir = os.environ["WORKSPACE"] + '\\' + d.replace('/','\\') + '\\' + Target + '_' + ToolChain
        else:
            (filename, ext) = os.path.splitext(os.environ["WORKSPACE"] + '\\' + d.replace('/','\\') + '\\' + Target + '_' + ToolChain + '\\' + Arch + '\\' + ModuleFile)
            DestDir = filename
        FileList = glob.glob(DestDir + '\\makefile')
        FileNum = len(FileList)
        if FileNum > 0:
            SameTypeFileInDir(FileNum, 'makefile', DestDir, StartTime)
            p = Popen(["nmake", "/nologo", "-f", FileList[0], t], env=os.environ, cwd=os.path.dirname(FileList[0]))
            p.communicate()
            if p.returncode != None:
                return p.returncode
        else:
            return 1
        
def ALLFunc(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
    try:
        AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
        AutoGenResult.CreateAutoGenFile()
        makefile = AutoGenResult.CreateMakefile()
    except Exception, e:
        TrackInfo(opt.debug)
        print e
        return 1
    if makefile != "":
        p = Popen(["nmake", "/nologo", "-f", makefile, 'all'], env=os.environ, cwd=os.path.dirname(makefile))
        p.communicate()
        if p.returncode != None:
            return p.returncode
    else:
        print "Can find Makefile.\n"
        return 1


def CalculateTime(StartTime):
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

def SameTypeFileInDir(FileNum, FileType, Dir, StartTime):
    if FileNum >= 2:
        print "There are %d %s files in %s.\n" % (FileNum, FileType, CurWorkDir)
        CalculateTime(StartTime)
        sys.exit(1)

def TrackInfo(DebugLevel = None):
    if DebugLevel != None:
        last_type, last_value, last_tb = sys.exc_info()
        traceback.print_exception(last_type, last_value, last_tb)



if __name__ == '__main__':
#
# Parse the options and args
#
    try:
        (opt, args) = MyOptionParser()
        #Add check for len of args list
    except Exception, e:
        print e
        sys.exit(1)


#
# Record Start Time
#
    StartTime = time.time()
    print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

#
# Check environment variable: EDK_TOOLS_PATH, WORKSPACE, PATH
#
    StatusCode = CheckEnvVariable()
    if StatusCode != 0:
        CalculateTime(StartTime)
        sys.exit(StatusCode)

#
# Call Parser
#
    try:
        if opt.DSCFILE == None:
            ewb = WorkspaceBuild(opt.DSCFILE)
            opt.DSCFILE = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM][0]
            if opt.DSCFILE == '':
                pass
            else:
                ewb = WorkspaceBuild(opt.DSCFILE)
        else:
            ewb = WorkspaceBuild(opt.DSCFILE)
    except Exception, e:
        print e
        CalculateTime(StartTime)
        sys.exit(1)
#
# Merge the Build Options with Parser's Result
#
    if opt.TARGET_ARCH == None:
        opt.TARGET_ARCH = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
        if opt.TARGET_ARCH == ['']:
            opt.TARGET_ARCH = ['IA32', 'X64', 'IPF', 'EBC']
    print "TARGET_ARCH is", " ".join(opt.TARGET_ARCH)
            
##    if opt.DSCFILE == None:
##        opt.DSCFILE = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM][0]
###        if opt.DSCFILE == '':
###            print "ACTIVE_PLATFORM is None. Don't What to Build.\n"
###            exit()
##    print "ACTIVE_PLATFORM is %s" % opt.DSCFILE

    if opt.TARGET == None:
        opt.TARGET = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
        if opt.TARGET == ['']:
            opt.TARGET = ['DEBUG', 'RELEASE']
    print "TARGET is", " ".join(opt.TARGET)

    if opt.TOOL_CHAIN_TAG == None:
        opt.TOOL_CHAIN_TAG = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
        if opt.TOOL_CHAIN_TAG == ['']:
            print "TOOL_CHAIN_TAG is None. Don't What to Build.\n"
            CalculateTime(StartTime)
            sys.exit(1)
    print "TOOL_CHAIN_TAG is", " ".join(opt.TOOL_CHAIN_TAG)

    if opt.NUM == None:
        opt.NUM = ewb.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER][0]
        print "MAX_CONCURRENT_THREAD_NUMBER is", " ".join(opt.NUM)
    else:
        print "MAX_CONCURRENT_THREAD_NUMBER is", opt.NUM

    if opt.FDFFILE == None and opt.DSCFILE != '':
        opt.FDFFILE = ewb.DscDatabase[os.path.normpath(opt.DSCFILE)].Defines.DefinesDictionary[TAB_DSC_DEFINES_FLASH_DEFINITION][0]
    print "FDF FILE is", opt.FDFFILE

    if opt.verbose != None:
        EdkLogger.setLevel(EdkLogger.VERBOSE)
    elif opt.quiet != None:
        EdkLogger.setLevel(EdkLogger.QUIET)
    elif opt.debug != None:
        EdkLogger.setLevel(opt.debug)
    else:
        EdkLogger.setLevel(EdkLogger.INFO)

#
# Merge Arch
#
    if opt.DSCFILE != None and opt.DSCFILE != '':
        opt.TARGET_ARCH = list(set(opt.TARGET_ARCH) & set(ewb.SupArchList))
    
#
# Platform Build or Module Build
#
    CurWorkDir = os.getcwd()

    if opt.INFFILE:
        if opt.DSCFILE:
            ModuleFile = opt.INFFILE
            print "MODULE build:", ModuleFile
            PlatformFile = str(os.path.normpath(opt.DSCFILE))
            print "PlatformFile is:", PlatformFile
            StatusCode = Process(ModuleFile, PlatformFile, ewb, opt, args, StartTime)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"
    elif len(glob.glob(CurWorkDir + '\\*.inf')) > 0:
        FileList = glob.glob(CurWorkDir + '\\*.inf')
        FileNum = len(FileList)
        SameTypeFileInDir(FileNum, 'inf', CurWorkDir, StartTime)
        if opt.DSCFILE != None and opt.DSCFILE != '':
            if ewb.Workspace.WorkspaceDir[len(ewb.Workspace.WorkspaceDir)-1] == '\\':
                ModuleFile = FileList[0][len(ewb.Workspace.WorkspaceDir):]
            else:
                ModuleFile = FileList[0][len(ewb.Workspace.WorkspaceDir)+1:]
            print "Module build:", ModuleFile
            PlatformFile = str(os.path.normpath(opt.DSCFILE))
            print "PlatformFile is:", PlatformFile
            StatusCode = Process(ModuleFile, PlatformFile, ewb, opt, args, StartTime)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"
    elif opt.DSCFILE:
        PlatformFile = os.path.normpath(opt.DSCFILE)
        print "Platform build:", PlatformFile
        StatusCode = Process(None, PlatformFile, ewb, opt, args, StartTime)
    else:
        FileList = glob.glob(CurWorkDir + '\\*.dsc')
        FileNum = len(FileList)
        if FileNum > 0:
            SameTypeFileInDir(FileNum, 'dsc', CurWorkDir, StartTime)
            if ewb.Workspace.WorkspaceDir[len(ewb.Workspace.WorkspaceDir)-1] == '\\':
                PlatformFile = FileList[0][len(ewb.Workspace.WorkspaceDir):]
            else:
                PlatformFile = FileList[0][len(ewb.Workspace.WorkspaceDir)+1:]
            print "Platform build:", PlatformFile
            #
            # Call Parser Again
            #
            ewb = WorkspaceBuild(PlatformFile)
            opt.TARGET_ARCH = list(set(opt.TARGET_ARCH) & set(ewb.SupArchList))
            StatusCode = Process(None, PlatformFile, ewb, opt, args, StartTime)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"

#
# Record Build Process Time
#
    CalculateTime(StartTime)

# To Do: add a judgement for return code
    sys.exit(StatusCode)
