## @file
# Install distribution package.
#
# Copyright (c) 2007, Intel Corporation
# All rights reserved. This program and the accompanying materials
# are licensed and made available under the terms and conditions of the BSD License
# which accompanies this distribution.  The full text of the license may be found at
# http://opensource.org/licenses/bsd-license.php
#
# THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
# WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
#

##
# Import Modules
#
import os
import sys
import glob
import shutil
import traceback
import platform
from optparse import OptionParser

import Common.EdkLogger as EdkLogger
from Common.BuildToolError import *
from Common.Misc import *
from Common.XmlParser import *
from Common.InfClassObjectLight import Inf
from Common.DecClassObjectLight import Dec

from PackageFile import *
from IpiDb import *
from DependencyRules import *
import md5

# Version and Copyright
VersionNumber = "0.1"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2008, Intel Corporation  All rights reserved."

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
        EdkLogger.error("InstallPkg", ATTRIBUTE_NOT_AVAILABLE, "Environment variable not found",
                        ExtraData="WORKSPACE")

    WorkspaceDir = os.path.normpath(os.environ["WORKSPACE"])
    if not os.path.exists(WorkspaceDir):
        EdkLogger.error("InstallPkg", FILE_NOT_FOUND, "WORKSPACE doesn't exist", ExtraData="%s" % WorkspaceDir)
    elif ' ' in WorkspaceDir:
        EdkLogger.error("InstallPkg", FORMAT_NOT_SUPPORTED, "No space is allowed in WORKSPACE path", 
                        ExtraData=WorkspaceDir)
    os.environ["WORKSPACE"] = WorkspaceDir

## Parse command line options
#
# Using standard Python module optparse to parse command line option of this tool.
#
#   @retval Opt   A optparse.Values object containing the parsed options
#   @retval Args  Target of build command
#
def MyOptionParser():
    UsageString = "%prog [-f] [-r] [-t] [-q | -v | -d <debug_level>] [-o <install_directory>] <distribution_package>"

    Parser = OptionParser(description=__copyright__,version=__version__,prog="InstallPkg",usage=UsageString)

    Parser.add_option("-?", action="help", help="show this help message and exit")

    Parser.add_option("-o", "--install-directory", action="store", type="string", dest="InstallDir",
            help="Install the distribution in $(WORKSPACE)/INSTALLDIR")

    Parser.add_option("-f", "--force", action="store_true", type=None, dest="ForceInstall",
            help="Force installation - ignore all rules.")

    Parser.add_option("-r", "--reinstall", action="store_true", type=None, dest="ReInstall",
            help="Reinstall the distribution.")

    Parser.add_option("-t", "--test", action="store_true", type=None, dest="TestMode",
            help="Try run the installation in order to find out dependency and collision issues.")

    Parser.add_option("-q", "--quiet", action="store_const", dest="LogLevel", const=EdkLogger.QUIET,
            help="Disable all messages except FATAL ERRORS.")

    Parser.add_option("-v", "--verbose", action="store_const", dest="LogLevel", const=EdkLogger.VERBOSE,
            help="Turn on verbose output")

    Parser.add_option("-d", "--debug", action="store", type="int", dest="LogLevel",
            help="Enable debug messages at specified level.")

    Parser.set_defaults(LogLevel=EdkLogger.INFO)

    (Opt, Args)=Parser.parse_args()
    # error check
    if len(Args) == 0:
        EdkLogger.error("InstallPkg", OPTION_MISSING, ExtraData=Parser.get_usage())
    if len(Args) > 1:
        EdkLogger.error("InstallPkg", OPTION_NOT_SUPPORTED, ExtraData="Only one distribution package can be installed")

    Opt.PackageFile = Args[0]
    return Opt

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
    EdkLogger.Initialize()
    Options = None
    try:
        Options = MyOptionParser()
        if Options.LogLevel < EdkLogger.DEBUG_9:
            EdkLogger.SetLevel(Options.LogLevel + 1)
        else:
            EdkLogger.SetLevel(Options.LogLevel)

        CheckEnvVariable()
        WorkspaceDir = os.environ["WORKSPACE"]
        if not Options.InstallDir:
            Options.InstallDir = WorkspaceDir

        # unzip to WORKSPACE/Build/<dist_pkg_file_name>
        DistFile = PackageFile(Options.PackageFile)
        UnpackDir = os.path.join(WorkspaceDir, "Build", os.path.dirname(Options.PackageFile))
        DistFile.Unpack(UnpackDir)
        DistPkgFile = glob.glob(os.path.join(UnpackDir, "*.pkg"))
        if not DistPkgFile:
            EdkLogger.error("InstallPkg", FILE_NOT_FOUND, "No .pkg file found in distribution package")
        ContentFile = glob.glob(os.path.join(UnpackDir, "*.zip"))
        if not ContentFile:
            EdkLogger.error("InstallPkg", FILE_NOT_FOUND, "No .zip file found in distribution package")
        DistPkgFile = DistPkgFile[0]
        ContentFile = ContentFile[0]

        ContentFileDir = os.path.join(UnpackDir, os.path.dirname(ContentFile))
        #ContentZipFile = PackageFile(ContentFile)
        #ContentZipFile.Unpack(ContentFileDir)

        # prepare check dependency
        #Db = IpiDb(DbPath)
        Db = IpiDatabase(os.path.normpath(os.path.join(WorkspaceDir, "Conf/.cache/build.db")))
        Db.InitDatabase()
        Dep = DependencyRules(Db)

        # retrieve the content and copy files to the installation directory
        DistPkgObj = DistributionPackageXml()
        DistPkg = DistPkgObj.FromXml(DistPkgFile)
        
        # verify MD5 signature
        Md5Sigature = md5.new(open(ContentFile).read())
        if DistPkg.Header.Signature != Md5Sigature.hexdigest():
            EdkLogger.error("InstallPkg", FILE_CHECKSUM_FAILURE, ExtraData=ContentFile)

        if Dep.CheckDpExists(DistPkg.Header.Guid, DistPkg.Header.Version):
            EdkLogger.error("InstallPkg", UNKNOWN_ERROR, "Distribution has been installed", ExtraData=DistFile)
        
        # check whether DP dependent packages exist in current workspace.    
        if not Dep.CheckDpDepexSatisfied(DistPkg):
            EdkLogger.error("InstallPkg", UNKNOWN_ERROR, "Distribution Dependency not satified", ExtraData=DistFile)

        InfObj = Inf()
        #Dec = DecObject()
        for Guid,Version,Path in DistPkg.PackageSurfaceArea:
            if Dep.CheckPackageExists(Guid, Version):
                EdkLogger.error("InstallPkg", UNKNOWN_ERROR, "Package has been installed", ExtraData=Path)
            Package = DistPkg.PackageSurfaceArea[Guid,Version,Path]
            for ModuleGuid,ModuleVersion,ModulePath in Package.Modules:
                Module = Package.Modules[ModuleGuid,ModuleVersion,ModulePath]
                if Dep.CheckModuleExists(ModuleGuid, ModuleVersion):
                    EdkLogger.error("InstallPkg", UNKNOWN_ERROR, "Module has been installed", ExtraData=ModulePath)
                SaveFileOnChange(os.path.join(Options.InstallDir, ModulePath, Module.ModuleHeader.Name, ".inf"), InfObj.ModuleToInf(Module), False)
            EdkLogger.info("Installing package ... %s" % Package.PackageHeader.Name)
            #shutil.copytree(os.path.join(ContentFileDir, Path), Options.InstallDir)
            #SaveFileOnChange(os.path.join(Options.InstallDir, Path, Package.Header.Name, ".dec"), Dec.PackageToDec(Package), False)

        # install standalone modules
        for Guid,Version,Path in DistPkg.ModuleSurfaceArea:
            if Dep.CheckModuleExists(Guid, Version):
                EdkLogger.error("InstallPkg", UNKNOWN_ERROR, "Module has been installed", ExtraData=ModulePath)
            Module = DistPkg.ModuleSurfaceArea[Guid,Version,Path]
            EdkLogger.info("Installing module ... %s" % Module.ModuleHeader.Name)
            #shutil.copytree(os.path.join(ContentFileDir, Path), Options.InstallDir)
            #SaveFileOnChange(os.path.join(Options.InstallDir, Path, Module.Header.Name, ".inf"), Inf.ModuleToInf(Module), False)

        for File in DistPkg.Tools.Files:
            pass
            #shutil.copyfile(os.path.join(ContentFileDir, File), os.path.join(Options.InstallDir, File))

        for File in DistPkg.MiscellaneousFiles.Files:
            pass
            #shutil.copyfile(os.path.join(ContentFileDir, File), os.path.join(Options.InstallDir, File))

        # update database
        Db.AddDPObject(DistPkg)

    except FatalError, X:
        if Options and Options.LogLevel < EdkLogger.DEBUG_9:
            EdkLogger.quiet("(Python %s on %s) " % (platform.python_version(), sys.platform) + traceback.format_exc())
        ReturnCode = X.args[0]
    except KeyboardInterrupt:
        ReturnCode = ABORT_ERROR
        if Options and Options.LogLevel < EdkLogger.DEBUG_9:
            EdkLogger.quiet("(Python %s on %s) " % (platform.python_version(), sys.platform) + traceback.format_exc())
    except:
        EdkLogger.error(
                    "\nInstallPkg",
                    CODE_ERROR,
                    "Unknown fatal error when installing [%s]" % Options.PackageFile,
                    ExtraData="\n(Please send email to dev@buildtools.tianocore.org for help, attaching following call stack trace!)\n",
                    RaiseError=False
                    )
        EdkLogger.quiet("(Python %s on %s) " % (platform.python_version(), sys.platform) + traceback.format_exc())
        ReturnCode = CODE_ERROR
    finally:
        Progressor.Abort()

if __name__ == '__main__':
    sys.exit(Main())

