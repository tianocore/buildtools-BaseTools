#!/usr/bin/env python
import sys
import os
import re
import os.path as path
import imp

import Common.EdkLogger
import GenC
import GenMake
import GenDepex

from BuildInfo import *
from StrGather import *
from Common.BuildToolError import *
from Common.EdkIIWorkspaceBuild import *
from Common.EdkIIWorkspace import *
from Common.DataType import *

#
# generate AutoGen.c, AutoGen.h
# parse unicode file and generate XXXXString.h, XXXXString.c
# generate makefile
#

gPlatformDatabase = {}      # {arch : {dsc file path : PlatformBuildClassObject}}
gModuleDatabase = {}        # {arch : {inf file path : ModuleBuildClassObject}}
gPackageDatabase = {}       # {arch : {dec file path : PackageBuildClassObject}}
gAutoGenDatabase = {}       # (module/package/platform obj, BuildTarget, ToolChain, Arch) : build info
gWorkspace = None
gWorkspaceDir = ""
gDepexTokenPattern = re.compile("(\(|\)|\w+| \S+\.inf)")
gMakeTypeMap = {"MSFT":"nmake", "GCC":"gmake"}

gDefaultOutputFlag = "-o "

gOutputFlag = {
    ("MSFT", "CC", "OUTPUT")      :   "/Fo",
    ("MSFT", "SLINK", "OUTPUT")   :   "/OUT:",
    ("MSFT", "DLINK", "OUTPUT")   :   "/OUT:",
    ("MSFT", "ASMLINK", "OUTPUT") :   "/OUT:",
    ("MSFT", "PCH", "OUTPUT")     :   "/Fp",
    ("MSFT", "ASM", "OUTPUT")     :   "/Fo",

    ("INTEL", "CC", "OUTPUT")          :   "/Fo",
    ("INTEL", "SLINK", "OUTPUT")       :   "/OUT:",
    ("INTEL", "DLINK", "OUTPUT")       :   "/OUT:",
    ("INTEL", "ASMLINK", "OUTPUT")     :   "/OUT:",
    ("INTEL", "PCH", "OUTPUT")         :   "/Fp",
    ("INTEL", "ASM", "OUTPUT")         :   "/Fo",
#    ("INTEL", "IPF", "ASM", "OUTPUT")  :   "-o ",

    ("GCC", "CC", "OUTPUT")        :   "-o ",
    ("GCC", "SLINK", "OUTPUT")     :   "-cr ",
    ("GCC", "DLINK", "OUTPUT")     :   "-o ",
    ("GCC", "ASMLINK", "OUTPUT")   :   "-o ",
    ("GCC", "PCH", "OUTPUT")       :   "-o ",
    ("GCC", "ASM", "OUTPUT")       :   "-o ",

#   ("OUTPUT")                     :    "-o "
}

gIncludeFlag = {"MSFT" : "/I", "GCC" : "-I", "INTEL" : "-I"}

def FindModuleOwnerPackage(module, pkgdb):
    for pkg in pkgdb:
        pkgDir = path.dirname(pkg)
        if module.DescFilePath.find(pkgDir) == 0:
            return pkgdb[pkg]
    return None

class AutoGen(object):

    def __init__(self, moduleFile, platformFile, workspace, target, toolchain, arch):
        global gModuleDatabase, gPackageDatabase, gPlatformDatabase, gAutoGenDatabase, gWorkspace, gWorkspaceDir

        if gWorkspace == None:
            gWorkspace = workspace
        if gWorkspaceDir == "":
            gWorkspaceDir = workspace.Workspace.WorkspaceDir

        if gModuleDatabase == {}:
            for a in workspace.Build:
                gModuleDatabase[a] = gWorkspace.Build[a].ModuleDatabase
        if gPackageDatabase == {}:
            for a in workspace.Build:
                gPackageDatabase[a] = gWorkspace.Build[a].PackageDatabase
        if gPlatformDatabase == {}:
            for a in workspace.Build:
                gPlatformDatabase[a] = gWorkspace.Build[a].PlatformDatabase

        self.ToolChain = toolchain
        self.BuildTarget = target
        self.IsMakefileCreated = False
        self.IsAutoGenCodeCreated = False

        key = (self.BuildTarget, self.ToolChain, str(platformFile))
        if moduleFile == None:
            #
            # autogen for platform
            #
            self.PlatformBuildInfo = {}     # arch : PlatformBuildInfo Object
            self.Platform = {}
            self.IsPlatformAutoGen = True
            if type(arch) == type([]):
                self.Arch = arch
            else:
                self.Arch = [arch]
                
            self.Platform = {}
            self.BuildInfo = {}
            for a in self.Arch:
                if a not in gPlatformDatabase or str(platformFile) not in gPlatformDatabase[a]:
                    raise AutoGenError(msg="[%s] is not active platform, or %s is not supported!" % (platformFile, a))
                p = gPlatformDatabase[a][str(platformFile)]
                self.Platform[a] = p
                self.BuildInfo[a] = self.GetPlatformBuildInfo(p, self.BuildTarget, self.ToolChain, a)
            gAutoGenDatabase[key] = self
            return
        elif key not in gAutoGenDatabase:
            gAutoGenDatabase[key] = AutoGen(None, platformFile, workspace, target, toolchain, arch)

        #print "-------------",moduleFile,"----------------"
        #
        # autogen for module
        #
        self.IsPlatformAutoGen = False
        if type(arch) == type([]):
            if len(arch) > 1:
                raise AutoGenError(msg="Cannot AutoGen a module for more than one platform objects at the same time!")
            self.Arch = arch[0]
        else:
            self.Arch = arch

        if self.Arch not in gPlatformDatabase or str(platformFile) not in gPlatformDatabase[arch]:
            raise AutoGenError(msg="[%s] is not active platform, or %s is not supported!" % (platformFile, self.Arch))
        if self.Arch not in gModuleDatabase or str(moduleFile) not in gModuleDatabase[self.Arch]:
            raise AutoGenError(msg="[%s] for %s is not found in active platform [%s]!" % (moduleFile, self.Arch, platformFile))
        self.Module = gModuleDatabase[self.Arch][str(moduleFile)]
        self.Platform = gPlatformDatabase[arch][str(platformFile)]

        self.Package = FindModuleOwnerPackage(self.Module, gPackageDatabase[arch])
        if self.Package == None:
            raise AutoGenError(msg="Cannot find owner package for [%s]!" % (moduleFile))

        self.AutoGenC = GenC.AutoGenString()
        self.AutoGenH = GenC.AutoGenString()

        self.BuildInfo = None
        self.GetModuleBuildInfo()
        gAutoGenDatabase[self.BuildTarget, self.ToolChain, self.Arch, self.Module] = self

    def GetModuleBuildInfo(self):
        key = (self.BuildTarget, self.ToolChain, self.Arch, self.Module)
        if key in gAutoGenDatabase:
            self.BuildInfo = gAutoGenDatabase[key].BuildInfo
            self.IsAutoGenCodeCreated = gAutoGenDatabase[key].IsAutoGenCodeCreated
            self.IsMakefileCreated = gAutoGenDatabase[key].IsMakefileCreated
            return gAutoGenDatabase[key].BuildInfo
        
        info = ModuleBuildInfo(self.Module)
        self.BuildInfo = info
        info.PlatformInfo = self.GetPlatformBuildInfo(self.Platform, self.BuildTarget, self.ToolChain, self.Arch)

        key = (self.Package, self.BuildTarget, self.ToolChain, self.Arch)
        if key in gAutoGenDatabase:
            info.PackageInfo = gAutoGenDatabase[key]
        else:
            info.PackageInfo = PackageBuildInfo(self.Package)
            self.InitPackageBuildInfo(info.PackageInfo)
            gAutoGenDatabase[key] = info.PackageInfo

        # basic information
        info.WorkspaceDir = gWorkspaceDir
        info.BuildTarget = self.BuildTarget
        info.ToolChain = self.ToolChain
        info.Arch = self.Arch
        info.IsBinary = False
        info.BaseName = self.Module.BaseName
        info.FileBase, info.FileExt = path.splitext(path.basename(self.Module.DescFilePath))
        info.SourceDir = path.dirname(self.Module.DescFilePath)
        info.BuildDir = os.path.join(info.PlatformInfo.BuildDir,
                                     info.Arch,
                                     info.SourceDir,
                                     info.FileBase)
        info.OutputDir = os.path.join(info.BuildDir, "OUTPUT")
        info.DebugDir = os.path.join(info.BuildDir, "DEBUG")
        info.MakefileDir = info.BuildDir
        if os.path.isabs(info.BuildDir):
            CreateDirectory(info.OutputDir)
            CreateDirectory(info.DebugDir)
        else:
            CreateDirectory(os.path.join(gWorkspaceDir, info.OutputDir))
            CreateDirectory(os.path.join(gWorkspaceDir, info.DebugDir))

        for type in self.Module.CustomMakefile:
            makeType = gMakeTypeMap[type]
            info.CustomMakefile[makeType] = os.path.join(info.SourceDir, self.Module.CustomMakefile[type])

        if self.Module.LibraryClass != None and self.Module.LibraryClass != "":
            info.IsLibrary = True
            info.DependentLibraryList = []
        else:
            info.IsLibrary = False
            info.DependentLibraryList = self.GetSortedLibraryList()

        info.DependentPackageList = self.GetDependentPackageList()

        info.BuildOption = self.GetModuleBuildOption(info.PlatformInfo)
        if "DLINK" in info.PlatformInfo.ToolStaticLib:
            info.SystemLibraryList = info.PlatformInfo.ToolStaticLib["DLINK"]

        info.PcdIsDriver = self.Module.PcdIsDriver
        info.PcdList = self.GetPcdList(info.DependentLibraryList)
        info.GuidList = self.GetGuidList()
        info.ProtocolList = self.GetProtocolGuidList()
        info.PpiList = self.GetPpiGuidList()
        info.MacroList = self.GetMacroList()
        info.DepexList = self.GetDepexTokenList(info)
        
        info.IncludePathList = [info.SourceDir, info.DebugDir]
        info.IncludePathList.extend(self.GetIncludePathList(info.DependentPackageList))

        info.SourceFileList = self.GetBuildFileList(info.PlatformInfo)
        info.AutoGenFileList = self.GetAutoGenFileList(info)

        return info

    def InitPackageBuildInfo(self, info):
        info.SourceDir = path.dirname(info.Package.DescFilePath)
        info.IncludePathList.append(info.SourceDir)
        for inc in info.Package.Includes:
            info.IncludePathList.append(os.path.join(info.SourceDir, inc))

    def GetPlatformBuildInfo(self, platform, target, toolchain, arch):
        key = target, toolchain, platform
        platformAutoGen = None
        if key in gAutoGenDatabase:
            platformAutoGen = gAutoGenDatabase[key]
            if arch in platformAutoGen.BuildInfo:
                return platformAutoGen.BuildInfo[arch]

        info = PlatformBuildInfo(platform)

        ruleFile = gWorkspace.Workspace.WorkspaceFile(r'Conf\build_rule.txt')
        info.BuildRule = imp.load_source("BuildRule", ruleFile)

        info.Arch = arch
        info.ToolChain = self.ToolChain
        info.BuildTarget = self.BuildTarget

        info.WorkspaceDir = gWorkspace.Workspace.WorkspaceDir
        info.SourceDir = path.dirname(platform.DescFilePath)
        info.OutputDir = platform.OutputDirectory
        info.BuildDir = path.join(info.OutputDir, self.BuildTarget + "_" + self.ToolChain)
        info.MakefileDir = info.BuildDir
        if platform.FlashDefinition != "":
            info.FdfFileList.append(path.join(gWorkspaceDir, platform.FlashDefinition))

        info.DynamicPcdList = self.GetDynamicPcdList(platform, arch)
        info.PcdTokenNumber = self.GeneratePcdTokenNumber(platform, info.DynamicPcdList)
        info.PackageList = gPackageDatabase[arch].values()

        self.ProcessToolDefinition(info)

        if platformAutoGen != None:
            platformAutoGen.BuildInfo = info
        return info

    def GetDepexTokenList(self, info):
        dxs = self.Module.Depex
        #
        # Append depex from dependent libraries
        #
        for lib in info.DependentLibraryList:
            if lib.Depex != "":
                dxs += " AND " + lib.Depex
        if dxs == "":
            return []

        tokenList = gDepexTokenPattern.findall(self.Module.Depex)
        for i in range(0, len(tokenList)):
            token = tokenList[i].strip()
            if token.endswith(".inf"):  # module file name
                moduleFile = os.path.normpath(token)
                token = gModuleDatabase[moduleFile].Guid
            elif token.upper() in GenDepex.DependencyExpression.SupportedOpcode: # Opcode name
                token = token.upper()
            else:   # GUID C Name
                guidCName = token
                for p in info.DependentPackageList:
                    if guidCName in p.Protocols:
                        token = p.Protocols[guidCName]
                        break
                    elif guidCName in p.Ppis:
                        token = p.Ppis[guidCName]
                        break
                    elif guidCName in p.Guids:
                        token = p.Guids[guidCName]
                        break
                else:
                    raise AutoGenError(msg="%s used in module %s cannot be found in any package!" % (guidCName, info.Name))
            tokenList[i] = token
        return tokenList

    def GetMacroList(self):
        return ["%s %s" % (name, self.Module.Specification[name]) for name in self.Module.Specification]
    
    def ProcessToolDefinition(self, info):
        toolDefinition = gWorkspace.ToolDef.ToolsDefTxtDictionary
        toolCodeList = gWorkspace.ToolDef.ToolsDefTxtDatabase["COMMAND_TYPE"]
        for tool in toolCodeList:
            keyBaseString = "%s_%s_%s_%s" % (info.BuildTarget, info.ToolChain, info.Arch, tool)
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
                os.environ["PATH"] = dll + os.pathsep + os.environ["PATH"]
            else:
                dll = ""
                
            key = "%s_SPATH" % keyBaseString
            if key in toolDefinition:
                lib = toolDefinition[key]
            else:
                lib = ""

            key = keyBaseString + "_OUTPUT"
            if key in toolDefinition:
                oflag = toolDefinition[key]
            elif (family, tool, "OUTPUT") in gOutputFlag:
                oflag = gOutputFlag[family, tool, "OUTPUT"]
                if oflag[0] == '"' and oflag[-1] == '"':
                    oflag = oflag[1:-1]
            else:
                oflag = gDefaultOutputFlag

            iflag = gIncludeFlag[family]
                
            info.ToolPath[tool] = os.path.join(path, name)
            info.ToolDynamicLib[tool] = dll
            info.ToolStaticLib[tool] = lib
            info.ToolChainFamily[tool] = family
            info.DefaultToolOption[tool] = option
            info.OutputFlag[tool] = oflag
            info.IncludeFlag[tool] = iflag

        if self.IsPlatformAutoGen:
            buildOptions = self.Platform[info.Arch].BuildOptions
        else:
            buildOptions = self.Platform.BuildOptions

        for key in buildOptions:
            family = key[0]
            target, tag, arch, tool, attr = key[1].split("_")
            if tool not in info.ToolPath:
                continue
            if family != None and family != "" and family != info.ToolChainFamily[tool]:
                continue
            if target == "*" or target == info.BuildTarget:
                if tag == "*" or tag == info.ToolChain:
                    if arch == "*" or arch == info.Arch:
                        info.BuildOption[tool] = buildOptions[key]
        for tool in info.DefaultToolOption:
            if tool not in info.BuildOption:
                info.BuildOption[tool] = ""

    def GetModuleBuildOption(self, platformInfo):
        buildOption = self.Module.BuildOptions
        optionList = {}
        for key in buildOption:
            family = key[0]
            target, tag, arch, tool, attr = key[1].split("_")
            if tool not in platformInfo.ToolPath:
                continue
            if family != None and family != "" and family != platformInfo.ToolChainFamily[tool]:
                continue
            if target == "*" or target == self.BuildTarget:
                if tag == "*" or tag == self.ToolChain:
                    if arch == "*" or arch == self.Arch:
                        optionList[tool] = buildOption[key]
        for tool in platformInfo.DefaultToolOption:
            if tool not in optionList:
                optionList[tool] = ""

        return optionList
    
    def GetBuildFileList(self, platformInfo):
        buildRule = platformInfo.BuildRule
        buildFileList = []
        fileList = self.Module.Sources
        for f in fileList:
            if f.TagName != "" and f.TagName != self.ToolChain:
                continue
            if f.ToolCode != "" and f.ToolCode not in platformInfo.ToolPath:
                continue

            dir = path.dirname(f.SourceFile)
            if dir != "":
                dir = path.join(self.BuildInfo.SourceDir, dir)
                if dir not in self.BuildInfo.IncludePathList:
                    self.BuildInfo.IncludePathList.insert(0, dir)

            # skip unknown file
            base, ext = path.splitext(f.SourceFile)
            if ext not in buildRule.FileTypeMapping:
                EdkLogger.verbose("Don't know how to process file %s (%s)" % (f.SourceFile, ext))
                continue
            
            # skip file which needs a tool having no matching toolchain family
            fileType = buildRule.FileTypeMapping[ext]
            if fileType == "Unicode-Text":
                self.BuildInfo.UnicodeFileList.append(os.path.join(gWorkspaceDir, self.BuildInfo.SourceDir, f.SourceFile))
                continue

            if f.ToolCode != "":
                toolCodeList = [f.ToolCode]
            else:
                if fileType in buildRule.ToolCodeMapping:
                    toolCodeList = buildRule.ToolCodeMapping[fileType]
                else:
                    toolCodeList = []

            # get the toolchain family from tools definition
            buildable = True
            if f.ToolChainFamily != "":
                for toolCode in toolCodeList:
                    if f.ToolChainFamily != platformInfo.ToolChainFamily[toolCode]:
                        EdkLogger.verbose("File %s for toolchain family %s is not supported" % (f.SourceFile, f.ToolChainFamily))
                        buildable = False
                        break
            else:
                if toolCodeList != []:
                    f.ToolChainFamily = platformInfo.ToolChainFamily[toolCodeList[0]]
                else:
                    buildable = False

            if not buildable:
                continue

            #buildFileList.append(f.SourceFile)
            buildFileList.append(f)

        return buildFileList

    def IsToolChainFamilySupported(self):
        pass

    def IsToolCodeSupported(self):
        pass

    def IsToolChainSupported(self):
        pass
    
    def GetDependentPackageList(self):
        if self.Package not in self.Module.Packages:
            self.Module.Packages.insert(0, str(self.Package))

        if self.Arch not in gPackageDatabase:
            raise AutoGenError(msg="[%s] is not supported!")
        packageDatabase = gPackageDatabase[self.Arch]

        packageList = []
        for pf in self.Module.Packages:
            if pf in packageList:
                continue
            if pf not in packageDatabase:
                raise AutoGenError(FILE_NOT_FOUND, name=pf)
            packageList.append(packageDatabase[pf])
        return packageList

    def GetAutoGenFileList(self, buildInfo):
        GenC.CreateCode(buildInfo, self.AutoGenC, self.AutoGenH)
        fileList = []
        if self.AutoGenC.String != "":
            fileList.append("AutoGen.c")
        if self.AutoGenH.String != "":
            fileList.append("AutoGen.h")
            #print self.AutoGenH.String
        return fileList
    
    def GetSortedLibraryList(self):
        moduleType = self.Module.ModuleType
        libraryConsumerList = [self.Module]
        
        libraryList         = []
        constructor         = []
        consumedByList      = {}
        libraryClassList    = []

        EdkLogger.verbose("")
        EdkLogger.verbose("Library instances of module [%s]:" % str(self.Module))
        while len(libraryConsumerList) > 0:
            module = libraryConsumerList.pop()
            for libc, libf in module.LibraryClasses.iteritems():
                if moduleType not in libc:
                    EdkLogger.debug(EdkLogger.DEBUG_3, "\t%s for module type %s is not supported" % libc)
                    continue
                if libf == None or libf == "":
                    EdkLogger.info("\tLibrary instance of library class %s is not found" % libc[0])
                    continue
                
                libm = gModuleDatabase[self.Arch][libf]
                if libm not in libraryList and libc not in libraryClassList:
                    libraryConsumerList.append(libm)
                    libraryList.append(libm)
                    libraryClassList.append(libc)
                    EdkLogger.verbose("\t" + libc[0] + " : " + str(libm))

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
                errorMessage = 'Module library [%s] with constructors have a cycle:\n\t' % str(m)
                errorMessage += "\n\tconsumed by ".join([str(l) for l in consumedByList[m]])
                raise AutoGenError(msg=errorMessage)
            if m not in SortedLibraryList:
                SortedLibraryList.append(m)

        #
        # Build the list of constructor and destructir names
        # The DAG Topo sort produces the destructor order, so the list of constructors must generated in the reverse order
        #
        SortedLibraryList.reverse()
        return SortedLibraryList

    def GetDynamicPcdList(self, platform, arch):
        pcdList = []
        notFoundPcdList = set()
        noDatumTypePcdList = set()
        pcdConsumerList = set()
        for f in gModuleDatabase[arch]:
            m = gModuleDatabase[arch][f]
            for key in m.Pcds:
                if key not in platform.Pcds:
                    notFoundPcdList.add(" | ".join(key))
                    pcdConsumerList.add(str(m))
                    continue
                    # raise AutoGenError(msg="PCD [%s %s] not found in platform" % key)
                mPcd = m.Pcds[key]
                pPcd = platform.Pcds[key]
                if mPcd.DatumType == "VOID*" and pPcd.MaxDatumSize == None:
                    noDatumTypePcdList.add(" | ".join(key))
                    pcdConsumerList.add(str(m))
                    #raise AutoGenError(msg="No MaxDatumSize specified for PCD %s|%s" % (pPcd.TokenCName, pPcd.TokenSpaceGuidCName))

                if pPcd.Type in GenC.gDynamicPcd + GenC.gDynamicExPcd:
                    if m.ModuleType in ["PEIM", "PEI_CORE"]:
                        pPcd.Phase = "PEI"
                    if pPcd not in pcdList:
                        pPcd.DatumType = mPcd.DatumType
                        pcdList.append(pPcd)
        if len(notFoundPcdList) > 0 or len(noDatumTypePcdList) > 0:
            notFoundPcdListString = "\n\t\t".join(notFoundPcdList)
            noDatumTypePcdListString = "\n\t\t".join(noDatumTypePcdList)
            moduleListString = "\n\t\t".join(pcdConsumerList)
            raise AutoGenError(msg="\n\tPCD(s) not found in platform:\n\t\t%s\
                                    \n\tPCD(s) without MaxDatumSize:\n\t\t%s\
                                    \n\tUsed by:\n\t\t%s\n"
                                    % (notFoundPcdListString, noDatumTypePcdListString, moduleListString))
        return pcdList

    def GeneratePcdTokenNumber(self, platform, dynamicPcdList):
        pcdTokenNumber = {}
        tokenNumber = 1
        for pcd in dynamicPcdList:
            if pcd.Phase == "PEI":
                EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (pcd.TokenCName, pcd.TokenSpaceGuidCName, pcd.Phase, tokenNumber))
                pcdTokenNumber[pcd.TokenCName, pcd.TokenSpaceGuidCName] = tokenNumber
                tokenNumber += 1

        for pcd in dynamicPcdList:
            if pcd.Phase == "DXE":
                EdkLogger.debug(EdkLogger.DEBUG_5, "%s %s (%s) -> %d" % (pcd.TokenCName, pcd.TokenSpaceGuidCName, pcd.Phase, tokenNumber))
                pcdTokenNumber[pcd.TokenCName, pcd.TokenSpaceGuidCName] = tokenNumber
                tokenNumber += 1
                
        platformPcds = platform.Pcds
        for key in platformPcds:
            pcd = platformPcds[key]
            if key not in pcdTokenNumber:
                pcdTokenNumber[key] = tokenNumber
                tokenNumber += 1
        return pcdTokenNumber

    def GetPcdList(self, dependentLibraryList):
        platformPcds = self.Platform.Pcds

        pcdList = []
        for m in dependentLibraryList + [self.Module]:
            for pcdKey in m.Pcds:
                pcd = m.Pcds[pcdKey]
                #if pcdKey not in platformPcds:
                #    EdkLogger.info("%s / %s not in current platform" % pcdKey)
                if (pcd.Type in GenC.gDynamicPcd + GenC.gDynamicExPcd) and self.Module.ModuleType in ["PEIM", "PEI_CORE"]:
                    pcd.Phase = "PEI"
                if pcd not in pcdList:
                    pcdList.append(pcd)
        return pcdList

    def GetGuidList(self):
        guid = {}
        Key = ""
        for Key in self.Module.Guids:
            for p in self.BuildInfo.DependentPackageList:
                if Key in p.Guids:
                    guid[Key] = p.Guids[Key]
                    break
                if Key in p.Protocols:
                    guid[Key] = p.Protocols[Key]
                    break
                if Key in p.Ppis:
                    guid[Key] = p.Ppis[Key]
                    break
            else:
                packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                raise AutoGenError(msg='GUID [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, self.BuildInfo.Name, packageListString))

        for lib in self.BuildInfo.DependentLibraryList:
            if lib.Guids == []:
                continue

            for Key in lib.Guids:
                for p in lib.Packages:
                    # print gPackageDatabase
                    p = gPackageDatabase[self.Arch][p]
                    if Key in p.Guids:
                        guid[Key] = p.Guids[Key]
                        break
                    if Key in p.Protocols:
                        guid[Key] = p.Protocols[Key]
                        break
                    if Key in p.Ppis:
                        guid[Key] = p.Ppis[Key]
                        break
                else:
                    packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                    raise AutoGenError(msg='GUID [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, lib.BaseName, packageListString))
        return guid

    def GetProtocolGuidList(self):
        guid = {}
        Key = ""
        for Key in self.Module.Protocols:
            for p in self.BuildInfo.DependentPackageList:
                    if Key in p.Guids:
                        guid[Key] = p.Guids[Key]
                        break
                    if Key in p.Protocols:
                        guid[Key] = p.Protocols[Key]
                        break
                    if Key in p.Ppis:
                        guid[Key] = p.Ppis[Key]
                        break
            else:
                packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                raise AutoGenError(msg='Protocol [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, self.BuildInfo.Name, packageListString))

        for lib in self.BuildInfo.DependentLibraryList:
            if lib.Protocols == []:
                continue
            for Key in lib.Protocols:
                for p in lib.Packages:
                    p = gPackageDatabase[self.Arch][p]
                    if Key in p.Guids:
                        guid[Key] = p.Guids[Key]
                        break
                    if Key in p.Protocols:
                        guid[Key] = p.Protocols[Key]
                        break
                    if Key in p.Ppis:
                        guid[Key] = p.Ppis[Key]
                        break
                else:
                    packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                    raise AutoGenError(msg='Protocol [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, lib.BaseName, packageListString))

        return guid

    def GetPpiGuidList(self):
        guid = {}
        Key = ""
        for Key in self.Module.Ppis:
            for p in self.BuildInfo.DependentPackageList:
                if Key in p.Guids:
                    guid[Key] = p.Guids[Key]
                    break
                if Key in p.Protocols:
                    guid[Key] = p.Protocols[Key]
                    break
                if Key in p.Ppis:
                    guid[Key] = p.Ppis[Key]
                    break
            else:
                packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                raise AutoGenError(msg='PPI [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, self.BuildInfo.Name, packageListString))

        for lib in self.BuildInfo.DependentLibraryList:
            if lib.Ppis == []:
                continue
            for Key in lib.Ppis:
                for p in lib.Packages:
                    p = gPackageDatabase[self.Arch][p]
                    if Key in p.Guids:
                        guid[Key] = p.Guids[Key]
                        break
                    if Key in p.Protocols:
                        guid[Key] = p.Protocols[Key]
                        break
                    if Key in p.Ppis:
                        guid[Key] = p.Ppis[Key]
                        break
                else:
                    packageListString = "\n\t".join([p.PackageName for p in self.BuildInfo.DependentPackageList])
                    raise AutoGenError(msg='PPI [%s] used by [%s] cannot be found in dependent packages:\n\t%s' % (Key, lib.BaseName, packageListString))
        return guid

    def GetIncludePathList(self, dependentPackageList):
        includePathList = []
        for inc in self.Module.Includes:
            includePathList.append(inc)
            
        for package in dependentPackageList:
            packageDir = path.dirname(package.DescFilePath)
            includePathList.append(packageDir)
            for inc in package.Includes:
                inc = os.path.join(packageDir, inc)
                if inc not in includePathList:
                    includePathList.append(inc)
        return includePathList

    def CreateMakefile(self, filePath=None):
        myBuildOption = {
            "ENABLE_PCH"        :   False,
            "ENABLE_LOCAL_LIB"  :   True,
        }
        if self.IsMakefileCreated:
            return

        if self.IsPlatformAutoGen:
            for arch in self.BuildInfo:
                info = self.BuildInfo[arch]
                for moduleFile in info.Platform.Modules:
                    key = (info.BuildTarget, info.ToolChain, arch, moduleFile)
                    moduleAutoGen = None
                    if key not in gAutoGenDatabase:
                        moduleAutoGen = AutoGen(moduleFile, info.Platform, gWorkspace,
                                                info.BuildTarget, info.ToolChain, info.Arch)
                    else:
                        moduleAutoGen = gAutoGenDatabase[key]
                    moduleAutoGen.CreateMakefile()
        else:
            platformInfo = self.BuildInfo.PlatformInfo
            if not self.BuildInfo.IsLibrary:
                if self not in platformInfo.ModuleAutoGenList:
                    platformInfo.ModuleAutoGenList.append(self)
            elif self not in platformInfo.LibraryAutoGenList:
                platformInfo.LibraryAutoGenList.append(self)

            for lib in self.BuildInfo.DependentLibraryList:
                EdkLogger.debug(EdkLogger.DEBUG_1, "###" + str(lib))
                key = (self.BuildTarget, self.ToolChain, self.Arch, lib)
                libraryAutoGen = None
                if key not in gAutoGenDatabase:
                    libraryAutoGen = AutoGen(lib, self.Platform, gWorkspace,
                                             self.BuildTarget, self.ToolChain, self.Arch)
                else:
                    libraryAutoGen = gAutoGenDatabase[key]
                if libraryAutoGen not in self.BuildInfo.LibraryAutoGenList:
                    self.BuildInfo.LibraryAutoGenList.append(libraryAutoGen)
                libraryAutoGen.CreateMakefile()

            makefile = GenMake.Makefile(self.BuildInfo, myBuildOption)
            f = makefile.Generate()
            self.IsMakefileCreated = True
            EdkLogger.info("Generated [%s] for module %s" % (path.basename(f), self.BuildInfo.Name))
            return f

        makefile = GenMake.Makefile(self.BuildInfo, myBuildOption)
        f = makefile.Generate()
        self.IsMakefileCreated = True
        EdkLogger.info("Generated [%s] for platform %s" % (path.basename(f), self.BuildInfo[self.Arch[0]].Name))

        return f

    def CreateAutoGenFile(self, filePath=None):
        if self.IsAutoGenCodeCreated:
            return
        
        if self.IsPlatformAutoGen:
            for arch in self.BuildInfo:
                info = self.BuildInfo[arch]
                for moduleFile in info.Platform.Modules:
                    key = (info.BuildTarget, info.ToolChain, arch, moduleFile)
                    moduleAutoGen = None
                    if key not in gAutoGenDatabase:
                        moduleAutoGen = AutoGen(moduleFile, info.Platform, gWorkspace,
                                                info.BuildTarget, info.ToolChain, info.Arch)
                    else:
                        moduleAutoGen = gAutoGenDatabase[key]
                    moduleAutoGen.CreateAutoGenFile()
            print
        else:
            platformInfo = self.BuildInfo.PlatformInfo
            if not self.BuildInfo.IsLibrary and self not in platformInfo.ModuleAutoGenList:
                platformInfo.ModuleAutoGenList.append(self)
            elif self.BuildInfo.IsLibrary and self not in platformInfo.LibraryAutoGenList:
                platformInfo.LibraryAutoGenList.append(self)

            for lib in self.BuildInfo.DependentLibraryList:
                key = (self.BuildTarget, self.ToolChain, self.Arch, lib)
                libraryAutoGen = None
                if key not in gAutoGenDatabase:
                    libraryAutoGen = AutoGen(lib, self.Platform, gWorkspace,
                                             self.BuildTarget, self.ToolChain, self.Arch)
                else:
                    libraryAutoGen = gAutoGenDatabase[key]
                if libraryAutoGen not in self.BuildInfo.LibraryAutoGenList:
                    self.BuildInfo.LibraryAutoGenList.append(libraryAutoGen)
                libraryAutoGen.CreateAutoGenFile()

            autoGenList = GenC.Generate(os.path.join(self.BuildInfo.WorkspaceDir, self.BuildInfo.DebugDir),
                                        self.AutoGenC, self.AutoGenH)
                          
            if self.BuildInfo.DepexList != []:
                dpx = GenDepex.DependencyExpression(self.BuildInfo.DepexList, self.BuildInfo.ModuleType)
                dpxFile = dpx.Generate(os.path.join(gWorkspaceDir, self.BuildInfo.OutputDir, self.BuildInfo.Name + ".depex"))
                autoGenList.append(dpxFile)

            self.IsAutoGenCodeCreated = True
            EdkLogger.info("Generated [%s] files for module %s" % (" ".join([path.basename(f) for f in autoGenList]), self.BuildInfo.Name))

            return autoGenList

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
    apf = os.path.normpath(ewb.TargetTxt.TargetTxtDictionary["ACTIVE_PLATFORM"][0])
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
        print " LibraryList:","\n   ","\n    ".join([str(l) for l in bi.DependentLibraryList])

        print

##        for key in gAutoGenDatabase:
##            if str(myPlatform) == str(key[0]):
##                pi = gAutoGenDatabase[key]
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
        ag = AutoGen(myModule, myPlatform, myWorkspace, myBuildTarget, myToolchain, myArch)
        ag.CreateAutoGenFile()
        ag.CreateMakefile()

        #PrintAutoGen(ag)
##        for lib in ag.ModuleBuildInfo.DependentLibraryList:
##            ag = AutoGen(lib, myPlatform, myWorkspace, myArch, myToolchain, myBuildTarget)
##            ag.CreateAutoGenFile()
##            ag.CreateMakefile()
##            #PrintAutoGen(ag)
    platformAutoGen = AutoGen(None, apf, myWorkspace, myBuildTarget, myToolchain, myWorkspace.SupArchList)
    platformAutoGen.CreateAutoGenFile()
    platformAutoGen.CreateMakefile()
