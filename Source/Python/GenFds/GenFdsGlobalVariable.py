## @file
# Global variables for GenFds
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
import subprocess
from Common import BuildToolError
from Common import EdkLogger

## Global variables
#
#
class GenFdsGlobalVariable:
    FvDir = ''
    OuputDir = ''
    BinDir = ''
    # will be FvDir + os.sep + 'Ffs'
    FfsDir = ''
    FdfParser = None
    LibDir = ''
    WorkSpace = None
    WorkSpaceDir = ''
    EdkSourceDir = ''
    OutputDirFromDsc = ''
    TargetName = ''
    ToolChainTag = ''
    RuleDict = {}
    DefaultRule = None
    ArchList = None
    VtfDict = {}
    ActivePlatform = None
    VerboseMode = False
    SharpCounter = 0
    SharpNumberPerLine = 40

    ## SetDir()
    #
    #   @param  OutputDir           Output directory
    #   @param  FdfParser           FDF contents parser
    #   @param  Workspace           The directory of workspace
    #   @param  ArchList            The Arch list of platform
    #
    def SetDir (OutputDir, FdfParser, WorkSpace, ArchList):
        GenFdsGlobalVariable.VerboseLogger( "GenFdsGlobalVariable.OuputDir :%s" %OutputDir)
        GenFdsGlobalVariable.OuputDir = os.path.normpath(OutputDir)
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FvDir = os.path.join(GenFdsGlobalVariable.OuputDir, 'Fv')
        GenFdsGlobalVariable.FfsDir = os.path.join(GenFdsGlobalVariable.FvDir, 'Ffs')
        if ArchList != None:
            GenFdsGlobalVariable.ArchList = ArchList
            
        if not os.path.exists(GenFdsGlobalVariable.FvDir) :
            os.makedirs(GenFdsGlobalVariable.FvDir)
    
    ## SetDefaultRule()
    #
    #   @param  Rule           Rule object to generate FFS
    #    
    def SetDefaultRule (Rule) :
        GenFdsGlobalVariable.DefaultRule = Rule

    ## ReplaceWorkspaceMacro()
    #
    #   @param  String           String that may contain macro
    #
    def ReplaceWorkspaceMacro(String):
        Str = String.replace('$(WORKSPACE)', GenFdsGlobalVariable.WorkSpaceDir)
        if os.path.exists(Str):
            Str = os.path.realpath(Str)
        else:
            Str = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, String)
        return os.path.normpath(Str)
    
    def CallExternalTool (cmd, errorMess):
        if GenFdsGlobalVariable.VerboseMode:
            GenFdsGlobalVariable.InfLogger (cmd)
        else:
            sys.stdout.write ('#')
            sys.stdout.flush()
            GenFdsGlobalVariable.SharpCounter = GenFdsGlobalVariable.SharpCounter + 1
            if GenFdsGlobalVariable.SharpCounter % GenFdsGlobalVariable.SharpNumberPerLine == 0:
                sys.stdout.write('\n')
        #GenFdsGlobalVariable.VerboseLogger(cmd)
        PopenObject = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr= subprocess.PIPE)
        (out, error) = PopenObject.communicate()

        while PopenObject.returncode == None :
            PopenObject.wait()
        if PopenObject.returncode != 0:
            GenFdsGlobalVariable.InfLogger ("Return Value = %d" %PopenObject.returncode)
            GenFdsGlobalVariable.InfLogger (out)
            GenFdsGlobalVariable.InfLogger (error)
            GenFdsGlobalVariable.InfLogger (errorMess)
            sys.exit(1)

    def VerboseLogger (msg):
        EdkLogger.verbose(msg)

    def InfLogger (msg):
        EdkLogger.info(msg)
        
    def ErrorLogger (msg, File = None, Line = None, ExtraData = None):
        EdkLogger.error('GenFds', BuildToolError.GENFDS_ERROR, msg, File, Line, ExtraData)

    def DebugLogger (Level, msg):
        EdkLogger.debug(Level, msg)

    ## ReplaceWorkspaceMacro()
    #
    #   @param  Str           String that may contain macro
    #   @param  MacroDict     Dictionary that contains macro value pair
    #
    def MacroExtend (Str, MacroDict = {}):
        if Str == None :
            return None
        
        Dict = {'$(WORKSPACE)'   : GenFdsGlobalVariable.WorkSpaceDir,
                '$(EDK_SOURCE)'  : GenFdsGlobalVariable.EdkSourceDir,
                '$(OUTPUT_DIRECTORY)': GenFdsGlobalVariable.OutputDirFromDsc,
                '$(TARGET)' : GenFdsGlobalVariable.TargetName,
                '$(TOOL_CHAIN_TAG)' : GenFdsGlobalVariable.ToolChainTag
               }
        if MacroDict != None  and len (MacroDict) != 0:
            Dict.update(MacroDict)

        for key in Dict.keys():
            if Str.find(key) >= 0 :
                Str = Str.replace (key, Dict[key])
        
        if Str.find('$(ARCH)') >= 0:
            if len(GenFdsGlobalVariable.ArchList) == 1:
                Str = Str.replace('$(ARCH)', GenFdsGlobalVariable.ArchList[0])
            else:
                GenFdsGlobalVariable.InfLogger ("\nNo way to determine $(ARCH) for %s\n" % Str)
                sys.exit(1)
            
        return Str


    SetDir = staticmethod(SetDir)
    SetDefaultRule = staticmethod(SetDefaultRule)
    ReplaceWorkspaceMacro = staticmethod(ReplaceWorkspaceMacro)
    CallExternalTool = staticmethod(CallExternalTool)
    VerboseLogger = staticmethod(VerboseLogger)
    InfLogger = staticmethod(InfLogger)
    ErrorLogger = staticmethod(ErrorLogger)
    DebugLogger = staticmethod(DebugLogger)
    MacroExtend = staticmethod (MacroExtend)
