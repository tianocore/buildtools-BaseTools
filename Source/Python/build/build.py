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
from Common.Misc import *
import Common.EdkLogger

VersionNumber = "0.02"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."

gSupportedTarget = ['all', 'genc', 'genmake', 'modules', 'libraries', 'fds', 'clean', 'cleanall', 'cleanlib', 'run']
gBuildConfiguration = "Conf/target.txt"

def CheckEnvVariable():
    if "WORKSPACE" not in os.environ:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please set environment variable: WORKSPACE!\n")

    if "EDK_TOOLS_PATH" not in os.environ == None:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please set environment variable: EDK_TOOLS_PATH!\n")

    if "PATH" not in os.environ:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please set environment variable: PATH!\n")

    PathString = os.environ["PATH"]
    if sys.platform == "win32":
        ToolPath = os.path.normpath(os.path.join(os.environ["EDK_TOOLS_PATH"], "Bin\\Win32"))
    elif sys.platform == "win64":
        ToolPath = os.path.normpath(os.path.join(os.environ["EDK_TOOLS_PATH"], "Bin\\Win64"))
    else:
        ToolPath = os.path.normpath(os.path.join(os.environ["EDK_TOOLS_PATH"], "Bin/Linux"))

    if PathString.find(ToolPath) == -1:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please execute %s to set %s in environment variable: PATH!\n"
                            % (os.path.normpath(os.path.join(PathString, 'edksetup.bat')), ToolPath))

def NormFile(FilePath, Workspace):
    if os.path.isabs(FilePath):
        FileFullPath = os.path.normpath(FilePath)
    else:
        FileFullPath = os.path.normpath(os.path.join(Workspace, FilePath))

    if not os.path.isfile(FileFullPath):
        EdkLogger.error("build", FILE_NOT_FOUND, "%s.\n\tPlease give file in absolute path or relative to WORKSPACE!"  % FileFullPath)

    if Workspace[-1] in ["\\", "/"]:
        return FileFullPath[len(Workspace):]
    else:
        return FileFullPath[(len(Workspace) + 1):]

def ReadMessage(From, To, ExitFlag):
    while not ExitFlag.isSet():
        Line = From.readline()
        if Line != "":
            To(Line.rstrip())

def LaunchCommand(CommandStringList, WorkingDir):
    if not os.path.isdir(WorkingDir):
        EdkLogger.error("build", FILE_NOT_FOUND, ExtraData=WorkingDir)

    Proc = Popen(CommandStringList, stdout=PIPE, stderr=PIPE, env=os.environ, cwd=WorkingDir)

    EndOfProcedure = Event()
    EndOfProcedure.clear()
    if Proc.stdout:
        StdOutThread = Thread(target=ReadMessage, args=(Proc.stdout, EdkLogger.info, EndOfProcedure))
        StdOutThread.setDaemon(True)
        StdOutThread.start()

    if Proc.stderr:
        StdErrThread = Thread(target=ReadMessage, args=(Proc.stderr, EdkLogger.quiet, EndOfProcedure))
        StdErrThread.setDaemon(True)
        StdErrThread.start()

    Proc.wait()
    EndOfProcedure.set()
    if Proc.stdout:
        StdOutThread.join()
    if Proc.stderr:
        StdErrThread.join()

    if Proc.returncode != 0:
        EdkLogger.error("build", UNKNOWN_ERROR, "failed to execute command",
                        ExtraData="%s [%s]" % (" ".join(CommandStringList), WorkingDir))

class BuildObjectClass:
    def __init__(self, Obj, Target):
        self.BuildObject = Obj
        self.Dependency = []
        self.WorkingDir = ""
        self.Target = Target

    def __str__(self):
        return str(self.BuildObject)

    def __eq__(self, Other):
        return Other != None and self.BuildObject == Other.BuildObject

    def __hash__(self):
        return hash(self.BuildObject)

class ModuleMakeObject(BuildObjectClass):
    def __init__(self, Obj, Target):
        BuildObjectClass.__init__(self, Obj, Target)
        self.Dependency = [ModuleMakeObject(La, Target) for La in self.BuildObject.BuildInfo.LibraryAutoGenList]
        self.WorkingDir = Obj.GetMakeFileDir()
        if Target in [None, "", "all"]:
            self.Target = "pbuild"

class PlatformMakeObject(BuildObjectClass):
    def __init__(self, Obj, Target):
        BuildObjectClass.__init__(self, Obj, Target)
        self.Dependency.extend([ModuleMakeObject(Lib, Target) for Lib in self.BuildObject.BuildInfo.LibraryAutoGenList])
        self.Dependency.extend([ModuleMakeObject(Mod, Target) for Mod in self.BuildObject.BuildInfo.ModuleAutoGenList])
        self.WorkingDir = Obj.GetMakeFileDir()

class BuildTask:
    _PendingQueue = sdict()
    _PendingQueueLock = threading.Lock()

    _ReadyQueue = sdict()
    _ReadyQueueLock = threading.Lock()

    _ProcessingQueue = sdict()

    _CompleteFlag = threading.Event()
    _CompleteFlag.clear()

    _ErrorFlag = threading.Event()
    _ErrorFlag.clear()
    _ErrorMessage = ""

    _Thread = None
    _SchedulerStarted = False

    @staticmethod
    def StartScheduler(MaxThreadNumber, ExitFlag):
        SchedulerThread = Thread(target=BuildTask.Scheduler, args=(MaxThreadNumber, ExitFlag))
        SchedulerThread.setDaemon(True)
        SchedulerThread.start()
        BuildTask._SchedulerStarted = True

    @staticmethod
    def Scheduler(MaxThreadNumber, ExitFlag):
        try:
            BuildTask._Thread = BoundedSemaphore(MaxThreadNumber)
            while (len(BuildTask._PendingQueue) > 0 or len(BuildTask._ReadyQueue) > 0 \
                   or not ExitFlag.isSet()) and not BuildTask._ErrorFlag.isSet():
                EdkLogger.debug(EdkLogger.DEBUG_5, "Pending Queue (%d), Ready Queue (%d)"
                                % (len(BuildTask._PendingQueue), len(BuildTask._ReadyQueue)))

                BuildTask._PendingQueueLock.acquire()
                BuildObjectList = BuildTask._PendingQueue.keys()
                BuildTask._PendingQueueLock.release()

                for BuildObject in BuildObjectList:
                    Bt = BuildTask._PendingQueue[BuildObject]
                    if Bt.IsReady():
                        BuildTask._PendingQueueLock.acquire()
                        BuildTask._ReadyQueue[BuildObject] = BuildTask._PendingQueue.pop(BuildObject)
                        BuildTask._PendingQueueLock.release()

                while True:
                    if len(BuildTask._ReadyQueue) == 0:
                        break
                    # wait for active thread(s) exit
                    BuildTask._Thread.acquire(True)
                    Bo = BuildTask._ReadyQueue.keys()
                    Bt = BuildTask._ReadyQueue.pop(Bo[0])
                    Bt.Start()
                # avoid tense loop
                time.sleep(0.01)

            while not BuildTask._ErrorFlag.isSet() and \
                  BuildTask._Thread._Semaphore__value != BuildTask._Thread._initial_value:
                EdkLogger.verbose( "Waiting for thread ending...(%d ended)" % BuildTask._Thread._Semaphore__value)
                # avoid tense loop
                time.sleep(0.1)
            BuildTask._CompleteFlag.set()
            BuildTask._SchedulerStarted = False
        except Exception, e:
            BuildTask._ErrorFlag.set()
            BuildTask._ErrorMessage = "build thread scheduler error\n\t%s" % str(e)
            BuildTask._CompleteFlag.set()
            BuildTask._SchedulerStarted = False

    @staticmethod
    def WaitForComplete():
        BuildTask._CompleteFlag.wait()

    @staticmethod
    def IsOnGoing():
        return BuildTask._SchedulerStarted

    @staticmethod
    def HasError():
        return BuildTask._ErrorFlag.isSet()

    @staticmethod
    def GetErrorMessage():
        return BuildTask._ErrorMessage

    @staticmethod
    def New(BuildObject, Dependency=None):
        if BuildObject in BuildTask._ProcessingQueue:
            Bt = BuildTask._ProcessingQueue[BuildObject]
            return Bt

        Bt = BuildTask()
        Bt._Init(BuildObject, Dependency)
        BuildTask._ProcessingQueue[BuildObject] = Bt

        BuildTask._PendingQueueLock.acquire()
        BuildTask._PendingQueue[BuildObject] = Bt
        BuildTask._PendingQueueLock.release()

        return Bt

    def _Init(self, BuildObject, Dependency=None):
        self.BuildObject = BuildObject

        self.DependencyList = []
        if Dependency == None:
            Dependency = BuildObject.Dependency
        else:
            Dependency.extend(BuildObject.Dependency)
        self.AddDependency(Dependency)

        self.CompleteFlag = False

    def IsReady(self):
        ReadyFlag = True
        for Dep in self.DependencyList:
            if Dep.CompleteFlag == True:
                continue
            ReadyFlag = False
            break

        return ReadyFlag

    def AddDependency(self, Dependency):
        for Dep in Dependency:
            self.DependencyList.append(BuildTask.New(Dep))    # BuildTask list

    def _CommandThread(self, CommandStringList, WorkingDir):
        try:
            LaunchCommand(CommandStringList, WorkingDir)
            self.CompleteFlag = True
        except Exception, e:
            BuildTask._ErrorFlag.set()
            BuildTask._ErrorMessage = "broken by %s\n    %s [%s]" % \
                                      (threading.currentThread().getName(),
                                       " ".join(CommandStringList), WorkingDir)
        BuildTask._Thread.release()

    def Start(self):
        if sys.platform in ["win32", "win64"]:
            CommandList = ["nmake", "/nologo", self.BuildObject.Target]
        else:
            CommandList = ["make", self.BuildObject.Target]

        self.BuildTread = Thread(target=self._CommandThread, args=(CommandList, self.BuildObject.WorkingDir))
        self.BuildTread.start()

class Build():
    def __init__(self, Target, WorkspaceDir, Platform, Module, Arch, ToolChain, BuildTarget,
                 FlashDefinition, FdList=[], FvList=[], MakefileType="nmake", SpawnMode=False, ThreadNumber=2):

        self.WorkspaceDir = WorkspaceDir

        self.Target         = Target
        self.PlatformFile   = Platform
        self.ModuleFile     = Module
        self.ArchList       = Arch
        self.ToolChainList  = ToolChain
        self.BuildTargetList= BuildTarget
        self.Fdf            = FlashDefinition
        self.FdList         = FdList
        self.FvList         = FvList
        self.MakefileType   = MakefileType
        self.SpawnMode      = SpawnMode
        self.ThreadNumber   = ThreadNumber

        self.TargetTxt    = TargetTxtClassObject()
        self.ToolDef      = ToolDefClassObject()

        self.Progress = Progressor()

        self.Progress.Start("Loading build configuration")
        self.LoadConfiguration()
        self.InitBuild()
        self.Progress.Stop("done!")

        EdkLogger.info('')
        EdkLogger.quiet("%-24s = %s" % ("WORKSPACE", os.environ["WORKSPACE"]))
        EdkLogger.quiet("%-24s = %s" % ("EDK_TOOLS_PATH", os.environ["EDK_TOOLS_PATH"]))
        EdkLogger.info('')
        EdkLogger.info('%-24s = %s' % ("TARGET_ARCH", ' '.join(self.ArchList)))
        EdkLogger.info('%-24s = %s' % ("TARGET", ' '.join(self.BuildTargetList)))
        EdkLogger.info('%-24s = %s' % ("TOOL_CHAIN_TAG", ' '.join(self.ToolChainList)))

        EdkLogger.info('')
        if self.PlatformFile != None and self.PlatformFile != "":
            EdkLogger.info('%-24s = %s' % ("Active Platform", self.PlatformFile))

        if self.Fdf != None and self.Fdf != "":
            EdkLogger.info('%-24s = %s' % ("Flash Image Definition", self.Fdf))

        if self.ModuleFile != None and self.ModuleFile != "":
            EdkLogger.info('%-24s = %s' % ("Active Module", self.ModuleFile))

        if self.SpawnMode:
            EdkLogger.verbose('%-24s = %s' % ("Max Thread Number", self.ThreadNumber))

        self.Progress.Start("\nEstablishing build database")
        if self.Fdf != None and self.Fdf != "":
            FdfFile = os.path.join(self.WorkspaceDir, self.Fdf)
            Fdf = FdfParser(FdfFile)
            Fdf.ParseFile()
            PcdSet = Fdf.profile.PcdDict
        else:
            PcdSet = {}

        self.Ewb.GenBuildDatabase(PcdSet)
        self.Platform = self.Ewb.Build[self.ArchList[0]].PlatformDatabase[self.PlatformFile]
        self.Progress.Stop("done!")

    def LoadConfiguration(self):
        #
        # Check target.txt and tools_def.txt and Init them
        #
        BuildConfigurationFile = os.path.normpath(os.path.join(self.WorkspaceDir, gBuildConfiguration))
        if os.path.isfile(BuildConfigurationFile) == True:
            StatusCode = self.TargetTxt.LoadTargetTxtFile(BuildConfigurationFile)

            ToolDefinitionFile = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_CONF]
            ToolDefinitionFile = os.path.normpath(os.path.join(self.WorkspaceDir, ToolDefinitionFile))
            if os.path.isfile(ToolDefinitionFile) == True:
                StatusCode = self.ToolDef.LoadToolDefFile(ToolDefinitionFile)
            else:
                EdkLogger.error("build", FILE_NOT_FOUND, ExtraData=ToolDefinitionFile)
        else:
            EdkLogger.error("build", FILE_NOT_FOUND, ExtraData=BuildConfigurationFile)

        if self.ArchList == None or self.ArchList == []:
            self.ArchList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
            if self.ArchList == []:
                self.ArchList = ARCH_LIST

        if self.BuildTargetList == None or self.BuildTargetList == []:
            self.BuildTargetList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
            if self.BuildTargetList == None or self.BuildTargetList == []:
                self.BuildTargetList = ['DEBUG', 'RELEASE']

        if self.ToolChainList == None or self.ToolChainList == []:
            self.ToolChainList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
            if self.ToolChainList == None or self.ToolChainList == []:
                EdkLogger.error("build", RESOURCE_NOT_AVAILABLE, ExtraData="No toolchain given. Don't know how to build.\n")

        if self.ThreadNumber == None or self.ThreadNumber == "":
            self.ThreadNumber = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MAX_CONCURRENT_THREAD_NUMBER]
            if self.ThreadNumber == '':
                self.ThreadNumber = 1
            else:
                self.ThreadNumber = int(self.ThreadNumber, 0)

        if self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_MULTIPLE_THREAD].lower() in ["enable", "true"]:
            self.SpawnMode = True

        if self.PlatformFile == None:
            self.PlatformFile = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_ACTIVE_PLATFORM]
            self.PlatformFile = NormFile(self.PlatformFile, self.WorkspaceDir)

    def InitBuild(self):
        if self.PlatformFile == None or self.PlatformFile == "":
            EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE,
                            ExtraData="No active platform specified in target.txt or command line! Nothing can be built.\n")

        Wb = WorkspaceBuild(self.PlatformFile, self.WorkspaceDir)
        PcdSet = {}
        if self.Fdf != None:
            self.Fdf = NormFile(self.Fdf, self.WorkspaceDir)
            Wb.Fdf = self.Fdf
        else:
            self.Fdf = Wb.Fdf

        # parse FDF file to get PCD information
        if self.Fdf != None and self.Fdf != "":
            if Wb.Fdf == None or Wb.Fdf == "":
                Wb.Fdf = self.Fdf

            Wb.FdTargetList.extend(self.FdList)
            Wb.FvTargetList.extend(self.FvList)
        else:
            PcdSet = {}
            if self.FdList != []:
                EdkLogger.info("No flash definition file found. FD [%s] will be ignored." % " ".join(self.FdList))
            if self.FvList != []:
                EdkLogger.info("No flash definition file found. FV [%s] will be ignored." % " ".join(self.FvList))

        Wb.TargetTxt = self.TargetTxt
        Wb.ToolDef = self.ToolDef
        #
        # Merge Arch
        #
        ArchList = list(set(self.ArchList) & set(Wb.SupArchList))
        if len(ArchList) == 0:
            EdkLogger.error("build", PARAMETER_INVALID,
                            ExtraData = "Active platform supports [%s] only, but [%s] is given."
                                        % (" ".join(Wb.SupArchList), " ".join(self.ArchList)))
        elif len(ArchList) != len(self.ArchList):
            SkippedArchList = set(self.ArchList).symmetric_difference(set(Wb.SupArchList))
            EdkLogger.info("! Arch [%s] is ignored because active platform supports [%s] but [%s] is specified !"
                           % (" ".join(SkippedArchList), " ".join(Wb.SupArchList), " ".join(self.ArchList)))
        self.ArchList = ArchList

        # Merge build target
        BuildTargetList = list(set(self.BuildTargetList) & set(Wb.BuildTarget))
        if BuildTargetList == []:
            EdkLogger.error("build", PARAMETER_INVALID, "Active platform only supports [%s], but [%s] is given"
                                % (" ".join(Wb.BuildTarget), " ".join(self.BuildTargetList)))
        self.BuildTargetList = BuildTargetList

        self.Ewb = Wb

    def LaunchBuildCommand(self, Target, WorkingDir):
        if sys.platform in ["win32", "win64"]:
            LaunchCommand(["nmake", "/nologo", Target], WorkingDir)
        else:
            LaunchCommand(["make", Target], WorkingDir)

    def _Build(self, Target, Platform, Module, BuildTarget, ToolChain, Arch, CreateDepModuleCodeFile=True, CreateDepModuleMakeFile=True):
        ProgressPrompt = "Generating code/makefile for "
        if Module != None:
            ProgressPrompt += "module"
            AutoGenResult = ModuleAutoGen.New(self.Ewb, Platform, Module, BuildTarget, ToolChain, Arch)
        else:
            ProgressPrompt += "platform"
            AutoGenResult = PlatformAutoGen.New(self.Ewb, Platform, BuildTarget, ToolChain, Arch)

        if AutoGenResult == None:
            return

        # skip file generation for some targets
        if Target not in ['clean', 'cleanlib', 'cleanall', 'run']:
            #
            # no need to generate code/makefile for dependent modules/libraries
            # if the target is 'fds'
            #
            if Target == 'fds':
                CreateDepModuleCodeFile = False
                CreateDepModuleMakeFile = False

            self.Progress.Start(ProgressPrompt)

            # for target which must generate AutoGen code and makefile
            AutoGenResult.CreateCodeFile(CreateDepModuleCodeFile)
            if Target == "genc":
                self.Progress.Stop("done!")
                return

            AutoGenResult.CreateMakeFile(CreateDepModuleMakeFile)
            if Target == "genmake":
                self.Progress.Stop("done!")
                return

            self.Progress.Stop("done!")

        EdkLogger.info("")
        self.LaunchBuildCommand(Target, os.path.join(self.WorkspaceDir, AutoGenResult.GetMakeFileDir()))

    def _BuildPlatform(self):
        for BuildTarget in self.BuildTargetList:
            for ToolChain in self.ToolChainList:
                self._Build(self.Target, self.PlatformFile, None, BuildTarget, ToolChain, self.ArchList)

    def _BuildModule(self):
        for BuildTarget in self.BuildTargetList:
            for ToolChain in self.ToolChainList:
                #
                # module build needs platform build information, so get platform
                # AutoGen first
                #
                if self.Target == 'fds':
                    #
                    # we need to re-generate the command in platform's Makefile
                    # in case the user changed command line option for 'fds' target
                    #
                    PlatformAutoGen.New(self.Ewb, self.PlatformFile, BuildTarget, ToolChain, self.ArchList, True)
                    self._Build("genmake", self.PlatformFile, None, BuildTarget, ToolChain, self.ArchList, False, False)
                else:
                    PlatformAutoGen.New(self.Ewb, self.PlatformFile, BuildTarget, ToolChain, self.ArchList)

                for Arch in self.ArchList:
                    self._Build(self.Target, self.PlatformFile, self.ModuleFile, BuildTarget, ToolChain, Arch)

    def _MultiThreadBuildPlatform(self):
        for BuildTarget in self.BuildTargetList:
            for ToolChain in self.ToolChainList:
                Pa = PlatformAutoGen.New(self.Ewb, self.PlatformFile, BuildTarget, ToolChain, self.ArchList)
                ExitFlag = threading.Event()
                ExitFlag.clear()
                for Arch in self.ArchList:
                    for Module in Pa.Platform[Arch].Modules:
                        Ma = ModuleAutoGen.New(self.Ewb, self.PlatformFile, Module, BuildTarget, ToolChain, Arch)

                        if self.Target not in ['clean', 'cleanlib', 'cleanall', 'run', 'fds']:
                            # for target which must generate AutoGen code and makefile
                            Ma.CreateCodeFile(True)
                            if self.Target == "genc":
                                continue

                            Ma.CreateMakeFile(True)
                            if self.Target == "genmake":
                                continue

                        Bt = BuildTask.New(ModuleMakeObject(Ma, self.Target))

                        if not BuildTask.IsOnGoing():
                            BuildTask.StartScheduler(self.ThreadNumber, ExitFlag)

                        if BuildTask.HasError():
                            # we need a full version of makefile for platform
                            Pa.CreateModuleAutoGen()
                            Pa.CreateMakeFile(False)
                            EdkLogger.error("build", UNKNOWN_ERROR, BuildTask.GetErrorMessage())

                ExitFlag.set()
                BuildTask.WaitForComplete()
                # in case there's an interruption. we need a full version of makefile for platform
                Pa.CreateModuleAutoGen()
                Pa.CreateMakeFile(False)
                if BuildTask.HasError():
                    EdkLogger.error("build", UNKNOWN_ERROR, BuildTask.GetErrorMessage())

                if self.Fdf != '' and self.Target in ["", "all", "fds"]:
                    self.LaunchBuildCommand("fds", Pa.GetMakeFileDir())

    def Launch(self):
        if self.ModuleFile == None or self.ModuleFile == "":
            if not self.SpawnMode or self.Target not in ["", "all"]:
                self.SpawnMode = False
                self._BuildPlatform()
            else:
                self._MultiThreadBuildPlatform()
        else:
            self._BuildModule()

def MyOptionParser():
    parser = OptionParser(description=__copyright__,version=__version__,prog="build.exe",usage="%prog [options] [target]")
    parser.add_option("-a", "--arch", action="append", type="choice", choices=['IA32','X64','IPF','EBC'], dest="TargetArch",
        help="ARCHS is one of list: IA32, X64, IPF or EBC, which overrides target.txt's TARGET_ARCH definition. To specify more archs, please repeat this option.")
    parser.add_option("-p", "--platform", action="store", type="string", dest="PlatformFile",
        help="Build the platform specified by the DSC file name argument, overrides target.txt's ACTIVE_PLATFORM definition.")
    parser.add_option("-m", "--module", action="store", type="string", dest="ModuleFile",
        help="Build the module specified by the INF file name argument.")
    parser.add_option("-b", "--buildtarget", action="append", type="choice", choices=['DEBUG','RELEASE'], dest="BuildTarget",
        help="BuildTarget is one of list: DEBUG, RELEASE, which overrides target.txt's TARGET definition. To specify more TARGET, please repeat this option.")
    parser.add_option("-t", "--tagname", action="append", type="string", dest="ToolChain",
        help="Using the Tool Chain Tagname to build the platform, overrides target.txt's TOOL_CHAIN_TAG definition.")
    parser.add_option("-s", "--spawn", action="store_true", type=None, dest="SpawnMode",
        help="If this flag is specified, as soon as a module can be built, the build will start, without waiting for AutoGen to complete remaining modules. While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.")
    parser.add_option("-n", action="store", type="int", dest="ThreadNumber",
        help="Build the platform using multi-threaded compiler, this option must combine with spawn option. The value overrides target.txt's MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER, less than 2 will disable multi-thread builds.")
    parser.add_option("-f", "--fdf", action="store", type="string", dest="FdfFile",
        help="The name of the FDF file to use, which overrides the setting in the DSC file.")
    parser.add_option("-r", "--rom-image", action="append", type="string", dest="RomImage", default=[],
        help="The name of FD to be generated. The name must be from [FD] section in FDF file.")
    parser.add_option("-i", "--fv-image", action="append", type="string", dest="FvImage", default=[],
        help="The name of FV to be generated. The name must be from [FV] section in FDF file.")
    parser.add_option("-k", "--msft", action="store_const", dest="MakefileType", const="nmake", help="Make Option: Generate only NMAKE Makefiles: Makefile")
    parser.add_option("-g", "--gcc", action="store_const", dest="MakefileType", const="gmake", help="Make Option: Generate only GMAKE Makefiles: GNUmakefile")
    parser.add_option("-l", "--all", action="store_const", dest="MakefileType", const="all", help="Make Option: Generate both NMAKE and GMAKE makefiles.")

    parser.add_option("-j", "--log", action="store", dest="LogFile", help="Putlog in specified file as well as on console.")
    parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed.")
    parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")

    (opt, args)=parser.parse_args()
    return (opt, args)

def Main():
    StartTime = time.clock()
    #
    # Parse the options and args
    #
    (Option, Target) = MyOptionParser()

    if len(Target) == 0:
        Target = "all"
    elif len(Target) >= 2:
        EdkLogger.error("build", OPTION_NOT_SUPPORTED, "More than on targets are not supported.",
                        ExtraData="Please select one of: %s" %(' '.join(gSupportedTarget)))
    else:
        Target = Target[0].lower()

    if Option.verbose != None:
        EdkLogger.SetLevel(EdkLogger.VERBOSE)
    elif Option.quiet != None:
        EdkLogger.SetLevel(EdkLogger.QUIET)
    elif Option.debug != None:
        EdkLogger.SetLevel(Option.debug + 1)
    else:
        EdkLogger.SetLevel(EdkLogger.INFO)

    if Option.LogFile != None:
        EdkLogger.SetLogFile(Option.LogFile)

    EdkLogger.quiet(time.strftime("%H:%M:%S, %b.%d %Y ", time.localtime()) + "[00:00]" + "\n")
    ReturnCode = 0
    try:
        #
        # Check environment variable: EDK_TOOLS_PATH, WORKSPACE, PATH
        #
        CheckEnvVariable()
        Workspace = os.getenv("WORKSPACE")

        WorkingDirectory = os.getcwd()
        if Option.ModuleFile != None:
            Option.ModuleFile = NormFile(Option.ModuleFile, Workspace)
        else:
            FileList = glob.glob(os.path.normpath(os.path.join(WorkingDirectory, '*.inf')))
            FileNum = len(FileList)
            if FileNum >= 2:
                EdkLogger.error("build", None, "There are %d INF files in %s.\n" % (FileNum, WorkingDirectory))
            elif FileNum == 1:
                Option.ModuleFile = NormFile(FileList[0], Workspace)

        if Option.PlatformFile != None:
            Option.PlatformFile = NormFile(Option.PlatformFile, Workspace)
        else:
            FileList = glob.glob(os.path.normpath(os.path.join(WorkingDirectory, '*.dsc')))
            FileNum = len(FileList)
            if FileNum >= 2:
                EdkLogger.error("build", None, "There are %d DSC files in %s.\n" % (FileNum, WorkingDirectory))
            elif FileNum == 1:
                Option.PlatformFile = NormFile(FileList[0], Workspace)

        if Option.FdfFile != None:
            Option.FdfFile = NormFile(Option.FdfFile, Workspace)

        MyBuild = Build(Target, Workspace, Option.PlatformFile, Option.ModuleFile, Option.TargetArch,
                        Option.ToolChain, Option.BuildTarget, Option.FdfFile, Option.RomImage, Option.FvImage,
                        Option.MakefileType, Option.SpawnMode, Option.ThreadNumber)
        MyBuild.Launch()
    except Exception, e:
        EdkLogger.quiet("")
        if Option != None and Option.debug:
            EdkLogger.quiet(traceback.format_exc())
        else:
            EdkLogger.quiet(e)
        ReturnCode = 1

    FinishTime = time.clock()
    BuildDuration = time.strftime("%M:%S", time.gmtime(int(round(FinishTime - StartTime))))
    EdkLogger.quiet("\n%s [%s]" % (time.strftime("%H:%M:%S, %b.%d %Y", time.localtime()), BuildDuration))

    return ReturnCode

if __name__ == '__main__':
    sys.exit(Main())
