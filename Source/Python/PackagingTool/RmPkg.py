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

from IpiDb import *
from DependencyRules import *

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
        EdkLogger.error("RmPkg", ATTRIBUTE_NOT_AVAILABLE, "Environment variable not found",
                        ExtraData="WORKSPACE")

    WorkspaceDir = os.path.normpath(os.environ["WORKSPACE"])
    if not os.path.exists(WorkspaceDir):
        EdkLogger.error("RmPkg", FILE_NOT_FOUND, "WORKSPACE doesn't exist", ExtraData="%s" % WorkspaceDir)
    elif ' ' in WorkspaceDir:
        EdkLogger.error("RmPkg", FORMAT_NOT_SUPPORTED, "No space is allowed in WORKSPACE path", 
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
    UsageString = "%prog [-f] [-t template-file] [-q | -v | -d debug_level] <dist_package1> <dist_package2> ..."

    Parser = OptionParser(description=__copyright__,version=__version__,prog="RmPkg",usage=UsageString)

    Parser.add_option("-?", action="help", help="show this help message and exit")

#    Parser.add_option("-f", "--force", action="store_true", type=None, dest="ForceRemove",
#            help="Force creation - overwrite existing one.")

    Parser.add_option("-n", "--package-version", action="store", type="string", dest="PackageVersion",
            help="The version of distribution package to be removed.")

    Parser.add_option("-g", "--package-guid", action="store", type="string", dest="PackageGuid",
            help="The GUID of distribution package to be removed.")

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
        EdkLogger.error("RmPkg", OPTION_MISSING, ExtraData=Parser.get_usage())
    if len(Args) > 1:
        EdkLogger.error("RmPkg", OPTION_NOT_SUPPORTED, ExtraData="Only one distribution package can be removed at one time.")

    Opt.DistPackage = Args[0]
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

        # prepare check dependency
        Db = IpiDatabase(os.path.normpath(os.path.join(WorkspaceDir, "Conf/.cache/XML.db")))
        Db.InitDatabase()
        Dep = DependencyRules(Db)
        
        if not Dep.CheckDpDepexForRemove(Options.PackageGuid, Optins.PackageVersion):
            pass
        DistPkg = Db.GetDp(Options.PackageGuid, Optins.PackageVersion)
        TODO: Remove package from DB
        TODO: Remove installation directory
        #RemoveDirectory(PackagePath, True)

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
                    "\nRmPkg",
                    CODE_ERROR,
                    "Unknown fatal error when removing package",
                    ExtraData="\n(Please send email to dev@buildtools.tianocore.org for help, attaching following call stack trace!)\n",
                    RaiseError=False
                    )
        EdkLogger.quiet("(Python %s on %s) " % (platform.python_version(), sys.platform) + traceback.format_exc())
        ReturnCode = CODE_ERROR
    finally:
        Progressor.Abort()

if __name__ == '__main__':
    sys.exit(Main())

