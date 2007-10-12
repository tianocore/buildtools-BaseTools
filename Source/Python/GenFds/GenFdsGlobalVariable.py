import os
import sys
import subprocess
from Common import BuildToolError
from Common import EdkLogger

class GenFdsGlobalVariable:
    FvDir = ''
    OuputDir = ''
    BinDir = ''
    FfsDir = ''      # FvDir + os.sep + 'Ffs'
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

#    def ExtendMarco (String):
#        return String
    
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
        
    def SetDefaultRule (Rule) :
        GenFdsGlobalVariable.DefaultRule = Rule

    def ReplaceWorkspaceMarco(String):
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
#            for marco in MarcoDict.keys():
#                key = '$(' + marco + ')'
#                Dict[key] = MarcoDict.get(marco)
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
#    ExtendMarco = staticmethod(ExtendMarco)
    SetDefaultRule = staticmethod(SetDefaultRule)
    ReplaceWorkspaceMarco = staticmethod(ReplaceWorkspaceMarco)
    CallExternalTool = staticmethod(CallExternalTool)
    VerboseLogger = staticmethod(VerboseLogger)
    InfLogger = staticmethod(InfLogger)
    ErrorLogger = staticmethod(ErrorLogger)
    DebugLogger = staticmethod(DebugLogger)
    MacroExtend = staticmethod (MacroExtend)
