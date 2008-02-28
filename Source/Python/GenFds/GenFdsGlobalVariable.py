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
    OutputDirDict = {}
    BinDir = ''
    # will be FvDir + os.sep + 'Ffs'
    FfsDir = ''
    FdfParser = None
    LibDir = ''
    WorkSpace = None
    WorkSpaceDir = ''
    EdkSourceDir = ''
    OutputDirFromDscDict = {}
    TargetName = ''
    ToolChainTag = ''
    RuleDict = {}
    ArchList = None
    VtfDict = {}
    ActivePlatform = None
    FvAddressFileName = ''
    VerboseMode = False
    DebugLevel = -1
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
        GenFdsGlobalVariable.VerboseLogger( "GenFdsGlobalVariable.OutputDir :%s" %OutputDir)
#        GenFdsGlobalVariable.OutputDirDict = OutputDir
        GenFdsGlobalVariable.FdfParser = FdfParser
        GenFdsGlobalVariable.WorkSpace = WorkSpace
        GenFdsGlobalVariable.FvDir = os.path.join(GenFdsGlobalVariable.OutputDirDict[ArchList[0]], 'FV')
        if not os.path.exists(GenFdsGlobalVariable.FvDir) :
            os.makedirs(GenFdsGlobalVariable.FvDir)
        GenFdsGlobalVariable.FfsDir = os.path.join(GenFdsGlobalVariable.FvDir, 'Ffs')
        if not os.path.exists(GenFdsGlobalVariable.FfsDir) :
            os.makedirs(GenFdsGlobalVariable.FfsDir)
        if ArchList != None:
            GenFdsGlobalVariable.ArchList = ArchList
        
        T_CHAR_LF = '\n'    
        #
        # Create FV Address inf file
        #
        GenFdsGlobalVariable.FvAddressFileName = os.path.join(GenFdsGlobalVariable.FfsDir, 'FvAddress.inf')
        FvAddressFile = open (GenFdsGlobalVariable.FvAddressFileName, 'w')
        #
        # Add [Options]
        #
        FvAddressFile.writelines("[options]" + T_CHAR_LF)
        BsAddress = '0'
        for Arch in ArchList:
            if GenFdsGlobalVariable.WorkSpace.DscDatabase[GenFdsGlobalVariable.ActivePlatform].Platform.Header[Arch].BsBaseAddress:
                BsAddress = GenFdsGlobalVariable.WorkSpace.DscDatabase[GenFdsGlobalVariable.ActivePlatform].Platform.Header[Arch].BsBaseAddress
                break
        
        FvAddressFile.writelines("EFI_BOOT_DRIVER_BASE_ADDRESS = " + \
                                       BsAddress          + \
                                       T_CHAR_LF)
                                       
        RtAddress = '0'
        for Arch in ArchList:
            if GenFdsGlobalVariable.WorkSpace.DscDatabase[GenFdsGlobalVariable.ActivePlatform].Platform.Header[Arch].RtBaseAddress:
                RtAddress = GenFdsGlobalVariable.WorkSpace.DscDatabase[GenFdsGlobalVariable.ActivePlatform].Platform.Header[Arch].RtBaseAddress
                
        FvAddressFile.writelines("EFI_RUNTIME_DRIVER_BASE_ADDRESS = " + \
                                       RtAddress          + \
                                       T_CHAR_LF)
        
        FvAddressFile.close()

    ## ReplaceWorkspaceMacro()
    #
    #   @param  String           String that may contain macro
    #
    def ReplaceWorkspaceMacro(String):
        Str = String.replace('$(WORKSPACE)', GenFdsGlobalVariable.WorkSpaceDir)
        if os.path.exists(Str):
            if not os.path.isabs(Str):
                Str = os.path.abspath(Str)
        else:
            Str = os.path.join(GenFdsGlobalVariable.WorkSpaceDir, String)
        return os.path.normpath(Str)
    
    def CallExternalTool (cmd, errorMess):
        
        if type(cmd) not in (tuple, list):
            GenFdsGlobalVariable.ErrorLogger("ToolError!  Invalid parameter type in call to CallExternalTool")

        if GenFdsGlobalVariable.DebugLevel != -1:
            cmd += ('-d', str(GenFdsGlobalVariable.DebugLevel))
            GenFdsGlobalVariable.InfLogger (cmd)
            
        if GenFdsGlobalVariable.VerboseMode:
            cmd += ('-v',)
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
        if PopenObject.returncode != 0 or GenFdsGlobalVariable.VerboseMode or GenFdsGlobalVariable.DebugLevel != -1:
            GenFdsGlobalVariable.InfLogger ("Return Value = %d" %PopenObject.returncode)
            GenFdsGlobalVariable.InfLogger (out)
            GenFdsGlobalVariable.InfLogger (error)
            if PopenObject.returncode != 0:
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
    def MacroExtend (Str, MacroDict = {}, Arch = 'COMMON'):
        if Str == None :
            return None
        
        Dict = {'$(WORKSPACE)'   : GenFdsGlobalVariable.WorkSpaceDir,
                '$(EDK_SOURCE)'  : GenFdsGlobalVariable.EdkSourceDir,
#                '$(OUTPUT_DIRECTORY)': GenFdsGlobalVariable.OutputDirFromDsc,
                '$(TARGET)' : GenFdsGlobalVariable.TargetName,
                '$(TOOL_CHAIN_TAG)' : GenFdsGlobalVariable.ToolChainTag
               }
        OutputDir = GenFdsGlobalVariable.OutputDirFromDscDict[GenFdsGlobalVariable.ArchList[0]]
        if Arch != 'COMMON' and Arch in GenFdsGlobalVariable.ArchList:
            OutputDir = GenFdsGlobalVariable.OutputDirFromDscDict[Arch]
            
        Dict['$(OUTPUT_DIRECTORY)'] = OutputDir
            
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
    ReplaceWorkspaceMacro = staticmethod(ReplaceWorkspaceMacro)
    CallExternalTool = staticmethod(CallExternalTool)
    VerboseLogger = staticmethod(VerboseLogger)
    InfLogger = staticmethod(InfLogger)
    ErrorLogger = staticmethod(ErrorLogger)
    DebugLogger = staticmethod(DebugLogger)
    MacroExtend = staticmethod (MacroExtend)
