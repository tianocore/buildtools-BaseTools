## @file
# build a platform or a module
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
import os
import sys
import glob
import time
import traceback

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

# Version and Copyright
VersionNumber = "0.02"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."

## standard targets of build command
gSupportedTarget = ['all', 'genc', 'genmake', 'modules', 'libraries', 'fds', 'clean', 'cleanall', 'cleanlib', 'run']

## build configuration file
gBuildConfiguration = "Conf/target.txt"

## Check environment variables
#
#  Check environment variables that must be set for build. Currently they are
#
#   WORKSPACE           The directory all packages/platforms start from
#   EDK_TOOLS_PATH      The directory contains all tools needed by the build
#   PATH                $(EDK_TOOLS_PATH)/Bin/<sys> must be set in PATH
#
#   If any of above environment variable is not set or has error, the build
#   will be broken.
#
def CheckEnvVariable():
    # check WORKSPACE
    if "WORKSPACE" not in os.environ:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please set environment variable: WORKSPACE!\n")

    # check EDK_TOOLS_PATH
    if "EDK_TOOLS_PATH" not in os.environ == None:
        EdkLogger.error("build", ATTRIBUTE_NOT_AVAILABLE, "Please set environment variable: EDK_TOOLS_PATH!\n")

    # check PATH
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

## Get normalized file path
#
# Convert the path to be local format, and remove the WORKSPACE path at the
# beginning if the file path is given in full path.
#
# @param  FilePath      File path to be normalized
# @param  Workspace     Workspace path which the FilePath will be checked against
#
# @retval string        The normalized file path
#
def NormFile(FilePath, Workspace):
    # check if the path is absolute or relative
    if os.path.isabs(FilePath):
        FileFullPath = os.path.normpath(FilePath)
    else:
        FileFullPath = os.path.normpath(os.path.join(Workspace, FilePath))

    # check if the file path exists or not
    if not os.path.isfile(FileFullPath):
        EdkLogger.error("build", FILE_NOT_FOUND, ExtraData="\t%s (Please give file in absolute path or relative to WORKSPACE)"  % FileFullPath)

    # remove workspace directory from the beginning part of the file path
    if Workspace[-1] in ["\\", "/"]:
        return FileFullPath[len(Workspace):]
    else:
        return FileFullPath[(len(Workspace) + 1):]

## Get the output of an external program
#
# This is the entrance method of thread reading output of an external program and
# putting them in STDOUT/STDERR of current program.
#
# @param  From      The stream message read from
# @param  To        The stream message put on
# @param  ExitFlag  The flag used to indicate stopping reading
#
def ReadMessage(From, To, ExitFlag):
    while not ExitFlag.isSet():
        # read one line a time
        Line = From.readline()
        # empty string means nothing got (blank line must have LF/CR, so it's not empty)
        if Line != "":
            To(Line.rstrip())

## Launch an external program
#
# This method will call subprocess.Popen to execute an external program with
# given options in specified directory. Because of the dead-lock issue during
# redirecting output of the external program, threads are used to to do the
# redirection work.
#
# @param  Command               A list or string containing the call of the program
# @param  WorkingDir            The directory in which the program will be running
#
def LaunchCommand(Command, WorkingDir):
    # if working directory doesn't exist, Popen() will raise an exception
    if not os.path.isdir(WorkingDir):
        EdkLogger.error("build", FILE_NOT_FOUND, ExtraData=WorkingDir)

    try:
        # launch the command
        Proc = Popen(Command, stdout=PIPE, stderr=PIPE, env=os.environ, cwd=WorkingDir)

        # launch two threads to read the STDOUT and STDERR
        EndOfProcedure = Event()
        EndOfProcedure.clear()
        if Proc.stdout:
            StdOutThread = Thread(target=ReadMessage, args=(Proc.stdout, EdkLogger.info, EndOfProcedure))
            StdOutThread.setName("STDOUT-Redirector")
            StdOutThread.setDaemon(False)
            StdOutThread.start()

        if Proc.stderr:
            StdErrThread = Thread(target=ReadMessage, args=(Proc.stderr, EdkLogger.quiet, EndOfProcedure))
            StdErrThread.setName("STDERR-Redirector")
            StdErrThread.setDaemon(False)
            StdErrThread.start()

        # waiting for program exit
        Proc.wait()
    except:
        # prevent this method calling from aborting
        pass

    # terminate the threads redirecting the program output
    EndOfProcedure.set()
    if Proc.stdout:
        StdOutThread.join()
    if Proc.stderr:
        StdErrThread.join()

    # check the return code of the program
    if Proc.returncode != 0:
        if type(Command) != type(""):
            Command = " ".join(Command)
        EdkLogger.error("build", COMMAND_FAILURE, ExtraData="%s [%s]" % (Command, WorkingDir))

## The smallest unit that can be built in multi-thread build mode
#
# This is the base class of build unit. The "Obj" parameter must provide
# __str__(), __eq__() and __hash__() methods. Otherwise there could be build units
# missing build.
#
# Currently the "Obj" should be only ModuleAutoGen or PlatformAutoGen objects.
#
class BuildUnit:
    ## The constructor
    #
    #   @param  self        The object pointer
    #   @param  Obj         The object the build is working on
    #   @param  Target      The build target name, one of gSupportedTarget
    #   @param  Dependency  The BuildUnit(s) which must be completed in advance
    #   @param  WorkingDir  The directory build command starts in
    #
    def __init__(self, Obj, BuildComamnd, Target, Dependency, WorkingDir="."):
        self.BuildObject = Obj
        self.Dependency = Dependency
        self.WorkingDir = WorkingDir
        self.Target = Target
        self.BuildCommand = BuildComamnd

    ## str() method
    #
    #   It just returns the string representaion of self.BuildObject
    #
    #   @param  self        The object pointer
    #
    def __str__(self):
        return str(self.BuildObject)

    ## "==" operator method
    #
    #   It just compares self.BuildObject with "Other". So self.BuildObject must
    #   provide its own __eq__() method.
    #
    #   @param  self        The object pointer
    #   @param  Other       The other BuildUnit object compared to
    #
    def __eq__(self, Other):
        return Other != None and self.BuildObject == Other.BuildObject

    ## hash() method
    #
    #   It just returns the hash value of self.BuildObject which must be hashable.
    #
    #   @param  self        The object pointer
    #
    def __hash__(self):
        return hash(self.BuildObject)

## The smallest module unit that can be built by nmake/make command in multi-thread build mode
#
# This class is for module build by nmake/make build system. The "Obj" parameter
# must provide __str__(), __eq__() and __hash__() methods. Otherwise there could
# be make units missing build.
#
# Currently the "Obj" should be only ModuleAutoGen object.
#
class ModuleMakeUnit(BuildUnit):
    ## The constructor
    #
    #   @param  self        The object pointer
    #   @param  Obj         The ModuleAutoGen object the build is working on
    #   @param  Target      The build target name, one of gSupportedTarget
    #
    def __init__(self, Obj, Target):
        Dependency = [ModuleMakeUnit(La, Target) for La in Obj.BuildInfo.LibraryAutoGenList]
        BuildUnit.__init__(self, Obj, Obj.GetBuildCommand(), Target, Dependency, Obj.GetMakeFileDir())
        if Target in [None, "", "all"]:
            self.Target = "pbuild"

## The smallest platform unit that can be built by nmake/make command in multi-thread build mode
#
# This class is for platform build by nmake/make build system. The "Obj" parameter
# must provide __str__(), __eq__() and __hash__() methods. Otherwise there could
# be make units missing build.
#
# Currently the "Obj" should be only PlatformAutoGen object.
#
class PlatformMakeUnit(BuildUnit):
    ## The constructor
    #
    #   @param  self        The object pointer
    #   @param  Obj         The PlatformAutoGen object the build is working on
    #   @param  Target      The build target name, one of gSupportedTarget
    #
    def __init__(self, Obj, Target):
        Dependency = [ModuleMakeUnit(Lib, Target) for Lib in self.BuildObject.BuildInfo.LibraryAutoGenList]
        Dependency.extend([ModuleMakeUnit(Mod, Target) for Mod in self.BuildObject.BuildInfo.ModuleAutoGenList])
        BuildUnit.__init__(self, Obj, Obj.GetBuildCommand(), Target, Dependency, Obj.GetMakeFileDir())

## The class representing the task of a module build or platform build
#
# This class manages the build tasks in multi-thread build mode. Its jobs include
# scheduling thread running, catching thread error, monitor the thread status, etc.
#
class BuildTask:
    # queue for tasks waiting for schedule
    _PendingQueue = sdict()
    _PendingQueueLock = threading.Lock()

    # queue for tasks ready for running
    _ReadyQueue = sdict()
    _ReadyQueueLock = threading.Lock()

    # queue containing all build tasks, in case duplicate build
    _TaskQueue = sdict()

    # flag indicating no thread is running
    _CompleteFlag = threading.Event()
    _CompleteFlag.clear()

    # flag indicating error occurs in a running thread
    _ErrorFlag = threading.Event()
    _ErrorFlag.clear()
    _ErrorMessage = ""

    # BoundedSemaphore object used to control the number of running threads
    _Thread = None

    # flag indicating if the scheduler is started or not
    _SchedulerStarted = False

    ## Start the task scheduler thread
    #
    #   @param  MaxThreadNumber     The maximum thread number
    #   @param  ExitFlag            Flag used to end the scheduler
    #
    @staticmethod
    def StartScheduler(MaxThreadNumber, ExitFlag):
        SchedulerThread = Thread(target=BuildTask.Scheduler, args=(MaxThreadNumber, ExitFlag))
        SchedulerThread.setName("Build-Task-Scheduler")
        SchedulerThread.setDaemon(False)
        SchedulerThread.start()
        BuildTask._SchedulerStarted = True

    ## Scheduler method
    #
    #   @param  MaxThreadNumber     The maximum thread number
    #   @param  ExitFlag            Flag used to end the scheduler
    #
    @staticmethod
    def Scheduler(MaxThreadNumber, ExitFlag):
        try:
            # use BoundedSemaphore to control the maximum running threads
            BuildTask._Thread = BoundedSemaphore(MaxThreadNumber)
            #
            # scheduling loop, which will exits when no pending/ready task and
            # indicated to do so, or there's error in running thread
            #
            while (len(BuildTask._PendingQueue) > 0 or len(BuildTask._ReadyQueue) > 0 \
                   or not ExitFlag.isSet()) and not BuildTask._ErrorFlag.isSet():
                EdkLogger.debug(EdkLogger.DEBUG_5, "Pending Queue (%d), Ready Queue (%d)"
                                % (len(BuildTask._PendingQueue), len(BuildTask._ReadyQueue)))
                # get all pending tasks
                BuildTask._PendingQueueLock.acquire()
                BuildObjectList = BuildTask._PendingQueue.keys()
                BuildTask._PendingQueueLock.release()

                #
                # check if their dependency is resolved, and if true, move them
                # into ready queue
                #
                for BuildObject in BuildObjectList:
                    Bt = BuildTask._PendingQueue[BuildObject]
                    if Bt.IsReady():
                        BuildTask._PendingQueueLock.acquire()
                        BuildTask._ReadyQueue[BuildObject] = BuildTask._PendingQueue.pop(BuildObject)
                        BuildTask._PendingQueueLock.release()

                # launch build thread until the maximum number of threads is reached
                while not BuildTask._ErrorFlag.isSet():
                    # empty ready queue, do nothing further
                    if len(BuildTask._ReadyQueue) == 0:
                        break
                    # wait for active thread(s) exit
                    BuildTask._Thread.acquire(True)
                    # start a new build thread
                    Bo = BuildTask._ReadyQueue.keys()
                    Bt = BuildTask._ReadyQueue.pop(Bo[0])
                    Bt.Start()
                # avoid tense loop
                time.sleep(0.01)

            # wait for all running threads exit if no error occured
            if BuildTask._ErrorFlag.isSet():
                EdkLogger.quiet("\nWaiting for all Command-Threads exit...")
            # while not BuildTask._ErrorFlag.isSet() and \
            while BuildTask._Thread._Semaphore__value < BuildTask._Thread._initial_value:
                EdkLogger.verbose("Waiting for thread ending...(%d)" %
                                  (BuildTask._Thread._initial_value - BuildTask._Thread._Semaphore__value)
                                 )
                EdkLogger.debug(EdkLogger.DEBUG_9, "Threads [%s]" %
                                ", ".join([Th.getName() for Th in threading.enumerate()]))
                # avoid tense loop
                time.sleep(0.1)
            BuildTask._CompleteFlag.set()
            BuildTask._SchedulerStarted = False
        except BaseException, X:
            #
            # TRICK: hide the output of threads left runing, so that the user can
            #        catch the error message easily
            #
            EdkLogger.SetLevel(EdkLogger.QUIET)
            BuildTask._ErrorFlag.set()
            BuildTask._ErrorMessage = "build thread scheduler error\n\t%s" % str(e)
            BuildTask._CompleteFlag.set()
            BuildTask._SchedulerStarted = False

    ## Wait for all running method exit
    #
    @staticmethod
    def WaitForComplete():
        BuildTask._CompleteFlag.wait()

    ## Check if the scheduler is running or not
    #
    @staticmethod
    def IsOnGoing():
        return BuildTask._SchedulerStarted

    ## Abort the build
    @staticmethod
    def Abort():
        BuildTask._ErrorFlag.set()
        BuildTask._CompleteFlag.wait()

    ## Check if there's error in running thread
    #
    #   Since the main thread cannot catch exceptions in other thread, we have to
    #   use threading.Event to communicate this formation to main thread.
    #
    @staticmethod
    def HasError():
        return BuildTask._ErrorFlag.isSet()

    ## Get error message in running thread
    #
    #   Since the main thread cannot catch exceptions in other thread, we have to
    #   use a static variable to communicate this message to main thread.
    #
    @staticmethod
    def GetErrorMessage():
        return BuildTask._ErrorMessage

    ## Factory method to create a BuildTask object
    #
    #   This method will check if a module is building or has been built. And if
    #   true, just return the associated BuildTask object in the _TaskQueue. If
    #   not, create and return a new BuildTask object. The new BuildTask object
    #   will be appended to the _PendingQueue for scheduling later.
    #
    #   @param  BuildItem       A BuildUnit object representing a build object
    #   @param  Dependency      The dependent build object of BuildItem
    #
    @staticmethod
    def New(BuildItem, Dependency=None):
        if BuildItem in BuildTask._TaskQueue:
            Bt = BuildTask._TaskQueue[BuildItem]
            return Bt

        Bt = BuildTask()
        Bt._Init(BuildItem, Dependency)
        BuildTask._TaskQueue[BuildItem] = Bt

        BuildTask._PendingQueueLock.acquire()
        BuildTask._PendingQueue[BuildItem] = Bt
        BuildTask._PendingQueueLock.release()

        return Bt

    ## The real constructor of BuildTask
    #
    #   @param  BuildItem       A BuildUnit object representing a build object
    #   @param  Dependency      The dependent build object of BuildItem
    #
    def _Init(self, BuildItem, Dependency=None):
        self.BuildItem = BuildItem

        self.DependencyList = []
        if Dependency == None:
            Dependency = BuildItem.Dependency
        else:
            Dependency.extend(BuildItem.Dependency)
        self.AddDependency(Dependency)
        # flag indicating build completes, used to avoid unnecessary re-build
        self.CompleteFlag = False

    ## Check if all dependent build tasks are completed or not
    #
    def IsReady(self):
        ReadyFlag = True
        for Dep in self.DependencyList:
            if Dep.CompleteFlag == True:
                continue
            ReadyFlag = False
            break

        return ReadyFlag

    ## Add dependent build task
    #
    #   @param  Dependency      The list of dependent build objects
    #
    def AddDependency(self, Dependency):
        for Dep in Dependency:
            self.DependencyList.append(BuildTask.New(Dep))    # BuildTask list

    ## The thread wrapper of LaunchCommand function
    #
    # @param  Command               A list or string contains the call of the command
    # @param  WorkingDir            The directory in which the program will be running
    #
    def _CommandThread(self, Command, WorkingDir):
        try:
            LaunchCommand(Command, WorkingDir)
            self.CompleteFlag = True
        except Exception, X:
            #
            # TRICK: hide the output of threads left runing, so that the user can
            #        catch the error message easily
            #
            EdkLogger.SetLevel(EdkLogger.QUIET)
            BuildTask._ErrorFlag.set()
            BuildTask._ErrorMessage = "%s broken\n    %s [%s]" % \
                                      (threading.currentThread().getName(), Command, WorkingDir)
        # indicate there's a thread is available for another build task
        BuildTask._Thread.release()

    ## Start build task thread
    #
    def Start(self):
        Command = self.BuildItem.BuildCommand + " " + self.BuildItem.Target
        self.BuildTread = Thread(target=self._CommandThread, args=(Command, self.BuildItem.WorkingDir))
        self.BuildTread.setName("Command-Thread")
        self.BuildTread.setDaemon(False)
        self.BuildTread.start()

## The class implementing the EDK2 build process
#
#   The build process includes:
#       1. Load configuration from target.txt and tools_def.txt in $(WORKSPACE)/Conf
#       2. Parse DSC file of active platform
#       3. Parse FDF file if any
#       4. Establish build database, including parse all other files (module, package)
#       5. Create AutoGen files (C code file, depex file, makefile) if necessary
#       6. Call build command
#
class Build():
    ## Constructor
    #
    # Constructor will load all necessary configurations, parse platform, modules
    # and packages and the establish a database for AutoGen.
    #
    #   @param  Target              The build command target, one of gSupportedTarget
    #   @param  WorkspaceDir        The directory of workspace
    #   @param  Platform            The DSC file of active platform
    #   @param  Module              The INF file of active module, if any
    #   @param  Arch                The Arch list of platform or module
    #   @param  ToolChain           The name list of toolchain
    #   @param  BuildTarget         The "DEBUG" or "RELEASE" build
    #   @param  FlashDefinition     The FDF file of active platform
    #   @param  FdList=[]           The FD names to be individually built
    #   @param  FvList=[]           The FV names to be individually built
    #   @param  MakefileType        The type of makefile (for MSFT make or GNU make)
    #   @param  SpawnMode           Indicate multi-thread build mode
    #   @param  ThreadNumber        The maximum number of thread if in multi-thread build mode
    #
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

        # print dot charater during doing some time-consuming work
        self.Progress = Progressor()

        # parse target.txt, tools_def.txt, and platform file
        self.Progress.Start("Loading build configuration")
        try:
            self.LoadConfiguration()
            self.InitBuild()
        except BaseException, X:
            self.Progress.Stop("")
            raise
        self.Progress.Stop("done!")

        # print current build environment and configuration
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

        # establish build database, INF/DEC files will be parsed in this stage
        self.Progress.Start("\nEstablishing build database")
        try:
            if self.Fdf != None and self.Fdf != "":
                FdfFile = os.path.join(self.WorkspaceDir, self.Fdf)

                Fdf = FdfParser(FdfFile)
                Fdf.ParseFile()

                PcdSet = Fdf.profile.PcdDict
            else:
                PcdSet = {}

            self.Ewb.GenBuildDatabase(PcdSet)
            self.Platform = self.Ewb.Build[self.ArchList[0]].PlatformDatabase[self.PlatformFile]

        except BaseException, X:
            self.Progress.Stop("")
            if isinstance(X, Warning):
                EdkLogger.error(X.ToolName, BUILD_ERROR, X.message, X.FileName, X.LineNumber, RaiseError = False)
            raise
        self.Progress.Stop("done!")

    ## Load configuration
    #
    #   This method will parse target.txt and get the build configurations.
    #
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

        # if no ARCH given in command line, get it from target.txt
        if self.ArchList == None or len(self.ArchList) == 0:
            self.ArchList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET_ARCH]
            if len(self.ArchList) == 0:
                self.ArchList = ARCH_LIST

        # if no build target given in command line, get it from target.txt
        if self.BuildTargetList == None or len(self.BuildTargetList) == 0:
            self.BuildTargetList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TARGET]
            if self.BuildTargetList == None or len(self.BuildTargetList) == 0:
                self.BuildTargetList = ['DEBUG', 'RELEASE']

        # if no tool chain given in command line, get it from target.txt
        if self.ToolChainList == None or len(self.ToolChainList) == 0:
            self.ToolChainList = self.TargetTxt.TargetTxtDictionary[DataType.TAB_TAT_DEFINES_TOOL_CHAIN_TAG]
            if self.ToolChainList == None or len(self.ToolChainList) == 0:
                EdkLogger.error("build", RESOURCE_NOT_AVAILABLE, ExtraData="No toolchain given. Don't know how to build.\n")

        # check if the tool chains are defined or not
        NewToolChainList = []
        for ToolChain in self.ToolChainList:
            if ToolChain not in self.ToolDef.ToolsDefTxtDatabase[TAB_TOD_DEFINES_TOOL_CHAIN_TAG]:
                EdkLogger.warn("build", "Tool chain [%s] is not defined" % ToolChain)
            else:
                NewToolChainList.append(ToolChain)
        # if no tool chain available, break the build
        if len(NewToolChainList) == 0:
            EdkLogger.error("build", RESOURCE_NOT_AVAILABLE,
                            ExtraData="[%s] not defined. No toolchain available for build!\n" % ", ".join(self.ToolChainList))
        else:
            self.ToolChainList = NewToolChainList

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
            if self.PlatformFile == None or self.PlatformFile == "":
                WorkingDirectory = os.getcwd()
                FileList = glob.glob(os.path.normpath(os.path.join(WorkingDirectory, '*.dsc')))
                FileNum = len(FileList)
                if FileNum >= 2:
                    EdkLogger.error("build", None, "There are %d DSC files in %s.\n" % (FileNum, WorkingDirectory))
                elif FileNum == 1:
                    self.PlatformFile = NormFile(FileList[0], self.WorkspaceDir)
            else:
                self.PlatformFile = NormFile(self.PlatformFile, self.WorkspaceDir)

    ## Initialize build configuration
    #
    #   This method will parse DSC file and merge the configurations from
    #   command line and target.txt, then get the final build configurations.
    #
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
        if self.ArchList == None or len(self.ArchList) == 0:
            ArchList = Wb.SupArchList
        else:
            ArchList = list(set(self.ArchList) & set(Wb.SupArchList))
        if len(ArchList) == 0:
            EdkLogger.error("build", PARAMETER_INVALID,
                            ExtraData = "Active platform supports [%s] only, but [%s] is given."
                                        % (" ".join(Wb.SupArchList), " ".join(self.ArchList)))
        elif len(ArchList) != len(self.ArchList):
            SkippedArchList = set(self.ArchList).symmetric_difference(set(Wb.SupArchList))
            EdkLogger.verbose("\nArch [%s] is ignored because active platform supports [%s] but [%s] is specified !"
                           % (" ".join(SkippedArchList), " ".join(Wb.SupArchList), " ".join(self.ArchList)))
        self.ArchList = ArchList

        # Merge build target
        if self.BuildTargetList == None or len(self.BuildTargetList) == 0:
            BuildTargetList = Wb.BuildTarget
        else:
            BuildTargetList = list(set(self.BuildTargetList) & set(Wb.BuildTarget))
        if BuildTargetList == []:
            EdkLogger.error("build", PARAMETER_INVALID, "Active platform only supports [%s], but [%s] is given"
                                % (" ".join(Wb.BuildTarget), " ".join(self.BuildTargetList)))
        self.BuildTargetList = BuildTargetList

        self.Ewb = Wb

    ## Build a module or platform
    #
    # Create autogen code and makfile for a module or platform, and the launch
    # "make" command to build it
    #
    #   @param  Target                      The target of build command
    #   @param  Platform                    The platform file
    #   @param  Module                      The module file
    #   @param  BuildTarget                 The name of build target, one of "DEBUG", "RELEASE"
    #   @param  ToolChain                   The name of toolchain to build
    #   @param  Arch                        The arch of the module/platform
    #   @param  CreateDepModuleCodeFile     Flag used to indicate creating code
    #                                       for dependent modules/Libraries
    #   @param  CreateDepModuleMakeFile     Flag used to indicate creating makefile
    #                                       for dependent modules/Libraries
    #
    def _Build(self, Target, Platform, Module, BuildTarget, ToolChain, Arch, CreateDepModuleCodeFile=True, CreateDepModuleMakeFile=True):
        # skip file generation for some targets
        if Target not in ['clean', 'cleanlib', 'cleanall', 'run']:
            #
            # no need to generate code/makefile for dependent modules/libraries
            # if the target is 'fds'
            #
            if Target == 'fds':
                CreateDepModuleCodeFile = False
                CreateDepModuleMakeFile = False
                CreateDepModuleAutoGenObject = True
            else:
                CreateDepModuleAutoGenObject = False

            if Module != None:
                self.Progress.Start("Generating code/makefile for module")
                AutoGenResult = ModuleAutoGen.New(self.Ewb, Platform, Module, BuildTarget,
                                                  ToolChain, Arch)
            else:
                self.Progress.Start("Generating code/makefile for platform")
                AutoGenResult = PlatformAutoGen.New(self.Ewb, Platform, BuildTarget,
                                                    ToolChain, Arch, CreateDepModuleAutoGenObject)



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
        else:
            if Module != None:
                AutoGenResult = ModuleAutoGen.New(self.Ewb, Platform, Module, BuildTarget,
                                                  ToolChain, Arch)
            else:
                AutoGenResult = PlatformAutoGen.New(self.Ewb, Platform, BuildTarget,
                                                    ToolChain, Arch, False)

        EdkLogger.info("")
        BuildCommand = AutoGenResult.GetBuildCommand()
        if BuildCommand == None or BuildCommand == "":
            EdkLogger.error("build", OPTION_MISSING, ExtraData="No MAKE command found for [%s, %s, %s]" % Key)

        BuildCommand = "%s %s" % (BuildCommand, Target)
        LaunchCommand(BuildCommand, os.path.join(self.WorkspaceDir, AutoGenResult.GetMakeFileDir()))

    ## Build active platform for different build targets and different tool chains
    #
    def _BuildPlatform(self):
        for BuildTarget in self.BuildTargetList:
            for ToolChain in self.ToolChainList:
                self._Build(self.Target, self.PlatformFile, None, BuildTarget, ToolChain, self.ArchList)

    ## Build active module for different build targets, different tool chains and different archs
    #
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

    ## Build a platform in multi-thread mode
    #
    def _MultiThreadBuildPlatform(self):
        for BuildTarget in self.BuildTargetList:
            for ToolChain in self.ToolChainList:
                Pa = PlatformAutoGen.New(self.Ewb, self.PlatformFile, BuildTarget, ToolChain, self.ArchList)
                # multi-thread exit flag
                ExitFlag = threading.Event()
                ExitFlag.clear()
                for Arch in self.ArchList:
                    for Module in Pa.Platform[Arch].Modules:
                        # Get ModuleAutoGen object to generate C code file and makefile
                        Ma = ModuleAutoGen.New(self.Ewb, self.PlatformFile, Module, BuildTarget, ToolChain, Arch)
                        # Not to auto-gen for targets 'clean', 'cleanlib', 'cleanall', 'run', 'fds'
                        if self.Target not in ['clean', 'cleanlib', 'cleanall', 'run', 'fds']:
                            # for target which must generate AutoGen code and makefile
                            Ma.CreateCodeFile(True)
                            if self.Target == "genc":
                                continue

                            Ma.CreateMakeFile(True)
                            if self.Target == "genmake":
                                continue
                        # Generate build task for the module
                        Bt = BuildTask.New(ModuleMakeUnit(Ma, self.Target))
                        # Break build if any build thread has error
                        if BuildTask.HasError():
                            # we need a full version of makefile for platform
                            ExitFlag.set()
                            BuildTask.WaitForComplete()
                            Pa.CreateModuleAutoGen()
                            Pa.CreateMakeFile(False)
                            EdkLogger.error("build", BUILD_ERROR, BuildTask.GetErrorMessage())
                        # Start task scheduler
                        if not BuildTask.IsOnGoing():
                            BuildTask.StartScheduler(self.ThreadNumber, ExitFlag)

                #
                # All modules have been put in build tasks queue. Tell task scheduler
                # to exit if all tasks are completed
                #
                ExitFlag.set()
                BuildTask.WaitForComplete()
                # in case there's an interruption. we need a full version of makefile for platform
                Pa.CreateModuleAutoGen()
                Pa.CreateMakeFile(False)
                if BuildTask.HasError():
                    EdkLogger.error("build", BUILD_ERROR, BuildTask.GetErrorMessage())

                # Generate FD image if there's a FDF file found
                if self.Fdf != '' and self.Target in ["", "all", "fds"]:
                    self.LaunchBuildCommand(Pa.GetBuildCommand() + " fds", Pa.GetMakeFileDir())

    ## Launch the module or platform build
    #
    def Launch(self):
        try:
            if self.ModuleFile == None or self.ModuleFile == "":
                if not self.SpawnMode or self.Target not in ["", "all"]:
                    self.SpawnMode = False
                    self._BuildPlatform()
                else:
                    self._MultiThreadBuildPlatform()
            else:
                self._BuildModule()
        except BaseException, X:
            self.Progress.Stop("")
            raise

    ## Do some clean-up works when error occurred
    def Relinquish(self):
        if self.SpawnMode == True:
            BuildTask.Abort()

## Parse command line options
#
# Using standard Python module optparse to parse command line option of this tool.
#
#   @retval Opt   A optparse.Values object containing the parsed options
#   @retval Args  Target of build command
#
def MyOptionParser():
    Parser = OptionParser(description=__copyright__,version=__version__,prog="build.exe",usage="%prog [options] [target]")
    Parser.add_option("-a", "--arch", action="append", type="choice", choices=['IA32','X64','IPF','EBC'], dest="TargetArch",
        help="ARCHS is one of list: IA32, X64, IPF or EBC, which overrides target.txt's TARGET_ARCH definition. To specify more archs, please repeat this option.")
    Parser.add_option("-p", "--platform", action="store", type="string", dest="PlatformFile",
        help="Build the platform specified by the DSC file name argument, overrides target.txt's ACTIVE_PLATFORM definition.")
    Parser.add_option("-m", "--module", action="store", type="string", dest="ModuleFile",
        help="Build the module specified by the INF file name argument.")
    Parser.add_option("-b", "--buildtarget", action="append", type="choice", choices=['DEBUG','RELEASE'], dest="BuildTarget",
        help="BuildTarget is one of list: DEBUG, RELEASE, which overrides target.txt's TARGET definition. To specify more TARGET, please repeat this option.")
    Parser.add_option("-t", "--tagname", action="append", type="string", dest="ToolChain",
        help="Using the Tool Chain Tagname to build the platform, overrides target.txt's TOOL_CHAIN_TAG definition.")
    Parser.add_option("-s", "--spawn", action="store_true", type=None, dest="SpawnMode",
        help="If this flag is specified, as soon as a module can be built, the build will start, without waiting for AutoGen to complete remaining modules. While this option provides feedback that looks fast, due to overhead of the AutoGen function, this option is slower than letting AutoGen complete before starting the MAKE phase.")
    Parser.add_option("-n", action="store", type="int", dest="ThreadNumber",
        help="Build the platform using multi-threaded compiler, this option must combine with spawn option. The value overrides target.txt's MULTIPLE_THREAD and MAX_CONCURRENT_THREAD_NUMBER, less than 2 will disable multi-thread builds.")
    Parser.add_option("-f", "--fdf", action="store", type="string", dest="FdfFile",
        help="The name of the FDF file to use, which overrides the setting in the DSC file.")
    Parser.add_option("-r", "--rom-image", action="append", type="string", dest="RomImage", default=[],
        help="The name of FD to be generated. The name must be from [FD] section in FDF file.")
    Parser.add_option("-i", "--fv-image", action="append", type="string", dest="FvImage", default=[],
        help="The name of FV to be generated. The name must be from [FV] section in FDF file.")
    Parser.add_option("-k", "--msft", action="store_const", dest="MakefileType", const="nmake", help="Make Option: Generate only NMAKE Makefiles: Makefile")
    Parser.add_option("-g", "--gcc", action="store_const", dest="MakefileType", const="gmake", help="Make Option: Generate only GMAKE Makefiles: GNUmakefile")
    Parser.add_option("-l", "--all", action="store_const", dest="MakefileType", const="all", help="Make Option: Generate both NMAKE and GMAKE makefiles.")

    Parser.add_option("-w", "--warning-as-error", action="store_true", dest="WarningAsError", help="Treat warning in tools as error.")
    Parser.add_option("-j", "--log", action="store", dest="LogFile", help="Putlog in specified file as well as on console.")
    Parser.add_option("-q", "--quiet", action="store_true", type=None, help="Disable all messages except FATAL ERRORS.")
    Parser.add_option("-v", "--verbose", action="store_true", type=None, help="Turn on verbose output with informational messages printed, "\
                                                                               "including library instances selected, final dependency expression, "\
                                                                               "and warning messages, etc.")
    Parser.add_option("-d", "--debug", action="store", type="int", help="Enable debug messages at specified level.")

    (Opt, Args)=Parser.parse_args()
    return (Opt, Args)

## Tool entrance method
#
# This method mainly dispatch specific methods per the command line options.
# If no error found, return zero value so the caller of this tool can know
# if it's executed successfully or not.
#
#   @retval 0     Tool was successful
#   @retval 1     Tool failed
#
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

    if Option.WarningAsError == True:
        EdkLogger.SetWarningAsError()

    EdkLogger.quiet(time.strftime("%H:%M:%S, %b.%d %Y ", time.localtime()) + "[00:00]" + "\n")
    ReturnCode = 0
    MyBuild = None
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

        if Option.FdfFile != None:
            Option.FdfFile = NormFile(Option.FdfFile, Workspace)

        MyBuild = Build(Target, Workspace, Option.PlatformFile, Option.ModuleFile, Option.TargetArch,
                        Option.ToolChain, Option.BuildTarget, Option.FdfFile, Option.RomImage, Option.FvImage,
                        Option.MakefileType, Option.SpawnMode, Option.ThreadNumber)
        MyBuild.Launch()
    except BaseException, X:
        if MyBuild != None:
            # for multi-thread build exits safely
            MyBuild.Relinquish()

        EdkLogger.quiet("")
        if Option != None and Option.debug != None:
            EdkLogger.quiet(traceback.format_exc())
        else:
            EdkLogger.quiet(str(X))
        ReturnCode = 1

    FinishTime = time.clock()
    BuildDuration = time.strftime("%M:%S", time.gmtime(int(round(FinishTime - StartTime))))
    EdkLogger.quiet("\n%s [%s]" % (time.strftime("%H:%M:%S, %b.%d %Y", time.localtime()), BuildDuration))

    return ReturnCode

if __name__ == '__main__':
    sys.exit(Main())
