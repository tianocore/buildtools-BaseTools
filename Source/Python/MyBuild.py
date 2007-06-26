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

    myToolchainList = ewb.TargetTxt.TargetTxtDictionary["TOOL_CHAIN_TAG"]
    print "Valid tool chain(s) is", " ".join(myToolchainList)
    #print myToolchain

    buildTargetList = ewb.TargetTxt.TargetTxtDictionary["TARGET"]
    if len(buildTargetList) == 0:
        myBuildTargetList = ewb.BuildTarget
    else:
        myBuildTargetList = set(buildTargetList) & set(ewb.BuildTarget)

    print "Valid build target(s) is", " ".join(myBuildTargetList)
    #print myBuildTarget

    targetArchList = ewb.TargetTxt.TargetTxtDictionary["TARGET_ARCH"]
    if len(targetArchList) == 0:
        myArchList = ewb.SupArchList
    else:
        myArchList = set(ewb.SupArchList) & set(targetArchList)
    print "Valid target architecture(s) is", " ".join(myArchList)

    import glob
    buildmf = ""
    buildpf = ""
    makefile = ""
    filesInCurrentDir = glob.glob(os.getcwd() + '\\*.inf')
    if len(filesInCurrentDir) > 0:
        buildmf = filesInCurrentDir[0][len(myWorkspace.Workspace.WorkspaceDir)+1:]
        print "Module build:",buildmf
        buildpf = os.path.normpath(apf)
    elif apf == "":
        filesInCurrentDir = glob.glob(os.getcwd() + '\\*.dsc')
        if len(filesInCurrentDir) > 0:
            buildpf = filesInCurrentDir[0][len(myWorkspace.Workspace.WorkspaceDir)+1:]
            print "Platform build:",buildpf
    else:
        buildpf = os.path.normpath(apf)
        print "Platform build:",buildpf

    print "############################################################\n"
    
    myBuildOption = {
        "ENABLE_PCH"        :   False,
        "ENABLE_LOCAL_LIB"  :   True,
    }

    t = ""
    if len(sys.argv) > 1:
        t = sys.argv[1]
    for target in myBuildTargetList:
        for toolchain in myToolchainList:
            if buildmf == "" and buildpf != "":
                platformAutoGen = AutoGen(None, buildpf, myWorkspace, target, toolchain, list(myArchList))
                platformAutoGen.CreateAutoGenFile()
                makefile = platformAutoGen.CreateMakefile()
                if makefile != "":
                    p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()
            elif buildmf != "" and buildpf != "":
                for arch in myArchList:
                    ag = AutoGen(buildmf, buildpf, myWorkspace, target, toolchain, arch)
                    ag.CreateAutoGenFile()
                    makefile = ag.CreateMakefile()

                    if makefile != "":
                        p = Popen(["nmake", "/nologo", "-f", makefile, t], env=os.environ, cwd=os.path.dirname(makefile)).communicate()
            else:
                print "Nothing to be built"
                break

    print "\n[Finished in %s]" % (time.strftime("%M:%S", time.gmtime(int(round(time.clock() - startTime)))))
