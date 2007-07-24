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

from NewTargetTxtClassObject import *
from NewEdkIIWorkspaceBuild import *
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

class Build():
    def __init__(self, opt, args):
        self.SysPlatform  = sys.platform
        self.EdkToolsPath = os.getenv("EDK_TOOLS_PATH")
        self.WorkSpace    = os.getenv("WORKSPACE")
        self.Path         = os.getenv("PATH")
        self.Opt          = opt
        self.Args         = args
        self.TargetTxt    = NewTargetTxtClassObject()
        self.ToolDef      = ToolDefClassObject()
        self.Sem          = None
        self.StartTime    = time.time()
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
        

    def CheckEnvVariable(self):
        print "Running Operating System =", self.SysPlatform

        if self.EdkToolsPath == None:
            print "Please set environment variable: EDK_TOOLS_PATH !\n"
            return 1
        else:
            print "EDK_TOOLS_PATH = %s" % self.EdkToolsPath

        if self.WorkSpace == None:
            print "Please set environment variable: WORKSPACE !\n"
            return 1
        else:
            print "WORKSPACE = %s" % self.WorkSpace

        if self.Path == None:
            print "Please set environment variable: PATH !\n"
            return 1
        else:
            if self.SysPlatform == "win32":
                #print EDK_TOOLS_PATH + "\Bin\Win32"
                if str(self.Path).find(self.EdkToolsPath + "\Bin\Win32") == -1:
                    print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win32 in environment variable: PATH!\n" % (self.EdkToolsPath, self.EdkToolsPath)
                    return 1
            if self.SysPlatform == "win64":
                #print EDK_TOOLS_PATH + "\Bin\Win64"
                if str(self.Path).find(self.EdkToolsPath + "\Bin\Win64") == -1:
                    print "Please execute %s\Bin\Win32\edksetup.bat to set %s\Bin\Win64 in environment variable: PATH!\n" % (self.EdkToolsPath, self.EdkToolsPath)
                    return 1
        return 0

    def LibBuild(LibFile, PlatformFile, ewb, a, b, c):
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
                SameTypeFileInDir(FileNum, 'makefile', DestDir, self.StartTime)
                BuildSpawn(self.Sem, FileList[0], 'lbuild', 1).start()
            else:
                print "There isn't makefils in %s.\n" % DestDir
                return 1

    def ModuleBuild(ModuleFile, PlatformFile, ewb, a, b, c, ModuleAutoGen):
        ModuleAutoGen.CreateAutoGenFile()
        ModuleAutoGen.CreateMakefile()
        for f in ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY']:
            (filename, ext) = os.path.splitext(os.environ["WORKSPACE"] + '\\' + f.replace('/','\\') + '\\' + a + '_' + b + '\\' + c + '\\' + ModuleFile)
            DestDir = filename
            FileList = glob.glob(DestDir + '\\makefile')
            FileNum = len(FileList)
            if FileNum > 0:
                SameTypeFileInDir(FileNum, 'makefile', DestDir, self.StartTime)
                for i in range(0, int(self.Opt.NUM)):
                    self.Sem.acquire()
                p = Popen(["nmake", "/nologo", "-f", FileList[0], 'pbuild'], env=os.environ, cwd=os.path.dirname(FileList[0]))
                p.communicate()
                if p.returncode != 0:
                    return p.returncode
                for i in range(0, int(self.Opt.NUM)):
                    self.Sem.release()
            else:
                print "There isn't makefile in %s.\n" % DestDir
                return 1

    def SameTypeFileInDir(FileNum, FileType, Dir):
        if FileNum >= 2:
            print "There are %d %s files in %s.\n" % (FileNum, FileType, CurWorkDir)
            self.CalculateTime()
            sys.exit(1)

    def TrackInfo(self):
        if self.Opt.debug != None:
            last_type, last_value, last_tb = sys.exc_info()
            traceback.print_exception(last_type, last_value, last_tb)

    def GenCFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
        except Exception, e:
            TrackInfo()
            print e
            return 1

    def GenMakeFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
            makefile = AutoGenResult.CreateMakefile()
        except Exception, e:
            TrackInfo()
            print e
            return 1


    def CleanAllFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
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
                p = Popen(["nmake", "/nologo", "-f", FileList[0], 'cleanall'], env=os.environ, cwd=os.path.dirname(FileList[0]))
                p.communicate()
                if p.returncode != None:
                    return p.returncode
            else:
                return 1

    def ALLFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
            makefile = AutoGenResult.CreateMakefile()
        except Exception, e:
            TrackInfo()
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


    def Process(self, ModuleFile, PlatformFile, ewb):

        #
        # Merge Arch
        #
        self.Opt.TARGET_ARCH = list(set(self.Opt.TARGET_ARCH) & set(ewb.SupArchList))

        GenC = 0
        GenMake = 0
        CleanAll = 0
        for t in self.Args:
            t = t.lower()
            if t == 'genc':
                GenC = 1
            elif t == 'genmake':
                GenMake = 1
            elif t == 'cleanall':
                CleanAll = 1

        if self.Opt.spawn == True:
            for a in self.Opt.TARGET:
                for b in self.Opt.TOOL_CHAIN_TAG:
                    if ModuleFile == None:
                        PlatformAutoGen = AutoGen(None, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                        print "PlatformAutoGen : %s", PlatformFile
                        for c in self.Opt.TARGET_ARCH:
                            li = []
                            for d in PlatformAutoGen.Platform[c].Modules:
                                if ewb.InfDatabase[d].Defines.DefinesDictionary['LIBRARY_CLASS'] == ['']:
                                    print "Module : %s, Arch : %s" % (d, c)
                                    ModuleAutoGen = AutoGen(d, PlatformFile, ewb, a, b, c)
                                    for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                                        print "Library: %s, Arch : %s" % (e, c)
                                        if e in li:
                                            continue
                                        else:
                                            li.append(e)
                                        self.LibBuild(e, PlatformFile, ewb, a, b, c)
                                    self.ModuleBuild(d, PlatformFile, ewb, a, b, c, ModuleAutoGen)
                                else:
                                    self.LibBuild(d, PlatformFile, ewb, a, b, c)

                        PlatformAutoGen.CreateAutoGenFile()
                        PlatformAutoGen.CreateMakefile()
                        for i in range(0, int(self.Opt.NUM)):
                            Sem.acquire()
                        print "successful"
                        for i in range(0, int(self.Opt.NUM)):
                            Sem.release()
                            
                        # call GenFds
                        #GenFds -f C:\Work\Temp\T1\Nt32Pkg\Nt32Pkg.fdf -o $(BUILD_DIR) -p Nt32Pkg\Nt32Pkg.dsc
                        if self.Opt.FDFFILE != '':
                            self.Opt.FDFFILE =  os.environ["WORKSPACE"] + '\\' + self.Opt.FDFFILE.replace('/','\\')
                            f = ewb.DscDatabase[PlatformFile].Defines.DefinesDictionary['OUTPUT_DIRECTORY']
                            f = os.environ["WORKSPACE"] + '\\' + f.replace('/', '\\') + '\\' + a + '_' + b
                            if os.path.isdir(f + "\\" + "FV") != True:
                                os.mkdir(f + "\\" + "FV")
                            p = Popen(["GenFds", "-f", self.Opt.FDFFILE, "-o", f, "-p", self.Opt.DSCFILE], env=os.environ, cwd=os.path.dirname(self.Opt.FDFFILE))
                            p.communicate()
                            if p.returncode != 0:
                                return p.returncode

                    else:
                        for c in self.Opt.TARGET_ARCH:
                            ModuleAutoGen = AutoGen(ModuleFile, PlatformFile, ewb, a, b, c)
                            print "ModuleAutoGen : %s"  % ModuleFile
                            for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                                print "Library: %s" % stre
                                self.LibBuild(e, PlatformFile, ewb, a, b, c)
                            self.ModuleBuild(ModuleFile, PlatformFile, ewb, a, b, c, ModuleAutoGen)
            return 0

    # normal build
        for a in self.Opt.TARGET:
            for b in self.Opt.TOOL_CHAIN_TAG:
                if ModuleFile == None:
                    if GenC == 1:
                        self.GenCFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    elif GenMake == 1:
                        self.GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    elif CleanAll == 1:
                        self.CleanAllFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    else:
                        self.ALLFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                else:
                    for c in self.Opt.TARGET_ARCH:
                        if GenC == 1:
                            self.GenCFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                        elif GenMake == 1:
                            self.GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                        elif CleanAll == 1:
                            self.CleanAllFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                        else:
                            self.ALLFunc(ModuleFile, PlatformFile, ewb, a, b, c)
        return 0

    def CalculateTime(self):
        print time.strftime("Current time is %a, %d %b %Y %H:%M:%S +0000", time.localtime())
        Hour = 0
        Min = 0
        Sec = int(time.time() - self.StartTime)
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




if __name__ == '__main__':
#
# Parse the options and args
#
    try:
        (opt, args) = MyOptionParser()
    except Exception, e:
        print e
        sys.exit(1)

#
# Check environment variable: EDK_TOOLS_PATH, WORKSPACE, PATH
#
    build = Build(opt, args)
    StatusCode = build.CheckEnvVariable()
    if StatusCode != 0:
        build.CalculateTime()
        sys.exit(StatusCode)

#
# Check target.txt and tools_def.txt and Init them
#
    if os.path.isfile(build.WorkSpace + '\\Conf\\target.txt') == True:
        StatusCode =build.TargetTxt.LoadTargetTxtFile(build.WorkSpace + '\\Conf\\target.txt')
        if os.path.isfile(build.WorkSpace + '\\' + build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF]) == True:
            StatusCode = build.ToolDef.LoadToolDefFile(build.WorkSpace + '\\' + build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF])
        else:
            print "%s is not existed." % build.WorkSpace + '\\' + build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF]
            build.CalculateTime()
            sys.exit(1)
    else:
        print "%s is not existed." % build.WorkSpace + '\\Conf\\target.txt'
        build.CalculateTime()
        sys.exit(1)

#
# Merge the Build Options
#
    if build.Opt.TARGET_ARCH == None:
        build.Opt.TARGET_ARCH = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
        if build.Opt.TARGET_ARCH == ['']:
            build.Opt.TARGET_ARCH = ['IA32', 'X64', 'IPF', 'EBC']
    print "TARGET_ARCH is", " ".join(opt.TARGET_ARCH)

    if build.Opt.DSCFILE == None:
        build.Opt.DSCFILE = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]
    print "ACTIVE_PLATFORM is %s" % build.Opt.DSCFILE

    if build.Opt.TARGET == None:
        build.Opt.TARGET = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
        if build.Opt.TARGET == ['']:
            build.Opt.TARGET_ARCH = ['DEBUG', 'RELEASE']
    print "TARGET is", " ".join(build.Opt.TARGET)

    if build.Opt.TOOL_CHAIN_TAG == None:
        build.Opt.TOOL_CHAIN_TAG = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
        if build.Opt.TOOL_CHAIN_TAG == '':
            print "TOOL_CHAIN_TAG is None. Don't What to Build.\n"
            build.CalculateTime()
            sys.exit(1)
    print "TOOL_CHAIN_TAG is", build.Opt.TOOL_CHAIN_TAG

    if build.Opt.NUM == None:
        build.Opt.NUM = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER]
    if build.Opt.NUM == '':
        build.Opt.NUM = 1
    else:
        build.Opt.NUM = int(build.Opt.NUM)
    print "MAX_CONCURRENT_THREAD_NUMBER is", build.Opt.NUM
    if build.Opt.spawn == True:
        build.Sem = BoundedSemaphore(int(build.Opt.NUM))

    if build.Opt.verbose != None:
        EdkLogger.setLevel(EdkLogger.VERBOSE)
    elif build.Opt.quiet != None:
        EdkLogger.setLevel(EdkLogger.QUIET)
    elif build.Opt.debug != None:
        EdkLogger.setLevel(build.Opt.debug)
    else:
        EdkLogger.setLevel(EdkLogger.INFO)

#
# Call Parser
#
    if (build.Opt.DSCFILE != None or build.Opt.DSCFILE != '') and os.path.isfile(build.WorkSpace + '\\' + build.Opt.DSCFILE) == False:
        print "The input file: %s is not existed!", build.Opt.DSCFILE
        build.CalculateTime()
        sys.exit(1)
    if build.Opt.FDFFILE != None and os.path.isfile(build.WorkSpace + '\\' + build.Opt.FDFFILE) == False:
        print "The input file: %s is not existed!", build.Opt.FDFFILE
        build.CalculateTime()
        sys.exit(1)
    try:
        if build.Opt.DSCFILE != None and build.Opt.DSCFILE != '':
            ewb = NewWorkspaceBuild(build.Opt.DSCFILE, build.WorkSpace)  #opt.DSCFILE is relative path plus filename
    except Exception, e:
        print e
        build.CalculateTime()
        sys.exit(1)

#
# Platform Build or Module Build
#
    CurWorkDir = os.getcwd()

    if build.Opt.INFFILE:
        if build.Opt.DSCFILE:
            ModuleFile = build.Opt.INFFILE
            print "MODULE build:", ModuleFile
            PlatformFile = str(os.path.normpath(build.Opt.DSCFILE))
            print "PlatformFile is:", PlatformFile
            StatusCode = build.Process(ModuleFile, PlatformFile, ewb, build.Opt)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"
    elif len(glob.glob(CurWorkDir + '\\*.inf')) > 0:
        FileList = glob.glob(CurWorkDir + '\\*.inf')
        FileNum = len(FileList)
        if FileNum >= 2:
            print "There are %d INF filss in %s.\n" % (FileNum, CurWorkDir)
            sys.exit(1)
        if build.Opt.DSCFILE:
            if ewb.Workspace.WorkspaceDir[len(ewb.Workspace.WorkspaceDir)-1] == '\\':
                ModuleFile = FileList[0][len(ewb.Workspace.WorkspaceDir):]
            else:
                ModuleFile = FileList[0][len(ewb.Workspace.WorkspaceDir)+1:]
            print "Module build:", ModuleFile
            PlatformFile = str(os.path.normpath(build.Opt.DSCFILE))
            print "PlatformFile is:", PlatformFile
            StatusCode = build.Process(ModuleFile, PlatformFile, ewb)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"
    elif build.Opt.DSCFILE:
        PlatformFile = os.path.normpath(build.Opt.DSCFILE)
        print "Platform build:", PlatformFile
        StatusCode = build.Process(None, PlatformFile, ewb)
    else:
        FileList = glob.glob(CurWorkDir + '\\*.dsc')
        FileNum = len(FileList)
        if FileNum > 0:
            if FileNum >= 2:
                print "There are %d DSC files in %s.\n" % (FileNum, CurWorkDir)
                sys.exit(1)
            if os.environ('WORKSPACE')[len(os.environ('WORKSPACE'))-1] == '\\':
                PlatformFile = FileList[0][len(os.environ('WORKSPACE')):]
            else:
                PlatformFile = FileList[0][len(os.environ('WORKSPACE'))+1:]
            print "Platform build:", PlatformFile
            #
            # Call Parser Again
            #
            ewb = NewWorkspaceBuild(PlatformFile, build.WorkSpace)
            StatusCode = build.Process(None, PlatformFile, ewb)
        else:
            print "ERROR: DON'T KNOW WHAT TO BUILD\n"

#
# Record Build Process Time
#
    build.CalculateTime()

# To Do: add a judgement for return code
    sys.exit(StatusCode)
