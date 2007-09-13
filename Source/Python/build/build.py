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
from subprocess import *

from Common.TargetTxtClassObject import *
from Common.ToolDefClassObject import *
from Common.EdkIIWorkspaceBuild import *
from Common.DataType import *
from AutoGen.AutoGen import *
from GenFds.FdfParser import *
from Common.BuildToolError import *
import Common.EdkLogger
from BuildSpawn import *


VersionNumber = "0.01"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."


class Build():
    def __init__(self, opt, args):
        self.SysPlatform  = sys.platform
        self.EdkToolsPath = os.getenv("EDK_TOOLS_PATH")
        self.WorkSpace    = os.getenv("WORKSPACE")
        self.Path         = os.getenv("PATH")
        self.Opt          = opt
        self.Args         = args
        self.ArgList      = ['all', 'genc', 'genmake', 'modules', 'libraries', 'clean', 'cleanall', 'cleanlib', 'run']
        self.TargetTxt    = TargetTxtClassObject()
        self.ToolDef      = ToolDefClassObject()
        self.Sem          = None
        self.StartTime    = time.time()
        self.GenC         = None
        self.GenMake      = None
        self.All          = None
        self.ReturnCode   = [0,1]
        if len(self.Args) == 0:
            self.All = 1
        elif len(self.Args) >= 2:
            EdkLogger.quiet("There are too many targets in command line input, please select one from: %s" %(''.join(elem + ' ' for elem in self.ArgList)))
        else:
            t = self.Args[0].lower()
            if t not in self.ArgList:
                EdkLogger.quiet("'%s' is an invalid targets, please select one from: %s" %(self.Args[0], ''.join(elem + ' ' for elem in self.ArgList)))
                self.isexit(1)
            if t == 'genc':
                self.GenC = 1
            elif t == 'genmake':
                self.GenMake = 1
            elif t == 'all' or t == '':
                self.All = 1
            else:
                self.Args = t
        EdkLogger.quiet(time.strftime("%a, %d %b %Y %H:%M:%S +0000\n", time.localtime()))


    def CheckEnvVariable(self):
        EdkLogger.quiet("Running Operating System = %s" % self.SysPlatform)

        if self.EdkToolsPath == None:
            EdkLogger.quiet("ERROR: Please set environment variable: EDK_TOOLS_PATH !\n")
            return 1
        else:
            EdkLogger.quiet("EDK_TOOLS_PATH = %s" % self.EdkToolsPath)

        if self.WorkSpace == None:
            EdkLogger.quiet("ERROR: Please set environment variable: WORKSPACE !\n")
            return 1
        else:
            EdkLogger.quiet("WORKSPACE = %s" % self.WorkSpace)

        if self.Path == None:
            EdkLogger.quiet("ERROR: Please set environment variable: PATH !\n")
            return 1
        else:
            if self.SysPlatform == "win32":
                #print EDK_TOOLS_PATH + "\Bin\Win32"
                if str(self.Path).find(os.path.normpath(os.path.join(self.EdkToolsPath, "\Bin\Win32"))) == -1:
                    path = os.path.normpath(os.path.join(self.EdkToolsPath, "\Bin\Win32"))
                    EdkLogger.quiet("ERROR: Please execute %s to set %s in environment variable: PATH!\n" % (os.path.normpath(os.path.join(path, 'edksetup.bat')), path))
                    return 1
            if self.SysPlatform == "win64":
                #print EDK_TOOLS_PATH + "\Bin\Win64"
                if str(self.Path).find(os.path.normpath(os.path.join(self.EdkToolsPath, "\Bin\Win64"))) == -1:
                    path = os.path.normpath(os.path.join(self.EdkToolsPath, "\Bin\Win64"))
                    EdkLogger.quiet("ERROR: Please execute %s to set %s in environment variable: PATH!\n" % (os.path.normpath(os.path.join(path, 'edksetup.bat')), path))
                    return 1
        return 0

    def Parser(self, ewb):
        pcdSet = {}
        if self.Opt.FDFFILE == None:
            self.Opt.FDFFILE = ewb.Fdf
            if os.path.isabs(os.path.normpath(self.Opt.FDFFILE)) == True:
                EdkLogger.quiet("ERROR: The file: %s specified in DSC file should be described in a WORKSPACE realtive path!" % self.Opt.FDFFILE)
                self.isexit(1)
            if self.Opt.FDFFILE != '' and os.path.isfile(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE))) == False:
                EdkLogger.quiet("ERROR: The file: %s does not exist!" % self.Opt.FDFFILE)
                self.isexit(1)
            if self.Opt.FDFFILE != '':
                (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE)))
                if ext.lower() != '.fdf':
                    EdkLogger.quiet("ERROR: The file: %s is not a FDF file!" % self.Opt.FDFFILE)
                    self.isexit(1)
                fdf = FdfParser(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE)))
                fdf.ParseFile()
                pcdSet = fdf.profile.PcdDict
        else:
            if self.Opt.FDFFILE[0] == '.':
                EdkLogger.quiet("ERROR: Please specify a absolute path or a WORKSPACE realtive path for FDF file.")
                self.isexit(1)
            if os.path.isfile(os.path.abspath(self.Opt.FDFFILE)) == True:
                (filename, ext) = os.path.splitext(os.path.abspath(self.Opt.FDFFILE))
                if ext.lower() != '.fdf':
                    EdkLogger.quiet("ERROR: The input file: %s is not a FDF file!" % self.Opt.FDFFILE)
                    self.isexit(1)
                fdf = FdfParser(os.path.abspath(self.Opt.FDFFILE))
                fdf.ParseFile()
                pcdSet = fdf.profile.PcdDict
                if self.WorkSpace[len(self.WorkSpace)-1] == '\\' or self.WorkSpace[len(self.WorkSpace)-1] == '/':
                    self.Opt.FDFFILE = self.Opt.FDFFILE[len(self.WorkSpace):]
                else:
                    self.Opt.FDFFILE = self.Opt.FDFFILE[len(self.WorkSpace)+1:]
            elif os.path.isfile(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE))) == True:
                (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE)))
                if ext.lower() != '.fdf':
                    EdkLogger.quiet("ERROR: The input file: %s is not a FDF file!" % self.Opt.FDFFILE)
                    self.isexit(1)
                fdf = FdfParser(os.path.normpath(os.path.join(self.WorkSpace, self.Opt.FDFFILE)))
                fdf.ParseFile()
                pcdSet = fdf.profile.PcdDict
            else:
                EdkLogger.quiet("ERROR: The file: %s does not exist!" % self.Opt.FDFFILE)
                self.isexit(1)

        if self.Opt.FDFFILE != '':
            EdkLogger.info('FDFFILE is: %s' % self.Opt.FDFFILE)
            ewb.Fdf = self.Opt.FDFFILE

        ewb.GenBuildDatabase(pcdSet)
        ewb.TargetTxt = self.TargetTxt
        ewb.ToolDef = self.ToolDef

    def LibBuild(self, LibFile, PlatformFile, ewb, a, b, c):
        LibraryAutoGen = AutoGen(LibFile, PlatformFile, ewb, str(a), b, str(c))
        LibraryAutoGen.CreateAutoGenFile()
        LibraryAutoGen.CreateMakefile()
        for Platform in ewb.Build[c].PlatformDatabase.values():
            d = Platform.OutputDirectory
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(os.environ["WORKSPACE"], d, a + '_' + b, c, str(LibFile))))
            DestDir = filename
            EdkLogger.info('Makefile DestDir is: %s' % DestDir)
            FileList = glob.glob(os.path.normpath(os.path.join(DestDir, 'makefile')))
            FileNum = len(FileList)
            if FileNum > 0:
                self.SameTypeFileInDir(FileNum, 'makefile', DestDir)
                BuildSpawn(self.ReturnCode, self.Sem, FileList[0], 'pbuild', 1).start()
            else:
                EdkLogger.quiet("ERROR: There is no Makefile in %s.\n" % DestDir)
                self.isexit(1)

    def ModuleBuild(self, ModuleFile, PlatformFile, ewb, a, b, c, ModuleAutoGen):
        ModuleAutoGen.CreateAutoGenFile()
        ModuleAutoGen.CreateMakefile()
        for Platform in ewb.Build[c].PlatformDatabase.values():
            d = Platform.OutputDirectory
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(os.environ["WORKSPACE"], d, a + '_' + b, c, ModuleFile)))
            DestDir = filename
            FileList = glob.glob(os.path.normpath(os.path.join(DestDir, 'makefile')))
            FileNum = len(FileList)
            if FileNum > 0:
                self.SameTypeFileInDir(FileNum, 'makefile', DestDir)
                for i in range(0, int(self.Opt.NUM)):
                    self.Sem.acquire()
                self.Launch(["nmake", "/nologo", "-f", FileList[0], 'pbuild'], os.path.dirname(FileList[0]))
            else:
                EdkLogger.quiet("ERROR: There is no Makefile in %s.\n" % DestDir)
                self.isexit(1)

    def SameTypeFileInDir(self, FileNum, FileType, Dir):
        if FileNum >= 2:
            EdkLogger.quiet("ERROR: There are %d %s files in %s." % (FileNum, FileType, Dir))
            self.isexit(1)

    def TrackInfo(self, e):
        if self.Opt.debug != None:
            last_type, last_value, last_tb = sys.exc_info()
            traceback.print_exception(last_type, last_value, last_tb)
        else:
            print e

    def GenCFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
        except Exception, e:
            self.TrackInfo(e)
            self.isexit(1)

    def GenMakeFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
            makefile = AutoGenResult.CreateMakefile()
        except Exception, e:
            self.TrackInfo(e)
            self.isexit(1)


    def OtherFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        if type(Arch) == type([]):
            for Platform in ewb.Build[Arch[0]].PlatformDatabase.values():
                d = Platform.OutputDirectory
        else:
            for Platform in ewb.Build[Arch].PlatformDatabase.values():
                d = Platform.OutputDirectory
        if ModuleFile == None:
            DestDir = os.path.normpath(os.path.join(os.environ["WORKSPACE"], d, Target + '_' + ToolChain))
        else:
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(os.environ["WORKSPACE"], d, Target + '_' + ToolChain, Arch, ModuleFile)))
            DestDir = filename
        FileList = glob.glob(os.path.normpath(os.path.join(DestDir, 'makefile')))
        FileNum = len(FileList)
        if FileNum > 0:
            self.SameTypeFileInDir(FileNum, 'makefile', DestDir)
            self.Launch(["nmake", "/nologo", self.Args], os.path.dirname(FileList[0]))
        else:
            self.isexit(1)

    def AllFunc(self, ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch):
        try:
            AutoGenResult = AutoGen(ModuleFile, PlatformFile, ewb, Target, ToolChain, Arch)
            AutoGenResult.CreateAutoGenFile()
            AutoGenResult.CreateMakefile()
        except Exception, e:
            self.TrackInfo(e)
            self.isexit(1)
        self.Launch(["nmake", "/nologo", 'all'], os.path.join(os.environ["WORKSPACE"], AutoGenResult.GetMakefileDir()))

    def Process(self, ModuleFile, PlatformFile, ewb):
        #
        # Merge Arch
        #
        self.Opt.TARGET_ARCH = list(set(self.Opt.TARGET_ARCH) & set(ewb.SupArchList))
        if len(self.Opt.TARGET_ARCH) == 0:
            EdkLogger.quiet("ERROR: Please specify an ARCH, then try again.")
            self.isexit(1)

        try:
            if self.Opt.spawn == True:
                for a in self.Opt.TARGET:
                    for b in self.Opt.TOOL_CHAIN_TAG:
                        if ModuleFile == None:
                            PlatformAutoGen = AutoGen(None, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                            EdkLogger.info("PlatformAutoGen: %s" % PlatformFile)
                            for c in self.Opt.TARGET_ARCH:
                                li = []
                                for d in PlatformAutoGen.Platform[c].Modules:
                                    if ewb.InfDatabase[d].Defines.DefinesDictionary['LIBRARY_CLASS'] == ['']:
                                        EdkLogger.info("Module : %s, Arch : %s" % (d, c))
                                        ModuleAutoGen = AutoGen(d, PlatformFile, ewb, a, b, c)
                                        for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                                            EdkLogger.info("Library: %s, Arch : %s" % (e, c))
                                            if e in li:
                                                continue
                                            else:
                                                li.append(e)
                                            # Thread build error
                                            if self.ReturnCode[0] == 1:
                                                self.isexit(1)
                                            self.LibBuild(e, PlatformFile, ewb, a, b, c)
                                        # Thread build error
                                        if self.ReturnCode[0] == 1:
                                            self.isexit(1)
                                        self.ModuleBuild(d, PlatformFile, ewb, a, b, c, ModuleAutoGen)
                                    else:
                                        EdkLogger.info("Library: %s, Arch : %s" % (d, c))
                                        self.LibBuild(d, PlatformFile, ewb, a, b, c)

                            PlatformAutoGen.CreateAutoGenFile()
                            PlatformAutoGen.CreateMakefile()
                            for i in range(0, int(self.Opt.NUM)):
                                self.Sem.acquire()
                            for i in range(0, int(self.Opt.NUM)):
                                self.Sem.release()

                            #GenFds -f C:\Work\Temp\T1\Nt32Pkg\Nt32Pkg.fdf -o $(BUILD_DIR) -p Nt32Pkg\Nt32Pkg.dsc
                            if self.Opt.FDFFILE != '':
                                for Platform in ewb.Build[self.Opt.TARGET_ARCH[0]].PlatformDatabase.values():
                                    f = Platform.OutputDirectory
                                f = os.path.normpath(os.path.join(os.environ["WORKSPACE"], f, a + '_' + b))
                                if os.path.isdir(os.path.normpath(os.path.join(f, "FV"))) != True:
                                    os.mkdir(os.path.normpath(os.path.join(f, "FV")))
                                archlist = ''.join(elem + ',' for elem in self.Opt.TARGET_ARCH)
                                arch = archlist[:len(archlist)-1]
                                self.Launch(["GenFds", "-f", self.Opt.FDFFILE, "-o", f, "-a", arch, "-p", self.Opt.DSCFILE], os.path.dirname(self.Opt.FDFFILE))
                        else:
                            for c in self.Opt.TARGET_ARCH:
                                #To Do: check the arch of the module
                                ModuleAutoGen = AutoGen(ModuleFile, PlatformFile, ewb, a, b, c)
                                EdkLogger.info("ModuleAutoGen : %s"  % ModuleFile)
                                for e in ModuleAutoGen.BuildInfo.DependentLibraryList:
                                    EdkLogger.info("Library: %s" % e)
                                    self.LibBuild(e, PlatformFile, ewb, a, b, c)
                                self.ModuleBuild(ModuleFile, PlatformFile, ewb, a, b, c, ModuleAutoGen)
                return 0
        except Exception, e:
            self.TrackInfo(e)
            self.isexit(1)

    # normal build
        for a in self.Opt.TARGET:
            for b in self.Opt.TOOL_CHAIN_TAG:
                if ModuleFile == None:
                    if self.GenC == 1:
                        self.GenCFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    elif self.GenMake == 1:
                        self.GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    elif self.All == 1:
                        self.AllFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                    else:
                        self.OtherFunc(ModuleFile, PlatformFile, ewb, a, b, self.Opt.TARGET_ARCH)
                else:
                    #
                    # Check the arch of Module
                    #
                    li = []
                    for c in self.Opt.TARGET_ARCH:
                        ss = 0
                        for elem in ewb.Build[c].ModuleDatabase.values():
                            if ModuleFile != elem.DescFilePath:
                                continue
                            else:
                                ss = 1
                                break
                        if ss == 0:
                            li.append(c)
                        if ss == 1:
                            EdkLogger.quiet("Module: %s, ARCH: %s" %(ModuleFile, c))
                            if self.GenC == 1:
                                self.GenCFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                            elif self.GenMake == 1:
                                self.GenMakeFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                            elif self.All == 1:
                                self.AllFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                            else:
                                self.OtherFunc(ModuleFile, PlatformFile, ewb, a, b, c)
                    if len(li) != 0:
                        EdkLogger.error("Module: %s doesn't support the ARCH: %s" %(ModuleFile, ''.join(elem + ' ' for elem in li)))
        return 0

    def CalculateTime(self):
        EdkLogger.quiet(time.strftime("\n%a, %d %b %Y %H:%M:%S +0000", time.localtime()))
        Hour = 0
        Min = 0
        Sec = int(time.time() - self.StartTime)
        Hour = Sec/3600
        Min = (Sec%3600)/60
        Sec = (Sec%3600)%60
        if Hour < 10 and Min < 10 and Sec < 10:
            EdkLogger.quiet("Total Run Time is 0%d:0%d:0%d" %(Hour, Min, Sec))
        elif Hour < 10 and Min < 10 and Sec > 10:
            EdkLogger.quiet("Total Run Time is 0%d:0%d:%2d" %(Hour, Min, Sec))
        elif Hour < 10 and Min > 10 and Sec < 10:
            EdkLogger.quiet("Total Run Time is 0%d:%2d:0%d" %(Hour, Min, Sec))
        elif Hour < 10 and Min > 10 and Sec > 10:
            EdkLogger.quiet("Total Run Time is 0%d:%2d:%2d" %(Hour, Min, Sec))
        elif Hour > 10 and Min < 10 and Sec < 10:
            EdkLogger.quiet("Total Run Time is %2d:0%d:0%d" %(Hour, Min, Sec))
        elif Hour > 10 and Min < 10 and Sec > 10:
            EdkLogger.quiet("Total Run Time is %2d:0%d:%2d" %(Hour, Min, Sec))
        elif Hour > 10 and Min > 10 and Sec < 10:
            EdkLogger.quiet("Total Run Time is %2d:%2d:0%d" %(Hour, Min, Sec))
        elif Hour > 10 and Min < 10 and Sec > 10:
            EdkLogger.quiet("Total Run Time is %2d:%2d:0%d" %(Hour, Min, Sec))

    def isexit(self, StatusCode):
        if StatusCode != 0:
            self.CalculateTime()
            sys.exit(StatusCode)

    def _ReadMessage(self, From, To, ExitFlag):
        while not ExitFlag.isSet():
            Line = From.readline()
            if Line != "":
                To(Line.rstrip())

    def Launch(self, CommandStringList, WorkingDir):
        Proc = Popen(CommandStringList, stdout=PIPE, stderr=PIPE, env=os.environ, cwd=WorkingDir)

        EndOfProcedure = Event()
        EndOfProcedure.clear()
        if Proc.stdout:
            StdOutThread = Thread(target=self._ReadMessage, args=(Proc.stdout, EdkLogger.info, EndOfProcedure))
            StdOutThread.setDaemon(True)
            StdOutThread.start()

        if Proc.stderr:
            StdErrThread = Thread(target=self._ReadMessage, args=(Proc.stderr, EdkLogger.quiet, EndOfProcedure))
            StdErrThread.setDaemon(True)
            StdErrThread.start()

        Proc.wait()
        EndOfProcedure.set()
        if Proc.stdout:
            StdOutThread.join()
        if Proc.stderr:
            StdErrThread.join()

        if Proc.returncode != 0:
            self.isexit(Proc.returncode)

def MyOptionParser():
    parser = OptionParser(description=__copyright__,version=__version__,prog="build.exe",usage="%prog [options] [target]")
    parser.add_option("-a", "--arch", action="append", type="choice", choices=['IA32','X64','IPF','EBC'], dest="TARGET_ARCH",
        help="ARCHS is one of list: IA32, X64, IPF or EBC, which overrides target.txt's TARGET_ARCH definition. To specify more archs, please repeat this option.")
    parser.add_option("-p", "--platform", action="store", type="string", dest="DSCFILE",
        help="Build the platform specified by the DSC file name argument, overrides target.txt's ACTIVE_PLATFORM definition.")
    parser.add_option("-m", "--module", action="store", type="string", dest="INFFILE",
        help="Build the module specified by the INF file name argument.")
    parser.add_option("-b", "--buildtarget", action="append", type="choice", choices=['DEBUG','RELEASE'], dest="TARGET",
        help="TARGET is one of list: DEBUG, RELEASE, which overrides target.txt's TARGET definition. To specify more TARGET, please repeat this option.")
    parser.add_option("-t", "--tagname", action="append", type="string", dest="TOOL_CHAIN_TAG",
        help="Using the Tool Chain Tagname to build the platform, overrides target.txt's TOOL_CHAIN_TAG definition.")
    parser.add_option("-s", "--spawn", action="store_true", type=None,
        help="If this flag is specified, as soon as a module can be built, the build will start, without waiting for AutoGen to complete remaining modules. While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.")
    parser.add_option("-n", action="store", type="int", dest="NUM",
        help="Build the platform using multi-threaded compiler, this option must combine with spawn option. The value overrides target.txt's MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER, less than 2 will disable multi-thread builds.")
    parser.add_option("-f", "--fdf", action="store", type="string", dest="FDFFILE",
        help="The name of the FDF file to use, which overrides the setting in the DSC file.")
    parser.add_option("-k", "--msft", action="store_true", type=None, help="Make Option: Generate only NMAKE Makefiles: Makefile")
    parser.add_option("-g", "--gcc", action="store_true", type=None, help="Make Option: Generate only GMAKE Makefiles: GNUmakefile")
    parser.add_option("-l", "--all", action="store_true", type=None, help="Make Option: Generate both NMAKE and GMAKE makefiles.")
    parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")

    (opt, args)=parser.parse_args()
    return (opt, args)



def main():
#
# Parse the options and args
#
    (opt, args) = MyOptionParser()

#
# Check environment variable: EDK_TOOLS_PATH, WORKSPACE, PATH
#
    build = Build(opt, args)
    StatusCode = build.CheckEnvVariable()
    build.isexit(StatusCode)
#
# Check target.txt and tools_def.txt and Init them
#
    if os.path.isfile(os.path.normpath(os.path.join(build.WorkSpace, 'Conf\\target.txt'))) == True:
        StatusCode = build.TargetTxt.LoadTargetTxtFile(os.path.normpath(os.path.join(build.WorkSpace, 'Conf\\target.txt')))
        build.isexit(StatusCode)
        if os.path.isfile(os.path.normpath(os.path.join(build.WorkSpace, build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF]))) == True:
            build.ToolDef.LoadToolDefFile(os.path.normpath(os.path.join(build.WorkSpace, build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF])))
            build.isexit(StatusCode)
        else:
            EdkLogger.info("ERROR: %s does not exist." % os.path.normpath(os.path.join(build.WorkSpace, build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF])))
            build.isexit(1)
    else:
        EdkLogger.info("ERROR: %s does not exist." % os.path.normpath(os.path.join(build.WorkSpace, 'Conf\\target.txt')))
        build.isexit(1)
#
# Merge the Build Options except input file(DSCFILE, FDFFILE)
#
    if build.Opt.verbose != None:
        EdkLogger.setLevel(EdkLogger.VERBOSE)
    elif build.Opt.quiet != None:
        EdkLogger.setLevel(EdkLogger.QUIET)
    elif build.Opt.debug != None:
        EdkLogger.setLevel(build.Opt.debug + 1)
    else:
        EdkLogger.setLevel(EdkLogger.INFO)

    if build.Opt.INFFILE != None:
        if build.Opt.INFFILE[0] == '.':
            EdkLogger.quiet("ERROR: Please specify an absolute path or a WORKSPACE realtive path for the MODULE (.inf) file.")
            build.isexit(1)
        if os.path.isfile(os.path.abspath(build.Opt.INFFILE)) == True:
            realpath = os.path.abspath(build.Opt.INFFILE)
            (filename, ext) = os.path.splitext(realpath)
            if ext.lower() != '.inf':
                EdkLogger.quiet("ERROR: The input file: %s is not a INF file!" % build.Opt.INFFILE)
                build.isexit(1)
            if build.WorkSpace[len(build.WorkSpace)-1] == '\\' or build.WorkSpace[len(build.WorkSpace)-1] == '/':
                build.Opt.INFFILE = realpath[len(build.WorkSpace):]
            else:
                build.Opt.INFFILE = realpath[len(build.WorkSpace)+1:]
        elif os.path.isfile(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.INFFILE))) == True:
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.INFFILE)))
            if ext.lower() != '.inf':
                EdkLogger.quiet("ERROR: The input file: %s is not a INF file!" % build.Opt.INFFILE)
                build.isexit(1)
        else:
            EdkLogger.quiet("The input file: %s does not exist!"  % build.Opt.INFFILE)
            build.isexit(1)

    if build.Opt.TARGET_ARCH == None:
        build.Opt.TARGET_ARCH = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
        if build.Opt.TARGET_ARCH == []:
            build.Opt.TARGET_ARCH = ARCH_LIST
    EdkLogger.info('TARGET_ARCH is: %s' % ''.join(elem + ' ' for elem in build.Opt.TARGET_ARCH))

    if build.Opt.TARGET == None:
        build.Opt.TARGET = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
        if build.Opt.TARGET == []:
            build.Opt.TARGET = ['DEBUG', 'RELEASE']
    EdkLogger.info('TARGET is: %s' % ''.join(elem + ' ' for elem in build.Opt.TARGET))

    if build.Opt.TOOL_CHAIN_TAG == None:
        build.Opt.TOOL_CHAIN_TAG = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
        if build.Opt.TOOL_CHAIN_TAG == []:
            EdkLogger.quiet("TOOL_CHAIN_TAG is None. Don't What to Build.\n")
            build.isexit(1)
    EdkLogger.info('TOOL_CHAIN_TAG is: %s' % ''.join(elem + ' ' for elem in build.Opt.TOOL_CHAIN_TAG))

    if build.Opt.NUM == None:
        build.Opt.NUM = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER]
    if build.Opt.NUM == '':
        build.Opt.NUM = 1
    else:
        build.Opt.NUM = int(build.Opt.NUM)
    EdkLogger.info('MAX_CONCURRENT_THREAD_NUMBER is: %s' % build.Opt.NUM)
    if build.Opt.spawn == True:
        build.Sem = BoundedSemaphore(int(build.Opt.NUM))

#
# Marge DSC file with cmd input and default value in target.txt
#
    if build.Opt.DSCFILE == None:
        build.Opt.DSCFILE = build.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]
        if os.path.isabs(os.path.normpath(build.Opt.DSCFILE)) == True:
            EdkLogger.quiet("ERROR: The file: %s specified in target.txt should be described in a WORKSPACE realtive path!" % build.Opt.DSCFILE)
            build.isexit(1)
        if build.Opt.DSCFILE != '' and os.path.isfile(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE))) == False:
            EdkLogger.quiet("ERROR: The file: %s does not exist!" % os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE)))
            build.isexit(1)
        if build.Opt.DSCFILE != '':
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE)))
            if ext.lower() != '.dsc':
                EdkLogger.quiet("ERROR: The file: %s is not a DSC file!" % os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE)))
                build.isexit(1)
    else:
        if build.Opt.DSCFILE[0] == '.':
            EdkLogger.quiet("ERROR: Please specify an absolute path or a WORKSPACE realtive path for the PLATFORM (.dsc) file.")
            build.isexit(1)
        if os.path.isfile(os.path.abspath(build.Opt.DSCFILE)) == True:
            realpath = os.path.abspath(build.Opt.DSCFILE)
            (filename, ext) = os.path.splitext(realpath)
            if ext.lower() != '.dsc':
                EdkLogger.quiet("ERROR: The input file: %s is not a DSC file!" % build.Opt.DSCFILE)
                build.isexit(1)
            if build.WorkSpace[len(build.WorkSpace)-1] == '\\' or build.WorkSpace[len(build.WorkSpace)-1] == '/':
                build.Opt.DSCFILE = realpath[len(build.WorkSpace):]
            else:
                build.Opt.DSCFILE = realpath[len(build.WorkSpace)+1:]
        elif os.path.isfile(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE))) == True:
            (filename, ext) = os.path.splitext(os.path.normpath(os.path.join(build.WorkSpace, build.Opt.DSCFILE)))
            if ext.lower() != '.dsc':
                EdkLogger.quiet("ERROR: The input file: %s is not a DSC file!" % build.Opt.DSCFILE)
                build.isexit(1)
        else:
            EdkLogger.quiet("ERROR: The input file: %s does not exist!"  % build.Opt.DSCFILE)
            build.isexit(1)

#
# Call Parser and Merge FDF file
#
    try:
        if build.Opt.DSCFILE != '':
            EdkLogger.info('ACTIVE_PLATFORM is: %s' % build.Opt.DSCFILE)
            ewb = WorkspaceBuild(build.Opt.DSCFILE, build.WorkSpace)
            build.Parser(ewb)
    except Exception, e:
        build.TrackInfo(e)
        build.isexit(1)

#
# Platform Build or Module Build
#
    CurWorkDir = os.getcwd()
#
#    CurWorkDir = 'C:\Work\R9\LakeportX64Dev\LakeportX64Pkg\AcpiPlatformDxe'
#

    if build.Opt.INFFILE:
        if build.Opt.DSCFILE:
            ModuleFile = os.path.normpath(build.Opt.INFFILE)
            EdkLogger.info('MODULE build: %s' % ModuleFile)
            PlatformFile = os.path.normpath(build.Opt.DSCFILE)
            EdkLogger.info('PlatformFile is: %s' % PlatformFile)
            StatusCode = build.Process(ModuleFile, PlatformFile, ewb)
        else:
            EdkLogger.quiet("ERROR: ACTIVE_PLATFORM isn't specified. DON'T KNOW WHAT TO BUILD\n")
    elif len(glob.glob(os.path.normpath(os.path.join(CurWorkDir, '*.inf')))) > 0:
        FileList = glob.glob(os.path.normpath(os.path.join(CurWorkDir, '*.inf')))
        FileNum = len(FileList)
        if FileNum >= 2:
            EdkLogger.quiet("ERROR: There are %d INF files in %s.\n" % (FileNum, CurWorkDir))
            build.isexit(1)
        if build.Opt.DSCFILE:
            if ewb.WorkspaceDir[len(ewb.WorkspaceDir)-1] == '\\' or ewb.WorkspaceDir[len(ewb.WorkspaceDir)-1] == '/':
                ModuleFile = os.path.normpath(FileList[0][len(ewb.WorkspaceDir):])
            else:
                ModuleFile = os.path.normpath(FileList[0][len(ewb.WorkspaceDir)+1:])
            EdkLogger.info('MODULE build: %s' % ModuleFile)
            PlatformFile = os.path.normpath(build.Opt.DSCFILE)
            EdkLogger.info('PlatformFile is: %s' % PlatformFile)
            StatusCode = build.Process(ModuleFile, PlatformFile, ewb)
        else:
            EdkLogger.quiet("ERROR: ACTIVE_PLATFORM isn't specified. DON'T KNOW WHAT TO BUILD\n")
    elif build.Opt.DSCFILE:
        PlatformFile = os.path.normpath(build.Opt.DSCFILE)
        EdkLogger.info('Platform build: %s' % PlatformFile)
        StatusCode = build.Process(None, PlatformFile, ewb)
    else:
        FileList = glob.glob(os.path.normpath(os.path.join(CurWorkDir, '*.dsc')))
        FileNum = len(FileList)
        if FileNum > 0:
            if FileNum >= 2:
                EdkLogger.quiet("ERROR: There are %d DSC files in %s.\n" % (FileNum, CurWorkDir))
                build.isexit(1)
            if build.WorkSpace[len(build.WorkSpace)-1] == '\\' or build.WorkSpace[len(build.WorkSpace)-1] == '/':
                PlatformFile = os.path.normpath(FileList[0][len(build.WorkSpace):])
            else:
                PlatformFile = os.path.normpath(FileList[0][len(build.WorkSpace)+1:])
            #
            # Call Parser Again
            #
            build.Opt.DSCFILE = PlatformFile
            try:
                EdkLogger.info('Platform build: %s' % build.Opt.DSCFILE)
                ewb = WorkspaceBuild(PlatformFile, build.WorkSpace)
                build.Parser(ewb)
            except Exception, e:
                build.TrackInfo(e)
                build.isexit(1)
            StatusCode = build.Process(None, PlatformFile, ewb)
        else:
            EdkLogger.quiet("ERROR: ACTIVE_PLATFORM isn't specified. DON'T KNOW WHAT TO BUILD\n")

#
# Record Build Process Time
#
    build.CalculateTime()

# To Do: add a judgement for return code
    sys.exit(StatusCode)


if __name__ == '__main__':

    try:
        main()
    except Exception:
        last_type, last_value, last_tb = sys.exc_info()
        traceback.print_exception(last_type, last_value, last_tb)
        sys.exit(1)
