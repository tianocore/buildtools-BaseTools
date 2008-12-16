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

from PackageFile import *

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
        EdkLogger.error("MkPkg", ATTRIBUTE_NOT_AVAILABLE, "Environment variable not found",
                        ExtraData="WORKSPACE")

    WorkspaceDir = os.path.normpath(os.environ["WORKSPACE"])
    if not os.path.exists(WorkspaceDir):
        EdkLogger.error("MkPkg", FILE_NOT_FOUND, "WORKSPACE doesn't exist", ExtraData="%s" % WorkspaceDir)
    elif ' ' in WorkspaceDir:
        EdkLogger.error("MkPkg", FORMAT_NOT_SUPPORTED, "No space is allowed in WORKSPACE path", 
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
    UsageString = "%prog [-f] [-t template-file] [-q | -v | -d debug_level] [-o distribution_file] [-m module_file] [-p package_file]"

    Parser = OptionParser(description=__copyright__,version=__version__,prog="MkPkg",usage=UsageString)

    Parser.add_option("-?", action="help", help="show this help message and exit")

    Parser.add_option("-o", "--output-file", action="store", type="string", dest="DistributionFile",
            help="The distribution file to be created.")

    Parser.add_option("-f", "--force", action="store_true", type=None, dest="ForceCreate",
            help="Force creation - overwrite existing one.")

    Parser.add_option("-t", "--template-file", action="store", type=None, dest="TemplateFile",
            help="The name of the FAR template to be used for creating the distribution file.")

    Parser.add_option("-m", "--module", action="append", type="string", dest="ModuleFileList",
            help="The inf file of module to be distributed standalone.")

    Parser.add_option("-p", "--package", action="append", type="string", dest="PackageFileList",
            help="The inf file of package to be distributed.")

    #Parser.add_option("-s", "--scan", action="store_true", dest="Scan",
    #    help="The application will scan the workspace to locate INF and/or DEC"\
    #         "files that do not have an associated MSA or SPD file.  It will "\
    #         "provide an output report displaying these files. Using -si will "\
    #         "prompt the user to create any missing MSA and/or SPD files for the workspace.")

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
        EdkLogger.error("MkPkg", OPTION_MISSING, ExtraData=Parser.get_usage())
    if len(Args) > 1:
        EdkLogger.error("MkPkg", OPTION_NOT_SUPPORTED, ExtraData="Only one distribution package can be installed")

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


        ContentFile = PackageFile("content.zip", "w")
        DistPkg = DistributionPackageXml()
        if Options.PackageFileList:
            for PackageFile in Options.PackageFileList:
                TODO: Add PackageFile
                ContentFile.Pack(os.path.dirname(PackageFile))

        if Options.ModuleFileList:
            for ModuleFile in Options.ModuleFileList:
                TODO: Add ModuleFile
                ContentFile.Pack(os.path.dirname(ModuleFile))

        ContentFile.Close()
        Md5Sigature = md5.new(open(ContentFile).read())
        DistPkg.Header.Signature = Md5Sigature.hexdigest()

        if not Options.DistributionFile:
            Options.DistributionFile = "DistributionPackage.zip"
        DistPkgFile = PackageFile(Options.DistributionFile, "w")
        DistPkgFile.PackFile(ContentFile)
        DistPkgFile.PackData(DistPkg.ToXml(), "dist.pkg")
        DistPkgFile.Close()

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
                    "\nMkPkg",
                    CODE_ERROR,
                    "Unknown fatal error when installing [%s]" % Args,
                    ExtraData="\n(Please send email to dev@buildtools.tianocore.org for help, attaching following call stack trace!)\n",
                    RaiseError=False
                    )
        EdkLogger.quiet("(Python %s on %s) " % (platform.python_version(), sys.platform) + traceback.format_exc())
        ReturnCode = CODE_ERROR
    finally:
        Progressor.Abort()

if __name__ == '__main__':
    sys.exit(Main())

