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
"""build command

TODO
"""
import os, sys, imp, getopt, string, xml.dom.minidom, shutil
import os.path as path
import EdkLogger

from SequentialDict import *
from EdkIIWorkspaceBuild import *
from EdkIIWorkspace import *
from GenMake import *

from optparse import OptionParser
from subprocess import *

VersionNumber = "0.01"
__version__ = "%prog Version " + VersionNumber
__copyright__ = "Copyright (c) 2007, Intel Corporation  All rights reserved."


# check environment

# setup environment

# call tool_setup.bat / edksetup.bat ?

# be compatibile with Ant build.bat

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
def GetOptions():
    parser = OptionParser(description=__copyright__,version=__version__)

    parser.add_option("-a", "--arch", dest="arch", default=False, action="store_true",
                      help="build the source without doing check-out in advance")
    parser.add_option("-c", "--checkout-only", dest="checkout_only", default=False, action="store_true",
                      help="check-out source tree only, no build will be issued")
    parser.add_option("-s", "--dir", dest="dir", default="verify", metavar="DIRECTORY",
                      help="the root directory for the source tree, default to 'verify'")
    parser.add_option("-f", "--build-cfg", dest="build_cfg", default="Build.cfg", metavar="FILE",
                      help="configuration file specifying the build steps, default to Build.cfg")
    parser.add_option("-e", "--empty-tree", dest="empty_tree", default=False, action="store_true",
                      help="empty source tree first")
    parser.add_option("-v", "--verbose", dest="verbose", default=False, action="store_true",
                      help="build with verbose information")
    parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true",
                      help="build with debug information")
    parser.add_option("-q", "--quiet", dest="quiet", default=False, action="store_true",
                      help="build with little information")
    parser.add_option("-l", "--log", dest="log", default=None, metavar="FILE",
                      help="specify a log file")

    (options, args) = parser.parse_args()
    return options

# determine build mode (platform build, single module build, launch mode build)

# call parser

# call AutoGen

# call makefile

# timing, result analysis, log, report

# build.exe [options] [targets]

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    print "Running Operating System =", sys.platform
    ewb = WorkspaceBuild()
    #print ewb.Build.keys()

    myArch = ewb.Build["IA32"].Arch
    print myArch

    myBuild = ewb.Build["IA32"]

    myWorkspace = ewb
    apf = ewb.TargetTxt.TargetTxtDictionary["ACTIVE_PLATFORM"][0]
    myPlatform = myBuild.PlatformDatabase[os.path.normpath(apf)]

    LoadBuildRule(myWorkspace.Workspace.WorkspaceFile('Tools/Conf/build.rule'))

    import glob
    buildmf = ""
    makefile = ""
    filesInCurrentDir = glob.glob(os.getcwd() + '\\*.inf')
    if len(filesInCurrentDir) > 0:
        #mf = "EdkModulePkg/Application/HelloWorld/HelloWorld.inf"
        buildmf = filesInCurrentDir[0][len(myWorkspace.Workspace.WorkspaceDir)+1:]
        print buildmf

    for mf in myBuild.ModuleDatabase:
        #mf = "MdePkg\\Library\\BaseLib\\BaseLib.inf"
        #if mf in myPlatform.Modules and mf in myBuild.ModuleDatabase:
        #print mf

        myModule = myBuild.ModuleDatabase[mf]

        myPackage = FindModuleOwner(myModule.DescFilePath, myBuild.PackageDatabase)

        myToolchain = ewb.TargetTxt.TargetTxtDictionary["TOOL_CHAIN_TAG"][0]
        #print myToolchain

        myBuildTarget = ewb.TargetTxt.TargetTxtDictionary["TARGET"][0]
        #print myBuildTarget

        myBuildOption = {
            "ENABLE_PCH"        :   False,
            "ENABLE_LOCAL_LIB"  :   True,
        }

        myMakefile = Makefile(myModule, myPackage, myPlatform, myWorkspace, myToolchain, myBuildTarget,
                              myArch, myBuildOption, "nmake")
        if buildmf == myModule.DescFilePath:
            makefile = myMakefile.Generate()
        else:
            myMakefile.Generate()

    if makefile != "":
        p = Popen(["nmake", "-f", makefile], env=os.environ).communicate()
    #sts = os.waitpid(p.pid, 0)
