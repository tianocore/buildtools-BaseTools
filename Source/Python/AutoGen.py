#!/usr/bin/env python
import sys, os
import EdkLogger
import os.path as path
import imp
import GenC
import GenMake

from EdkIIWorkspaceBuild import *
from DataType import *
from BuildInfo import *

#
# generate AutoGen.c, AutoGen.h
# parse unicode file and generate XXXXString.h, XXXXString.c
# generate makefile
#

gPlatformDatabase = {}
gModuleDatabase = {}
gPackageDatabase = {}
gBuildInfoDatabase = {}     # (module/package/platform obj, BuildTarget, ToolChain, Arch) : build info

def FindModuleOwnerPackage(module, pkgdb):
    for pkg in pkgdb:
        pkgDir = path.dirname(pkg)
        if module.DescFilePath.find(pkgDir) == 0:
            return pkgdb[pkg]
    return None

class AutoGen(object):

    def __init__(self, module, platform, workspace, arch, toolchain, target):
        self.Module = module
        self.Platform = platform
        self.Workspace = workspace
        self.Arch = arch
        self.ToolChain = toolchain
        self.BuildTarget = target
        self.WorkspaceDir = workspace.Workspace.WorkspaceDir
        
        global gModuleDatabase, gPackageDatabase, gPlatformDatabase, gBuildInfoDatabase
        if gModuleDatabase == {}:
            gModuleDatabase = self.Workspace.Build[arch].ModuleDatabase
        if gPackageDatabase == {}:
            gPackageDatabase = self.Workspace.Build[arch].PackageDatabase
        if gPlatformDatabase == {}:
            gPlatformDatabase = self.Workspace.Build[arch].PlatformDatabase

        self.Package = FindModuleOwnerPackage(self.Module, gPackageDatabase)
        self.AutoGenC = GenC.AutoGenString()
        self.AutoGenH = GenC.AutoGenString()

        key = (module, target, toolchain, arch)
        if key not in gBuildInfoDatabase:
            self.ModuleBuildInfo = ModuleBuildInfo(module)
            self.InitModuleBuildInfo(self.ModuleBuildInfo)
            gBuildInfoDatabase[key] = self.ModuleBuildInfo
        else:
            self.ModuleBuildInfo = gBuildInfoDatabase[key]

    def InitModuleBuildInfo(self, info):
        key = (self.Platform, self.BuildTarget, self.ToolChain, self.Arch)
        if key in gBuildInfoDatabase:
            info.PlatformInfo = gBuildInfoDatabase[key]
        else:
            info.PlatformInfo = PlatformBuildInfo(self.Platform)
            self.InitPlatformBuildInfo(info.PlatformInfo)
            gBuildInfoDatabase[key] = info.PlatformInfo

        key = (self.Package, self.BuildTarget, self.ToolChain, self.Arch)
        if key in gBuildInfoDatabase:
            info.PackageInfo = gBuildInfoDatabase[key]
        else:
            info.PackageInfo = PackageBuildInfo(self.Package)
            self.InitPackageBuildInfo(info.PackageInfo)
            gBuildInfoDatabase[key] = info.PackageInfo

        # basic information
        info.WorkspaceDir = self.WorkspaceDir
        info.BuildTarget = self.BuildTarget
        info.ToolChain = self.ToolChain
        info.Arch = self.Arch
        info.IsBinary = False
        info.BaseName = self.Module.BaseName
        info.FileBase, info.FileExt = path.splitext(path.basename(self.Module.DescFilePath))
        info.SourceDir = path.dirname(self.Module.DescFilePath)
        info.BuildDir = os.path.join(info.PlatformInfo.BuildDir,
                                     info.SourceDir,
                                     info.FileBase)
        info.OutputDir = os.path.join(info.BuildDir, "OUTPUT")
        info.DebugDir = os.path.join(info.BuildDir, "DEBUG")
        info.MakefileDir = info.BuildDir

        if self.Module.LibraryClass != None and self.Module.LibraryClass != "":
            info.IsLibrary = True
            info.DependentLibraryList = []
        else:
            info.IsLibrary = False
            info.DependentLibraryList = self.GetSortedLibraryList()

        info.DependentPackageList = self.GetDependentPackageList()


        info.BuildOption = self.GetModuleBuildOption()

        info.PcdList = self.GetPcdList()
        info.GuidList = self.GetGuidList()
        info.ProtocolList = self.GetProtocolGuidList()
        info.PpiList = self.GetPpiGuidList()
        info.MacroList = self.GetMacroList()
        
        info.InclduePathList = self.GetIncludePathList()

        #GenC.CreateCode(info, self.AutoGenC, self.AutoGenH)
        
        info.AutoGenFileList = self.GetAutoGenFileList()
        info.SourceFileList = self.GetBuildFileList()
        # info.ObjectFileList = []
        # info.DependentFileList = self.GetFileDependency()

    def InitPackageBuildInfo(self, info):
        info.SourceDir = path.dirname(info.Package.DescFilePath)
        info.IncludePathList.append(info.SourceDir)
        for inc in info.Package.Includes:
            info.IncludePathList.append(os.path.join(info.SourceDir, inc))

    def InitPlatformBuildInfo(self, info):
        ruleFile = self.Workspace.Workspace.WorkspaceFile('Tools/Conf/build.rule')
        info.BuildRule = imp.load_source("BuildRule", ruleFile)

        info.SourceDir = path.dirname(self.Platform.DescFilePath)
        info.OutputDir = self.Platform.OutputDirectory
        info.BuildDir = path.join(info.OutputDir, self.BuildTarget + "_" + self.ToolChain, self.Arch)
        info.DebugDir = path.join(info.BuildDir, "DEBUG")
        info.LibraryDir = info.BuildDir
        info.FvDir = path.join(info.BuildDir, "FV")
        info.MakefileDir = info.BuildDir

        info.PcdTokenNumber = self.GeneratePcdTokenNumber()
        info.DynamicPcdList = self.GetDynamicPcdList()

        self.ProcessToolDefinition(info)

    def GetMacroList(self):
        return ["%s %s" % (name, self.Module.Specification[name]) for name in self.Module.Specification]
    
    def ProcessToolDefinition(self, info):
        toolDefinition = self.Workspace.ToolDef.ToolsDefTxtDictionary
        toolCodeList = self.Workspace.ToolDef.ToolsDefTxtDatabase["COMMAND_TYPE"]
        for tool in toolCodeList:
            keyBaseString = "%s_%s_%s_%s" % (self.BuildTarget, self.ToolChain, self.Arch, tool)
            key = "%s_NAME" % keyBaseString
            if key not in toolDefinition:
                continue
            name = toolDefinition[key]
            
            key = "%s_PATH" % keyBaseString
            if key in toolDefinition:
                path = toolDefinition[key]
            else:
                path = ""

            key = "%s_FAMILY" % keyBaseString
            if key in toolDefinition:
                family = toolDefinition[key]
            else:
                family = ""

            key = "%s_FLAGS" % keyBaseString
            if key in toolDefinition:
                option = toolDefinition[key]
            else:
                option = ""
                
            key = "%s_DPATH" % keyBaseString
            if key in toolDefinition:
                dll = toolDefinition[key]
            else:
                dll = ""
                
            key = "%s_SPATH" % keyBaseString
            if key in toolDefinition:
                lib = toolDefinition[key]
            else:
                lib = ""

            info.ToolPath[tool] = os.path.join(path, name)
            info.ToolDynamicLib[tool] = dll
            info.ToolStaticLib[tool] = lib
            info.ToolChainFamily[tool] = family
            info.DefaultToolOption[tool] = option

        #print "$$$$$$$",self.Platform.BuildOptions
        for key in self.Platform.BuildOptions:
            target, tag, arch, tool, attr = key.split("_")
            if tool not in info.ToolPath:
                continue
            if target == "*" or target == self.BuildTarget:
                if tag == "*" or tag == self.ToolChain:
                    if arch == "*" or arch == self.Arch:
                        info.BuildOption[tool] = self.Platform.BuildOptions[key]

    def GetModuleBuildOption(self):
        buildOption = self.Module.BuildOptions
        #print "#########",buildOption
        optionList = {}
        for key in buildOption:
            target, tag, arch, tool, attr = key.split("_")
            if target == "*" or target == self.BuildTarget:
                if tag == "*" or tag == self.ToolChain:
                    if arch == "*" or arch == self.Arch:
                        optionList[tool] = buildOption[key]
        return optionList
    
    def GetBuildFileList(self):
        platformInfo = self.ModuleBuildInfo.PlatformInfo
        buildRule = platformInfo.BuildRule
        buildFileList = []
        fileList = self.Module.Sources
        for f in fileList:
            if f.TagName != "" and f.TagName != self.ToolChain:
                continue
            if f.ToolCode != "" and f.ToolCode not in platformInfo.ToolPath:
                continue

            # skip unknown file
            base, ext = path.splitext(f.SourceFile)
            if ext not in buildRule.FileTypeMapping:
                EdkLogger.info("Don't know how to process file %s" % f.SourceFile)
                continue
            
            # skip file which needs a tool having no matching toolchain family
            if f.ToolCode != "":
                toolCode = f.ToolCode
            else:
                fileType = buildRule.FileTypeMapping[ext]
                toolCode = buildRule.ToolCodeMapping[fileType]
            # get the toolchain family from tools definition
            if f.ToolChainFamily != "" and f.ToolChainFamily != platformInfo.ToolChainFamily[toolcode]:
                continue

            buildFileList.append(f.SourceFile)
        return buildFileList

    def GetDependentPackageList(self):
        if self.Package not in self.Module.Packages:
            self.Module.Packages.insert(0, str(self.Package))
            
        packageList = []
        for pf in self.Module.Packages:
            package = gPackageDatabase[pf]
            if pf in packageList:
                continue
            key = (package, self.BuildTarget, self.ToolChain, self.Arch)
            if key in gBuildInfoDatabase:
                packageList.append(gBuildInfoDatabase[key])
            else:
                packageBuildInfo = PackageBuildInfo(package)
                self.InitPackageBuildInfo(packageBuildInfo)
                packageList.append(packageBuildInfo)
                gBuildInfoDatabase[key] = packageBuildInfo
        #print "$$$$$$$", [str(p) for p in packageList]
        return packageList

    def GetAutoGenFileList(self):
        fileList = []
        if self.AutoGenC.String != "":
            fileList.append("AutoGen.c")
        if self.AutoGenH.String != "":
            fileList.append("AutoGen.h")
        return fileList
    
    def GetSortedLibraryList(self):
        moduleType = self.Module.ModuleType
        libraryConsumerList = [self.Module]
        
        libraryList         = []
        constructor         = []
        consumedByList      = {}
        libraryClassList    = []

        while len(libraryConsumerList) > 0:
            module = libraryConsumerList.pop()
            for libc, libf in module.LibraryClasses.iteritems():
                if moduleType not in libc or libf == None or libf == "":
                    continue
                
                libm = gModuleDatabase[libf]
                if libm not in libraryList and libc not in libraryClassList:
                    libraryConsumerList.append(libm)
                    libraryList.append(libm)
                    libraryClassList.append(libc)

                if libm.ConstructorList != [] and libm not in constructor:
                    constructor.append(libm)
                    
                if libm not in consumedByList:
                    consumedByList[libm] = []
                if module != self.Module:
                    if module in consumedByList[libm]:
                        continue
                    consumedByList[libm].append(module)
        #
        # Initialize the sorted output list to the empty set
        #
        SortedLibraryList = []
        #
        # Q <- Set of all nodes with no incoming edges
        #
        Q = []
        for m in libraryList:
            if consumedByList[m] == []:
                Q.insert(0, m)
        #
        # while Q is not empty do
        #
        while Q != []:
            #
            # remove node n from Q
            #
            n = Q.pop()
            #
            # output n
            #
            SortedLibraryList.append(n)
            #
            # for each node m with an edge e from n to m do
            #
            for m in libraryList:
                if n not in consumedByList[m]:
                    continue
                #
                # remove edge e from the graph
                #
                consumedByList[m].remove(n)
                #
                # If m has no other incoming edges then
                #
                if consumedByList[m] == []:
                    #
                    # insert m into Q
                    #
                    Q.insert(0,m)

            EdgeRemoved = True
            while Q == [] and EdgeRemoved:
                EdgeRemoved = False
                #
                # for each node m with a constructor
                #
                for m in libraryList:
                    if m in constructor:
                        #
                        # for each node n without a constructor with an edge e from m to n
                        #
                        for n in consumedByList[m]:
                            if n not in constructor:
                                #
                                # remove edge e from the graph
                                #
                                consumedByList[m].remove(n)
                                EdgeRemoved = True
                                if consumedByList[m] == []:
                                    #
                                    # insert m into Q
                                    #
                                    Q.insert(0,m)
                                    break
                    if Q != []:
                        break

        #
        # if any remaining node m in the graph has a constructor and an incoming edge, then the graph has a cycle
        #
        for m in libraryList:
            if consumedByList[m] != [] and m in constructor:
                EdkLogger.error('Module libraries with constructors have a cycle')
            if m not in SortedLibraryList:
                SortedLibraryList.append(m)

        #
        # Build the list of constructor and destructir names
        # The DAG Topo sort produces the destructor order, so the list of constructors must generated in the reverse order
        #
        SortedLibraryList.reverse()
        return SortedLibraryList

    def GetDynamicPcdList(self):
        pcdList = []
        for key in self.Platform.Pcds:
            pcd = self.Platform.Pcds[key]
            if pcd.Type == TAB_PCDS_DYNAMIC:
                pcdList.append(key)
        return pcdList

    def GeneratePcdTokenNumber(self):
        pcdTokenNumber = {}
        tokenNumber = 1
        platformInfo = self.ModuleBuildInfo.PlatformInfo
        for pcd in platformInfo.DynamicPcdList:
            pcdTokenNumber[PCD] = tokenNumber
            tokenNumber += 1

        platformPcds = self.Platform.Pcds
        for key in platformPcds:
            pcd = platformPcds[key]
            if key not in pcdTokenNumber:
                pcdTokenNumber[key] = tokenNumber
                tokenNumber += 1
        return pcdTokenNumber

    def PreprocessPcd(self, pcd):
        if pcd.DatumType == None or pcd.DatumType == "" or\
           pcd.TokenValue == None or pcd.TokenValue == "":
            for pkg in gPackageDatabase:
                package = gPackageDatabase[pkg]
                key = (pcd.TokenCName, pcd.TokenSpaceGuidCName)
                if key in package.Pcds:
                    pcd.DatumType = package.Pcds[key].DatumType
                    pcd.TokenValue = package.Pcds[key].TokenValue
                    break
        
    def GetPcdList(self):
        platformPcds = self.Platform.Pcds
        #EdkLogger.info(self.Module.BaseName + " PCD settings")

        pcdList = []
        for m in self.ModuleBuildInfo.DependentLibraryList + [self.Module]:
            # EdkLogger.info("  " + m.BaseName)
            pcdList.extend(m.Pcds.values())
##            for key in modulePcds:
##                if key not in platformPcds:
##                    EdkLogger.error("No matching PCD in platform: %s %s" % key)
##                    continue
##                pcd = platformPcds[key]
##                #self.PreprocessPcd(pcd)
##                #EdkLogger.info("    %s %s %s (%s)" % (pcd.TokenSpaceGuidCName, pcd.TokenCName, pcd.Type, pcd.DatumType))
##                pcdList.append(pcd)
        return pcdList

    def GetGuidList(self):
        guidList = set(self.Module.Guids)
        for lib in self.ModuleBuildInfo.DependentLibraryList:
            guidList |= set(lib.Guids)
        return list(guidList)

    def GetProtocolGuidList(self):
        guidList = set(self.Module.Protocols)
        for lib in self.ModuleBuildInfo.DependentLibraryList:
            guidList |= set(lib.Protocols)
        return list(guidList)

    def GetPpiGuidList(self):
        guidList = set(self.Module.Ppis)
        for lib in self.ModuleBuildInfo.DependentLibraryList:
            guidList |= set(lib.Ppis)
        return guidList

    def GetIncludePathList(self):
        includePathList = self.Module.Includes
        if self.ModuleBuildInfo.PackageInfo not in self.ModuleBuildInfo.DependentPackageList:
            includePathList.extend(self.ModuleBuildInfo.PackageInfo.IncludePathList)
            
        for packageInfo in self.ModuleBuildInfo.DependentPackageList:
            #print "%%%%%%%%%%",str(packageInfo)
            includePathList.extend(packageInfo.IncludePathList)
        #print "@@@@@@", includePathList
        return includePathList

    def CreateMakefile(self, filePath=None):
        myBuildOption = {
            "ENABLE_PCH"        :   False,
            "ENABLE_LOCAL_LIB"  :   True,
        }
        makefile = GenMake.Makefile(self.ModuleBuildInfo, myBuildOption)
        return makefile.Generate()

    def CreateAutoGenCode(self, filePath=None):
        return GenC.CreateCode(self.ModuleBuildInfo, self.AutoGenC, self.AutoGenH)

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

    #LoadBuildRule(myWorkspace.Workspace.WorkspaceFile('Tools/Conf/build.rule'))

    myToolchain = ewb.TargetTxt.TargetTxtDictionary["TOOL_CHAIN_TAG"][0]
    #print myToolchain

    myBuildTarget = ewb.TargetTxt.TargetTxtDictionary["TARGET"][0]
    #print myBuildTarget

    myBuildOption = {
        "ENABLE_PCH"        :   False,
        "ENABLE_LOCAL_LIB"  :   True,
    }
    
    def PrintAutoGen(ag):
        bi = ag.ModuleBuildInfo

        print " WorkSpaceDir =",bi.WorkspaceDir
        print " SourceDir =",bi.SourceDir
        print " Is Library =",bi.IsLibrary
        print " BaseName =",bi.BaseName
        print " FileBase =",bi.FileBase
        print " FileExt =",bi.FileExt
        print " BuildDir =",bi.BuildDir
        print " OutputDir =",bi.OutputDir
        print " DebugDir =",bi.DebugDir
        print " MakefileDir =",bi.MakefileDir

        print " Include Path:","\n   ","\n    ".join(bi.InclduePathList)
        print " SourceFileList:","\n   ","\n    ".join(bi.SourceFileList)

        print " BuildOption:","\n   ","\n    ".join(["%s = %s" % (tool,bi.BuildOption[tool]) for tool in bi.BuildOption])
        print " PcdList:","\n   ","\n    ".join([pcd.TokenCName for pcd in bi.PcdList])
        print " GuidList:","\n   ","\n    ".join(bi.GuidList)
        print " ProtocolList:","\n   ","\n    ".join(bi.ProtocolList)
        print " PpiList:","\n   ","\n    ".join(bi.PpiList)

        print

##        for key in gBuildInfoDatabase:
##            if str(myPlatform) == str(key[0]):
##                pi = gBuildInfoDatabase[key]
##                print " BuildDir =",pi.BuildDir
##                print " OutputDir =",pi.OutputDir
##                print " DebugDir =",pi.DebugDir
##                print " LibraryDir =",pi.LibraryDir
##                print " FvDir =",pi.FvDir
##                print " MakefileDir =",pi.MakefileDir
##                print " PcdTokenNumber:","\n   ","\n    ".join(["%s = %s" % (pcd,pi.PcdTokenNumber[pcd]) for pcd in pi.PcdTokenNumber])
##                print " DynamicPcdList:","\n   ","\n    ".join([str(pcd) for pcd in pi.DynamicPcdList])
##
##                print " ToolPath:","\n   ","\n    ".join(["%s = %s" % (tool,pi.ToolPath[tool]) for tool in pi.ToolPath])
##                print " ToolDynamicLib:","\n   ","\n    ".join(["%s = %s" % (tool,pi.ToolDynamicLib[tool]) for tool in pi.ToolDynamicLib])
##                print " ToolStaticLib:","\n   ","\n    ".join(["%s = %s" % (tool,pi.ToolStaticLib[tool]) for tool in pi.ToolStaticLib])
##                print " ToolChainFamily:","\n   ","\n    ".join(["%s = %s" % (tool,pi.ToolChainFamily[tool]) for tool in pi.ToolChainFamily])
##                print " BuildOption:","\n   ","\n    ".join(["%s = %s" % (tool,pi.BuildOption[tool]) for tool in pi.BuildOption])
##                print " DefaultToolOption:","\n   ","\n    ".join(["%s = %s" % (tool,pi.DefaultToolOption[tool]) for tool in pi.DefaultToolOption])

    for mf in myBuild.ModuleDatabase:
        #mf = "MdePkg\\Library\\BaseLib\\BaseLib.inf"
        #if mf in myPlatform.Modules and mf in myBuild.ModuleDatabase:
        #print mf
        myModule = myBuild.ModuleDatabase[mf]
        if myModule.LibraryClass != None and myModule.LibraryClass != "":
            continue    # skip library instance

        ag = AutoGen(myModule, myPlatform, myWorkspace, myArch, myToolchain, myBuildTarget)
        ag.CreateAutoGenCode()
        ag.CreateMakefile()
        
        PrintAutoGen(ag)
        for lib in ag.ModuleBuildInfo.DependentLibraryList:
            ag = AutoGen(lib, myPlatform, myWorkspace, myArch, myToolchain, myBuildTarget)
            ag.CreateAutoGenCode()
            ag.CreateMakefile()
            PrintAutoGen(ag)


