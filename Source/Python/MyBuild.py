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
from AutoGen import *

from optparse import OptionParser
from subprocess import *

# This acts like the main() function for the script, unless it is 'import'ed into another
# script.
if __name__ == '__main__':
    import time
    startTime = time.clock()

    print "############################################################"
    print "Host Platform is", sys.platform
    ewb = WorkspaceBuild()
    myWorkspace = ewb
    apf = ewb.TargetTxt.TargetTxtDictionary["ACTIVE_PLATFORM"][0]
    print "Active Platform is",apf

    myToolchain = ewb.TargetTxt.TargetTxtDictionary["TOOL_CHAIN_TAG"][0]
    print "First valid tool chain is", myToolchain
    #print myToolchain

    myBuildTarget = ewb.TargetTxt.TargetTxtDictionary["TARGET"][0]
    print "First build target is",myBuildTarget
    #print myBuildTarget

    import glob
    buildmf = ""
    makefile = ""
    filesInCurrentDir = glob.glob(os.getcwd() + '\\*.inf')
    if len(filesInCurrentDir) > 0:
        buildmf = filesInCurrentDir[0][len(myWorkspace.Workspace.WorkspaceDir)+1:]
        print "Module build:",buildmf

    myBuildOption = {
        "ENABLE_PCH"        :   False,
        "ENABLE_LOCAL_LIB"  :   True,
    }

    for arch in ewb.Build:
        if not arch.upper() == "IA32":
            continue
        myArch = ewb.Build[arch].Arch
        print "Current target architecture is",myArch

        myBuild = ewb.Build[arch]
        myPlatform = myBuild.PlatformDatabase[os.path.normpath(apf)]

        buildAg = None
        for mf in myBuild.ModuleDatabase:
            myModule = myBuild.ModuleDatabase[mf]

            ag = AutoGen(myModule, myPlatform, myWorkspace, myArch, myToolchain, myBuildTarget)
            ag.CreateAutoGenFile()
            if buildmf == str(myModule):
                makefile = ag.CreateMakefile()
                buildAg = ag
            else:
                ag.CreateMakefile()

        print "############################################################\n"
        t = ""
        if len(sys.argv) > 1:
            t = sys.argv[1]
        if makefile != "":
            p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()

    print "\n[Finished in %s]" % (time.strftime("%M:%S", time.gmtime(int(time.clock() - startTime))))
